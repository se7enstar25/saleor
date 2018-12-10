from django_countries import countries
import stripe

from ... import TransactionKind
from ...utils import create_transaction
from . import errors
from .forms import StripePaymentModalForm
from .utils import get_amount_for_stripe, get_amount_from_stripe


def get_client_token(**_):
    """Not implemented for stripe gateway currently. The client token can be
    generated by Stripe's checkout.js or stripe.js automatically.
    """
    return


def authorize(payment, payment_token, **connection_params):
    client, error = _get_client(**connection_params), ''

    # Get amount from payment
    amount = payment.total

    try:
        # Authorize without capture
        response = _create_stripe_charge(
            client=client, payment=payment, amount=amount,
            payment_token=payment_token, capture=False)
    except stripe.error.StripeError as exc:
        response = _get_error_response_from_exc(exc)
        error = exc.user_message

    # Create transaction
    txn = _create_transaction(
        payment=payment,
        amount=amount,
        kind=TransactionKind.AUTH,
        response=response)

    return txn, error


def capture(payment, amount, **connection_params):
    client, error = _get_client(**connection_params), ''

    # Get amount from argument or payment, and convert to stripe's amount
    amount = amount or payment.total
    stripe_amount = get_amount_for_stripe(amount, payment.currency)

    capture_txn = payment.transactions.filter(
        kind=TransactionKind.AUTH, is_success=True).first()

    if capture_txn is not None:
        try:
            # Retrieve stripe charge and capture specific amount
            stripe_charge = client.Charge.retrieve(capture_txn.token)
            response = stripe_charge.capture(amount=stripe_amount)
        except stripe.error.StripeError as exc:
            response = _get_error_response_from_exc(exc)
            error = exc.user_message
    else:
        error = errors.ORDER_NOT_AUTHORIZED
        response = dict()

    # Create transaction
    txn = _create_transaction(
        payment=payment,
        amount=amount,
        kind=TransactionKind.CAPTURE,
        response=response)

    return txn, error


def charge(payment, payment_token, amount, **connection_params):
    client, error = _get_client(**connection_params), ''

    # Get amount from argument or payment
    amount = amount or payment.total

    try:
        # Charge without pre-authorize
        response = _create_stripe_charge(
            client=client, payment=payment, amount=amount,
            payment_token=payment_token, capture=True)
    except stripe.error.StripeError as exc:
        response = _get_error_response_from_exc(exc)
        error = exc.user_message

    # Create transaction
    txn = _create_transaction(
        payment=payment,
        amount=amount,
        kind=TransactionKind.CHARGE,
        response=response)

    return txn, error


def refund(payment, amount, **connection_params):
    client, error = _get_client(**connection_params), ''

    # Get amount from argument or payment, and convert to stripe's amount
    amount = amount or payment.total
    stripe_amount = get_amount_for_stripe(amount, payment.currency)

    capture_txn = payment.transactions.filter(
        kind=TransactionKind.CHARGE, is_success=True).first()

    if capture_txn is not None:
        try:
            # Retrieve stripe charge and refund specific amount
            stripe_charge = client.Charge.retrieve(capture_txn.token)
            response = client.Refund.create(
                charge=stripe_charge.id, amount=stripe_amount)
        except stripe.error.StripeError as exc:
            response = _get_error_response_from_exc(exc)
            error = exc.user_message
    else:
        error = errors.ORDER_NOT_CHARGED
        response = dict()

    # Create transaction
    txn = _create_transaction(
        payment=payment,
        amount=amount,
        kind=TransactionKind.REFUND,
        response=response)

    return txn, error


def void(payment, **connection_params):
    client, error = _get_client(**connection_params), ''

    capture_txn = payment.transactions.filter(
        kind=TransactionKind.CHARGE, is_success=True).first()

    if capture_txn is not None:
        try:
            # Retrieve stripe charge and refund all
            stripe_charge = client.Charge.retrieve(capture_txn.token)
            response = client.Refund.create(charge=stripe_charge.id)
        except stripe.error.StripeError as exc:
            response = _get_error_response_from_exc(exc)
            error = exc.user_message
    else:
        error = errors.ORDER_NOT_AUTHORIZED
        response = dict()

    # Create transaction
    txn = _create_transaction(
        payment=payment,
        amount=payment.total,
        kind=TransactionKind.VOID,
        response=response)

    return txn, error


def get_form_class():
    return StripePaymentModalForm


def _get_client(**connection_params):
    stripe.api_key = connection_params.get('secret_key')
    return stripe


def _create_stripe_charge(client, payment, amount, payment_token, capture):
    """Create a charge with specific amount, ignoring payment's total."""
    # Get currency
    currency = str(payment.currency).upper()

    # Get appropriate amount for stripe
    stripe_amount = get_amount_for_stripe(amount, currency)

    # Get billing name from payment
    name = '%s %s' % (
        payment.billing_last_name, payment.billing_first_name)

    # Update shipping address to prevent fraud in Stripe
    shipping = dict(name=name, address=dict(
        line1=payment.order.shipping_address.street_address_1,
        line2=payment.order.shipping_address.street_address_2,
        city=payment.order.shipping_address.city,
        state=payment.order.shipping_address.country_area,
        country=dict(countries).get(
            payment.order.shipping_address.country, ''),
        postal_code=payment.order.shipping_address.postal_code,
    ))

    # Create stripe charge
    stripe_charge = client.Charge.create(
        capture=capture,
        amount=stripe_amount,
        currency=currency,
        source=payment_token,
        shipping=shipping,
        description=name)

    return stripe_charge


def _create_transaction(payment, amount, kind, response):
    # Get currency from response or payment
    currency = response.get('currency', payment.currency)

    # Get amount from response or payment
    if 'amount' in response:
        amount = get_amount_from_stripe(response.get('amount'), currency)

    # Get token, which is an empty string for error responses
    token = response.get('id', '')

    # Check if the response's status is flagged as succeeded
    is_success = (response.get('status') == 'succeeded')

    # Create transaction
    txn = create_transaction(
        payment=payment,
        token=token,
        kind=kind,
        is_success=is_success,
        amount=amount,
        currency=currency,
        gateway_response=response)

    return txn


def _get_error_response_from_exc(exc):
    response = exc.json_body

    # Some errors from stripe don't json_body as None
    # such as stripe.error.InvalidRequestError
    if response is None:
        response = dict()

    return response
