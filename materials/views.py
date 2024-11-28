from rest_framework import viewsets
from materials.models import Course, Module, Lesson
from materials.serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from users.permissions import IsAdmin, IsOwner, IsStudent, IsTeacher


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

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


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

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
