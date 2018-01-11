from django import forms
from django.utils.translation import npgettext, pgettext_lazy
from django_filters import (
    CharFilter, ChoiceFilter, ModelMultipleChoiceFilter, RangeFilter,
    OrderingFilter)

from ...core.filters import SortedFilterSet
from ..widgets import PriceRangeWidget
from ...product.models import (
    Category, Product, ProductAttribute, ProductClass, StockLocation)

PRODUCT_SORT_BY_FIELDS = {
    'name': pgettext_lazy('Product list sorting option', 'name'),
    'price': pgettext_lazy('Product type list sorting option', 'price')}

PRODUCT_ATTRIBUTE_SORT_BY_FIELDS = {
    'name': pgettext_lazy('Product attribute list sorting option', 'name')}

PRODUCT_CLASS_SORT_BY_FIELDS = {
    'name': pgettext_lazy('Product type list sorting option', 'name')}

STOCK_LOCATION_SORT_BY_FIELDS = {
    'name': pgettext_lazy('Stock location list sorting option', 'name')}

PUBLISHED_CHOICES = (
    ('1', pgettext_lazy('Is publish filter choice', 'Published')),
    ('0', pgettext_lazy('Is publish filter choice', 'Not published')))

FEATURED_CHOICES = (
    ('1', pgettext_lazy('Is featured filter choice', 'Featured')),
    ('0', pgettext_lazy('Is featured filter choice', 'Not featured')))


class ProductFilter(SortedFilterSet):
    name = CharFilter(
        label=pgettext_lazy('Product list filter label', 'Name'),
        lookup_expr='icontains')
    categories = ModelMultipleChoiceFilter(
        label=pgettext_lazy('Product list filter label', 'Categories'),
        name='categories',
        queryset=Category.objects.all())
    product_class = ModelMultipleChoiceFilter(
        label=pgettext_lazy('Product list filter label', 'Product type'),
        name='product_class',
        queryset=ProductClass.objects.all())
    price = RangeFilter(
        label=pgettext_lazy('Product list filter label', 'Price'),
        name='price',
        widget=PriceRangeWidget)
    is_published = ChoiceFilter(
        label=pgettext_lazy('Product list filter label', 'Is published'),
        choices=PUBLISHED_CHOICES,
        empty_label=pgettext_lazy('Filter empty choice label', 'All'),
        widget=forms.Select)
    is_featured = ChoiceFilter(
        label=pgettext_lazy(
            'Product list is featured filter label', 'Is featured'),
        choices=FEATURED_CHOICES,
        empty_label=pgettext_lazy('Filter empty choice label', 'All'),
        widget=forms.Select)
    sort_by = OrderingFilter(
        label=pgettext_lazy('Product list filter label', 'Sort by'),
        fields=PRODUCT_SORT_BY_FIELDS.keys(),
        field_labels=PRODUCT_SORT_BY_FIELDS)

    class Meta:
        model = Product
        fields = []

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard products list',
            'Found %(counter)d matching product',
            'Found %(counter)d matching products',
            number=counter) % {'counter': counter}


class ProductAttributeFilter(SortedFilterSet):
    name = CharFilter(
        label=pgettext_lazy('Product attribute list filter label', 'Name'),
        lookup_expr='icontains')
    sort_by = OrderingFilter(
        label=pgettext_lazy('Product attribute list filter label', 'Sort by'),
        fields=PRODUCT_CLASS_SORT_BY_FIELDS.keys(),
        field_labels=PRODUCT_CLASS_SORT_BY_FIELDS)

    class Meta:
        model = ProductAttribute
        fields = []

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard '
            'product attributes list',
            'Found %(counter)d matching attribute',
            'Found %(counter)d matching attributes',
            number=counter) % {'counter': counter}


class ProductClassFilter(SortedFilterSet):
    name = CharFilter(
        label=pgettext_lazy('Product type list filter label', 'Name'),
        lookup_expr='icontains')
    sort_by = OrderingFilter(
        label=pgettext_lazy('Product class list filter label', 'Sort by'),
        fields=PRODUCT_CLASS_SORT_BY_FIELDS.keys(),
        field_labels=PRODUCT_CLASS_SORT_BY_FIELDS)

    class Meta:
        model = ProductClass
        fields = ['name', 'product_attributes', 'variant_attributes']

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            'Number of matching records in the dashboard product types list',
            'Found %(counter)d matching product type',
            'Found %(counter)d matching product types',
            number=counter) % {'counter': counter}


class StockLocationFilter(SortedFilterSet):
    sort_by = OrderingFilter(
        label=pgettext_lazy(
            'Stock location list filter label', 'Sort by'),
        fields=STOCK_LOCATION_SORT_BY_FIELDS.keys(),
        field_labels=STOCK_LOCATION_SORT_BY_FIELDS)
    name = CharFilter(
        label=pgettext_lazy('Stock location list filter label', 'Name'),
        lookup_expr='icontains')

    class Meta:
        model = StockLocation
        fields = []
