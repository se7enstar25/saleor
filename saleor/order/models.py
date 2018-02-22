from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import pgettext_lazy
from django_prices.models import MoneyField, TaxedMoneyField
from payments import PaymentStatus, PurchasedItem
from payments.models import BasePayment
from prices import Money, TaxedMoney

from . import OrderStatus
from ..account.models import Address
from ..core.utils import ZERO_TAXED_MONEY, build_absolute_uri
from ..discount.models import Voucher
from ..product.models import Product


class Order(models.Model):
    created = models.DateTimeField(
        default=now, editable=False)
    last_status_change = models.DateTimeField(
        default=now, editable=False)
    status = models.CharField(
        max_length=32, default=OrderStatus.UNFULFILLED,
        choices=OrderStatus.CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='orders',
        on_delete=models.SET_NULL)
    language_code = models.CharField(
        max_length=35, default=settings.LANGUAGE_CODE)
    tracking_client_id = models.CharField(
        max_length=36, blank=True, editable=False)
    billing_address = models.ForeignKey(
        Address, related_name='+', editable=False,
        on_delete=models.PROTECT)
    shipping_address = models.ForeignKey(
        Address, related_name='+', editable=False, null=True,
        on_delete=models.PROTECT)
    user_email = models.EmailField(
        blank=True, default='', editable=False)
    shipping_price_net = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        default=0, editable=False)
    shipping_price_gross = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        default=0, editable=False)
    shipping_price = TaxedMoneyField(
        net_field='shipping_price_net', gross_field='shipping_price_gross')
    shipping_method_name = models.CharField(
        max_length=255, null=True, default=None, blank=True, editable=False)
    token = models.CharField(max_length=36, unique=True)
    total_net = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        default=Money(0, settings.DEFAULT_CURRENCY))
    total_gross = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        default=Money(0, settings.DEFAULT_CURRENCY))
    total = TaxedMoneyField(net_field='total_net', gross_field='total_gross')
    voucher = models.ForeignKey(
        Voucher, null=True, related_name='+', on_delete=models.SET_NULL)
    discount_amount = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        blank=True, null=True)
    discount_name = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        ordering = ('-last_status_change',)
        permissions = (
            ('view_order',
             pgettext_lazy('Permission description', 'Can view orders')),
            ('edit_order',
             pgettext_lazy('Permission description', 'Can edit orders')))

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid4())
        return super().save(*args, **kwargs)

    def is_fully_paid(self):
        total_paid = sum(
            [
                payment.get_total_price() for payment in
                self.payments.filter(status=PaymentStatus.CONFIRMED)],
            TaxedMoney(
                net=Money(0, settings.DEFAULT_CURRENCY),
                gross=Money(0, settings.DEFAULT_CURRENCY)))
        return total_paid.gross >= self.total.gross

    def get_user_current_email(self):
        return self.user.email if self.user else self.user_email

    def _index_billing_phone(self):
        return self.billing_address.phone

    def _index_shipping_phone(self):
        return self.shipping_address.phone

    def __iter__(self):
        return iter(self.lines.all())

    def __repr__(self):
        return '<Order #%r>' % (self.id,)

    def __str__(self):
        return '#%d' % (self.id,)

    def get_unfulfilled_lines(self):
        return [line for line in self if not line.is_fulfilled()]

    def get_absolute_url(self):
        return reverse('order:details', kwargs={'token': self.token})

    def get_last_payment_status(self):
        last_payment = self.payments.last()
        if last_payment:
            return last_payment.status
        return None

    def get_last_payment_status_display(self):
        last_payment = self.payments.last()
        if last_payment:
            return last_payment.get_status_display()
        return None

    def is_pre_authorized(self):
        return self.payments.filter(status=PaymentStatus.PREAUTH).exists()

    def is_fulfilled(self):
        return all([line.is_fulfilled() for line in self])

    def is_shipping_required(self):
        return any(line.is_shipping_required for line in self)

    def get_status_display(self):
        """Order status display text."""
        return dict(OrderStatus.CHOICES)[self.status]

    def get_subtotal(self):
        subtotal_iterator = (line.get_total() for line in self)
        return sum(subtotal_iterator, ZERO_TAXED_MONEY)

    def get_total_quantity(self):
        return sum([line.quantity for line in self])

    def can_edit(self):
        return self.status == OrderStatus.UNFULFILLED

    def can_fulfill(self):
        statuses = {OrderStatus.UNFULFILLED, OrderStatus.PARTIALLY_FULFILLED}
        return self.status in statuses

    def can_cancel(self):
        return self.status != OrderStatus.CANCELED


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, related_name='lines', editable=False, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, blank=True, null=True, related_name='+',
        on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=128)
    product_sku = models.CharField(max_length=32)
    is_shipping_required = models.BooleanField()
    stock_location = models.CharField(max_length=100, default='')
    stock = models.ForeignKey(
        'product.Stock', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)])
    unit_price_net = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=4)
    unit_price_gross = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=4)
    unit_price = TaxedMoneyField(
        net_field='unit_price_net', gross_field='unit_price_gross')

    def __str__(self):
        return self.product_name

    def get_total(self):
        return self.unit_price * self.quantity

    @property
    def quantity_unfulfilled(self):
        return self.quantity - self.quantity_fulfilled

    @property
    def quantity_fulfilled(self):
        lines = FulfillmentLine.objects.filter(order_line=self)
        return sum([line.quantity for line in lines])

    def is_fulfilled(self):
        return self.quantity_fulfilled >= self.quantity


