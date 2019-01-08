import logging
from decimal import Decimal
from functools import wraps
from typing import Dict, List, Optional

from django.conf import settings
from django.db import transaction
from django.forms.models import model_to_dict
from prices import Money

from . import (
    ChargeStatus, GatewayError, PaymentError, get_payment_gateway,
    TransactionKind)
from ..core import analytics
from ..order import OrderEvents, OrderEventsEmails
from ..order.emails import send_payment_confirmation
from .models import Payment, Transaction

logger = logging.getLogger(__name__)

GENERIC_TRANSACTION_ERROR = 'Transaction was unsuccessful'


def get_billing_data(order):
    """Extracts order's billing address into payment-friendly billing data."""
    data = {}
    if order.billing_address:
        data = {
            'billing_first_name': order.billing_address.first_name,
            'billing_last_name': order.billing_address.last_name,
            'billing_company_name': order.billing_address.company_name,
            'billing_address_1': order.billing_address.street_address_1,
            'billing_address_2': order.billing_address.street_address_2,
            'billing_city': order.billing_address.city,
            'billing_postal_code': order.billing_address.postal_code,
            'billing_country_code': order.billing_address.country.code,
            'billing_email': order.user_email,
            'billing_country_area': order.billing_address.country_area}
    return data


def create_payment_information(
    payment: Payment, payment_token: str=None, amount: Decimal=None) -> Dict:
    """Extracts order information along with payment details.

    Returns information required to process payment and additional
    billing/shipping addresses for optional fraud-prevention mechanisms.
    """
    return {
        'token': payment_token,
        'amount': amount or payment.total,
        'currency': payment.currency,
        'billing': (
            payment.order.billing_address.as_data()
            if payment.order.billing_address else None),
        'shipping': (
            payment.order.shipping_address.as_data()
            if payment.order.shipping_address else None),
        'order_id': payment.order.id,
        'customer_ip_address': payment.customer_ip_address,
        'customer_email': payment.billing_email}


def handle_fully_paid_order(order):
    order.events.create(type=OrderEvents.ORDER_FULLY_PAID.value)
    if order.get_user_current_email():
        send_payment_confirmation.delay(order.pk)
        order.events.create(
            type=OrderEvents.EMAIL_SENT.value,
            parameters={
                'email': order.get_user_current_email(),
                'email_type': OrderEventsEmails.PAYMENT.value})
    try:
        analytics.report_order(order.tracking_client_id, order)
    except Exception:
        # Analytics failing should not abort the checkout flow
        logger.exception('Recording order in analytics failed')


def validate_payment(view):
    """Decorate a view to check if payment is authorized, so any actions
    can be performed on it.
    """

    @wraps(view)
    def func(payment: Payment, *args, **kwargs):
        if not payment.is_active:
            raise PaymentError('This payment is no longer active.')
        return view(payment, *args, **kwargs)
    return func


def create_payment(**payment_data):
    payment, _ = Payment.objects.get_or_create(**payment_data)
    return payment


def create_transaction(payment: Payment, kind: str, payment_information: Dict,
        gateway_response: Dict=None, error_msg=None) -> Transaction:
    """Creates a Transaction based on transaction kind and gateway response."""
    if gateway_response is None:
        gateway_response = {}

    txn, _ = Transaction.objects.get_or_create(
        payment=payment,
        kind=gateway_response.get('kind', kind),
        token=gateway_response.get(
            'transaction_id', payment_information['token']),
        is_success=gateway_response.get('is_success', False),
        amount=gateway_response.get('amount', payment_information['amount']),
        currency=gateway_response.get(
            'currency', payment_information['currency']),
        error=gateway_response.get('error', error_msg),
        gateway_response=gateway_response)
    return txn  # returns last created transaction


def gateway_get_client_token(gateway_name: str):
    """Gets client token, that will be used as a customer's identificator for
    client-side tokenization of the chosen payment method.
    """
    gateway, gateway_params = get_payment_gateway(gateway_name)
    return gateway.get_client_token(**gateway_params)


