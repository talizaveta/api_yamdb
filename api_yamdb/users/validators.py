import re
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя не может быть <me>',
            params={'value': value}
        )
    if re.search(r'^[\w.@+-]+$', value) is None:
        raise ValidationError(
            'Использованы недопустимые символы',
            params={'value': value}
        )
