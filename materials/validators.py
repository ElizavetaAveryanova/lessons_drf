import re

from rest_framework.serializers import ValidationError


class LinkValidator:
    """
    Проверка ссылки на видео
    :param value: вводимая ссылка
    :raise ValidationError: Выводит ошибку, если ссылка не соответствует требованиям
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(
            "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
        )
        tmp_val = dict(value).get(self.field)
        if not bool(reg.match(tmp_val)):
            raise ValidationError(
                "Допустимо добавлять ссылки на материалы, размещенные только на youtube"
            )