from rest_framework import serializers

from materials.validators import TitleValidator
from .models import Test, Question, Answer, TestResult, StudentAnswer


class TestSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField(read_only=True)

    def get_questions(self, instance):
        modules = Question.objects.filter(test=instance)
        return QuestionSerializer(modules, many=True).data

    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'course', 'completed_at', 'owner', 'questions')
        read_only_fields = ('owner',)
        validators = [TitleValidator('title')]


class QuestionSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Answer
        fields = ('pk', 'text', 'is_correct', 'question')
        read_only_fields = ('owner',)
        validators = [TitleValidator('text')]


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ('pk', 'student', 'question', 'answer')
        read_only_fields = ('student',)


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ('student', 'count_questions', 'count_right_answers', 'score')
