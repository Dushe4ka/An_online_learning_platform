from rest_framework.serializers import ValidationError


class YouTubeValidation:
    """ Валидатор для ссылки на YoutTube """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # OrderedDict переводим в dict, и получаем зн. поля, которое нужно валидировать.
        val = dict(value).get(self.field)
        if val and "youtube.com" not in val:
            raise ValidationError("Ссылка на видео должна быть только на YoutTube")
