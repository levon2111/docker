# -*- coding: utf-8 -*-

from docker.settings.base import *

DEBUG = True
THUMBNAIL_DEBUG = True

CLIENT_BASE_URL = 'http://docker-client.codebnb.me'
BASE_URL = 'http://docker-api.codebnb.me'
ALLOWED_HOSTS = ['*', ]

BASE_PATH = "/var/www/subdomains/codebnb/docker_api/public_html"

THIRD_PARTY_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docker',
        'USER': 'docker_user',
        'PASSWORD': 'asdfhc8wvntewczg9rk9v787455e5iqx',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
