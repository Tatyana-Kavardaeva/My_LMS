from rest_framework import serializers
from users.models import User


class AdminRequiredValidator:
    """ Ограничивает регистрацию пользователей с ролью 'администратор' """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        role = dict(value).get(self.field)

        if role == "admin":
            if User.objects.filter(role="admin").exists():
                raise serializers.ValidationError("Ошибка выбора роли. Выберите 'преподаватель' или 'студент'")
