from tests.models import Question, StudentAnswer


def calculate_score(result):
    """ Получает итоговую оценку за пройденный тест """
    test_id = result.test.pk
    count_questions = Question.objects.filter(test=test_id).count()
    count_right_answers = StudentAnswer.objects.filter(student=result.student, question__test=test_id,
                                                       answer__is_correct=True).count()

    percent = (count_right_answers / count_questions * 100) if count_questions > 0 else 0
    score = ""

    if 0 <= percent < 35:
        score = "d"
    elif 35 <= percent < 70:
        score = "c"
    elif 70 <= percent < 90:
        score = "b"
    elif 90 <= percent <= 100:
        score = "a"

    result.count_questions = count_questions
    result.count_right_answers = count_right_answers
    result.score = score
    result.save()
