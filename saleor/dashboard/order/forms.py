from django import forms
from django.utils.translation import ugettext_lazy as _
from satchless.item import InsufficientStock

from ...cart.forms import QuantityField
from ...order.models import DeliveryGroup, OrderedItem, OrderNote
from ...product.models import Product


class OrderNoteForm(forms.ModelForm):

    class Meta:
        model = OrderNote
        fields = ['content']
        widgets = {'content': forms.Textarea({
            'rows': 5, 'placeholder': _('Note')})}

    def __init__(self, *args, **kwargs):
        super(OrderNoteForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ''


class ManagePaymentForm(forms.Form):
    amount = forms.DecimalField(min_value=0, decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        self.payment = kwargs.pop('payment')
        super(ManagePaymentForm, self).__init__(*args, **kwargs)

    def handle_action(self, action, user):
        if action == 'capture' and self.payment.status == 'preauth':
            self.payment.capture(amount=self.cleaned_data['amount'], user=user)
        elif action == 'refund' and self.payment.status == 'confirmed':
            self.payment.refund(amount=self.cleaned_data['amount'], user=user)
        elif action == 'release' and self.payment.status == 'preauth':
            self.payment.release(user=user)


class MoveItemsForm(forms.ModelForm):
    quantity = QuantityField()
    groups = forms.ChoiceField()

    class Meta:
        model = OrderedItem
        fields = []

    def __init__(self, *args, **kwargs):
        super(MoveItemsForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['max'] = self.instance.quantity
        self.fields['groups'].choices = self.get_delivery_group_choices()

    def get_delivery_group_choices(self):
        group = self.instance.delivery_group
        groups = group.order.groups.exclude(pk=group.pk).exclude(
            status='cancelled')
        choices = [('new', _('New'))]
        choices.extend([(g.pk, 'Delivery group #%s' % g.pk) for g in groups])
        return choices

    def save(self, user=None):
        quantity = self.cleaned_data['quantity']
        choice = self.cleaned_data['groups']
        origin_group = DeliveryGroup.objects.select_subclasses().get(
            pk=self.instance.delivery_group.pk)
        if choice == 'new':
            group = origin_group
            group.pk = None
            group.id = None
            group.status = 'new'
            address = origin_group.address
            address.pk = None
            address.save()
            group.address = address
            group.save()
        else:
            group = DeliveryGroup.objects.get(pk=choice)
        self.instance.move_to_group(group, quantity, user)
        comment = _('Moved %(quantity)s items %(item)s from group '
                    '#%(old_group)s to group #%(new_group)s' % {
                    'quantity': quantity, 'item': self.instance,
                    'old_group': self.instance.delivery_group.pk,
                    'new_group': group.pk})
        group.order.create_history_entry(comment=comment, user=user)


class ChangeQuantityForm(forms.ModelForm):

    class Meta:
        model = OrderedItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(ChangeQuantityForm, self).__init__(*args, **kwargs)
        self.initial_quantity = self.instance.quantity
        self.fields['quantity'].widget.attrs['max'] = self.instance.quantity
        self.fields['quantity'].initial = self.initial_quantity

    def get_variant(self):
        p = Product.objects.select_subclasses().get(pk=self.instance.product.pk)
        return p.variants.get(sku=self.instance.product_sku)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        variant = self.get_variant()
        try:
            variant.check_quantity(quantity)
        except InsufficientStock as e:
            msg = _('Only %(remaining)d remaining in stock.')
            raise forms.ValidationError(msg % {'remaining': e.item.stock})
        return quantity

    def save(self, user):
        order = self.instance.delivery_group.order
        quantity = self.cleaned_data['quantity']
        self.instance.change_quantity(quantity)
        comment = _('Changed quantity for product %(product)s from '
                    '%(old_quantity)s to %(new_quantity)s' % {
                        'new_quantity': quantity,
                        'old_quantity': self.initial_quantity,
                        'product': self.instance.product})
        order.create_history_entry(comment=comment, user=user)


class ShipGroupForm(forms.ModelForm):

    class Meta:
        model = DeliveryGroup
        fields = []

    def clean(self):
        if self.instance.status != 'new':
            raise forms.ValidationError(_('Cannot ship this group'),
                                        code='invalid')

    def save(self, user):
        order = self.instance.order
        self.instance.change_status('shipped')
        comment = _('Shipped delivery group #%s' % self.instance.pk)
        order.history.create(status=order.status, comment=comment, user=user)
        statuses = [g.status for g in order.groups.all()]
        if 'shipped' in statuses and 'new' not in statuses:
            order.change_status('shipped')
