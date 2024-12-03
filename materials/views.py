# from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
# from rest_framework.views import APIView
from materials.tasks import send_information_about_enrolling
from materials.models import Course, Module, Lesson, Enrollment
from materials.pagination import MyPagination
from materials.serializers import CourseSerializer, ModuleSerializer, LessonSerializer, EnrollmentSerializer
from tests.views import CustomModelViewSet
from users.permissions import IsStudent, IsAdmin, IsTeacher


class CourseViewSet(CustomModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'student']:
            return Course.objects.all()
        return Course.objects.filter(owner=user)


class ModuleViewSet(CustomModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'student']:
            return Module.objects.all()
        return Module.objects.filter(owner=user)


class LessonViewSet(CustomModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'student']:
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class EnrollmentAPIView(GenericAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        enroll_item = Enrollment.objects.filter(student=user, course=course_item)

        if enroll_item.exists():
            enroll_item.delete()
            message = 'Вы отчислились с курса'
        else:
            Enrollment.objects.create(student=user, course=course_item)
            send_information_about_enrolling.delay(course_item.title, user.first_name, user.email,
                                                   course_item.owner.email)
            message = 'Вы зачислены на курс'
            print(course_item.owner.email)
            print(user.email)

        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'admin':
            queryset = Enrollment.objects.all()
        elif user.role == 'student':
            queryset = Enrollment.objects.filter(student=user)
        elif user.role == 'teacher':
            queryset = Enrollment.objects.filter(course__owner=user)
        else:
            return Response({"detail": "У вас нет доступа к этому ресурсу."}, status=403)

        # Сериализуем queryset перед отправкой ответа
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        # Проверяем, есть ли у пользователя роль
        if not self.request.user.role:
            raise PermissionDenied("У вас нет доступа к этому ресурсу.")

        if self.request.method == 'POST':
            # Для POST разрешаем доступ только студентам
            self.permission_classes = [IsStudent]
        elif self.request.method == 'GET':
            # Для GET разрешаем доступ admin, student, teacher
            self.permission_classes = [IsAdmin | IsStudent | IsTeacher]

        return super().get_permissions()
