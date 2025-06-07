from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import (
    UserActivityLog,
    DailySiteStatistics,
    TourBookingStatistic,
    TutorBookingStatistic,
    GuideBookingStatistic,
    FeedbackSummary,
    SystemNotification
)
from .serializers import (
    UserActivityLogSerializer,
    DailySiteStatisticsSerializer,
    TourBookingStatisticSerializer,
    TutorBookingStatisticSerializer,
    GuideBookingStatisticSerializer,
    FeedbackSummarySerializer,
    SystemNotificationSerializer
)

User = get_user_model()


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit,
    others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve user activity logs.
    Filterable by user and action type.
    """
    queryset = UserActivityLog.objects.select_related('user').all().order_by('-timestamp')
    serializer_class = UserActivityLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user__id', 'action']
    search_fields = ['description']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class DailySiteStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View aggregated daily site statistics.
    Filter by date range.
    """
    queryset = DailySiteStatistics.objects.all().order_by('-date')
    serializer_class = DailySiteStatisticsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'date': ['gte', 'lte'],
    }
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class TourBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Stats about tour bookings, filter by date, tour_type, location.
    """
    queryset = TourBookingStatistic.objects.all().order_by('-date')
    serializer_class = TourBookingStatisticSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'tour_type', 'location']
    search_fields = ['location']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class TutorBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Tutor booking stats, filterable by tutor and subject.
    """
    queryset = TutorBookingStatistic.objects.select_related('tutor').all().order_by('-date')
    serializer_class = TutorBookingStatisticSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'subject', 'tutor__id']
    search_fields = ['subject']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class GuideBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Guide booking stats, filterable by guide and region.
    """
    queryset = GuideBookingStatistic.objects.select_related('guide').all().order_by('-date')
    serializer_class = GuideBookingStatisticSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'region', 'guide__id']
    search_fields = ['region']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class FeedbackSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Feedback summary stats.
    """
    queryset = FeedbackSummary.objects.all().order_by('-date')
    serializer_class = FeedbackSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'date': ['gte', 'lte'],
    }
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class SystemNotificationViewSet(viewsets.ModelViewSet):
    """
    CRUD for system notifications.
    Only admins can create/update/delete,
    others can only read.
    """
    queryset = SystemNotification.objects.prefetch_related('recipients').all().order_by('-created_at')
    serializer_class = SystemNotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        # For normal users, show notifications where they are recipients
        return self.queryset.filter(recipients=user)
