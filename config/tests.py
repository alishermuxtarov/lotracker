from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {}
    }
}

CHECK_URL_PERMISSIONS = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

USE_TZ = True
