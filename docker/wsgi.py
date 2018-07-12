"""
WSGI config for fms_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_file = os.environ.get('DOCKER_MODE', 'local')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docker.settings.' + settings_file)

application = get_wsgi_application()
