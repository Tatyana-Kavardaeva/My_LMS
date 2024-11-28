from rest_framework import generics, viewsets
from tests.models import Test, Question, Answer, StudentAnswer, TestResult
from tests.serializers import TestSerializer, QuestionSerializer, AnswerSerializer, StudentAnswerSerializer, \
    TestResultSerializer
from users.permissions import IsAdmin, IsTeacher, IsOwner, IsStudent


class CustomModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin | IsOwner]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdmin | IsStudent | IsOwner]
        return super().get_permissions()


class TestViewSet(CustomModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionViewSet(CustomModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(CustomModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class StudentAnswerCreateAPIView(generics.CreateAPIView):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class TestResultListCreateAPIView(generics.ListCreateAPIView):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsStudent]
        elif self.request.method == 'GET':
            if self.request.user.groups.filter(name='Student').exists():
                self.permission_classes = [IsStudent]
            elif self.request.user.groups.filter(name='IsAdmin').exists():
                self.permission_classes = [IsAdmin]
            elif self.request.user.groups.filter(name='Teacher').exists():
                self.permission_classes = [IsTeacher]

        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.groups.filter(name='Admin').exists():
            return TestResult.objects.all()
        elif self.request.user.groups.filter(name='Student').exists():
            return TestResult.objects.filter(student=self.request.user)
        elif self.request.user.groups.filter(name='Teacher').exists():
            return TestResult.objects.filter(test__owner=self.request.user)
        return TestResult.objects.none()

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
    permission_classes = [IsStudent | IsAdmin]
