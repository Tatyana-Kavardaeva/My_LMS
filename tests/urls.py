from django.urls import path
from rest_framework.routers import SimpleRouter

from tests.apps import TestsConfig
from tests.views import (TestViewSet, QuestionViewSet, AnswerViewSet,
                         StudentAnswerCreateAPIView, TestResultListCreateAPIView, TestResultDetailAPIView, )

app_name = TestsConfig.name

router = SimpleRouter()
router.register('tests', TestViewSet)
router.register('questions', QuestionViewSet)
router.register('answers', AnswerViewSet)

urlpatterns = [
    path('student-answer/', StudentAnswerCreateAPIView.as_view(), name='student-answer-create'),
    path('results/', TestResultListCreateAPIView.as_view(), name='results'),
    path('results/<int:pk>/', TestResultDetailAPIView.as_view(), name='results-detail'),
    ] + router.urls