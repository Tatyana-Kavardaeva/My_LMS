from rest_framework import serializers
from materials.models import Course, Module, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_modules = serializers.SerializerMethodField(read_only=True)
    modules = serializers.SerializerMethodField(read_only=True)

    def get_count_modules(self, instance):
        return Module.objects.filter(course=instance).count()

    def get_modules(self, instance):
        modules = Module.objects.filter(course=instance)
        return ModuleSerializer(modules, many=True).data

    class Meta:
        model = Course
        fields = ('id', 'title', 'owner', 'count_modules', 'modules')
        read_only_fields = ('owner',)


class ModuleSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField(read_only=True)
    # lessons = serializers.SerializerMethodField(read_only=True)

    def get_count_lessons(self, instance):
        return Lesson.objects.filter(module=instance).count()

    # def get_lessons(self, instance):
    #     modules = Lesson.objects.filter(module=instance)
    #     return LessonSerializer(modules, many=True).data

    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ('owner',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)
