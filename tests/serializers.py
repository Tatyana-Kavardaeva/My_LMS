from rest_framework import serializers

from materials.validators import TitleValidator
from .models import Test, Question, Answer, TestResult, StudentAnswer


class TestSerializer(serializers.ModelSerializer):
    """ Serializer для модели Test. """

    questions = serializers.SerializerMethodField(read_only=True)

    def get_questions(self, instance):
        modules = Question.objects.filter(test=instance)
        return QuestionSerializer(modules, many=True).data

    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'course', 'owner', 'questions')
        read_only_fields = ('owner',)
        validators = [TitleValidator('title')]


class QuestionSerializer(serializers.ModelSerializer):
    """ Serializer для модели Question. """

    answers = serializers.SerializerMethodField(read_only=True)

    def get_answers(self, instance):
        answers = Answer.objects.filter(question=instance)
        return AnswerSerializer(answers, many=True).data

    class Meta:
        model = Question
        fields = ('id', 'text', 'test', 'answers')
        read_only_fields = ('owner',)
        validators = [TitleValidator('text')]


class AnswerSerializer(serializers.ModelSerializer):
    """ Serializer для модели Answer. """

    class Meta:
        model = Answer
        fields = ('pk', 'text', 'is_correct', 'question')
        read_only_fields = ('owner',)
        validators = [TitleValidator('text')]


class StudentAnswerSerializer(serializers.ModelSerializer):
    """ Serializer для модели StudentAnswer. """

    is_correct = serializers.SerializerMethodField(read_only=True)

    def get_is_correct(self, instance):
        return Answer.objects.get(pk=instance.answer.pk).is_correct

    class Meta:
        model = StudentAnswer
        fields = ('pk', 'student', 'question', 'answer', 'is_correct')
        read_only_fields = ('student',)


class TestResultSerializer(serializers.ModelSerializer):
    """ Serializer для модели TestResult. """

    student_answers = serializers.SerializerMethodField(read_only=True)

    def get_student_answers(self, instance):
        student_answers = StudentAnswer.objects.filter(student=instance.student)
        return StudentAnswerSerializer(student_answers, many=True).data

    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ('student', 'count_questions', 'count_right_answers', 'score', 'student_answers')
