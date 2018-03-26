from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from prices import Money

from ...discount import VoucherType
from ...discount.models import NotApplicable
from ...discount.utils import (
    get_product_or_category_voucher_discount, get_shipping_voucher_discount,
    get_value_voucher_discount)
from ...product.utils import decrease_stock

INVOICE_TEMPLATE = 'dashboard/order/pdf/invoice.html'
PACKING_SLIP_TEMPLATE = 'dashboard/order/pdf/packing_slip.html'


def get_statics_absolute_url(request):
    site = get_current_site(request)
    absolute_url = '%(protocol)s://%(domain)s%(static_url)s' % {
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': site.domain,
        'static_url': settings.STATIC_URL,
    }
    return absolute_url


def _create_pdf(rendered_template, absolute_url):
    from weasyprint import HTML
    pdf_file = (HTML(string=rendered_template, base_url=absolute_url)
                .write_pdf())
    return pdf_file


def create_invoice_pdf(order, absolute_url):
    ctx = {'order': order}
    rendered_template = get_template(INVOICE_TEMPLATE).render(ctx)
    pdf_file = _create_pdf(rendered_template, absolute_url)
    return pdf_file, order


def create_packing_slip_pdf(order, fulfillment, absolute_url):
    ctx = {'order': order, 'fulfillment': fulfillment}
    rendered_template = get_template(PACKING_SLIP_TEMPLATE).render(ctx)
    pdf_file = _create_pdf(rendered_template, absolute_url)
    return pdf_file, order


def fulfill_order_line(order_line, quantity):
    """Fulfill order line with given quantity."""
    decrease_stock(order_line.stock, quantity)
    order_line.quantity_fulfilled += quantity
    order_line.save(update_fields=['quantity_fulfilled'])


def update_order_with_user_addresses(order):
    """Update addresses in an order based on a user assigned to an order."""
    if order.shipping_address:
        order.shipping_address.delete()

    if order.billing_address:
        order.billing_address.delete()

    if order.user:
        order.billing_address = (
            order.user.default_billing_address.get_copy()
            if order.user.default_billing_address else None)
        order.shipping_address = (
            order.user.default_shipping_address.get_copy()
            if order.user.default_shipping_address else None)
        order.save()


def get_product_variants_and_prices(order, product):
    """Get variants and unit prices from order lines matching the product."""
    lines = (
        line for line in order.lines.all() if line.product == product)
    for line in lines:
        for dummy_i in range(line.quantity):
            variant = line.product.variants.get(sku=line.product_sku)
            if variant:
                yield variant, variant.get_price_per_item()


def get_category_variants_and_prices(order, root_category):
    """Get variants and unit prices from cart lines matching the category.

    Product is assumed to be in the category if it belongs to any of its
    descendant subcategories.
    """
    products = {line.product for line in order.lines.all() if line.product}
    matching_products = set()
    for product in products:
        if product.category.is_descendant_of(root_category, include_self=True):
            matching_products.add(product)
    for product in matching_products:
        for line in get_product_variants_and_prices(order, product):
            yield line


def _get_value_voucher_discount_for_order(order):
    """Calculate discount value for a voucher of value type."""
    try:
        discount_amount = get_value_voucher_discount(
            order.voucher, order.get_subtotal())
    except NotApplicable:
        discount_amount = Money(0, settings.DEFAULT_CURRENCY)
    return discount_amount


def _get_shipping_voucher_discount_for_order(order):
    """Calculate discount value for a voucher of shipping type."""
    try:
        discount_amount = get_shipping_voucher_discount(
            order.voucher, order.get_subtotal(), order.shipping_price)
    except NotApplicable:
        discount_amount = Money(0, settings.DEFAULT_CURRENCY)
    return discount_amount


def _get_product_or_category_voucher_discount_for_order(order):
    """Calculate discount value for a voucher of product or category type."""
    if order.voucher.type == VoucherType.PRODUCT:
        prices = [
            item[1] for item in get_product_variants_and_prices(
                order, order.voucher.product)]
    else:
        prices = [
            item[1] for item in get_category_variants_and_prices(
                order, order.voucher.category)]
    if not prices:
        return Money(0, settings.DEFAULT_CURRENCY)
    return get_product_or_category_voucher_discount(order.voucher, prices)


def get_voucher_discount_for_order(order):
    """Calculate discount value depending on voucher and discount types.

    Raise NotApplicable if voucher of given type cannot be applied.
    """
    if not order.voucher:
        return None
    if order.voucher.type == VoucherType.VALUE:
        return _get_value_voucher_discount_for_order(order)
    if order.voucher.type == VoucherType.SHIPPING:
        return _get_shipping_voucher_discount_for_order(order)
    if order.voucher.type in (VoucherType.PRODUCT, VoucherType.CATEGORY):
        return _get_product_or_category_voucher_discount_for_order(order)
    raise NotImplementedError('Unknown discount type')
