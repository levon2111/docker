# -*- coding: utf-8 -*-

import json

import pika
from django.conf import settings as django_settings

from . import settings


class BasePublisher(object):
    exchange_name = settings.QUEUE_SETTINGS['EXCHANGE_NAME']
    exchange_type = settings.QUEUE_SETTINGS['EXCHANGE_TYPE']

    def __init__(self, routing_key, body):
        self.body = body
        self.routing_key = routing_key

        self.__make_connection()
        self.__exchange_declare()
        self.__basic_publish()

    def __basic_publish(self):
        """
        Publish message to exchange
        :return:
        """

        if not django_settings.TESTING:
            body = json.dumps(self.body)

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=self.routing_key,
                body=body,
            )
            print(" [x] Sent %r" % body)
        self.connection.close()

    def __make_connection(self):
        """
        Make connection with RabbitMQ Server
        :return:
        """
        credentials = pika.PlainCredentials('docker_user', 'root')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', virtual_host='docker', credentials=credentials))
        self.channel = self.connection.channel()

    def __exchange_declare(self):
        """
        Create exchange if not exists
        :return:
        """

        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
