from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"blank": True, "null": True}
ROLES = [
    ('admin', 'Администратор'),
    ('teacher', 'Преподаватель'),
    ('student', 'Студент'),
]


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE)
    first_name = models.CharField(max_length=50, verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", **NULLABLE)
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Аватар", **NULLABLE)

    role = models.CharField(choices=ROLES, verbose_name="Роль", **NULLABLE)

    tg_chat_id = models.CharField(max_length=50, verbose_name="Телеграм chat-id", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
