from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Avg, Q
from django.contrib.auth import get_user_model

from .models import (
    UserActivityLog, DailySiteStatistics, TourBookingStatistic, TutorBookingStatistic,
    GuideBookingStatistic, FeedbackSummary, SystemNotification, DashboardStat, DashboardWidget
)
from .serializers import (
    UserActivityLogSerializer, DailySiteStatisticsSerializer, TourBookingStatisticSerializer, TutorBookingStatisticSerializer,
    GuideBookingStatisticSerializer, FeedbackSummarySerializer, SystemNotificationSerializer, DashboardStatSerializer, DashboardWidgetSerializer
)

User = get_user_model()

class IsAdminOrReadSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False

class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserActivityLogSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['timestamp', 'action']
    search_fields = ['action', 'description', 'user__email']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return UserActivityLog.objects.select_related("user").all()
        return UserActivityLog.objects.filter(user=user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_recent(self, request):
        logs = self.get_queryset().order_by('-timestamp')[:10]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

class DailySiteStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailySiteStatistics.objects.all()
    serializer_class = DailySiteStatisticsSerializer
    permission_classes = [permissions.IsAdminUser]

class TourBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourBookingStatistic.objects.all()
    serializer_class = TourBookingStatisticSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date', 'location', 'tour_type']
    search_fields = ['location', 'tour_type']
    permission_classes = [permissions.IsAdminUser]

class TutorBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TutorBookingStatistic.objects.select_related("tutor").all()
    serializer_class = TutorBookingStatisticSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date', 'subject']
    search_fields = ['tutor__email', 'subject']
    permission_classes = [permissions.IsAdminUser]

class GuideBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuideBookingStatistic.objects.select_related("guide").all()
    serializer_class = GuideBookingStatisticSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date', 'region']
    search_fields = ['guide__email', 'region']
    permission_classes = [permissions.IsAdminUser]

class FeedbackSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeedbackSummary.objects.all()
    serializer_class = FeedbackSummarySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'average_rating']
    permission_classes = [permissions.IsAdminUser]

class SystemNotificationViewSet(viewsets.ModelViewSet):
    queryset = SystemNotification.objects.prefetch_related("recipients").all()
    serializer_class = SystemNotificationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'notification_type']
    search_fields = ['title', 'message']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return SystemNotification.objects.all()
        return SystemNotification.objects.filter(recipients=user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return Response({'status': 'marked as read'})

class DashboardStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DashboardStat.objects.all()
    serializer_class = DashboardStatSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'], url_path='summary', permission_classes=[permissions.IsAdminUser])
    def summary(self, request):
        data = {
            "total_users": User.objects.count(),
            "total_bookings": DailySiteStatistics.objects.aggregate(total=Sum("total_bookings"))["total"] or 0,
            "total_reviews": DailySiteStatistics.objects.aggregate(total=Sum("total_reviews"))["total"] or 0,
            "avg_feedback_rating": FeedbackSummary.objects.aggregate(avg=Avg("average_rating"))["avg"] or 0,
            "active_today": DailySiteStatistics.objects.order_by('-date').first().active_users if DailySiteStatistics.objects.exists() else 0,
        }
        return Response(data)

class DashboardWidgetViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardWidgetSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return DashboardWidget.objects.all()
        return DashboardWidget.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_widgets(self, request):
        widgets = DashboardWidget.objects.filter(user=request.user)
        serializer = self.get_serializer(widgets, many=True)
        return Response(serializer.data)