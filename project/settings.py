# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the SHUUP® ENTERPRISE EDITION -
# END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
# and the Licensee.
import os

import dj_database_url
import environ

env = environ.Env(DEBUG=(bool, False))


def optenv(var):
    return env(var, default=None)


root = environ.Path(__file__) - 3

BASE_DIR = root()

DEBUG = env('DEBUG')

env.read_env(os.path.join(BASE_DIR, 'app', '.env'))

SECRET_KEY = env('SECRET_KEY')

DATABASES = {'default': dj_database_url.config()}

MEDIA_URL = env('MEDIA_URL', default='/media/')
STATIC_URL = env('STATIC_URL', default='/static/')

MEDIA_ROOT = root(env('MEDIA_LOCATION', default=os.path.join(BASE_DIR, 'var', 'media')))
STATIC_ROOT = root(env('STATIC_LOCATION', default=os.path.join(BASE_DIR, 'var', 'static')))

SHUUP_HOME_CURRENCY = env('SHOP_CURRENCY', default='USD')

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='*').split(',')


if env('EMAIL_URL', default=None):
    EMAIL_CONFIG = env.email_url('EMAIL_URL')
    vars().update(EMAIL_CONFIG)
else:
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'var', 'emails')
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'


BASE_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',

    # external apps that need to be loaded before Shuup
    'easy_thumbnails',
]

INSTALLED_APPS = BASE_APPS + [
    # Shuup
    'business_logic',
    'shuup.themes.classic_gray',
    'shuup_definite_theme',
    'shuup_megastore_theme',
    'shuup_multivendor',  # Overrides base for fun
    'shuup.admin',
    'shuup.core',
    'shuup.default_tax',
    'shuup.front',
    'shuup.front.apps.auth',
    'shuup.front.apps.carousel',
    'shuup.front.apps.customer_information',
    'shuup.front.apps.personal_order_history',
    'shuup.front.apps.saved_carts',
    'shuup.front.apps.registration',
    'shuup.front.apps.simple_order_notification',
    'shuup.front.apps.simple_search',
    'shuup.notify',
    'shuup.simple_cms',
    'shuup.discounts',
    'shuup.customer_group_pricing',
    'shuup.campaigns',
    'shuup.simple_supplier',
    'shuup.order_printouts',
    'shuup.utils',
    'shuup.xtheme',
    'shuup.reports',
    'shuup.default_reports',
    'shuup.regions',
    'shuup.importer',
    'shuup.default_importer',
    'shuup_us_taxes',
    'shuup_can_taxes',
    'shuup_stripe',
    'shuup_category_organizer',
    'shuup_xtheme_extra_layouts',
    'shuup_subscriptions',
    'shuup_stripe_subscriptions',
    'shuup_product_reviews',
    'shuup_wishlist',
    'shuup_product_comparison',
    'shuup_quickbooks',
    'shuup_stripe_connect',
    'shuup_cms_blog',
    'shuup.api',
    'shuup_mailchimp',
    'shuup_typography',
    'shuup_paypal_capture',
    'shuup.gdpr',
    'shuup_logging',
    'shuup.testing',
    'shuup_messages',

    # Externals
    'raven.contrib.django.raven_compat',
    'bootstrap3',
    'django_countries',
    'django_jinja',
    'filer',
    'registration',
    'reversion',
    'rest_framework',
    'rest_framework_swagger',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shuup.front.middleware.ProblemMiddleware',
    'shuup.front.middleware.ShuupFrontMiddleware',
    'shuup.xtheme.middleware.XthemeMiddleware',
    'shuup.admin.middleware.ShuupAdminMiddleware',
    'shuup_multivendor.middleware.ShuupMultivendorAdminMiddleware'
)

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
LANGUAGE_CODE = env('LANGUAGE_CODE', default='en')
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
RAVEN_CONFIG = {'dsn': optenv('SENTRY_DSN')}

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='no-reply@myshuup.com')

SITE_ID = env('SITE_ID', default=1)

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('fi', 'Finnish'),
    ('ja', 'Japanese'),
    ('zh-hans', 'Simplified Chinese'),
    ('pt-br', 'Portuguese (Brazil)'),
    ('it', 'Italian')
]

selected_languages = env('LANGUAGES', default='en,fi,ja,zh-hans,pt-br,it').split(',')
LANGUAGES = [(code, name) for code, name in LANGUAGE_CHOICES if code in selected_languages]

