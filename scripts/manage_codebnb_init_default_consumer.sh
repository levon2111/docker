#!/usr/bin/env bash

export WORKON_HOME=/var/envs
export PROJECT_HOME=/var/www
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin
export PIP_RESPECT_VIRTUALENV=true
export DOCKER_MODE=local

source /var/envs/docker/bin/activate

cd /var/www/docker/

python manage.py init_default_consumer
