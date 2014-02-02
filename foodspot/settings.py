# Django settings for foodspot project
import os
import configparser
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE, 'conf', 'foodspot.conf')
if not os.path.exists(CONFIG_PATH):
    raise ImproperlyConfigured('Could not read config: %s' % CONFIG_PATH)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DEBUG = config.getboolean('general', 'debug')
TEMPLATE_DEBUG = DEBUG

ADMINS = [('Tomek Paczkowski', 'tomek@hauru.eu')]
MANAGERS = ADMINS

ROOT_URLCONF = 'foodspot.urls'
WSGI_APPLICATION = 'foodspot.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'foodspot.texts',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ALLOWED_HOSTS = ['*']
SECRET_KEY = config.get('general', 'secret_key')

DATABASES = {
    'default': dj_database_url.parse(config.get('db', 'default'))
}

USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

TEMPLATE_DIRS = [os.path.join(BASE, 'templates')]
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )

STATICFILES_DIRS = [os.path.join(BASE, 'static')]
STATICFILES_STORAGE = \
    'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
STATIC_ROOT = config.get(
    'files', 'static', fallback=os.path.join(BASE, 'public'))
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
