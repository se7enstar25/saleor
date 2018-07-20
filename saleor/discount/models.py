from datetime import date
from decimal import Decimal
from functools import partial

from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils.translation import pgettext, pgettext_lazy
from django_countries.fields import CountryField
from django_prices.models import MoneyField
from django_prices.templatetags.prices_i18n import amount
from prices import Money, fixed_discount, percentage_discount

from . import DiscountValueType, VoucherType


class NotApplicable(ValueError):
    """Exception raised when a discount is not applicable to a checkout.

    The error is raised if the order value is below the minimum required
    price.
    Minimum price will be available as the `min_amount_spent` attribute.
    """

    def __init__(self, msg, min_amount_spent=None):
        super().__init__(msg)
        self.min_amount_spent = min_amount_spent


class VoucherQueryset(models.QuerySet):
    def active(self, date):
        return self.filter(
            Q(usage_limit__isnull=True) | Q(used__lt=F('usage_limit')),
            Q(end_date__isnull=True) | Q(end_date__gte=date),
            start_date__lte=date)


class Voucher(models.Model):
    type = models.CharField(
        max_length=20, choices=VoucherType.CHOICES, default=VoucherType.VALUE)
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=12, unique=True, db_index=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used = models.PositiveIntegerField(default=0, editable=False)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)

    discount_value_type = models.CharField(
        max_length=10, choices=DiscountValueType.CHOICES,
        default=DiscountValueType.FIXED)
    discount_value = models.DecimalField(
        max_digits=12, decimal_places=settings.DEFAULT_DECIMAL_PLACES)

    # not mandatory fields, usage depends on type
    countries = CountryField(multiple=True, blank=True)
    min_amount_spent = MoneyField(
        currency=settings.DEFAULT_CURRENCY, max_digits=12,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES, null=True, blank=True)
    products = models.ManyToManyField('product.Product', blank=True)
    collections = models.ManyToManyField('product.Collection', blank=True)

    objects = VoucherQueryset.as_manager()

    def __str__(self):
        if self.name:
            return self.name
        discount = '%s %s' % (
            self.discount_value, self.get_discount_value_type_display())
        if self.type == VoucherType.SHIPPING:
            if self.is_free:
                return pgettext('Voucher type', 'Free shipping')
            return pgettext(
                'Voucher type',
                '%(discount)s off shipping') % {'discount': discount}
        if self.type == VoucherType.PRODUCT:
            return pgettext(
                'Voucher type',
                '%(discount)s off %(product_num)d products') % {
                    'discount': discount,
                    'product_num': len(self.products.all())}
        # TODO its collections now
        if self.type == VoucherType.CATEGORY:
            return pgettext(
                'Voucher type',
                '%(discount)s off %(collections_num)d collections') % {
                    'discount': discount,
                    'collections_num': len(self.collections.all())}
        return pgettext(
            'Voucher type', '%(discount)s off') % {'discount': discount}

    @property
    def is_free(self):
        return (
            self.discount_value == Decimal(100) and
            self.discount_value_type == DiscountValueType.PERCENTAGE)

    def get_discount(self):
        if self.discount_value_type == DiscountValueType.FIXED:
            discount_amount = Money(
                self.discount_value, settings.DEFAULT_CURRENCY)
            return partial(fixed_discount, discount=discount_amount)
        if self.discount_value_type == DiscountValueType.PERCENTAGE:
            return partial(percentage_discount, percentage=self.discount_value)
        raise NotImplementedError('Unknown discount type')

    def get_discount_amount_for(self, price):
        discount = self.get_discount()
        gross_price = price.gross
        gross_after_discount = discount(gross_price)
        if gross_after_discount.amount < 0:
            return gross_price
        return gross_price - gross_after_discount

    def validate_min_amount_spent(self, value):
        min_amount_spent = self.min_amount_spent
        if min_amount_spent and value.gross < min_amount_spent:
            msg = pgettext(
                'Voucher not applicable',
                'This offer is only valid for orders over %(amount)s.')
            raise NotApplicable(msg % {
                'amount': amount(min_amount_spent)},
                min_amount_spent=min_amount_spent)


class Sale(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10, choices=DiscountValueType.CHOICES,
        default=DiscountValueType.FIXED)
    value = models.DecimalField(
        max_digits=12, decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0)
    products = models.ManyToManyField('product.Product', blank=True)
    categories = models.ManyToManyField('product.Category', blank=True)
    collections = models.ManyToManyField('product.Collection', blank=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        app_label = 'discount'
        permissions = ((
            'manage_discounts', pgettext_lazy(
                'Permission description', 'Manage sales and vouchers.')),)

    def __repr__(self):
        return 'Sale(name=%r, value=%r, type=%s)' % (
            str(self.name), self.value, self.get_type_display())

    def __str__(self):
        return self.name

    def get_discount(self):
        if self.type == DiscountValueType.FIXED:
            discount_amount = Money(self.value, settings.DEFAULT_CURRENCY)
            return partial(fixed_discount, discount=discount_amount)
        if self.type == DiscountValueType.PERCENTAGE:
            return partial(percentage_discount, percentage=self.value)
        raise NotImplementedError('Unknown discount type')
