from rest_framework import serializers


class TitleValidator:
    """ Проверяет наличие запрещенных слов в названиях материалов """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        words = ["казино", "криптовалюта", "крипта", "биржа", "обман", "полиция", "радар"]
        title = dict(value).get(self.field).lower()
        print(title)
        print(dict(value))
        for word in words:
            if word in title:
                raise serializers.ValidationError("Использованы запрещенные слова")
