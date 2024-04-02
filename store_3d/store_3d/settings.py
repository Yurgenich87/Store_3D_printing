import os
import sys
from pathlib import Path

from django.conf import settings

# Common settings
COMMON_CONTENT = {
    'name_store': '3D Master',
    'main': 'Main',
    'about': 'About',
    'services': 'Services',
    'contact': 'Contact',
    'phone': '+7 999 678 43 20',
    'email_store': 'store3dzepko@yandex.ru',
    'address': '40 Kirova St',
    'city': 'Novokuznetsk',
}

# Email settings
EMAIL_ADMIN = 'store3dzepko@mail.ru'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_PASSWORD = 'CeEvdV7hkSXZamK8VDET'
EMAIL_HOST_USER = EMAIL_ADMIN
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Authentication settings
AUTH_USER_MODEL = 'mainapp.User'


ALLOWED_HOSTS = [
    '127.0.0.1',
    'store3dzepko.pythonanywhere.com',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

APPEND_SLASH = True

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug mode
DEBUG = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'bootstrap5',
    'debug_toolbar',
]

# Middleware settings
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'mainapp.middleware.AdminRedirectMiddleware',
]


# Language code
LANGUAGE_CODE = 'en-us'

# Login and logout URLs
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'


# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Root URL configuration
ROOT_URLCONF = 'store_3d.urls'

# Secret key
SECRET_KEY = 'django-insecure-dsd$%#+z%2qsy@euh)lpsr5&#h4%i+)o@kbmsyhh8z^(uvr%0j'

# Static files finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# Static files settings
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# SASS processor settings
SASS_PROCESSOR_ROOT = STATIC_ROOT

# Templates directory
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

# Time zone settings
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# WSGI application
WSGI_APPLICATION = 'store_3d.wsgi.application'

# Additional content types
settings.CONTENT_TYPES = {
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "text/javascript",
    "json": "application/json",
}

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process} {thread} {message}',
            'style': '{',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': './logs/django.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'mainapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
