import os
import sys
from pathlib import Path

from django.conf import settings

# Общие настройки
COMMON_CONTENT = {
    'name_store': '3D Master',
    'main': 'Главная',
    'about': 'О нас',
    'services': 'Сервисы',
    'contact': 'Контакты',
    'phone': '+7 999 678 43 20',
    'email_store': 'store3dzepko@yandex.ru',
    'address': 'ул. Кирова, 40',
    'city': 'Новокузнецк',
}

# Настройки email
EMAIL_ADMIN = 'store3dzepko'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # Адрес SMTP-сервера
EMAIL_HOST_PASSWORD = 'ayncendtfishzsdx'
EMAIL_HOST_USER = EMAIL_ADMIN
EMAIL_PORT = 465  # Порт SMTP-сервера (обычно 465 для SSL)
EMAIL_USE_SSL = True  # Использовать SSL (а не TLS)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


AUTH_USER_MODEL = 'mainapp.User'

# Остальные настройки
ALLOWED_HOSTS = []
APPEND_SLASH = True
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DEBUG = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'bootstrap5',
]
LANGUAGE_CODE = 'en-us'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
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
ROOT_URLCONF = 'store_3d.urls'

SECRET_KEY = 'django-insecure-dsd$%#+z%2qsy@euh)lpsr5&#h4%i+)o@kbmsyhh8z^(uvr%0j'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

SASS_PROCESSOR_ROOT = STATIC_ROOT

SECRET_KEY = 'django-insecure-dsd$%#+z%2qsy@euh)lpsr5&#h4%i+)o@kbmsyhh8z^(uvr%0j'

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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = 'store_3d.wsgi.application'

# Дополнительные настройки
settings.CONTENT_TYPES = {
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "text/javascript",
    "json": "application/json",
}
