from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}

SCORE = [
    ("a", "отлично"),
    ("b", "хорошо"),
    ("c", "удовлетворительно"),
    ("d", "неудовлетворительно"),
]


class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста", **NULLABLE)
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="courses", on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тест",
        verbose_name_plural = "Тесты"
        ordering = ['completed_at']


class Question(models.Model):
    text = models.TextField(verbose_name="Текст вопроса")
    # right_answer = models.TextField(verbose_name="Правильный ответ")

    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE, verbose_name="Тест")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='results', on_delete=models.CASCADE,
                                verbose_name="Владелец")

    # question_type = models.CharField(max_length=50, )

    def __str__(self):
        return f"Вопрос: {self.text}"

    class Meta:
        verbose_name = "",
        verbose_name_plural = "",
        ordering = ['test']


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ли ответ?")

    def __str__(self):
        return self.text


class TestResult(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='results', on_delete=models.CASCADE,
                                verbose_name="Студент")
    test = models.ForeignKey(Test, related_name='results', on_delete=models.CASCADE)
    count_questions = models.IntegerField(default=0, verbose_name="Количество вопросов")
    count_right_answers = models.IntegerField(default=0, verbose_name="Количество правильных ответов")
    score = models.IntegerField(choices=SCORE, verbose_name="Оценка")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время получения результата")

    def __str__(self):
        return f'{self.student} - {self.test} - {self.score}'

    class Meta:
        verbose_name = "Результат тестирования",
        verbose_name_plural = "Результаты тестирования"
