from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from materials.pagination import MyPagination
from tests.models import Test, Question, Answer, StudentAnswer, TestResult
from tests.serializers import TestSerializer, QuestionSerializer, AnswerSerializer, StudentAnswerSerializer, \
    TestResultSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent
from tests.servicees import calculate_score


class CustomModelViewSet(viewsets.ModelViewSet):
    """
        Кастомный ViewSet для управления ресурсами с учетом роли пользователя.

        При создании ресурса автоматически присваивается текущий пользователь как его владелец.
        Разрешения для различных действий зависят от роли пользователя:
        - Для создания, обновления и удаления требуется роль администратора или учителя.
        - Для просмотра списка и отдельного объекта — роль администратора, студента или учителя.
    """

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if not self.request.user.role:
            raise PermissionDenied("У вас нет доступа к этому ресурсу.")

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdmin | IsStudent | IsTeacher]
        return super().get_permissions()


class TestViewSet(CustomModelViewSet):
    """ ViewSet для модели Test. """

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    pagination_class = MyPagination


class QuestionViewSet(CustomModelViewSet):
    """ ViewSet для модели Question. """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(CustomModelViewSet):
    """ ViewSet для модели Answer. """

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class StudentAnswerCreateAPIView(generics.CreateAPIView):
    """ API для создания ответов студентов на вопросы. """

    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class TestResultListCreateAPIView(generics.ListCreateAPIView):
    """ API для получения списка результатов тестов и их создания. """

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
        """ Определяет доступ к получению queryset в зависимости от роли пользователя. """
        if self.request.user.role == "admin":
            return TestResult.objects.all()
        elif self.request.user.role == "student":
            return TestResult.objects.filter(student=self.request.user)
        elif self.request.user.role == "teacher":
            return TestResult.objects.filter(test__owner=self.request.user)
        return TestResult.objects.none()

    def perform_create(self, serializer):
        """ При создании результата теста вычисляется оценка. """
        result = serializer.save(student=self.request.user)
        calculate_score(result)


class TestResultDetailAPIView(generics.RetrieveAPIView):
    """API для получения подробной информации о результатах тестов."""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    def get_permissions(self):
        """ Определяет разрешения для GET-запроса в зависимости от роли пользователя. """

        if self.request.method == 'GET':
            if self.request.user.role == "student":
                self.permission_classes = [IsStudent]
            elif self.request.user.role == "admin":
                self.permission_classes = [IsAdmin]
            elif self.request.user.role == "teacher":
                self.permission_classes = [IsTeacher]
            else:
                raise PermissionDenied("У вас нет прав для доступа к этому ресурсу.")

        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        """ Получает результат теста и проверяет доступ к нему. """
        result = self.get_object()

        # Проверка доступа для студента
        if self.request.user.role == "student":
            if result.student != self.request.user:
                raise PermissionDenied("У вас нет доступа к этому результату.")

        # Проверка доступа для преподавателя (он может смотреть только результаты тестов, которые он создал)
        elif self.request.user.role == "teacher":
            if result.test.owner != self.request.user:
                raise PermissionDenied("У вас нет доступа к этому результату.")

        # Администратор может просматривать все результаты
        elif self.request.user.groups.filter(name='Admin').exists():
            pass

        # Если роль не соответствует ни одной из вышеуказанных, доступ запрещен
        else:
            raise PermissionDenied("У вас нет прав для просмотра этого результата.")

        # Если проверки пройдены успешно, сериализуем данные и возвращаем ответ
        serializer = self.get_serializer(result)
        return Response(serializer.data)
