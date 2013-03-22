from delivery import DummyShipping, DigitalDelivery
from django.conf import settings
from django.utils.translation import ugettext
from itertools import groupby
from prices import Price
from product.models import StockedProduct, DigitalShip
from satchless import cart
from satchless.item import Item, ItemLine, ItemSet, Partitioner
from userprofile.forms import AddressForm
import datetime


class Group(ItemSet):

    def get_delivery_methods(self, **kwargs):
        raise NotImplementedError()

    def get_delivery_total(self, **kwargs):
        methods = self.get_delivery_methods()
        return min(method.get_price_per_item(**kwargs) for method in methods)


class ShippedGroup(Group):

    def get_delivery_methods(self):
        yield DummyShipping(self)


class DigitalGroup(Group):

    def get_delivery_methods(self, **kwargs):
        yield DigitalDelivery(self)


class CartPartitioner(Partitioner):

    def __iter__(self):
        for product_class, items in groupby(
                self.subject,
                lambda cart_item: cart_item.product.__class__):
            delivery_class = ShippedGroup
            if issubclass(product_class, DigitalShip):
                delivery_class = DigitalGroup
            delivery = delivery_class(items)
            yield delivery

    def get_delivery_subtotal(self, partion, **kwargs):
        return partion.get_delivery_total(**kwargs)

    def get_delivery_total(self, **kwargs):
        items = [self.get_delivery_subtotal(partion, **kwargs)
                 for partion in self]
        if not items:
            raise AttributeError(
                'Calling get_delivery_total() for an empty cart')
        return sum(items[1:], items[0])

    def __repr__(self):
        return 'CartPartitioner(%r)'%(list(self),)


class InsufficientStockException(Exception):

    def __init__(self, product):
        super(InsufficientStockException, self).__init__(
            'Insufficient stock for %r' % (product,))
        self.product = product


class Cart(cart.Cart):

    SESSION_KEY = 'cart'
    timestamp = None
    billing_address = None

    def __init__(self, *args, **kwargs):
        super(Cart, self).__init__(self, *args, **kwargs)
        self.timestamp = datetime.datetime.now()

    def __unicode__(self):
        return ugettext('Your cart (%(cart_count)s)') % {
            'cart_count': self.count()}

    def check_quantity(self, product, quantity, data=None):
        if (isinstance(product, StockedProduct) and
            quantity > product.stock):
            raise InsufficientStockException(product)
        return super(Cart, self).check_quantity(product, quantity, data)


def get_cart_from_request(request):
    try:
        return request.session[Cart.SESSION_KEY]
    except KeyError:
        _cart = Cart()
        request.session[Cart.SESSION_KEY] = _cart
        return _cart


def remove_cart_from_request(request):
    del request.session[Cart.SESSION_KEY]
