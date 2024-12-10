from django.db import models
from config import settings


NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """ Модель курса. """

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


class Module(models.Model):
    """ Модель модуля. """

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


class Lesson(models.Model):
    """ Модель урока. """

    title = models.CharField(max_length=100, verbose_name="Урок")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(upload_to="media/course", verbose_name="Изображение", blank=True, null=True)
    video = models.URLField(max_length=200, verbose_name="Ссылка на видео", blank=True, null=True)
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.SET_NULL, **NULLABLE,
                               verbose_name="Модуль")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="lessons", on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['pk']


class Enrollment(models.Model):
    """ Модель зачисления на курс. """

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return f"{self.student} {self.course}"

    class Meta:
        verbose_name = "Зачисление на курс"
        verbose_name_plural = "Зачисления на курс"
        ordering = ['pk']
