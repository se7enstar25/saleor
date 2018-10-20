from typing import Dict

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import pgettext_lazy
import braintree as braintree_sdk

from ... import TransactionType
from ...utils import create_transaction

# FIXME: Move to SiteSettings

# If this option is checked, then one needs to authorize the amount paid
# manually via the Braintree Dashboard
CONFIRM_MANUALLY = False
THREE_D_SECURE_REQUIRED = False


def get_customer_data(payment):
    return {
        'billing': {
            'first_name': payment.billing_first_name,
            'last_name': payment.billing_last_name,
            'company': payment.billing_company_name,
            'postal_code': payment.billing_postal_code,
            'street_address': payment.billing_address_1[:255],
            'extended_address': payment.billing_address_2[:255],
            "locality": payment.billing_city,
            'region': payment.billing_country_area,
            'country_code_alpha2': payment.billing_country_code},
        'risk_data': {
            'customer_ip': payment.customer_ip_address or ''
        },
        'customer': {
            'email': payment.billing_email}}


def get_error_for_client(errors):
    """Filters all error messages and decides which one is visible for the
    client side.
    """
    if not errors:
        return ''

    default_msg = pgettext_lazy(
        'payment error',
        'Unable to process transaction. Please try again in a moment')
    # FIXME: Provide list of visible errors and messages translations
    # FIXME: We should also store universal visible errors for all payment
    # gateways, and parse gateway-specific errors to this unified version
    error_codes_whitelist = []
    for error in errors:
        if error['code'] in error_codes_whitelist:
            return error['message']
    return default_msg


def extract_gateway_response(braintree_result) -> Dict:
    """Extract data from Braintree response that will be stored locally."""
    errors = []
    if not braintree_result.is_success:
        errors = [
            {'code': error.code, 'message': error.message}
            for error in braintree_result.errors.deep_errors]
    bt_transaction = braintree_result.transaction
    if not bt_transaction:
        return {'errors': errors}
    gateway_response = {
        'credit_card': bt_transaction.credit_card,
        'additional_processor_response': bt_transaction.additional_processor_response,  # noqa
        'gateway_rejection_reason': bt_transaction.gateway_rejection_reason,
        'processor_response_code': bt_transaction.processor_response_code,
        'processor_response_text': bt_transaction.processor_response_text,
        'processor_settlement_response_code': bt_transaction.processor_settlement_response_code,  # noqa
        'processor_settlement_response_text': bt_transaction.processor_settlement_response_text,  # noqa
        'risk_data': bt_transaction.risk_data,
        'status': bt_transaction.status,
        'errors': errors}
    return gateway_response


def get_gateway(sandbox_mode, merchant_id, public_key, private_key):
    if not all([merchant_id, private_key, public_key]):
        raise ImproperlyConfigured('Incorrectly configured Braintree gateway.')
    environment = braintree_sdk.Environment.Sandbox
    if not sandbox_mode:
        environment = braintree_sdk.Environment.Production

    gateway = braintree_sdk.BraintreeGateway(
        braintree_sdk.Configuration(
            environment=environment,
            merchant_id=merchant_id,
            public_key=public_key,
            private_key=private_key))
    return gateway


def get_client_token(**client_kwargs):
    gateway = get_gateway(**client_kwargs)
    client_token = gateway.client_token.generate()
    return client_token


def authorize(payment_method, transaction_token, **client_kwargs):
    gateway = get_gateway(**client_kwargs)
    result = gateway.transaction.sale({
        'amount': str(payment_method.total.gross.amount),
        'payment_method_nonce': transaction_token,
        'options': {
            'submit_for_settlement': CONFIRM_MANUALLY,
            'three_d_secure': {'required': THREE_D_SECURE_REQUIRED}},
        **get_customer_data(payment_method)})
    gateway_response = extract_gateway_response(result)
    error = get_error_for_client(gateway_response['errors'])
    txn = create_transaction(
        payment_method=payment_method,
        transaction_type=TransactionType.AUTH,
        amount=payment_method.total.gross.amount,
        gateway_response=gateway_response,
        token=getattr(result.transaction, 'id', ''),
        is_success=result.is_success)
    return txn, error


def capture(payment_method, amount=None, **client_kwargs):
    gateway = get_gateway(**client_kwargs)
    # FIXME we are assuming that appropriate transaction exists without
    # forcing the flow
    auth_transaction = payment_method.transactions.filter(
        transaction_type=TransactionType.AUTH).first()
    if not amount:
        amount = payment_method.total.gross.amount
    result = gateway.transaction.submit_for_settlement(
        transaction_id=auth_transaction.token, amount=amount)
    gateway_response = extract_gateway_response(result)
    error = get_error_for_client(gateway_response['errors'])

    txn = create_transaction(
        payment_method=payment_method,
        transaction_type=TransactionType.CAPTURE,
        amount=amount,
        token=result.transaction.id,
        is_success=result.is_success,
        gateway_response=gateway_response)
    return txn, error


def void(payment_method, **client_kwargs):
    gateway = get_gateway(**client_kwargs)
    # FIXME we are assuming that appropriate transaction exists without
    # forcing the flow
    auth_transaction = payment_method.transactions.filter(
        transaction_type=TransactionType.AUTH).first()
    result = gateway.transaction.void(transaction_id=auth_transaction.token)
    gateway_response = extract_gateway_response(result)
    error = get_error_for_client(gateway_response['errors'])
    txn = create_transaction(
        payment_method=payment_method,
        transaction_type=TransactionType.VOID,
        amount=payment_method.total.gross.amount,
        gateway_response=gateway_response,
        token=result.transaction.id,
        is_success=result.is_success)
    return txn, error


def refund(payment_method, amount=None, **client_kwargs):
    gateway = get_gateway(**client_kwargs)
    # FIXME we are assuming that appropriate transaction exists without
    # forcing the flow
    auth_transaction = payment_method.transactions.filter(
        transaction_type=TransactionType.CAPTURE).first()
    result = gateway.transaction.refund(
        transaction_id=auth_transaction.token, amount=amount)
    gateway_response = extract_gateway_response(result)
    error = get_error_for_client(gateway_response['errors'])
    txn = create_transaction(
        payment_method=payment_method,
        transaction_type=TransactionType.REFUND,
        amount=amount,
        token=result.transaction.id,
        is_success=result.is_success,
        gateway_response=gateway_response)
    return txn, error
