import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import transaction

from ..core.permissions import get_permission_names
from ..plugins.manager import PluginsManager
from ..webhook.models import Webhook, WebhookEvent
from .manifest_validations import clean_manifest_data
from .models import App, AppExtension, AppInstallation
from .types import AppExtensionTarget, AppType

REQUEST_TIMEOUT = 25


def send_app_token(target_url: str, token: str):
    domain = Site.objects.get_current().domain
    headers = {
        "Content-Type": "application/json",
        # X- headers will be deprecated in Saleor 4.0, proper headers are without X-
        "x-saleor-domain": domain,
        "saleor-domain": domain,
    }
    json_data = {"auth_token": token}
    response = requests.post(
        target_url, json=json_data, headers=headers, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()


def install_app(app_installation: AppInstallation, activate: bool = False):
    response = requests.get(app_installation.manifest_url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    assigned_permissions = app_installation.permissions.all()
    manifest_data = response.json()

    manifest_data["permissions"] = get_permission_names(assigned_permissions)

    clean_manifest_data(manifest_data)

    app = App.objects.create(
        name=app_installation.app_name,
        is_active=activate,
        identifier=manifest_data.get("id"),
        about_app=manifest_data.get("about"),
        data_privacy=manifest_data.get("dataPrivacy"),
        data_privacy_url=manifest_data.get("dataPrivacyUrl"),
        homepage_url=manifest_data.get("homepageUrl"),
        support_url=manifest_data.get("supportUrl"),
        configuration_url=manifest_data.get("configurationUrl"),
        app_url=manifest_data.get("appUrl"),
        version=manifest_data.get("version"),
        type=AppType.THIRDPARTY,
    )
    app.permissions.set(app_installation.permissions.all())
    for extension_data in manifest_data.get("extensions", []):
        extension = AppExtension.objects.create(
            app=app,
            label=extension_data.get("label"),
            url=extension_data.get("url"),
            mount=extension_data.get("mount"),
            target=extension_data.get("target", AppExtensionTarget.POPUP),
        )
        extension.permissions.set(extension_data.get("permissions", []))

    for webhook_data in manifest_data.get("webhooks", []):
        with transaction.atomic():
            webhook = Webhook(
                app=app,
                name=webhook_data["name"],
                target_url=webhook_data["targetUrl"],
                is_active=webhook_data["isActive"],
                subscription_query=webhook_data["query"],
            )
            webhook.full_clean()
            webhook.save()
            WebhookEvent.objects.bulk_create(
                [
                    WebhookEvent(webhook=webhook, event_type=event)
                    for event in (webhook_data.get("asyncEvents", []) + webhook_data.get("syncEvents", []))
                ]
            )

    _, token = app.tokens.create(name="Default token")

    try:
        send_app_token(target_url=manifest_data.get("tokenTargetUrl"), token=token)
    except requests.RequestException as e:
        app.delete()
        raise e
    PluginsManager(plugins=settings.PLUGINS).app_created(app)
    return app, token
