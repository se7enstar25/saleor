# encoding: utf-8
from __future__ import unicode_literals

from allauth.account.adapter import get_adapter
from allauth.account.forms import SetPasswordField
from django import forms
from django.utils.translation import ugettext_lazy as _

from .i18n import AddressMetaForm, get_address_form_class


def get_address_form(data, country_code, initial=None, instance=None, **kwargs):
    country_form = AddressMetaForm(data, initial=initial)
    preview = False

    if country_form.is_valid():
        country_code = country_form.cleaned_data['country']
        preview = country_form.cleaned_data['preview']

    address_form_class = get_address_form_class(country_code)

    if not preview and instance is not None:
        address_form_class = get_address_form_class(
            instance.country.code)
        address_form = address_form_class(
            data, instance=instance,
            **kwargs)
    else:
        initial_address = (
            initial if not preview
            else data.dict() if data is not None else data)
        address_form = address_form_class(
            not preview and data or None,
            initial=initial_address,
            **kwargs)
    return address_form, preview


class SetPasswordForm(forms.Form):
    password = SetPasswordField(label=_('New Password'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password'].user = self.user

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data['password'])
