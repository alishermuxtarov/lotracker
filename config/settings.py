import os
import sys
from socket import gethostname
import django.conf.locale

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
HOSTNAME = gethostname()
SECRET_KEY = '^dw5atbhvb^hlk-=0@_^txf79qax*#7v0nlpc#9htzse8xxt5b'

# Append module dir
sys.path.append(os.path.join(BASE_DIR, 'apps'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

# is test environment
TEST_MODE = len(sys.argv) > 1 and sys.argv[1] == 'test'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'corsheaders',
    'fcm_django',
    'tinymce',

    'authentication',
    'reference',
    'lotracker',
    'notifier',
    'content',
    'faq',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'smssender.middleware.SqlPrintingMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATE_ROOT = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_ROOT],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            # ]
        },
    },
]

TEMPLATE_DEBUG = False

WSGI_APPLICATION = 'config.wsgi.application'

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]

DATABASES = {
    'default': dj_database_url.config(engine="django.db.backends.postgresql_psycopg2")
}


AUTH_USER_MODEL = 'authentication.User'

# Internationalization

DATE_INPUT_FORMATS = ('%d.%m.%Y', '%Y-%m-%d')

SITE_ID = 1

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Locales
LANGUAGE_COOKIE_NAME = 'language'
gettext = lambda s: s
LANGUAGES = (
    ('uz', gettext('Ўзбек')),
    ('ru', gettext('Русский')),
)

# Add custom languages not provided by Django
EXTRA_LANG_INFO = {
    'uz': {
        'bidi': False,
        'code': 'uz',
        'name': 'Uzbek',
        'name_local': 'Ўзбек',
    },
}

django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)

LANGUAGE_CODE = 'ru'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

"""
Logging
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

"""
REST FRAMEWORK
"""
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.utils.authentication.CustomTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'lotracker.utils.pagination.StandardResultsSetPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'lotracker.utils.filters.CustomSearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'SEARCH_PARAM': 'q'
}

CORS_ORIGIN_ALLOW_ALL = True

SEND_CONFIRMATION_SMS = False

TOKEN = '980698405:AAHVG8mjRygMpvq6-eTUI9qnLp4s3QVYByk'

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "LotrackerPush",  # 532872763322
    "FCM_SERVER_KEY": "AAAAfBGxF7o:APA91bEChNG2W8PfEb3Q3ICOgrFoAUpzDuwHP5bIHpVYL0tNDv4k1OkW1wUz_gWpg20RE-8yllvFa48IB782jIQy49qTEcAmuMsdTRVmawIm94P3GCoyYzOysQlcGqOCyc-8Eb1Ujg2b",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
}

try:
    from config.local import *
except ImportError:
    pass

if DEBUG is True:
    INSTALLED_APPS.append('django_extensions')
