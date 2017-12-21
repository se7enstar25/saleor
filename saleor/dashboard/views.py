from django.conf import settings
from django.contrib.admin.views.decorators import \
    staff_member_required as _staff_member_required
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Q, Sum
from django.template.response import TemplateResponse
from payments import PaymentStatus

from ..order.models import Order, Payment
from ..order import OrderStatus
from ..product.models import Product


def staff_member_required(f):
    return _staff_member_required(f, login_url='account_login')


def superuser_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url='account_login'):
    """
    Decorator for views that checks that the user is logged in and is a
    superuser, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


@staff_member_required
def index(request):
    INDEX_PAGINATE_BY = 10
    orders_to_ship = Order.objects.open().select_related(
        'user').prefetch_related('groups', 'groups__lines', 'payments')
    orders_to_ship = [
        order for order in orders_to_ship if order.is_fully_paid()]
    payments = Payment.objects.filter(
        status=PaymentStatus.PREAUTH).order_by('-created')
    payments = payments.select_related('order', 'order__user')
    low_stock = get_low_stock_products()
    ctx = {'preauthorized_payments': payments[:INDEX_PAGINATE_BY],
           'orders_to_ship': orders_to_ship[:INDEX_PAGINATE_BY],
           'low_stock': low_stock[:INDEX_PAGINATE_BY]}
    return TemplateResponse(request, 'dashboard/index.html', ctx)


@staff_member_required
def styleguide(request):
    return TemplateResponse(request, 'dashboard/styleguide/index.html', {})


def get_low_stock_products():
    threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 10)
    products = Product.objects.annotate(
        total_stock=Sum('variants__stock__quantity'))
    return products.filter(Q(total_stock__lte=threshold)).distinct()
