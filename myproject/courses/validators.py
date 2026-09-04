import re
from rest_framework.serializers import ValidationError


def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведет на youtube.com
    """
    if not value:
        return value

    # Проверяем, что ссылка содержит youtube.com или youtu.be
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/'

    if not re.search(youtube_pattern, value):
        raise ValidationError(
            'Разрешены только ссылки на YouTube (youtube.com или youtu.be)'
        )

    return value


class YouTubeURLValidator:
    """
    Класс-валидатор для проверки ссылок на YouTube
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value:
            return validate_youtube_url(value)
        return attrs
    