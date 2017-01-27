from allauth.account.adapter import get_adapter
from allauth.account.forms import ChangePasswordForm
from allauth.account.utils import logout_on_password_change
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _

from .forms import get_address_form


@login_required
def details(request):
    password_form = get_or_process_password_form(request)
    ctx = {'addresses': request.user.addresses.all(),
           'orders': request.user.orders.prefetch_related('groups__items'),
           'change_password_form': password_form}

    return TemplateResponse(request, 'userprofile/details.html', ctx)


def get_or_process_password_form(request):
    form = ChangePasswordForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        logout_on_password_change(request, form.user)
        get_adapter(request).add_message(
            request,
            messages.SUCCESS,
            'account/messages/password_changed.txt')
    return form


@login_required
def address_edit(request, pk):
    address = get_object_or_404(request.user.addresses, pk=pk)
    address_form, preview = get_address_form(
        request.POST or None, instance=address,
        country_code=address.country.code)
    if address_form.is_valid() and not preview:
        address_form.save()
        message = _('Address successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('profile:details'))
    return TemplateResponse(
        request, 'userprofile/address-edit.html',
        {'address_form': address_form})

@login_required
def address_delete(request, pk):
    address = get_object_or_404(request.user.addresses, pk=pk)
    if request.method == 'POST':
        address.delete()
        messages.success(request, _('Address successfully deleted.'))
        return HttpResponseRedirect(reverse('profile:details') + '#addresses')
    return TemplateResponse(
        request, 'userprofile/address-delete.html', {'address': address})
