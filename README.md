Docker Development Guide

For apache configuration

    sudo apt-get install libapache2-mod-wsgi-py3

Development setup

Install required system packages:

    sudo apt-get install python3-pip
    sudo apt-get install python3-dev python3-setuptools
    sudo apt-get install libpq-dev
    sudo apt-get install postgresql postgresql-contrib

Create www directory where project sites and environment dir

    mkdir /var/www && mkdir /var/envs && mkdir /var/envs/bin

Install virtualenvwrapper

    sudo pip3 install virtualenvwrapper
    sudo pip3 install --upgrade virtualenv

Add these to your bashrc virutualenvwrapper work

    export WORKON_HOME=/var/envs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export PROJECT_HOME=/var/www
    export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin    
    source /usr/local/bin/virtualenvwrapper.sh

Create virtualenv

    cd /var/envs && mkvirtualenv --python=/usr/bin/python docker


Install requirements for a project.

    cd /var/www/docker && pip install -r requirements/local.txt
    sudo chown :www-data /var/www/docker

##Database creation
###For psql

    sudo su - postgres
    psql > DROP DATABASE IF EXISTS docker;
    psql > CREATE DATABASE docker;
    psql > CREATE USER docker_user WITH password 'root';
    psql > GRANT ALL privileges ON DATABASE docker TO docker_user;
    psql > ALTER USER docker_user CREATEDB;

    
Set up supervisor (pm2)

    $ sudo apt-get install python-software-properties
    $ curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
    $ sudo apt-get install nodejs
    $ cd /var/www/subdomains/codebnb/docker_api/public_html
    $ pm2 startup ubuntu14
    $ pm2 start scripts/manage_codebnb_init_default_consumer.sh --name docker_api_init_default_consumer
    $ pm2 save

More about pm2 is here https://github.com/Unitech/pm2


Configure rabbitmq-server to run workers.
Add virtual host, and set permissions.

    $ sudo rabbitmqctl add_vhost docker
    $ sudo rabbitmqctl add_user docker_user root
    $ sudo rabbitmqctl set_permissions -p docker docker_user ".*" ".*" ".*"