def clean_charge(payment: Payment, amount: Decimal):
    """Checks if payment can be charged."""
    if amount <= 0:
        raise PaymentError('Amount should be a positive number.')
    if not payment.can_charge():
        raise PaymentError('This payment cannot be charged.')
    if amount > payment.total or amount > (
            payment.total - payment.captured_amount):
        raise PaymentError('Unable to charge more than un-captured amount.')


def clean_capture(payment: Payment, amount: Decimal):
    """Checks if payment can be captured."""
    if amount <= 0:
        raise PaymentError('Amount should be a positive number.')
    if not payment.can_capture():
        raise PaymentError('This payment cannot be captured.')
    if amount > payment.total or amount > (
            payment.total - payment.captured_amount):
        raise PaymentError('Unable to capture more than authorized amount.')


def clean_authorize(payment: Payment):
    """Checks if payment can be authorized."""
    if not payment.can_authorize():
        raise PaymentError('Charged transactions cannot be authorized again.')


def call_gateway(
        func_name, transaction_kind, payment, payment_token, **extra_params):
    """Helper that calls the passed gateway function and handles exceptions.

    Additionally does validation of the returned gateway response."""
    gateway, gateway_params = get_payment_gateway(payment.gateway)
    gateway_response = None
    error_msg = None

    payment_information = create_payment_information(
        payment, payment_token, **extra_params
    )

    try:
        gateway_response = getattr(gateway, func_name)(
            payment_information=payment_information, **gateway_params)
        validate_gateway_response(gateway_response)
    except AttributeError:
        error_msg = 'Gateway doesn\'t implement {}'.format(func_name)
        logger.exception(error_msg)
    except GatewayError:
        error_msg = 'Gateway response validation failed'
        logger.exception(error_msg)
        gateway_response = None  # set response empty as the validation failed
    except Exception:
        error_msg = 'Gateway encountered an error'
        logger.exception(error_msg)
    finally:
        if not isinstance(gateway_response, list):
            gateway_response = [gateway_response]
        for response in gateway_response:
            transaction = create_transaction(
                payment=payment,
                kind=transaction_kind,
                payment_information=payment_information,
                error_msg=error_msg,
                gateway_response=response)

    if not transaction.is_success:
        # attempt to get errors from response, if none raise a generic one
        raise PaymentError(transaction.error or GENERIC_TRANSACTION_ERROR)

    return transaction


def validate_gateway_response(responses):
    """Validates response to be a correct format for Saleor to process."""
    if not isinstance(responses, (dict, list)):
        raise GatewayError('Gateway needs to return a dictionary or a list')

    if not isinstance(responses, list):
        responses = [responses]

    required_fields = {
        'transaction_id', 'is_success', 'kind', 'error', 'amount', 'currency'}
    for response in responses:
        if not required_fields.issubset(response):
            raise GatewayError(
                'Gateway response needs to contain following keys: {}'.format(
                    required_fields - response.keys()))
        #TODO: check if response is json serializable
        #TODO: check if response['kind'] is an allowed choice of TransactionKind


@validate_payment
def gateway_process_payment(
        payment: Payment, payment_token: str) -> Transaction:
    """Performs whole payment process on a gateway."""
    transaction = call_gateway(
        func_name='process_payment', transaction_kind=TransactionKind.CAPTURE,
        payment=payment, payment_token=payment_token, amount=payment.total)

    if transaction.is_success:
        payment.charge_status = ChargeStatus.CHARGED
        payment.captured_amount += transaction.amount
        payment.save(update_fields=['charge_status', 'captured_amount'])
        order = payment.order
        if order and order.is_fully_paid():
            handle_fully_paid_order(order)

    return transaction


