from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    FestivalViewSet, FestivalMediaViewSet, FestivalFactViewSet,
    FestivalAttendanceViewSet, FestivalFeedbackViewSet
)

router = DefaultRouter()
router.register('festivals', FestivalViewSet, basename='festival')
router.register('festival-media', FestivalMediaViewSet, basename='festivalmedia')
router.register('festival-facts', FestivalFactViewSet, basename='festivalfact')
router.register('attendances', FestivalAttendanceViewSet, basename='festivalattendance')
router.register('feedbacks', FestivalFeedbackViewSet, basename='festivalfeedback')

urlpatterns = [
    path('', include(router.urls)),
    path('attendances/<int:pk>/feedback/', 
         FestivalAttendanceViewSet.as_view({'post': 'feedback'}), 
         name='festivalattendance-feedback'),
    path('attendances/<int:pk>/update-status/', 
         FestivalAttendanceViewSet.as_view({'patch': 'update_status'}), 
         name='festivalattendance-update-status'),
]