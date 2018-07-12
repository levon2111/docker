# -*- coding: utf-8 -*-
from docker.settings.base import *

DEBUG = True
THUMBNAIL_DEBUG = True

BASE_URL = 'http://127.0.0.1:8000'
CLIENT_BASE_URL = 'http://localhost:4200'

BASE_PATH = "/var/www/docker/"

THIRD_PARTY_APPS += [
    'debug_toolbar',
    'django_extensions',
]

INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS + PROJECT_APPS


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docker',
        'USER': 'docker_user',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

SENDER_EMAIL = 'info@docker.codebnb.me'