class Fulfillment(models.Model):
    fulfillment_order = models.PositiveIntegerField(editable=False, null=True)
    order = models.ForeignKey(
        Order, related_name='fulfillments', editable=False,
        on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255, default='', blank=True)
    shipping_date = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return pgettext_lazy(
            'Fulfillment str', 'Fulfillment #%s') % (self.composed_id,)

    def save(self, *args, **kwargs):
        """"Assign an auto incremented value as a fulfillment order."""
        if not self.pk:
            groups = self.order.fulfillments.all()
            existing_max = groups.aggregate(Max('fulfillment_order'))
            existing_max = existing_max.get('fulfillment_order__max')
            self.fulfillment_order = (
                existing_max + 1 if existing_max is not None else 1)
        return super().save(*args, **kwargs)

    @property
    def composed_id(self):
        return '%s-%s' % (self.order.id, self.fulfillment_order)


class FulfillmentLine(models.Model):
    order_line = models.ForeignKey(
        OrderLine, related_name='+', on_delete=models.CASCADE)
    fulfillment = models.ForeignKey(
        Fulfillment, related_name='lines', on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)])


class PaymentQuerySet(models.QuerySet):
    def last(self):
        # using .all() here reuses data fetched by prefetch_related
        objects = list(self.all()[:1])
        if objects:
            return objects[0]
        return None


class Payment(BasePayment):
    order = models.ForeignKey(
        Order, related_name='payments', on_delete=models.PROTECT)

    objects = PaymentQuerySet.as_manager()

    class Meta:
        ordering = ('-pk',)

    def get_failure_url(self):
        return build_absolute_uri(
            reverse('order:details', kwargs={'token': self.order.token}))

    def get_success_url(self):
        return build_absolute_uri(
            reverse(
                'order:checkout-success', kwargs={'token': self.order.token}))

    def get_purchased_items(self):
        lines = [
            PurchasedItem(
                name=line.product_name, sku=line.product_sku,
                quantity=line.quantity,
                price=line.unit_price_gross.quantize(Decimal('0.01')).amount,
                currency=line.unit_price.currency)
            for line in self.order]

        voucher = self.order.voucher
        if voucher is not None:
            lines.append(
                PurchasedItem(
                    name=self.order.discount_name,
                    sku='DISCOUNT',
                    quantity=1,
                    price=-self.order.discount_amount.amount,
                    currency=self.order.discount_amount.currency))
        return lines

    def get_total_price(self):
        return TaxedMoney(
            net=Money(self.total - self.tax, self.currency),
            gross=Money(self.total, self.currency))

    def get_captured_price(self):
        return TaxedMoney(
            net=Money(self.captured_amount, self.currency),
            gross=Money(self.captured_amount, self.currency))


class OrderHistoryEntry(models.Model):
    date = models.DateTimeField(default=now, editable=False)
    order = models.ForeignKey(
        Order, related_name='history', on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.SET_NULL)

    class Meta:
        ordering = ('date', )


class OrderNote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.SET_NULL)
    date = models.DateTimeField(db_index=True, auto_now_add=True)
    order = models.ForeignKey(
        Order, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ('date', )