PARLER_DEFAULT_LANGUAGE_CODE = env('PARLER_DEFAULT_LANGUAGE_CODE', default='en')

PARLER_LANGUAGES = {
    None: [{'code': c, 'name': n} for (c, n) in LANGUAGES],
    'default': {'hide_untranslated': False}
}

_TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.request',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages'
)

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',
            'context_processors': _TEMPLATE_CONTEXT_PROCESSORS,
            'newstyle_gettext': True,
            'environment': 'shuup.xtheme.engine.XthemeEnvironment'
        },
        'NAME': 'jinja2',
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': _TEMPLATE_CONTEXT_PROCESSORS,
            'debug': True
        }
    },
]

CACHES = {'default': env.cache(default='memcache://127.0.0.1:11211')}

SHUUP_SETUP_WIZARD_PANE_SPEC = []  # TODO: fix these

SHUUP_ERROR_PAGE_HANDLERS_SPEC = [
    'shuup.admin.error_handlers:AdminPageErrorHandler',
    'shuup.front.error_handlers:FrontPageErrorHandler'
]

SHUUP_SIMPLE_SEARCH_LIMIT = 50

# Permissions
STAFF_PERMISSION_GROUP_NAME = "Staff"
VENDORS_PERMISSION_GROUP_NAME = "Vendors"

# Shuup (shuup.core)
SHUUP_ENABLE_MULTIPLE_SHOPS = False  # For multivendor marketplace multiple shops is not supported
SHUUP_ENABLE_MULTIPLE_SUPPLIERS = True
SHUUP_MANAGE_CONTACTS_PER_SHOP = True

SHUUP_PRICING_MODULE = "multivendor_supplier_pricing"
SHUUP_SHOP_PRODUCT_SUPPLIERS_STRATEGY = "shuup_multivendor.supplier_strategy:CheapestSupplierPriceSupplierStrategy"

SHUUP_REQUEST_SHOP_PROVIDER_SPEC = ("business_logic.core_shop_provider.DefaultShopProvider")

USA_TAX_DEFAULT_TAX_IDENTIFIER = CAN_TAX_DEFAULT_TAX_IDENTIFIER = "Default tax class"
USA_TAX_ADDITIONAL_TAX_CLASS_IDENTIFIERS = []

SHUUP_PROVIDES_BLACKLIST = {
    "admin_module": [
        "shuup.admin.modules.support:ShuupSupportModule",
        "shuup.testing.modules.sample_data:SampleDataAdminModule",
        "shuup.testing.modules.demo:DemoModule",
        "shuup.testing.modules.mocker:TestingAdminModule,"
    ],
    "admin_order_section": [
        "shuup.admin.modules.orders.sections:BasicDetailsOrderSection",
    ],
    "service_provider_admin_form": [
        "shuup.testing.service_forms:PseudoPaymentProcessorForm",
        "shuup.testing.service_forms:PaymentWithCheckoutPhaseForm",
        "shuup.testing.service_forms:CarrierWithCheckoutPhaseForm",
    ],
    "front_service_checkout_phase_provider": [
        "shuup.testing.simple_checkout_phase.PaymentPhaseProvider",
        "shuup.testing.simple_checkout_phase.ShipmentPhaseProvider",
    ],
    "admin_contact_toolbar_button": [
        "shuup.testing.modules.mocker.toolbar:MockContactToolbarButton",
    ],
    "admin_contact_toolbar_action_item": [
         "shuup.testing.modules.mocker.toolbar:MockContactToolbarActionItem",
    ],
    "admin_contact_edit_toolbar_button": [
        "shuup.testing.modules.mocker.toolbar:MockContactToolbarButton",
    ],
    "admin_product_toolbar_action_item": [
        "shuup.testing.modules.mocker.toolbar:MockProductToolbarActionItem",
    ],
    "admin_contact_section": [
        "shuup.testing.modules.mocker.sections:MockContactSection",
    ],
    "importers": [
        "shuup.testing.importers.DummyImporter",
        "shuup.testing.importers.DummyFileImporter"
    ],
    "xtheme": [
        __name__ + ".themes:ShuupTestingTheme",
        __name__ + ".themes:ShuupTestingThemeWithCustomBase",
    ],
    "pricing_module": [
        "shuup.testing.supplier_pricing.pricing:SupplierPricingModule"
    ],
}

