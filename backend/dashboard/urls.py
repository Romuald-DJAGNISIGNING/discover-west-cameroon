from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserActivityLogViewSet,
    DailySiteStatisticsViewSet,
    TourBookingStatisticViewSet,
    TutorBookingStatisticViewSet,
    GuideBookingStatisticViewSet,
    FeedbackSummaryViewSet,
    SystemNotificationViewSet,
)

router = DefaultRouter()
router.register(r'user-activities', UserActivityLogViewSet, basename='user-activity')
router.register(r'daily-stats', DailySiteStatisticsViewSet, basename='daily-stats')
router.register(r'tour-bookings', TourBookingStatisticViewSet, basename='tour-bookings')
router.register(r'tutor-bookings', TutorBookingStatisticViewSet, basename='tutor-bookings')
router.register(r'guide-bookings', GuideBookingStatisticViewSet, basename='guide-bookings')
router.register(r'feedback-summary', FeedbackSummaryViewSet, basename='feedback-summary')
router.register(r'system-notifications', SystemNotificationViewSet, basename='system-notifications')

urlpatterns = [
    path('', include(router.urls)),
]
