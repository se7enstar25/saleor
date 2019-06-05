# from __future__ import annotations
from collections import defaultdict
from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django_countries.fields import Country
from prices import Money, MoneyRange, TaxedMoney, TaxedMoneyRange

from . import ZERO_TAXED_MONEY
from .avatax import interface as avatax_interface
from .vatlayer import interface as vatlayer_interface

if TYPE_CHECKING:
    from ...discount.models import SaleQueryset
    from ...checkout.models import Checkout, CheckoutLine
    from ...product.models import Product, ProductVariant
    from ...account.models import Address
    from ...order.models import OrderLine


def get_total_gross(checkout: "Checkout", discounts: "SaleQueryset") -> TaxedMoney:
    """Calculate total gross for checkout"""

    if settings.VATLAYER_ACCESS_KEY:
        return vatlayer_interface.get_total_gross(checkout, discounts)
    elif settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return avatax_interface.get_total_gross(checkout, discounts)

    total = checkout.get_total(discounts)
    return TaxedMoney(net=total, gross=total)


def get_subtotal_gross(checkout: "Checkout", discounts: "SaleQueryset") -> TaxedMoney:
    """Calculate subtotal gross for checkout"""

    if settings.VATLAYER_ACCESS_KEY:
        return vatlayer_interface.get_subtotal_gross(checkout, discounts)
    elif settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return avatax_interface.get_subtotal_gross(checkout, discounts)

    subtotal = checkout.get_subtotal(discounts)
    return TaxedMoney(net=subtotal, gross=subtotal)


def get_shipping_gross(checkout: "Checkout", discounts: "SaleQueryset") -> TaxedMoney:
    """Calculate shipping gross for checkout"""
    if not checkout.shipping_method:
        return ZERO_TAXED_MONEY
    if settings.VATLAYER_ACCESS_KEY:
        return vatlayer_interface.get_shipping_gross(checkout, discounts)
    elif settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return avatax_interface.get_shipping_gross(checkout, discounts)
    total = checkout.shipping_method.get_total()
    return TaxedMoney(net=total, gross=total)


def get_lines_with_taxes(checkout: "Checkout", discounts):
    lines_taxes = defaultdict(lambda: Decimal("0.0"))

    if settings.VATLAYER_ACCESS_KEY:
        return vatlayer_interface.get_lines_with_taxes(checkout, discounts)
    elif settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return avatax_interface.get_lines_with_taxes(checkout, discounts)

    return [(line, lines_taxes[line.variant.sku]) for line in checkout.lines.all()]


def apply_taxes_to_shipping(price: Money, shipping_address: "Address") -> TaxedMoney:
    """Apply taxes for shipping methods that user can use during checkout"""
    if shipping_address:
        if settings.VATLAYER_ACCESS_KEY:
            return vatlayer_interface.apply_taxes_to_shipping(price, shipping_address)
        if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
            # FIXME
            pass
    return TaxedMoney(net=price, gross=price)


def get_tax_rate_type_choices():
    if settings.VATLAYER_ACCESS_KEY:
        return vatlayer_interface.get_tax_rate_type_choices()
    if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return []
    return []


def get_line_total_gross(checkout_line: "CheckoutLine", discounts: "SaleQueryset"):
    if settings.VATLAYER_ACCESS_KEY:
        return checkout_line.get_total(discounts)  # FIXME
    if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return avatax_interface.get_line_total_gross(checkout_line, discounts)
    total = checkout_line.get_total(discounts)
    return TaxedMoney(net=total, gross=total)


def refresh_order_line_unit_price(order_line: "OrderLine", discounts: "SaleQueryset"):
    """It updates unit_price for a given order line based on current price of variant"""
    if settings.VATLAYER_ACCESS_KEY:
        address = order_line.order.shipping_address or order_line.order.billing_address
        country = address.country if address else None
        variant = order_line.variant
        return vatlayer_interface.apply_taxes_to_variant(
            variant, variant.get_price(discounts), country
        )
    if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return avatax_interface.refresh_order_line_unit_price(order_line, discounts)
    price = order_line.variant.get_price(discounts)
    return TaxedMoney(net=price, gross=price)


def apply_taxes_to_variant(variant: "ProductVariant", price: Money, country: Country):
    if settings.VATLAYER_ACCESS_KEY:
        return vatlayer_interface.apply_taxes_to_variant(variant, price, country)
    if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return TaxedMoney(
            net=price, gross=price
        )  # FIXME for know we don't know how to get product prices
    return TaxedMoney(net=price, gross=price)


def apply_taxes_to_product(product: "Product", price: Money, country: Country):
    if settings.VATLAYER_ACCESS_KEY:
        return vatlayer_interface.apply_taxes_to_product(product, price, country)
    if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return TaxedMoney(net=price, gross=price)
    return TaxedMoney(net=price, gross=price)


def show_taxes_on_storefront() -> bool:
    """Specify if taxes are enabled"""
    if settings.VATLAYER_ACCESS_KEY:
        return True
    if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
        return False
    return False


def apply_taxes_to_shipping_price_range(prices: MoneyRange, country: Country):
    if country:
        if settings.VATLAYER_ACCESS_KEY:
            return vatlayer_interface.apply_taxes_to_shipping_price_range(
                prices, country
            )
        if settings.AVATAX_USERNAME_OR_ACCOUNT and settings.AVATAX_PASSWORD_OR_LICENSE:
            pass
    start = TaxedMoney(net=prices.start, gross=prices.start)
    stop = TaxedMoney(net=prices.stop, gross=prices.stop)
    return TaxedMoneyRange(start=start, stop=stop)
