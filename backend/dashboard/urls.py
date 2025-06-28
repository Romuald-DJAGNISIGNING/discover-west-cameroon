from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    UserActivityLogViewSet, DailySiteStatisticsViewSet, TourBookingStatisticViewSet,
    TutorBookingStatisticViewSet, GuideBookingStatisticViewSet, FeedbackSummaryViewSet,
    SystemNotificationViewSet, DashboardStatViewSet, DashboardWidgetViewSet
)

router = DefaultRouter()
router.register(r'activity-logs', UserActivityLogViewSet, basename="activitylog")
router.register(r'daily-stats', DailySiteStatisticsViewSet, basename="dailysitestats")
router.register(r'tour-booking-stats', TourBookingStatisticViewSet, basename="tourbookingstat")
router.register(r'tutor-booking-stats', TutorBookingStatisticViewSet, basename="tutorbookingstat")
router.register(r'guide-booking-stats', GuideBookingStatisticViewSet, basename="guidebookingstat")
router.register(r'feedback-summaries', FeedbackSummaryViewSet, basename="feedbacksummary")
router.register(r'system-notifications', SystemNotificationViewSet, basename="systemnotification")
router.register(r'dashboard-stats', DashboardStatViewSet, basename="dashboardstat")
router.register(r'widgets', DashboardWidgetViewSet, basename="dashboardwidget")

urlpatterns = [
    path('', include(router.urls)),
    path('role/', include('dashboard.urls_role_dashboards')),
    path('public/', include('dashboard.urls_public')),
]