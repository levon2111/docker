# -*- coding: utf-8 -*-

import json

import pika
from django.conf import settings as project_settings

from apps.core.queue_system.methods import ConsumerMethods
from . import settings


class BaseConsumer(object):
    exchange_name = settings.QUEUE_SETTINGS['EXCHANGE_NAME']
    exchange_type = settings.QUEUE_SETTINGS['EXCHANGE_TYPE']
    consumer_name = None

    def init_consumer(self):

        self.__make_connection()
        self.__queue_declare()
        self.__exchange_declare()
        self.__queue_bind()

    def base_consume(self):
        """
        Make consume for catching message
        :return:
        """

        self.channel.basic_consume(self.__callback, queue=self.queue_name)
        self.channel.start_consuming()

    def __callback(self, ch, method, properties, body):
        """
        The main method that will run automatically on catching message
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """

        try:
            body = json.loads(body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return False

        print('[*] Recieved [' + str(body) + ']')

        # Check if the passed routing key available in the settings
        try:
            settings.ROUTING_KEYS[self.consumer_name][method.routing_key]
        except KeyError:
            print('!!! INVALID CONSUMER OR ROUNTING KEY [' + str(self.consumer_name) + ' - ' + str(
                method.routing_key) + ']  !!!')
            return False

        # Call all methods in received routing key
        for consumer_method in settings.ROUTING_KEYS[self.consumer_name][method.routing_key]:

            ConsumerMethods.body = body
            try:
                getattr(ConsumerMethods, consumer_method)()
            except Exception as e:
                from django.core.mail import send_mail
                send_mail(
                    subject='Default consumers crashed',
                    message=str(e),
                    from_email=project_settings.SENDER_EMAIL,
                    recipient_list=['levon2111@gmail.com']
                )

    def __make_connection(self):
        """
        Make connection with RabbitMQ Server
        :return:
        """
        credentials = pika.PlainCredentials('docker_user', 'root')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', virtual_host='docker', credentials=credentials))
        self.channel = self.connection.channel()

    def __queue_declare(self):
        """
        Create queue
        :return:
        """

        queue_details = self.channel.queue_declare(exclusive=True)
        self.queue_name = queue_details.method.queue

    def __exchange_declare(self):
        """
        Create exchange if not exists
        :return:
        """

        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)

    def __queue_bind(self):
        """
        Make connection between queue and exchange by routing key
        :return:
        """

        try:
            settings.ROUTING_KEYS[self.consumer_name]
        except KeyError:
            return

        for key in settings.ROUTING_KEYS[self.consumer_name]:
            print(self.exchange_name)
            print(self.queue_name)
            self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=key)
