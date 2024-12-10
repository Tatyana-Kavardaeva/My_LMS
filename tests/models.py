from django.db import models

from config import settings
from materials.models import Course, Module, Lesson

NULLABLE = {"blank": True, "null": True}

SCORE = [
    ("a", "отлично"),
    ("b", "хорошо"),
    ("c", "удовлетворительно"),
    ("d", "неудовлетворительно"),
]


class Test(models.Model):
    """ Модель теста. """

    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста", **NULLABLE)
    course = models.ForeignKey(Course, related_name="tests", on_delete=models.CASCADE, verbose_name="Курс", **NULLABLE)
    module = models.ForeignKey(Module, related_name="tests", on_delete=models.CASCADE, verbose_name="Модуль",
                               **NULLABLE)
    lesson = models.ForeignKey(Lesson, related_name="tests", on_delete=models.CASCADE, verbose_name="Урок", **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tests", on_delete=models.CASCADE,
                              verbose_name='Владелец')

    def __str__(self):
        return f"Тест: {self.title}"

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ['pk']


class Question(models.Model):
    """ Модель вопроса. """

    text = models.TextField(verbose_name="Текст вопроса")
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE, verbose_name="Тест")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE,
                              verbose_name="Владелец")

    def __str__(self):
        return f"Вопрос: {self.text}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['test']


class Answer(models.Model):
    """ Модель ответа на вопрос в тесте """

    text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="answers", on_delete=models.CASCADE,
                              verbose_name="Владелец")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class StudentAnswer(models.Model):
    """ Модель ответа студента на вопрос в тесте. """

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="student_answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="student_answers", on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name="student_answers", on_delete=models.CASCADE)

    def __str__(self):
        return f"Ответ студента: {self.answer}"

    class Meta:
        verbose_name = "Ответ студента"
        verbose_name_plural = "Ответы студентов"


class TestResult(models.Model):
    """ Модель результата тестирования. """

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="results", on_delete=models.CASCADE,
                                verbose_name="Студент")
    test = models.ForeignKey(Test, related_name="results", on_delete=models.CASCADE)
    count_questions = models.IntegerField(default=0, verbose_name="Количество вопросов")
    count_right_answers = models.IntegerField(default=0, verbose_name="Количество правильных ответов")
    score = models.CharField(choices=SCORE, verbose_name="Оценка")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время получения результата")

    def __str__(self):
        return f'{self.student} - {self.test} - {self.score}'

    class Meta:
        verbose_name = "Результат тестирования"
        verbose_name_plural = "Результаты тестирования"
