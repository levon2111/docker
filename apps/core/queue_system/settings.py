# -*- coding: utf-8 -*-


QUEUE_SETTINGS = {
    'EXCHANGE_NAME': 'default',
    'EXCHANGE_TYPE': 'topic'
}

ROUTING_KEYS = {
    'default_consumer': {
        'core.send_email': ['send_email', ],
    },
}
