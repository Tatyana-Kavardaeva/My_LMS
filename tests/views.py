from rest_framework import generics, viewsets
from tests.models import Test, Question, Answer, StudentAnswer, TestResult
from tests.serializers import TestSerializer, QuestionSerializer, AnswerSerializer, StudentAnswerSerializer, \
    TestResultSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StudentAnswerCreateAPIView(generics.CreateAPIView):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class TestResultListCreateAPIView(generics.ListCreateAPIView):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    def perform_create(self, serializer):
        result = serializer.save(student=self.request.user)

        test_id = result.test.pk
        count_questions = Question.objects.filter(test=test_id).count()
        count_right_answers = 0
        score = ""
        student_answers = StudentAnswer.objects.filter(student=result.student, question__test=test_id)

        for student_answer in student_answers:

            if student_answer.answer.is_correct is True:
                count_right_answers += 1

        percent = count_right_answers / count_questions * 100

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
        result.test = result.test
        result.score = score

        result.save()


class TestResultDetailAPIView(generics.RetrieveAPIView):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
