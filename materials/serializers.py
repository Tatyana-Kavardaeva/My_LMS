from rest_framework import serializers
from materials.models import Course, Module, Lesson, Enrollment
from materials.validators import TitleValidator


class CourseSerializer(serializers.ModelSerializer):
    """ Serializer для модели Course. """

    count_modules = serializers.SerializerMethodField(read_only=True)
    modules = serializers.SerializerMethodField(read_only=True)
    is_enrolled = serializers.SerializerMethodField(read_only=True)

    def get_count_modules(self, instance):
        """ Получаем количество модулей в курсе. """
        return Module.objects.filter(course=instance).count()

    def get_modules(self, instance):
        """ Получаем список модулей курса. """
        modules = Module.objects.filter(course=instance)
        return ModuleSerializer(modules, many=True).data

    def get_is_enrolled(self, instance):
        """ Получаем статус зачисления на курс. """
        user = self.context['request'].user
        return Enrollment.objects.filter(student=user, course=instance).exists()

    class Meta:
        model = Course
        fields = ('id', 'title', 'owner', 'description', 'count_modules', 'modules', 'is_enrolled')
        read_only_fields = ('owner',)
        validators = [
            TitleValidator('title'),
            serializers.UniqueTogetherValidator(fields=["title"], queryset=Course.objects.all())
        ]


class ModuleSerializer(serializers.ModelSerializer):
    """ Serializer для модели Module. """

    count_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = serializers.SerializerMethodField(read_only=True)

    def get_count_lessons(self, instance):
        """ Получаем количество уроков. """
        return Lesson.objects.filter(module=instance).count()

    def get_lessons(self, instance):
        """ Получаем список уроков. """
        modules = Lesson.objects.filter(module=instance)
        return LessonSerializer(modules, many=True).data

    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ('owner',)
        validators = [TitleValidator('title')]


class LessonSerializer(serializers.ModelSerializer):
    """ Serializer для модели Lesson. """

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)
        validators = [TitleValidator('title')]


class EnrollmentSerializer(serializers.ModelSerializer):
    """ Serializer для модели Enrollment. """

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('student',)
