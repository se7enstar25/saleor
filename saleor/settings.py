import ast
import os.path
import warnings

import dj_database_url
import dj_email_url
import sentry_sdk
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django_prices.utils.formatting import get_currency_fraction
from sentry_sdk.integrations.django import DjangoIntegration


def get_list(text):
    return [item.strip() for item in text.split(",")]


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


DEBUG = get_bool_from_env("DEBUG", True)

SITE_ID = 1

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

ROOT_URLCONF = "saleor.urls"

WSGI_APPLICATION = "saleor.wsgi.application"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

ALLOWED_CLIENT_HOSTS = get_list(
    os.environ.get("ALLOWED_CLIENT_HOSTS", "localhost,127.0.0.1")
)

INTERNAL_IPS = get_list(os.environ.get("INTERNAL_IPS", "127.0.0.1"))

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://saleor:saleor@localhost:5432/saleor", conn_max_age=600
    )
}


TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("ar", _("Arabic")),
    ("az", _("Azerbaijani")),
    ("bg", _("Bulgarian")),
    ("bn", _("Bengali")),
    ("ca", _("Catalan")),
    ("cs", _("Czech")),
    ("da", _("Danish")),
    ("de", _("German")),
    ("el", _("Greek")),
    ("en", _("English")),
    ("es", _("Spanish")),
    ("es-co", _("Colombian Spanish")),
    ("et", _("Estonian")),
    ("fa", _("Persian")),
    ("fr", _("French")),
    ("hi", _("Hindi")),
    ("hu", _("Hungarian")),
    ("hy", _("Armenian")),
    ("id", _("Indonesian")),
    ("is", _("Icelandic")),
    ("it", _("Italian")),
    ("ja", _("Japanese")),
    ("ko", _("Korean")),
    ("lt", _("Lithuanian")),
    ("mn", _("Mongolian")),
    ("nb", _("Norwegian")),
    ("nl", _("Dutch")),
    ("pl", _("Polish")),
    ("pt", _("Portuguese")),
    ("pt-br", _("Brazilian Portuguese")),
    ("ro", _("Romanian")),
    ("ru", _("Russian")),
    ("sk", _("Slovak")),
    ("sq", _("Albanian")),
    ("sr", _("Serbian")),
    ("sw", _("Swahili")),
    ("sv", _("Swedish")),
    ("th", _("Thai")),
    ("tr", _("Turkish")),
    ("uk", _("Ukrainian")),
    ("vi", _("Vietnamese")),
    ("zh-hans", _("Simplified Chinese")),
    ("zh-hant", _("Traditional Chinese")),
]
LOCALE_PATHS = [os.path.join(PROJECT_ROOT, "locale")]
USE_I18N = True
USE_L10N = True
USE_TZ = True

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

EMAIL_URL = os.environ.get("EMAIL_URL")
SENDGRID_USERNAME = os.environ.get("SENDGRID_USERNAME")
SENDGRID_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
if not EMAIL_URL and SENDGRID_USERNAME and SENDGRID_PASSWORD:
    EMAIL_URL = "smtp://%s:%s@smtp.sendgrid.net:587/?tls=True" % (
        SENDGRID_USERNAME,
        SENDGRID_PASSWORD,
    )
email_config = dj_email_url.parse(
    EMAIL_URL or "console://demo@example.com:console@example/"
)

