from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomSessionViewSet,
    SessionMaterialViewSet,
    SessionFeedbackViewSet,
    InAppNotificationViewSet,
)

router = DefaultRouter()
router.register(r'sessions', CustomSessionViewSet, basename='customsession')
router.register(r'materials', SessionMaterialViewSet, basename='sessionmaterial')
router.register(r'feedbacks', SessionFeedbackViewSet, basename='sessionfeedback')
router.register(r'notifications', InAppNotificationViewSet, basename='inappnotification')

urlpatterns = [
    path('', include(router.urls)),
]