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
    AdminDashboardView,
    TutorDashboardView,
    LearnerDashboardView,
    VisitorDashboardView,
    GuideDashboardView,  
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
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('tutor/', TutorDashboardView.as_view(), name='tutor_dashboard'),
    path('guide/', GuideDashboardView.as_view(), name='guide_dashboard'),
    path('learner/', LearnerDashboardView.as_view(), name='learner_dashboard'),
    path('visitor/', VisitorDashboardView.as_view(), name='visitor_dashboard'),
]