# Shuup (shuup.admin)
SHUUP_ADMIN_SHOP_PROVIDER_SPEC = ("business_logic.admin_shop_provider.AdminShopProvider")
SHUUP_ADMIN_SUPPLIER_PROVIDER_SPEC = "shuup_multivendor.supplier_provider.MultivendorSupplierProvider"

# Shuup (shuup.front)
SHUUP_CHECKOUT_VIEW_SPEC = ("business_logic.views:CheckoutViewWithLoginAndRegisterVertical")
SHUUP_FRONT_OVERRIDE_SORTS_AND_FILTERS_LABELS_LOGIC = {
      "manufacturers": "Brands",
      "supplier": "Filter by vendor"
}

# Shuup Stripe Connect
STRIPE_WEBHOOK_SLUG = env('STRIPE_WEBHOOK_SLUG', default='callback')
STRIPE_WEBHOOK_KEY = env('STRIPE_WEBHOOK_KEY', default=None)
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default=None)
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default=None)
STRIPE_OAUTH_CLIENT_ID = env('STRIPE_OAUTH_CLIENT_ID', default=None)
STRIPE_SUBSCRIPTIONS_API_VERSION = env('STRIPE_SUBSCRIPTIONS_API_VERSION', default='2018')

# Quickbooks
QUICKBOOKS_CLIENT_ID = env("QUICKBOOKS_CLIENT_ID", default=None)
QUICKBOOKS_CLIENT_SECRET = env("QUICKBOOKS_CLIENT_SECRET", default=None)
QUICKBOOKS_SANDBOX_MODE = env.bool("QUICKBOOKS_SANDBOX_MODE", default=True)
QUICKBOOKS_AUTH_CALLBACK_URL = env("QUICKBOOKS_AUTH_CALLBACK_URL", default=None)

# Shuup (shuup.front.apps.registration)
SHUUP_REGISTRATION_REQUIRES_ACTIVATION = env.bool("SHUUP_REGISTRATION_REQUIRES_ACTIVATION", default=False)

# Shuup Multivendor
SHUUP_ADDRESS_HOME_COUNTRY = env("SHUUP_ADDRESS_HOME_COUNTRY", default="CA")
VENDOR_CAN_SHARE_PRODUCTS = env.bool("VENDOR_CAN_SHARE_PRODUCTS", default=True)
SHUUP_MULTIVENDOR_SUPPLIER_MODULE_IDENTIFIER = env("SHUUP_MULTIVENDOR_SUPPLIER_MODULE_IDENTIFIER", default="")
SHUUP_MULTIVENDOR_REGISTRATION_COUNTRIES = env.list("SHUUP_MULTIVENDOR_REGISTRATION_COUNTRIES", default=["CA"])
SHUUP_MULTIVENDOR_ENSURE_ADDRESS_GEOPOSITION = env.bool("SHUUP_MULTIVENDOR_ENSURE_ADDRESS_GEOPOSITION", default=True)
SHUUP_MULTIVENDOR_GOOGLE_MAPS_KEY = env("SHUUP_MULTIVENDOR_GOOGLE_MAPS_KEY", default=None)
SHUUP_MULTIVENDOR_CALCULATE_VENDOR_DISTANCE = env.bool("SHUUP_MULTIVENDOR_CALCULATE_VENDOR_DISTANCE", default=True)
SHUUP_MULTIVENDOR_VENDOR_DISTANCE_UNIT = env("SHUUP_MULTIVENDOR_VENDOR_DISTANCE_UNIT", default="km")

# Shuup API
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'shuup.api.permissions.ShuupAPIPermission',
    )
}

# Adjust default caches for demos so the bumping get better
# tests. Also ususally with demo there is not enough traffic
# to keep caches up for long time of period. If there is
# nobody browsing for 30 min all caches need to rebuild.
SHUUP_TEMPLATE_HELPERS_CACHE_DURATION = 60*420
SHUUP_DEFAULT_CACHE_DURATION = 60*420

SHUUP_LOGGING_ENABLE_BASIC_LOGGING = True
SHUUP_LOGGING_SKIP_MENU_ENTRY_URL_NAMES = []
SHUUP_NOTIFY_SCRIPT_RUNNER = "business_logic.script_runner.run_event"
