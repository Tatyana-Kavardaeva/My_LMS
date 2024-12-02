from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied

from materials.pagination import MyPagination
from tests.models import Test, Question, Answer, StudentAnswer, TestResult
from tests.serializers import TestSerializer, QuestionSerializer, AnswerSerializer, StudentAnswerSerializer, \
    TestResultSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent
from tests.servicees import calculate_score


class CustomModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if not self.request.user.role:
            raise PermissionDenied("У вас нет доступа к этому ресурсу.")

        if self.action == 'create':
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdmin | IsStudent | IsTeacher]
        return super().get_permissions()


class TestViewSet(CustomModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    pagination_class = MyPagination


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
        if not self.request.user.role:
            raise PermissionDenied("У вас нет доступа к этому ресурсу.")

        if self.request.method == 'POST':
            self.permission_classes = [IsStudent]
        elif self.request.method == 'GET':
            if self.request.user.role == "student":
                self.permission_classes = [IsStudent]
            elif self.request.user.role == "admin":
                self.permission_classes = [IsAdmin]
            elif self.request.user.role == "teacher":
                self.permission_classes = [IsTeacher]

        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.role == "admin":
            return TestResult.objects.all()
        elif self.request.user.role == "student":
            return TestResult.objects.filter(student=self.request.user)
        elif self.request.user.role == "teacher":
            return TestResult.objects.filter(test__owner=self.request.user)
        return TestResult.objects.none()

    def perform_create(self, serializer):
        result = serializer.save(student=self.request.user)
        calculate_score(result)


class TestResultDetailAPIView(generics.RetrieveAPIView):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    def get_permissions(self):
        if not self.request.user.role:
            raise PermissionDenied("У вас нет доступа к этому ресурсу.")

        if self.request.method == 'GET' and self.request.user.role == "student":
            self.permission_classes = [IsStudent]
        elif self.request.method == 'GET' and self.request.user.groups.filter(name='IsAdmin').exists():
            self.permission_classes = [IsAdmin]
        elif self.request.method == 'GET' and self.request.user.groups.filter(name='Teacher').exists():
            self.permission_classes = [IsTeacher]

        return super().get_permissions()

    # def get(self, request, *args, **kwargs):
    #     if self.request.user.groups.filter(name='Admin').exists():
    #         return TestResult.objects.all()
    #     elif self.request.user.groups.filter(name='Student').exists():
    #         return TestResult.objects.filter(student=self.request.user)
    #     elif self.request.user.groups.filter(name='Teacher').exists():
    #         return TestResult.objects.filter(test__owner=self.request.user)
    #     return TestResult.objects.none()
