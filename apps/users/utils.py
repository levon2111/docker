from django import forms
from django.contrib.auth import password_validation


def is_invalid_password(password, repeat_password, user):
    """
    check passwords strength and equality
    :param password:
    :param repeat_password:
    :return error message or None:
    """
    error_messages = {
        'not_match': 'Password and Repeat Password fields must match.',
    }

    if not password or (not password and not repeat_password):
        return

    error_message = ''
    try:
        password_validation.validate_password(password=password, )
    except forms.ValidationError as e:
        error_message = list(e.messages)

    if error_message:
        return forms.ValidationError(error_message)

    if password != repeat_password:
        return forms.ValidationError(error_messages['not_match'])
