from rest_framework import viewsets
from materials.models import Course, Module, Lesson
from materials.serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from users.permissions import IsAdmin, IsOwner, IsStudent, IsTeacher


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'student']:
            return Course.objects.all()  # Администраторы видят все курсы
        return Course.objects.filter(owner=user)  # Преподаватели видят только свои курсы

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdmin | IsStudent | IsTeacher]
        return super().get_permissions()


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'student']:
            return Module.objects.all()  # Администраторы видят все курсы
        return Module.objects.filter(owner=user)  # Преподаватели видят только свои курсы

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdmin | IsStudent | IsTeacher]
        return super().get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'student']:
            return Lesson.objects.all()  # Администраторы видят все курсы
        return Lesson.objects.filter(owner=user)  # Преподаватели видят только свои курсы

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdmin | IsTeacher]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAdmin | IsStudent | IsTeacher]
        return super().get_permissions()