from __future__ import unicode_literals

import logging
from functools import wraps

from django.conf import settings
from django.db.models import F
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import pgettext_lazy
from payments.signals import status_changed
from prices import Price
from satchless.item import InsufficientStock

from ..core import analytics
from ..product.models import Stock
from ..userprofile.utils import store_user_address
from .models import Order
from . import OrderStatus

logger = logging.getLogger(__name__)


def check_order_status(func):
    """Preserves execution of function if order is fully paid by redirecting
    to order's details page."""
    @wraps(func)
    def decorator(*args, **kwargs):
        token = kwargs.pop('token')
        order = get_object_or_404(Order, token=token)
        if order.is_fully_paid():
            return redirect('order:details', token=order.token)
        kwargs['order'] = order
        return func(*args, **kwargs)

    return decorator


@receiver(status_changed)
def order_status_change(sender, instance, **kwargs):
    """Handles payment status change and sets suitable order status."""
    order = instance.order
    if order.is_fully_paid():
        order.status = OrderStatus.FULLY_PAID
        order.save()
        order.create_history_entry(
            status=OrderStatus.FULLY_PAID, comment=pgettext_lazy(
                'Order status history entry', 'Order fully paid'))
        instance.send_confirmation_email()
        try:
            analytics.report_order(order.tracking_client_id, order)
        except Exception:
            # Analytics failing should not abort the checkout flow
            logger.exception('Recording order in analytics failed')


def order_cancel(order):
    """Cancells order by cancelling all associated shipment groups."""
    for group in order.groups.all():
        delivery_group_cancel(group, cancel_order=False)
    order.status = OrderStatus.CANCELLED
    order.save()


def order_recalculate(order):
    """Recalculates and assigns total price of order.
    Total price is a sum of items and shippings in order shipment groups. """
    prices = [
        group.get_total() for group in order
        if group.status != OrderStatus.CANCELLED]
    total_net = sum(p.net for p in prices)
    total_gross = sum(p.gross for p in prices)
    total = Price(
        net=total_net, gross=total_gross,
        currency=settings.DEFAULT_CURRENCY)
    shipping = [group.shipping_price for group in order]
    total_shipping = (
        sum(shipping[1:], shipping[0]) if shipping
        else Price(0, currency=settings.DEFAULT_CURRENCY))
    total += total_shipping
    order.total = total
    order.save()


def order_attach_to_user(order, user):
    """Associates existing order with user account."""
    order.user = user
    store_user_address(user, order.billing_address, billing=True)
    if order.shipping_address:
        store_user_address(user, order.shipping_address, shipping=True)
    order.save(update_fields=['user'])


def delivery_group_fill_with_partition(group, partition, discounts=None):
    """Fills shipment group with order lines created from partition items.
    """
    for item in partition:
        delivery_group_add_variant(
            group, item.variant, item.get_quantity(), discounts,
            add_to_existing=False)


def delivery_group_add_variant(
        group, variant, total_quantity, discounts=None, add_to_existing=True):
    """Adds total_quantity of variant to group.
    Raises InsufficientStock exception if quantity could not be fulfilled.

    By default, first adds variant to existing lines with same variant.
    It can be disabled with setting add_to_existing to False.

    Order lines are created by increasing quantity of lines,
    as long as total_quantity of variant will be added.
    """
    quantity_left = (
        delivery_group_add_variant_to_existing_lines(group, variant, total_quantity)
        if add_to_existing else total_quantity)
    price = variant.get_price_per_item(discounts)
    while quantity_left > 0:
        stock = variant.select_stockrecord()
        if not stock:
            raise InsufficientStock(variant)
        quantity = (
            stock.quantity_available
            if quantity_left > stock.quantity_available
            else quantity_left
        )
        group.lines.create(
            product=variant.product,
            product_name=variant.display_product(),
            product_sku=variant.sku,
            quantity=quantity,
            unit_price_net=price.net,
            unit_price_gross=price.gross,
            stock=stock,
            stock_location=stock.location.name)
        Stock.objects.allocate_stock(stock, quantity)
        # refresh stock for accessing quantity_allocated
        stock.refresh_from_db()
        quantity_left -= quantity


def delivery_group_add_variant_to_existing_lines(group, variant, total_quantity):
    """Adds variant to existing lines with same variant.

    Variant is added by increasing quantity of lines with same variant,
    as long as total_quantity of variant will be added
    or there is no more lines with same variant.

    Returns quantity that could not be fulfilled with existing lines.
    """
    # order descending by lines' stock available quantity
    lines = group.lines.filter(
        product=variant.product, product_sku=variant.sku,
        stock__isnull=False).order_by(
            F('stock__quantity_allocated') - F('stock__quantity'))

    quantity_left = total_quantity
    for line in lines:
        quantity = (
            line.stock.quantity_available
            if quantity_left > line.stock.quantity_available
            else quantity_left)
        line.quantity += quantity
        line.save()
        Stock.objects.allocate_stock(line.stock, quantity)
        quantity_left -= quantity
        if quantity_left == 0:
            break
    return quantity_left


def delivery_group_cancel(group, cancel_order=True):
    """Cancells shipment group and (optionally) it's order if necessary."""
    for line in group:
        if line.stock:
            Stock.objects.deallocate_stock(line.stock, line.quantity)
    group.status = OrderStatus.CANCELLED
    group.save()
    if cancel_order:
        other_groups = group.order.groups.all()
        statuses = set(other_groups.values_list('status', flat=True))
        if statuses == {OrderStatus.CANCELLED}:
            # Cancel whole order
            group.order.status = OrderStatus.CANCELLED
            group.order.save(update_fields=['status'])


def order_line_merge_with_duplicates(line):
    """Merges duplicated lines in shipment group into one (given) line.
    If there are no duplicates, nothing will happen.
    """
    lines = line.delivery_group.lines.filter(
        product=line.product, product_name=line.product_name,
        product_sku=line.product_sku, stock=line.stock)
    if lines.count() > 1:
        line.quantity = sum([line.quantity for line in lines])
        line.save()
        lines.exclude(pk=line.pk).delete()


def order_line_change_quantity(line, new_quantity):
    """Change the quantity of ordered items in a order line."""
    line.quantity = new_quantity
    line.save()

    if not line.delivery_group.get_total_quantity():
        line.delivery_group.delete()
        order = line.delivery_group.order
        if not order.get_lines():
            order.status = OrderStatus.CANCELLED
            order.save()
            order.create_history_entry(
                status=OrderStatus.CANCELLED, comment=pgettext_lazy(
                    'Order status history entry',
                    'Order cancelled. No items in order'))
