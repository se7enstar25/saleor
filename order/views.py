from .steps import BillingAddressStep
from cart import get_cart_from_request, remove_cart_from_request, \
    CartPartitioner
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from order.models import Order
from order.steps import SuccessStep
from satchless.process import ProcessManager


class CheckoutProcessManager(ProcessManager):

    def __init__(self, order, request):
        self.order = order
        self.request = request

    def __iter__(self):
        yield BillingAddressStep(self.order, self.request)
        yield SuccessStep(self.order, self.request)


def index(request, token=None):
    try:
        order = Order.objects.get(token=token)
    except Order.DoesNotExist:
        cart = get_cart_from_request(request)
        if not cart:
            return redirect('cart:index')
        order = Order.objects.create_from_partitions(CartPartitioner(cart))
    remove_cart_from_request(request)
    checkout = CheckoutProcessManager(order, request)
    return redirect(checkout.get_next_step())


def details(request, token, step):
    order = get_object_or_404(Order, token=token)
    checkout = CheckoutProcessManager(order, request)
    try:
        step = checkout[step]
    except KeyError:
        raise Http404()
    response = step.process()
    return response or redirect(checkout.get_next_step())

