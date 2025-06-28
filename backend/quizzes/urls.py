from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import QuizViewSet, QuestionViewSet, ChoiceViewSet, QuizAttemptViewSet, QuestionResponseViewSet

router = DefaultRouter()
router.register('quizzes', QuizViewSet, basename='quiz')
router.register('questions', QuestionViewSet, basename='question')
router.register('choices', ChoiceViewSet, basename='choice')
router.register('attempts', QuizAttemptViewSet, basename='quizattempt')
router.register('responses', QuestionResponseViewSet, basename='questionresponse')

urlpatterns = [
    path('', include(router.urls)),
]