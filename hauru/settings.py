# Django settings for hauru project
import os
import configparser
import dj_database_url

BASE = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE, 'hauru.conf')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DEBUG = config.getboolean('general', 'debug')
TEMPLATE_DEBUG = DEBUG

ADMINS = [('Tomek Paczkowski', 'tomek@hauru.eu')]
MANAGERS = ADMINS

ROOT_URLCONF = 'hauru.urls'
WSGI_APPLICATION = 'hauru.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
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
STATIC_ROOT = os.path.join(BASE, 'public')
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