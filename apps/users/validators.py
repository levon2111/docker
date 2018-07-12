from apps.users.utils import is_invalid_password


def check_valid_password(data, user=None):
    invalid_password_message = is_invalid_password(data.get('password'), data.get('repeat_password'), user=user)
    if invalid_password_message:
        return invalid_password_message
