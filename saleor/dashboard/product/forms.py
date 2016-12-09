from __future__ import unicode_literals

from django import forms
from django.db import transaction
from django.forms.models import ModelChoiceIterator, inlineformset_factory
from django.utils.translation import pgettext_lazy

from ...product.models import (AttributeChoiceValue, Product, ProductAttribute,
                               ProductImage, ProductVariant, Stock,
                               VariantImage, ProductClass, StockLocation)
from .widgets import ImagePreviewWidget


class ProductClassSelectorForm(forms.Form):
    product_cls = forms.ChoiceField(
        label=pgettext_lazy('Product class form label', 'Product class'),
        widget=forms.RadioSelect,
        choices=[])

    def __init__(self, *args, **kwargs):
        product_classes = kwargs.pop('product_classes', [])
        super(ProductClassSelectorForm, self).__init__(*args, **kwargs)
        self.fields['product_cls'].choices = [(obj.pk, obj.name)
                                              for obj in product_classes]


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        exclude = ['quantity_allocated']

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product')
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['variant'] = forms.ModelChoiceField(
            queryset=product.variants)


class ProductClassForm(forms.ModelForm):
    class Meta:
        model = ProductClass
        exclude = []

    def clean(self):
        data = super(ProductClassForm, self).clean()
        has_variants = self.cleaned_data['has_variants']
        product_attr = set(self.cleaned_data['product_attributes'])
        variant_attr = set(self.cleaned_data['variant_attributes'])
        if not has_variants and len(variant_attr) > 0:
            msg = pgettext_lazy(
                "Product Class Errors",
                "This class has no variants options selected.")
            self.add_error('variant_attributes', msg)
        if len(product_attr & variant_attr) > 0:
            msg = pgettext_lazy(
                "Product Class Errors",
                "Do not use same attributes in both product and variant.")
            self.add_error('variant_attributes', msg)
        return data


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['attributes', 'product_class']

    def __init__(self, *args, **kwargs):
        self.product_attributes = []
        super(ProductForm, self).__init__(*args, **kwargs)
        field = self.fields['name']
        field.widget.attrs['placeholder'] = pgettext_lazy(
            'Product form labels', 'Give your awesome product a name')
        field = self.fields['categories']
        field.widget.attrs['data-placeholder'] = pgettext_lazy(
            'Product form labels', 'Search')
        field = self.fields['variant_attributes']
        field.widget.attrs['data-placeholder'] = pgettext_lazy(
            'Product form labels', 'Search')
        self.product_attributes = \
            self.instance.product_class.product_attributes.all()
        self.product_attributes = self.product_attributes.prefetch_related(
            'values')
        self.prepare_fields_for_attributes()

    def prepare_fields_for_attributes(self):
        for attribute in self.product_attributes:
            field_defaults = {'label': attribute.display,
                              'required': False,
                              'initial': self.instance.get_attribute(
                                  attribute.pk)}
            if attribute.has_values():
                field = CachingModelChoiceField(
                    queryset=attribute.values.all(), **field_defaults)
            else:
                field = forms.CharField(**field_defaults)
            self.fields[attribute.get_formfield_name()] = field

    def iter_attribute_fields(self):
        for attr in self.product_attributes:
            yield self[attr.get_formfield_name()]

    def save(self, commit=True):
        attributes = {}
        for attribute in self.product_attributes:
            value = self.cleaned_data.pop(attribute.get_formfield_name())
            if value is not None:
                attributes[attribute.pk] = value.pk
        self.instance.attributes = attributes
        return super(ProductForm, self).save(commit=commit)


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        exclude = ['attributes', 'product', 'images']

    def __init__(self, *args, **kwargs):
        super(ProductVariantForm, self).__init__(*args, **kwargs)
        if self.instance.product.pk:
            self.fields['price_override'].widget.attrs[
                'placeholder'] = self.instance.product.price.gross
            self.fields['weight_override'].widget.attrs[
                'placeholder'] = self.instance.product.weight


class CachingModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ('', self.field.empty_label)
        for obj in self.queryset:
            yield self.choice(obj)


class CachingModelChoiceField(forms.ModelChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CachingModelChoiceIterator(self)
    choices = property(_get_choices, forms.ChoiceField._set_choices)


class VariantAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = []

    def __init__(self, *args, **kwargs):
        super(VariantAttributeForm, self).__init__(*args, **kwargs)
        attrs = self.instance.product.product_class.variant_attributes.all()
        self.available_attrs = attrs.prefetch_related('values')
        for attr in self.available_attrs:
            field_defaults = {'label': attr.display,
                              'required': True,
                              'initial': self.instance.get_attribute(attr.pk)}
            if attr.has_values():
                field = CachingModelChoiceField(
                    queryset=attr.values.all(), **field_defaults)
            else:
                field = forms.CharField(**field_defaults)
            self.fields[attr.get_formfield_name()] = field

    def save(self, commit=True):
        attributes = {}
        for attr in self.available_attrs:
            value = self.cleaned_data.pop(attr.get_formfield_name())
            attributes[attr.pk] = value.pk if hasattr(value, 'pk') else value
        self.instance.attributes = attributes
        return super(VariantAttributeForm, self).save(commit=commit)


class VariantBulkDeleteForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=ProductVariant.objects)

    def delete(self):
        items = ProductVariant.objects.filter(
            pk__in=self.cleaned_data['items'])
        items.delete()


class StockBulkDeleteForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=Stock.objects)

    def delete(self):
        items = Stock.objects.filter(pk__in=self.cleaned_data['items'])
        items.delete()


class ProductImageForm(forms.ModelForm):
    variants = forms.ModelMultipleChoiceField(
        queryset=ProductVariant.objects.none(),
        widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = ProductImage
        exclude = ('product', 'order')

    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)
        if self.instance.product:
            variants = self.fields['variants']
            variants.queryset = self.instance.product.variants.all()
            variants.initial = self.instance.variant_images.values_list(
                'variant', flat=True)
        if self.instance.image:
            self.fields['image'].widget = ImagePreviewWidget()

    @transaction.atomic
    def save_variant_images(self, instance):
        variant_images = []
        # Clean up old mapping
        instance.variant_images.all().delete()
        for variant in self.cleaned_data['variants']:
            variant_images.append(
                VariantImage(variant=variant, image=instance))
        VariantImage.objects.bulk_create(variant_images)

    def save(self, commit=True):
        instance = super(ProductImageForm, self).save(commit=commit)
        self.save_variant_images(instance)
        return instance


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        exclude = []


class StockLocationForm(forms.ModelForm):
    class Meta:
        model = StockLocation
        exclude = []


AttributeChoiceValueFormset = inlineformset_factory(
    ProductAttribute, AttributeChoiceValue, exclude=(), extra=1)
