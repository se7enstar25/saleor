from django.contrib.sites.models import Site
from django.core import signing
from django.core.urlresolvers import reverse

from ..cart.test_cart import variant, product  #    noqa
from ..cart.models import Cart
from ..shipping.models import ShippingMethod
from ..order import Status as OrderStatus
from ..order.models import Order


def test_checkout_flow(product, variant, client):
    """
    Basic test case that confirms if core checkout flow works
    """
    # Prepare some data
    variant.stock.create(quantity=100, location='Warehouse')
    cart = Cart.objects.create()
    cart.add(variant)
    shipping_method = ShippingMethod.objects.create(name='DHL')
    shipping_variant = shipping_method.price_per_country.create(price=10)

    # Resolve urls
    urls = {
        'cart': reverse('cart:index'),
        'checkout_index': reverse('checkout:index'),
        'checkout_shipping_address': reverse('checkout:shipping-address'),
        'checkout_shipping_method': reverse('checkout:shipping-method'),
        'checkout_summary': reverse('checkout:summary')}

    # This is anonymous checkout, so cart token in stored in signed cookie
    value = signing.get_cookie_signer(salt=Cart.COOKIE_NAME).sign(cart.token)
    client.cookies[Cart.COOKIE_NAME] = value

    # Go to cart page
    cart_page = client.get(urls['cart'])
    cart_lines = cart_page.context['cart_lines']
    assert len(cart_lines) == cart.lines.count()
    assert cart_lines[0]['product'] == variant
    # Enter checkout
    checkout_index = client.get(urls['checkout_index'])
    assert checkout_index.status_code == 302
    # Checkout index redirects directly to shipping address step
    assert checkout_index['Location'] == urls['checkout_shipping_address']
    shipping_address = client.get(urls['checkout_shipping_address'])
    assert shipping_address.status_code == 200
    # Enter shipping address data
    shipping_data = {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'street_address_1': 'Some street',
        'street_address_2': '',
        'city': 'Somewhere',
        'city_area': '',
        'country_area': '',
        'postal_code': '50-123',
        'country': 'PL'}
    shipping_response = client.post(
        urls['checkout_shipping_address'], data=shipping_data)
    # Select shipping method
    assert shipping_response.status_code == 302
    assert shipping_response['Location'] == urls['checkout_shipping_method']
    shipping_method_page = client.get(urls['checkout_shipping_method'])
    assert shipping_method_page.status_code == 200
    # Redirect to summary after shipping method selection
    shipping_method_response = client.post(
        urls['checkout_shipping_method'], data={'method': shipping_method.pk})
    assert shipping_method_response.status_code == 302
    assert shipping_method_response['Location'] == urls['checkout_summary']
    # Summary page asks for Billing address, default is the same as shipping
    summary_response = client.post(urls['checkout_summary'],
                                   data={'address': 'shipping_address'})
    assert summary_response.status_code == 302
    # After summary step, order is created and it waits for payment
    order = Order.objects.latest('pk')
    order_payment_url = reverse('order:payment', kwargs={'token': order.token})
    assert summary_response['Location'] == order_payment_url
    payment_method_page = client.get(order_payment_url)
    assert payment_method_page.status_code == 200
    # Select payment method
    payment_page = client.post(order_payment_url, data={'method': 'default'},
                               follow=True)
    assert len(payment_page.redirect_chain) == 1
    assert payment_page.status_code == 200
    # Go to payment details page, enter payment data
    payment_page_url = payment_page.redirect_chain[0][0]
    payment_data = {
        'status': 'preauth',
        'fraud_status': 'unknown',
        'gateway_response': '3ds-disabled',
        'verification_result': 'waiting'}
    payment_response = client.post(payment_page_url, data=payment_data)
    assert payment_response.status_code == 302
    # Target page contains full URL with domain from Site object
    site = Site.objects.get_current()
    order_details = reverse('order:details', kwargs={'token': order.token})
    expected_url = 'http://%s%s' % (site, order_details)
    assert payment_response['Location'] == expected_url
    order_details_page = client.get(order_details)
    assert order_details_page.status_code == 200
    # Check if order has correct totals and payments
    expected_total = variant.get_price() + shipping_variant.price
    assert order.total == expected_total
    assert order.payments.exists()
    payment = order.payments.latest('pk')
    assert payment.status == 'preauth'
    assert order.status == OrderStatus.NEW
