from django.db import models
from config import settings


NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Курс")
    description = models.TextField(verbose_name="Описание", **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="courses", on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['pk']
        constraints = [
            models.UniqueConstraint(fields=['title', 'owner'], name='unique_course_owner')
        ]


class Module(models.Model):
    title = models.CharField(max_length=100, verbose_name="Модуль")
    description = models.TextField(verbose_name="Описание", **NULLABLE)

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="modules", on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"
        ordering = ['pk']
        constraints = [
            models.UniqueConstraint(fields=['title', 'course', 'owner'], name='unique_module_owner')
        ]


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Урок")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(upload_to="media/course", verbose_name="Изображение", blank=True, null=True)
    video = models.URLField(max_length=200, verbose_name="Ссылка на видео", blank=True, null=True)

    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.SET_NULL, **NULLABLE,
                               verbose_name="Модуль")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="lessons", on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['pk']
        constraints = [
            models.UniqueConstraint(fields=['title', 'module', 'owner'], name='unique_lesson_owner')
        ]
