from rest_framework import serializers
from .models import Test, Question, Answer, TestResult


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'is_correct')
        read_only_fields = ('owner',)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'question_type', 'answers')
        read_only_fields = ('owner',)


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'created_at', 'owner', 'questions')
        read_only_fields = ('owner',)

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ('student', 'count_questions', 'count_right_answers', 'score')