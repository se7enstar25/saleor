import logging
from typing import TYPE_CHECKING, List, Tuple

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound
from django.http.request import split_domain_port

from ....graphql.core.enums import PluginErrorCode
from ....plugins.base_plugin import BasePlugin, ConfigurationTypeField
from ... import TransactionKind
from ...interface import (
    CustomerSource,
    GatewayConfig,
    GatewayResponse,
    PaymentData,
    PaymentMethodInfo,
)
from ...models import Transaction
from ...utils import price_from_minor_unit, price_to_minor_unit
from ..utils import get_supported_currencies, require_active_plugin
from .stripe_api import (
    cancel_payment_intent,
    capture_payment_intent,
    create_payment_intent,
    delete_webhook,
    get_or_create_customer,
    get_payment_method_details,
    is_secret_api_key_valid,
    list_customer_payment_methods,
    refund_payment_intent,
    retrieve_payment_intent,
    subscribe_webhook,
)
from .webhooks import handle_webhook

if TYPE_CHECKING:
    # flake8: noqa
    from ....plugins.models import PluginConfiguration

from .consts import (
    ACTION_REQUIRED_STATUSES,
    AUTHORIZED_STATUS,
    PLUGIN_ID,
    PLUGIN_NAME,
    PROCESSING_STATUS,
    SUCCESS_STATUS,
    WEBHOOK_PATH,
)

logger = logging.getLogger(__name__)


