from rest_framework.serializers import ModelSerializer

from materials.models import Course, Module, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
