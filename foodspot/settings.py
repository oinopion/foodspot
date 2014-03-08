# Django settings for foodspot project
from datetime import timedelta
import os
import configparser
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
import django_cache_url

BASE = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE, 'conf', 'foodspot.conf')
if not os.path.exists(CONFIG_PATH):
    raise ImproperlyConfigured('Could not read config: %s' % CONFIG_PATH)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DEBUG = config.getboolean('general', 'debug')
TEMPLATE_DEBUG = DEBUG

ADMINS = [
    ('Tomek Paczkowski', 'tomek@hauru.eu'),
    ('Ola Sendecka', 'ola@hauru.eu'),
]
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
    'django.contrib.sites',
    'django.contrib.redirects',
    'raven.contrib.django.raven_compat',
    'debug_toolbar',
    'foodspot.texts',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

ALLOWED_HOSTS = ['*']
SECRET_KEY = config.get('general', 'secret_key')

DATABASES = {
    'default': dj_database_url.parse(config.get('db', 'default'))
}
DATABASES['default']['CONN_MAX_AGE'] = timedelta(days=1).total_seconds()

CACHES = {
    'default': django_cache_url.parse(config.get('cache', 'default'))
}
CACHES['default']['TIMEOUT'] = timedelta(days=30).total_seconds()
CACHES['default']['KEY_PREFIX'] = config.get('cache', 'prefix', fallback='')

USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'pl-pl'
TIME_ZONE = 'Europe/Warsaw'

LOCALE_PATHS = [os.path.join(BASE, 'locale')]

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

SITE_ID = 1

RAVEN_CONFIG = {
    'dsn': config.get('services', 'sentry_dsn'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s '
                '%(process)d %(thread)d %(message)s'
            )
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['syslog'],
            'propagate': False,
            'level': 'INFO',
        },
        '': {
            'handlers': ['syslog'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}