EMAIL_FILE_PATH = email_config["EMAIL_FILE_PATH"]
EMAIL_HOST_USER = email_config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email_config["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = email_config["EMAIL_HOST"]
EMAIL_PORT = email_config["EMAIL_PORT"]
EMAIL_BACKEND = email_config["EMAIL_BACKEND"]
EMAIL_USE_TLS = email_config["EMAIL_USE_TLS"]
EMAIL_USE_SSL = email_config["EMAIL_USE_SSL"]

# WARNING: frontend confirmation screen is NOT created yet.
# Enabling this feature will cause incomplete registrations.
# Should remain disabled unless you know what you're doing!
ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL = False

ENABLE_SSL = get_bool_from_env("ENABLE_SSL", False)

if ENABLE_SSL:
    SECURE_SSL_REDIRECT = not DEBUG

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATICFILES_DIRS = [
    ("images", os.path.join(PROJECT_ROOT, "saleor", "static", "images"))
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

context_processors = [
    "django.template.context_processors.debug",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "saleor.checkout.context_processors.checkout_counter",
    "saleor.site.context_processors.site",
]

loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": context_processors,
            "loaders": loaders,
            "string_if_invalid": '<< MISSING VARIABLE "%s" >>' if DEBUG else "",
        },
    }
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "saleor.core.middleware.discounts",
    "saleor.core.middleware.google_analytics",
    "saleor.core.middleware.country",
    "saleor.core.middleware.currency",
    "saleor.core.middleware.site",
    "saleor.core.middleware.extensions",
    "saleor.graphql.middleware.jwt_middleware",
    "saleor.graphql.middleware.service_account_middleware",
]

INSTALLED_APPS = [
    # External apps that need to go before django's
    "storages",
    # Django modules
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.postgres",
    # Local apps
    "saleor.extensions",
    "saleor.account",
    "saleor.discount",
    "saleor.giftcard",
    "saleor.product",
    "saleor.checkout",
    "saleor.core",
    "saleor.graphql",
    "saleor.menu",
    "saleor.order",
    "saleor.seo",
    "saleor.shipping",
    "saleor.search",
    "saleor.site",
    "saleor.data_feeds",
    "saleor.page",
    "saleor.payment",
    "saleor.webhook",
    "saleor.wishlist",
    # External apps
    "versatileimagefield",
    "django_measurement",
    "django_prices",
    "django_prices_openexchangerates",
    "django_prices_vatlayer",
    "graphene_django",
    "mptt",
    "django_countries",
    "django_filters",
    "phonenumber_field",
]


ENABLE_DEBUG_TOOLBAR = get_bool_from_env("ENABLE_DEBUG_TOOLBAR", False)
if ENABLE_DEBUG_TOOLBAR:
    # Ensure the graphiql debug toolbar is actually installed before adding it
    try:
        __import__("graphiql_debug_toolbar")
    except ImportError as exc:
        msg = (
            f"{exc} -- Install the missing dependencies by "
            f"running `pip install -r requirements_dev.txt`"
        )
        warnings.warn(msg)
    else:
        INSTALLED_APPS += ["debug_toolbar", "graphiql_debug_toolbar"]
        MIDDLEWARE.append("saleor.graphql.middleware.DebugToolbarMiddleware")

        DEBUG_TOOLBAR_PANELS = [
            "ddt_request_history.panels.request_history.RequestHistoryPanel",
            "debug_toolbar.panels.timer.TimerPanel",
            "debug_toolbar.panels.headers.HeadersPanel",
            "debug_toolbar.panels.request.RequestPanel",
            "debug_toolbar.panels.sql.SQLPanel",
            "debug_toolbar.panels.profiling.ProfilingPanel",
        ]
        DEBUG_TOOLBAR_CONFIG = {"RESULTS_CACHE_SIZE": 100}

ENABLE_SILK = get_bool_from_env("ENABLE_SILK", False)
if ENABLE_SILK:
    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
    INSTALLED_APPS.append("silk")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(name)s %(message)s [PID:%(process)d:%(threadName)s]"
            )
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
        "django.server": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "saleor": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
        "saleor.graphql.errors.handled": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        # You can configure this logger to go to another file using a file handler.
        # Refer to https://docs.djangoproject.com/en/2.2/topics/logging/#examples.
        # This allow easier filtering from GraphQL query/permission errors that may
        # have been triggered by your frontend applications from the internal errors
        # that happen in backend
        "saleor.graphql.errors.unhandled": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "graphql.execution.utils": {"handlers": ["null"], "propagate": False},
    },
}

AUTH_USER_MODEL = "account.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    }
]

