from __future__ import unicode_literals

from django import forms
from django.utils.translation import pgettext_lazy

from ...product.models import (ProductImage, Stock, ProductVariant, Product)


PRODUCT_CLASSES = {
    Product: 'Default'
}


def get_verbose_name(model):
    return model._meta.verbose_name


class ProductClassForm(forms.Form):
    product_cls = forms.ChoiceField(
        label=pgettext_lazy('Product class form label', 'Product class'),
        widget=forms.RadioSelect,
        choices=[(cls.__name__, presentation) for cls, presentation in
                 PRODUCT_CLASSES.iteritems()])

    def __init__(self, *args, **kwargs):
        super(ProductClassForm, self).__init__(*args, **kwargs)
        self.fields['product_cls'].initial = PRODUCT_CLASSES.keys()[0].__name__


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        exclude = []
        widgets = {
            'product': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product')
        super(StockForm, self).__init__(*args, **kwargs)
        variants = product.variants.all()
        if variants:
            self.fields['variant'].choices = [(variant.pk, variant) for variant in variants]
        else:
            self.fields['variant'].widget.attrs['disabled'] = True


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = []


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        exclude = []
        widgets = {
            'product': forms.HiddenInput()
        }


def get_product_form(product):
    if isinstance(product, Product):
        return ProductForm
    else:
        raise ValueError('Unknown product class')


def get_product_cls_by_name(cls_name):
    for cls in PRODUCT_CLASSES.keys():
        if cls_name == cls.__name__:
            return cls
    raise ValueError('Unknown product class')


def get_variant_form(product):
    if isinstance(product, Product):
        return ProductVariantForm
    else:
        raise ValueError('Unknown product class')


def get_variant_cls(product):
    if isinstance(product, Product):
        return ProductVariant
    else:
        raise ValueError('Unknown product class')


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        exclude = ('product', 'order')
