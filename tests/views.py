from django.core.serializers import serialize
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Test, Question, Answer
from .serializers import TestSerializer, QuestionSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return Question.objects.filter(test_id=test_id)


class QuestionAnswerView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        answers_data = request.data
        correct_answers_count = 0
        for answer_data in answers_data:
            question_id = answer_data.get("question_id")
            answer_ids = answer_data.get("answer_ids")

            correct_answers = Answer.objects.filter(
                id__in=answer_ids,
                question_id=question_id,
                is_correct=True
            )

            # Если количество правильных ответов совпадает с выбранными, засчитываем.
            if correct_answers.count() == len(answer_ids):
                correct_answers_count += 1

        return Response({
            'message': f'Вы ответили правильно на {correct_answers_count} из {len(answers_data)} вопросов.'
        })