DEFAULT_COUNTRY = os.environ.get("DEFAULT_COUNTRY", "US")
DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "USD")
DEFAULT_DECIMAL_PLACES = get_currency_fraction(DEFAULT_CURRENCY)
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 3

# The default max length for the display name of the
# sender email address.
# Following the recommendation of https://tools.ietf.org/html/rfc5322#section-2.1.1
DEFAULT_MAX_EMAIL_DISPLAY_NAME_LENGTH = 78

# note: having multiple currencies is not supported yet
AVAILABLE_CURRENCIES = [DEFAULT_CURRENCY]

COUNTRIES_OVERRIDE = {
    "EU": pgettext_lazy(
        "Name of political and economical union of european countries", "European Union"
    )
}

OPENEXCHANGERATES_API_KEY = os.environ.get("OPENEXCHANGERATES_API_KEY")

# VAT configuration
# Enabling vat requires valid vatlayer access key.
# If you are subscribed to a paid vatlayer plan, you can enable HTTPS.
VATLAYER_ACCESS_KEY = os.environ.get("VATLAYER_ACCESS_KEY")
VATLAYER_USE_HTTPS = get_bool_from_env("VATLAYER_USE_HTTPS", False)

# Avatax supports two ways of log in - username:password or account:license
AVATAX_USERNAME_OR_ACCOUNT = os.environ.get("AVATAX_USERNAME_OR_ACCOUNT")
AVATAX_PASSWORD_OR_LICENSE = os.environ.get("AVATAX_PASSWORD_OR_LICENSE")
AVATAX_USE_SANDBOX = get_bool_from_env("AVATAX_USE_SANDBOX", DEBUG)
AVATAX_COMPANY_NAME = os.environ.get("AVATAX_COMPANY_NAME", "DEFAULT")
AVATAX_AUTOCOMMIT = get_bool_from_env("AVATAX_AUTOCOMMIT", False)

ACCOUNT_ACTIVATION_DAYS = 3

LOGIN_REDIRECT_URL = "home"

GOOGLE_ANALYTICS_TRACKING_ID = os.environ.get("GOOGLE_ANALYTICS_TRACKING_ID")


def get_host():
    from django.contrib.sites.models import Site

    return Site.objects.get_current().domain


PAYMENT_HOST = get_host

PAYMENT_MODEL = "order.Payment"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

MESSAGE_TAGS = {messages.ERROR: "danger"}

LOW_STOCK_THRESHOLD = 10
MAX_CHECKOUT_LINE_QUANTITY = int(os.environ.get("MAX_CHECKOUT_LINE_QUANTITY", 50))

TEST_RUNNER = "tests.runner.PytestTestRunner"

ALLOWED_HOSTS = get_list(os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1"))
ALLOWED_GRAPHQL_ORIGINS = os.environ.get("ALLOWED_GRAPHQL_ORIGINS", "*")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Amazon S3 configuration
# See https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_LOCATION = os.environ.get("AWS_LOCATION", "")
AWS_MEDIA_BUCKET_NAME = os.environ.get("AWS_MEDIA_BUCKET_NAME")
AWS_MEDIA_CUSTOM_DOMAIN = os.environ.get("AWS_MEDIA_CUSTOM_DOMAIN")
AWS_QUERYSTRING_AUTH = get_bool_from_env("AWS_QUERYSTRING_AUTH", False)
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_STATIC_CUSTOM_DOMAIN")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", None)
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = os.environ.get("AWS_DEFAULT_ACL", None)

# Google Cloud Storage configuration
GS_PROJECT_ID = os.environ.get("GS_PROJECT_ID")
GS_STORAGE_BUCKET_NAME = os.environ.get("GS_STORAGE_BUCKET_NAME")
GS_MEDIA_BUCKET_NAME = os.environ.get("GS_MEDIA_BUCKET_NAME")
GS_AUTO_CREATE_BUCKET = get_bool_from_env("GS_AUTO_CREATE_BUCKET", False)

