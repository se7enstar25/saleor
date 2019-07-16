import importlib
from typing import TYPE_CHECKING, Any, List, Union

from django.conf import settings
from django_countries.fields import Country
from prices import Money, MoneyRange, TaxedMoney, TaxedMoneyRange

from ..taxes import TaxType, quantize_price

if TYPE_CHECKING:
    from ...checkout.models import Checkout, CheckoutLine
    from ...product.models import Product
    from ...account.models import Address
    from ...order.models import OrderLine, Order


class BaseManager:
    """Base manager for handling a plugins logic"""

    plugins = None

    def __init__(self, plugins: List[str]):
        self.plugins = []
        for plugin_path in plugins:
            plugin_path, _, plugin_name = plugin_path.rpartition(".")
            plugin_module = importlib.import_module(plugin_path)
            plugin_class = getattr(plugin_module, plugin_name)
            self.plugins.append(plugin_class())

    def run_plugin_method(self, name: str, default_value: Any, *args, **kwargs):
        value = default_value
        for p in self.plugins:
            plugin_value = getattr(p, name, NotImplemented)(
                *args, **kwargs, previous_value=value
            )
            if plugin_value == NotImplemented:
                continue
            value = plugin_value
        return value

    def calculate_checkout_total(
        self, checkout: "Checkout", discounts: List["DiscountInfo"]
    ) -> TaxedMoney:
        total = checkout.get_total(discounts)
        default_value = quantize_price(
            TaxedMoney(net=total, gross=total), total.currency
        )
        return self.run_plugin_method(
            "calculate_checkout_total", default_value, checkout, discounts
        )

    def calculate_checkout_subtotal(
        self, checkout: "Checkout", discounts: List["DiscountInfo"]
    ) -> TaxedMoney:
        subtotal = checkout.get_subtotal(discounts)
        default_value = quantize_price(
            TaxedMoney(net=subtotal, gross=subtotal), subtotal.currency
        )
        return self.run_plugin_method(
            "calculate_checkout_subtotal", default_value, checkout, discounts
        )

    def calculate_checkout_shipping(
        self, checkout: "Checkout", discounts: List["DiscountInfo"]
    ) -> TaxedMoney:
        total = checkout.get_shipping_price()
        total = TaxedMoney(net=total, gross=total)
        default_value = quantize_price(total, total.currency)
        return self.run_plugin_method(
            "calculate_checkout_shipping", default_value, checkout, discounts
        )

    def calculate_order_shipping(self, order: "Order") -> TaxedMoney:
        shipping_price = order.shipping_method.price
        default_value = quantize_price(
            TaxedMoney(net=shipping_price, gross=shipping_price),
            shipping_price.currency,
        )
        return self.run_plugin_method("calculate_order_shipping", default_value, order)

    def calculate_checkout_line_total(
        self, checkout_line: "CheckoutLine", discounts: List["DiscountInfo"]
    ):
        total = checkout_line.get_total(discounts)
        default_value = quantize_price(
            TaxedMoney(net=total, gross=total), total.currency
        )
        return self.run_plugin_method(
            "calculate_checkout_line_total", default_value, checkout_line, discounts
        )

    def calculate_order_line_unit(self, order_line: "OrderLine"):
        unit_price = order_line.unit_price
        default_value = quantize_price(unit_price, unit_price.currency)
        return self.run_plugin_method(
            "calculate_order_line_unit", default_value, order_line
        )

    def get_tax_rate_type_choices(self) -> List[TaxType]:
        default_value = []
        return self.run_plugin_method("get_tax_rate_type_choices", default_value)

    def show_taxes_on_storefront(self) -> bool:
        default_value = False
        return self.run_plugin_method("show_taxes_on_storefront", default_value)

    def taxes_are_enabled(self) -> bool:

        default_value = False
        return self.run_plugin_method("taxes_are_enabled", default_value)

    def apply_taxes_to_product(
        self, product: "Product", price: Money, country: Country, **kwargs
    ):
        default_value = quantize_price(
            TaxedMoney(net=price, gross=price), price.currency
        )
        return self.run_plugin_method(
            "apply_taxes_to_product", default_value, product, price, country, **kwargs
        )

    def apply_taxes_to_shipping(
        self, price: Money, shipping_address: "Address"
    ) -> TaxedMoney:
        default_value = quantize_price(
            TaxedMoney(net=price, gross=price), price.currency
        )
        return self.run_plugin_method(
            "apply_taxes_to_shipping", default_value, price, shipping_address
        )

    def apply_taxes_to_shipping_price_range(self, prices: MoneyRange, country: Country):
        start = TaxedMoney(net=prices.start, gross=prices.start)
        stop = TaxedMoney(net=prices.stop, gross=prices.stop)
        default_value = quantize_price(
            TaxedMoneyRange(start=start, stop=stop), start.currency
        )
        return self.run_plugin_method(
            "apply_taxes_to_shipping_price_range", default_value, prices, country
        )

    def preprocess_order_creation(
        self, checkout: "Checkout", discounts: List["DiscountInfo"]
    ):
        default_value = None
        return self.run_plugin_method(
            "preprocess_order_creation", default_value, checkout, discounts
        )

    def postprocess_order_creation(self, order: "Order"):
        default_value = None
        return self.run_plugin_method(
            "postprocess_order_creation", default_value, order
        )

    # FIXME these methods should be more generic
    def assign_tax_code_to_object_meta(
        self, obj: Union["Product", "ProductType"], tax_code: str
    ):
        default_value = None
        return self.run_plugin_method(
            "assign_tax_code_to_object_meta", default_value, obj, tax_code
        )

    def get_tax_code_from_object_meta(
        self, obj: Union["Product", "ProductType"]
    ) -> TaxType:
        default_value = TaxType(code="", description="")
        return self.run_plugin_method(
            "get_tax_code_from_object_meta", default_value, obj
        )


def get_extensions_manager(
    manager_path: str = settings.EXTENSIONS_MANAGER,
    plugins: List[str] = settings.PLUGINS,
) -> BaseManager:
    manager_path, _, manager_name = manager_path.rpartition(".")
    manager_module = importlib.import_module(manager_path)
    manager_class = getattr(manager_module, manager_name, None)
    return manager_class(plugins)
