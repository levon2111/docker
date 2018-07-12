import hashlib
import json
import random
import string
import uuid

from django.conf import settings
from django.core import serializers

from apps.core.queue_system.publisher import BasePublisher


def generate_unique_key(value, length=40):
    """
    generate key from passed value
    :param value:
    :param length: key length
    :return:
    """

    salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(26)).encode(
        'utf-8')
    value = value.encode('utf-8')
    unique_key = hashlib.sha1(salt + value).hexdigest()

    return unique_key[:length]


def send_email_job(to, template, context, subject):
    from_email = settings.SENDER_EMAIL
    to_email = [to]

    context['client_side_url'] = settings.CLIENT_BASE_URL

    # New job
    BasePublisher(
        routing_key='core.send_email',
        body={
            'context': context,
            'to': to_email,
            'from_email': from_email,
            'template': template,
            'subject': subject,
        }
    )


def send_email_job_registration(text, to, template, context, subject):
    to_email = [to]
    context['client_side_url'] = settings.CLIENT_BASE_URL

    # New job
    BasePublisher(
        routing_key='core.send_email',
        body={
            'context': context,
            'to': to_email,
            'from_email': text + ' <info@docker.codebnb.me>',
            'template': template,
            'subject': subject,
        }
    )


def model_to_dict(instance):
    """
    Generate dict object from received model instance
    :param instance:
    :return: dict
    """

    serialized_instance = json.loads(serializers.serialize('json', [instance, ]))[0]
    instance_dict = serialized_instance['fields']

    # add instance pk to the fields dict
    instance_dict['id'] = serialized_instance['pk']

    return instance_dict


def get_file_path(filename, folder):
    """
    generate file path for field
    :param filename: selected file name
    :param folder: upload destination folder
    :return:
    """

    if hasattr(settings, 'AMAZON_S3_BUCKET'):
        folder = settings.AMAZON_S3_BUCKET + '/' + folder

    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)

    return folder + '/' + filename


def add_list_to_request(request, key):
    """
    # Fix list field issue when content-type is not www-urlencoded
    :param request:
    :param key:
    :return:
    """

    if key in request.data:
        try:
            data = json.loads(request.data[key])
        except (TypeError, ValueError,):
            return

        request.data.setlist(key, data)


def increase_month(date, month):
    """
    Increase Month
    :param date:
    :param month:
    :return:
    """

    m, y = (date.month + month) % 12, date.year + (date.month + month - 1) // 12
    if not m:
        m = 12
    d = min(date.day,
            [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])

    return date.replace(day=d, month=m, year=y)


def generate_html_list(objects_list):
    """
    Generates HTML <ul> <li> </li> </ul> lists from received objects_list
    :param objects_list: list of strings
    :return: (string) Html list
    """

    result = '<ul>'
    for object in objects_list:
        result += '<li> {0} </li>'.format(object)
    result += '</ul>'

    return result