@validate_payment
def gateway_charge(payment: Payment, payment_token: str,
        amount: Decimal=None) -> Transaction:
    """Performs authorization and capture in a single run.

    For gateways not supporting the authorization it should be a
    dedicated CHARGE transaction.

    For gateways not supporting capturing without authorizing,
    it should create two transaction - auth and capture, but only the last one
    is returned.
    """
    if amount is None:
        amount = payment.get_charge_amount()
    clean_charge(payment, amount)

    transaction = call_gateway('charge',
        transaction_kind=TransactionKind.CHARGE, payment=payment,
        payment_token=payment_token, amount=amount)

    if transaction.is_success:
        payment.charge_status = ChargeStatus.CHARGED
        payment.captured_amount += transaction.amount
        payment.save(update_fields=['charge_status', 'captured_amount'])
        order = payment.order
        if order and order.is_fully_paid():
            handle_fully_paid_order(order)

    return transaction


@validate_payment
def gateway_authorize(payment: Payment, payment_token: str) -> Transaction:
    """Authorizes the payment and creates relevant transaction.

    Args:
     - payment_token: One-time-use reference to payment information.
    """
    clean_authorize(payment)

    return call_gateway('authorize',
        transaction_kind=TransactionKind.AUTH, payment=payment,
        payment_token=payment_token)


@validate_payment
def gateway_capture(payment: Payment, amount: Decimal=None) -> Transaction:
    """Captures the money that was reserved during the authorization stage."""
    if amount is None:
        amount = payment.get_charge_amount()
    clean_capture(payment, amount)

    auth_transaction = payment.transactions.filter(
        kind=TransactionKind.AUTH, is_success=True).first()
    if auth_transaction is None:
        raise PaymentError('Cannot capture unauthorized transaction')
    payment_token = auth_transaction.token

    transaction = call_gateway('capture',
        transaction_kind=TransactionKind.CAPTURE, payment=payment,
        payment_token=payment_token, amount=amount)

    if transaction.is_success:
        payment.charge_status = ChargeStatus.CHARGED
        payment.captured_amount += transaction.amount
        payment.save(update_fields=['charge_status', 'captured_amount'])
        order = payment.order
        if order and order.is_fully_paid():
            handle_fully_paid_order(order)

    return transaction


@validate_payment
def gateway_void(payment) -> Transaction:
    if not payment.can_void():
        raise PaymentError('Only pre-authorized transactions can be voided.')

    auth_transaction = payment.transactions.filter(
        kind=TransactionKind.AUTH, is_success=True).first()
    if auth_transaction is None:
        raise PaymentError('Cannot void unauthorized transaction')
    payment_token = auth_transaction.token

    transaction = call_gateway('void', transaction_kind=TransactionKind.VOID,
        payment=payment, payment_token=payment_token)

    if transaction.is_success:
        payment.is_active = False
        payment.save(update_fields=['is_active'])

    return transaction


@validate_payment
def gateway_refund(payment, amount: Decimal=None) -> Transaction:
    """Refunds the charged funds back to the customer.
    Refunds can be total or partial.
    """
    if amount is None:
        # If no amount is specified, refund the maximum possible
        amount = payment.captured_amount

    if not payment.can_refund():
        raise PaymentError('This payment cannot be refunded.')

    if amount <= 0:
        raise PaymentError('Amount should be a positive number.')
    if amount > payment.captured_amount:
        raise PaymentError('Cannot refund more than captured')

    transaction = payment.transactions.filter(
        kind__in=[TransactionKind.CAPTURE, TransactionKind.CHARGE],
        is_success=True).first()
    if transaction is None:
        raise PaymentError('Cannot refund uncaptured/uncharged transaction')
    payment_token = transaction.token

    transaction = call_gateway('refund',
        transaction_kind=TransactionKind.REFUND, payment=payment,
        payment_token=payment_token, amount=amount)

    if transaction.is_success:
        changed_fields = ['captured_amount']
        payment.captured_amount -= transaction.amount
        if not payment.captured_amount:
            payment.charge_status = ChargeStatus.FULLY_REFUNDED
            payment.is_active = False
            changed_fields += ['charge_status', 'is_active']
        payment.save(update_fields=changed_fields)

    return transaction