class StripeGatewayPlugin(BasePlugin):
    PLUGIN_NAME = PLUGIN_NAME
    PLUGIN_ID = PLUGIN_ID
    DEFAULT_CONFIGURATION = [
        {"name": "public_api_key", "value": None},
        {"name": "secret_api_key", "value": None},
        {"name": "automatic_payment_capture", "value": True},
        {"name": "supported_currencies", "value": ""},
        {"name": "webhook_endpoint_id", "value": None},
        {"name": "webhook_secret_key", "value": None},
    ]

    CONFIG_STRUCTURE = {
        "public_api_key": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "Provide Stripe public API key.",
            "label": "Public API key",
        },
        "secret_api_key": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": "Provide Stripe secret API key.",
            "label": "Secret API key",
        },
        "automatic_payment_capture": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": "Determines if Saleor should automatically capture payments.",
            "label": "Automatic payment capture",
        },
        "supported_currencies": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "Determines currencies supported by gateway."
            " Please enter currency codes separated by a comma.",
            "label": "Supported currencies",
        },
        "webhook_endpoint_id": {
            "type": ConfigurationTypeField.OUTPUT,
            "help_text": "Unique identifier for the webhook endpoint object.",
            "label": "Webhook endpoint",
        },
    }

    def __init__(self, *args, **kwargs):

        # Webhook details are not listed in CONFIG_STRUCTURE as user input is not
        # required here
        plugin_configuration = kwargs.get("configuration")
        raw_configuration = {
            item["name"]: item["value"] for item in plugin_configuration
        }
        webhook_secret = raw_configuration.get("webhook_secret_key")

        super().__init__(*args, **kwargs)
        configuration = {item["name"]: item["value"] for item in self.configuration}
        self.config = GatewayConfig(
            gateway_name=PLUGIN_NAME,
            auto_capture=configuration["automatic_payment_capture"],
            supported_currencies=configuration["supported_currencies"],
            connection_params={
                "public_api_key": configuration["public_api_key"],
                "secret_api_key": configuration["secret_api_key"],
                "webhook_id": configuration["webhook_endpoint_id"],
                "webhook_secret": webhook_secret,
            },
            store_customer=True,
        )

    def webhook(self, request: WSGIRequest, path: str, previous_value) -> HttpResponse:
        config = self.config
        if path.startswith(WEBHOOK_PATH, 1):  # 1 as we don't check the '/'
            return handle_webhook(request, config, self.channel.slug)  # type: ignore
        logger.warning(
            "Received request to incorrect stripe path", extra={"path": path}
        )
        return HttpResponseNotFound()

    @require_active_plugin
    def token_is_required_as_payment_input(self, previous_value):
        return False

    @require_active_plugin
    def get_supported_currencies(self, previous_value):
        return get_supported_currencies(self.config, PLUGIN_NAME)

    @property
    def order_auto_confirmation(self):
        site_settings = Site.objects.get_current().settings
        return site_settings.automatically_confirm_all_new_orders

    def _get_transaction_details_for_stripe_status(
        self, status: str
    ) -> Tuple[str, bool]:
        kind = TransactionKind.AUTH
        action_required = True

        # payment still requires an action
        if status in ACTION_REQUIRED_STATUSES:
            kind = TransactionKind.ACTION_TO_CONFIRM
        elif status == PROCESSING_STATUS:
            kind = TransactionKind.PENDING
            action_required = False
        elif status == SUCCESS_STATUS:
            kind = TransactionKind.CAPTURE
            action_required = False
        elif status == AUTHORIZED_STATUS:
            kind = TransactionKind.AUTH
            action_required = False

        return kind, action_required

    @require_active_plugin
    def process_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":

        api_key = self.config.connection_params["secret_api_key"]

        auto_capture = self.config.auto_capture
        if self.order_auto_confirmation is False:
            auto_capture = False

        data = payment_information.data

        payment_method_id = data.get("payment_method_id") if data else None

        setup_future_usage = None
        if payment_information.reuse_source:
            setup_future_usage = data.get("setup_future_usage") if data else None

        off_session = data.get("off_session") if data else None

        payment_method_types = data.get("payment_method_types") if data else None

        customer = None
        # confirm that we creates customer on stripe side only for log-in customers
        # Stripe doesn't allow to search users by email, so each create customer
        # call creates new customer on Stripe side.
        if payment_information.graphql_customer_id:
            customer = get_or_create_customer(
                api_key=api_key,
                customer_email=payment_information.customer_email,
                customer_id=payment_information.customer_id,
            )
        intent, error = create_payment_intent(
            api_key=api_key,
            amount=payment_information.amount,
            currency=payment_information.currency,
            auto_capture=auto_capture,
            customer=customer,
            payment_method_id=payment_method_id,
            metadata={
                "channel": self.channel.slug,  # type: ignore
                "payment_id": payment_information.graphql_payment_id,
            },
            setup_future_usage=setup_future_usage,
            off_session=off_session,
            payment_method_types=payment_method_types,
            customer_email=payment_information.customer_email,
        )

        if error and payment_method_id and not intent:
            # we can receive an error which is caused by a required authentication
            # but stripe already created payment_intent.
            stripe_error = error.error
            intent = getattr(stripe_error, "payment_intent", None)
            error = None if intent else error

        raw_response = None
        client_secret = None
        intent_id = None
        kind = TransactionKind.ACTION_TO_CONFIRM
        action_required = True
        if intent:
            kind, action_required = self._get_transaction_details_for_stripe_status(
                intent.status
            )
            client_secret = intent.client_secret
            raw_response = intent.last_response.data
            intent_id = intent.id

        return GatewayResponse(
            is_success=True if not error else False,
            action_required=action_required,
            kind=kind,
            amount=payment_information.amount,
            currency=payment_information.currency,
            transaction_id=intent.id if intent else "",
            error=error.user_message if error else None,
            raw_response=raw_response,
            action_required_data={"client_secret": client_secret, "id": intent_id},
            customer_id=customer.id if customer else None,
            psp_reference=intent.id if intent else None,
        )

    @require_active_plugin
    def confirm_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        payment_intent_id = payment_information.token
        api_key = self.config.connection_params["secret_api_key"]

        # before we will call stripe API, let's check if the transaction object hasn't
        # been created by webhook handler
        payment_transaction = Transaction.objects.filter(
            payment_id=payment_information.payment_id,
            is_success=True,
            action_required=False,
            kind__in=[
                TransactionKind.AUTH,
                TransactionKind.CAPTURE,
                TransactionKind.PENDING,
            ],
        ).first()

        if payment_transaction:
            return GatewayResponse(
                is_success=True,
                action_required=False,
                kind=payment_transaction.kind,
                amount=payment_transaction.amount,
                currency=payment_transaction.currency,
                transaction_id=payment_transaction.token,
                error=None,
                raw_response=payment_transaction.gateway_response,
                transaction_already_processed=True,
            )

        payment_intent = None
        error = None
        payment_method_info = None
        if payment_intent_id:
            payment_intent, error = retrieve_payment_intent(api_key, payment_intent_id)

        kind = TransactionKind.AUTH
        if payment_intent:
            amount = price_from_minor_unit(
                payment_intent.amount, payment_intent.currency
            )
            currency = payment_intent.currency

            kind, action_required = self._get_transaction_details_for_stripe_status(
                payment_intent.status
            )
            if kind == TransactionKind.CAPTURE:
                payment_method_info = get_payment_method_details(payment_intent)
        else:
            action_required = False
            amount = payment_information.amount
            currency = payment_information.currency

        raw_response = None
        if payment_intent and payment_intent.last_response:
            raw_response = payment_intent.last_response.data

        return GatewayResponse(
            is_success=True if payment_intent else False,
            action_required=action_required,
            kind=kind,
            amount=amount,
            currency=currency,
            transaction_id=payment_intent.id if payment_intent else "",
            error=error.user_message if error else None,
            raw_response=raw_response,
            psp_reference=payment_intent.id if payment_intent else None,
            payment_method_info=payment_method_info,
        )

    @require_active_plugin
    def capture_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        payment_intent_id = payment_information.token
        capture_amount = price_to_minor_unit(
            payment_information.amount, payment_information.currency
        )
        payment_intent, error = capture_payment_intent(
            api_key=self.config.connection_params["secret_api_key"],
            payment_intent_id=payment_intent_id,  # type: ignore
            amount_to_capture=capture_amount,
        )

        raw_response = None
        if payment_intent and payment_intent.last_response:
            raw_response = payment_intent.last_response.data

        payment_method_info = None
        if payment_intent and payment_intent.status == SUCCESS_STATUS:
            payment_method_info = get_payment_method_details(payment_intent)

        return GatewayResponse(
            is_success=True if payment_intent else False,
            action_required=False,
            kind=TransactionKind.CAPTURE,
            amount=payment_information.amount,
            currency=payment_information.currency,
            transaction_id=payment_intent.id if payment_intent else "",
            error=error.user_message if error else None,
            raw_response=raw_response,
            payment_method_info=payment_method_info,
        )

    @require_active_plugin
    def refund_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        payment_intent_id = payment_information.token
        refund_amount = price_to_minor_unit(
            payment_information.amount, payment_information.currency
        )
        refund, error = refund_payment_intent(
            api_key=self.config.connection_params["secret_api_key"],
            payment_intent_id=payment_intent_id,  # type: ignore
            amount_to_refund=refund_amount,
        )

        raw_response = None
        if refund and refund.last_response:
            raw_response = refund.last_response.data

        return GatewayResponse(
            is_success=True if refund else False,
            action_required=False,
            kind=TransactionKind.REFUND,
            amount=payment_information.amount,
            currency=payment_information.currency,
            transaction_id=refund.id if refund else "",
            error=error.user_message if error else None,
            raw_response=raw_response,
        )

    @require_active_plugin
    def void_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        payment_intent_id = payment_information.token

        payment_intent, error = cancel_payment_intent(
            api_key=self.config.connection_params["secret_api_key"],
            payment_intent_id=payment_intent_id,  # type: ignore
        )

        raw_response = None
        if payment_intent and payment_intent.last_response:
            raw_response = payment_intent.last_response.data

        return GatewayResponse(
            is_success=True if payment_intent else False,
            action_required=False,
            kind=TransactionKind.VOID,
            amount=payment_information.amount,
            currency=payment_information.currency,
            transaction_id=payment_intent.id if payment_intent else "",
            error=error.user_message if error else None,
            raw_response=raw_response,
        )

    @require_active_plugin
    def list_payment_sources(
        self, customer_id: str, previous_value
    ) -> List[CustomerSource]:
        payment_methods, error = list_customer_payment_methods(
            api_key=self.config.connection_params["secret_api_key"],
            customer_id=customer_id,
        )
        if payment_methods:
            channel_slug: str = self.channel.slug  # type: ignore
            customer_sources = [
                CustomerSource(
                    id=payment_method.id,
                    gateway=PLUGIN_ID,
                    credit_card_info=PaymentMethodInfo(
                        exp_year=payment_method.card.exp_year,
                        exp_month=payment_method.card.exp_month,
                        last_4=payment_method.card.last4,
                        name=None,
                        brand=payment_method.card.brand,
                    ),
                )
                for payment_method in payment_methods
                if payment_method.metadata.get("channel") == channel_slug
            ]
            previous_value.extend(customer_sources)
        return previous_value

    @classmethod
    def pre_save_plugin_configuration(cls, plugin_configuration: "PluginConfiguration"):
        configuration = plugin_configuration.configuration
        flat_configuration = {item["name"]: item["value"] for item in configuration}

        api_key = flat_configuration["secret_api_key"]
        webhook_id = flat_configuration.get("webhook_endpoint_id")
        webhook_secret = flat_configuration.get("webhook_secret_key")

        if not plugin_configuration.active:
            if webhook_id:
                # delete all webhook details when we disable a stripe integration.
                webhook_id_field = [
                    c_field
                    for c_field in configuration
                    if c_field["name"] == "webhook_endpoint_id"
                ][0]
                webhook_id_field["value"] = ""

                plugin_configuration.configuration.remove(
                    {
                        "name": "webhook_secret_key",
                        "value": webhook_secret,
                    }
                )
                delete_webhook(api_key, webhook_id)

            return

        # check saved domain. Make sure that it is not localhost domain. We are not able
        # to subscribe to stripe webhooks with localhost.
        domain = Site.objects.get_current().domain
        localhost_domains = ["localhost", "127.0.0.1"]
        domain, _ = split_domain_port(domain)
        if not domain:
            logger.warning(
                "Site doesn't have defined domain. Unable to subscribe Stripe webhooks"
            )
            return
        if domain in localhost_domains:
            logger.warning(
                "Unable to subscribe localhost domain - %s to Stripe webhooks. Stripe "
                "webhooks require domain which will be accessible from the network",
                domain,
            )
            return

        webhook = None
        if not webhook_id and not webhook_secret:
            webhook = subscribe_webhook(
                api_key, plugin_configuration.channel.slug  # type: ignore
            )

        if not webhook:
            logger.warning(
                "Unable to subscribe to Stripe webhook", extra={"domain": domain}
            )
            return
        cls._update_or_create_config_field(
            plugin_configuration.configuration, "webhook_endpoint_id", webhook.id
        )
        cls._update_or_create_config_field(
            plugin_configuration.configuration, "webhook_secret_key", webhook.secret
        )

    @classmethod
    def _update_or_create_config_field(cls, configuration, field, value):
        for c_field in configuration:
            if c_field["name"] == field:
                c_field["value"] = value
                return
        configuration.append({"name": field, "value": value})

    @classmethod
    def validate_plugin_configuration(cls, plugin_configuration: "PluginConfiguration"):
        configuration = plugin_configuration.configuration
        configuration = {item["name"]: item["value"] for item in configuration}
        required_fields = ["secret_api_key", "public_api_key"]
        all_required_fields_provided = all(
            [configuration.get(field) for field in required_fields]
        )
        if plugin_configuration.active:
            if not all_required_fields_provided:
                raise ValidationError(
                    {
                        field: ValidationError(
                            "The parameter is required.",
                            code=PluginErrorCode.REQUIRED.value,
                        )
                    }
                    for field in required_fields
                )

            api_key = configuration["secret_api_key"]
            if not is_secret_api_key_valid(api_key):
                raise ValidationError(
                    {
                        "secret_api_key": ValidationError(
                            "Secret API key is incorrect",
                            code=PluginErrorCode.INVALID.value,
                        )
                    }
                )

    @require_active_plugin
    def get_payment_config(self, previous_value):
        return [
            {
                "field": "api_key",
                "value": self.config.connection_params["public_api_key"],
            },
        ]
