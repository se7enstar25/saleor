from datetime import date

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from ..checkout.models import Checkout
from ..core.utils.promo_code import InvalidPromoCode
from . import GiftCardExpiryType
from .models import GiftCard


def add_gift_card_code_to_checkout(
    checkout: Checkout, email: str, promo_code: str, currency: str
):
    """Add gift card data to checkout by code.

    Raise InvalidPromoCode if gift card cannot be applied.
    """
    try:
        # only active gift card with currency the same as channel currency can be used
        gift_card = (
            GiftCard.objects.active(date=date.today())
            .filter(currency=currency)
            .get(code=promo_code)
        )
    except GiftCard.DoesNotExist:
        raise InvalidPromoCode()

    used_by_email = gift_card.used_by_email
    # gift card can be used only by one user
    if used_by_email and used_by_email != email:
        raise InvalidPromoCode()

    checkout.gift_cards.add(gift_card)


def remove_gift_card_code_from_checkout(checkout: Checkout, gift_card_code: str):
    """Remove gift card data from checkout by code."""
    gift_card = checkout.gift_cards.filter(code=gift_card_code).first()
    if gift_card:
        checkout.gift_cards.remove(gift_card)


def deactivate_gift_card(gift_card: GiftCard):
    """Set gift card status as inactive."""
    if gift_card.is_active:
        gift_card.is_active = False
        gift_card.save(update_fields=["is_active"])


def activate_gift_card(gift_card: GiftCard):
    """Set gift card status as active."""
    if not gift_card.is_active:
        gift_card.is_active = True
        gift_card.save(update_fields=["is_active"])


def calculate_expiry_date(gift_card: GiftCard):
    """Calculate gift card expiry date for gift card with expiry period settings.

    Return None for gift card with different expiry settings.
    """
    today = timezone.now().date()
    expiry_date = None
    if gift_card.expiry_type == GiftCardExpiryType.EXPIRY_PERIOD:
        time_delta = {f"{gift_card.expiry_period_type}s": gift_card.expiry_period}
        expiry_date = today + relativedelta(**time_delta)  # type: ignore
    return expiry_date