# If GOOGLE_APPLICATION_CREDENTIALS is set there is no need to load OAuth token
# See https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    GS_CREDENTIALS = os.environ.get("GS_CREDENTIALS")

if AWS_STORAGE_BUCKET_NAME:
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
elif GS_STORAGE_BUCKET_NAME:
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

if AWS_MEDIA_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "saleor.core.storages.S3MediaStorage"
    THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
elif GS_MEDIA_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "saleor.core.storages.GCSMediaStorage"
    THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "products": [
        ("product_gallery", "thumbnail__540x540"),
        ("product_gallery_2x", "thumbnail__1080x1080"),
        ("product_small", "thumbnail__60x60"),
        ("product_small_2x", "thumbnail__120x120"),
        ("product_list", "thumbnail__255x255"),
        ("product_list_2x", "thumbnail__510x510"),
    ],
    "background_images": [("header_image", "thumbnail__1080x440")],
    "user_avatars": [("default", "thumbnail__445x445")],
}

VERSATILEIMAGEFIELD_SETTINGS = {
    # Images should be pre-generated on Production environment
    "create_images_on_demand": get_bool_from_env("CREATE_IMAGES_ON_DEMAND", DEBUG)
}

PLACEHOLDER_IMAGES = {
    60: "images/placeholder60x60.png",
    120: "images/placeholder120x120.png",
    255: "images/placeholder255x255.png",
    540: "images/placeholder540x540.png",
    1080: "images/placeholder1080x1080.png",
}

DEFAULT_PLACEHOLDER = "images/placeholder255x255.png"

LOGOUT_ON_PASSWORD_CHANGE = False

SEARCH_BACKEND = "saleor.search.backends.postgresql"

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]


GRAPHQL_JWT = {"JWT_PAYLOAD_HANDLER": "saleor.graphql.utils.create_jwt_payload"}

# CELERY SETTINGS
CELERY_BROKER_URL = (
    os.environ.get("CELERY_BROKER_URL", os.environ.get("CLOUDAMQP_URL")) or ""
)
CELERY_TASK_ALWAYS_EAGER = not CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", None)

# Rich-text editor
ALLOWED_TAGS = [
    "a",
    "b",
    "blockquote",
    "br",
    "em",
    "h2",
    "h3",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "strong",
    "ul",
]
ALLOWED_ATTRIBUTES = {"*": ["align", "style"], "a": ["href", "title"], "img": ["src"]}
ALLOWED_STYLES = ["text-align"]


# Slugs for menus precreated in Django migrations
DEFAULT_MENUS = {"top_menu_name": "navbar", "bottom_menu_name": "footer"}

# This enable the new 'No Captcha reCaptcha' version (the simple checkbox)
# instead of the old (deprecated) one. For more information see:
#   https://github.com/praekelt/django-recaptcha/blob/34af16ba1e/README.rst
NOCAPTCHA = True

# Set Google's reCaptcha keys
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")


#  Sentry
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

GRAPHENE = {
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
}

EXTENSIONS_MANAGER = "saleor.extensions.manager.ExtensionsManager"

PLUGINS = [
    "saleor.extensions.plugins.avatax.plugin.AvataxPlugin",
    "saleor.extensions.plugins.vatlayer.plugin.VatlayerPlugin",
    "saleor.extensions.plugins.webhook.plugin.WebhookPlugin",
    "saleor.payment.gateways.dummy.plugin.DummyGatewayPlugin",
    "saleor.payment.gateways.stripe.plugin.StripeGatewayPlugin",
    "saleor.payment.gateways.braintree.plugin.BraintreeGatewayPlugin",
    "saleor.payment.gateways.razorpay.plugin.RazorpayGatewayPlugin",
]

# Whether DraftJS should be used be used instead of HTML
# True to use DraftJS (JSON based), for the 2.0 dashboard
# False to use the old editor from dashboard 1.0
USE_JSON_CONTENT = get_bool_from_env("USE_JSON_CONTENT", False)
