

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorialViewSet, TutorialStepViewSet

router = DefaultRouter()
router.register(r'tutorials', TutorialViewSet, basename='tutorial')
router.register(r'tutorial-steps', TutorialStepViewSet, basename='tutorial-step')

urlpatterns = [
    path('', include(router.urls)),
]
