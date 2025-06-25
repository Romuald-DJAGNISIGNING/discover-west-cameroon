from rest_framework import viewsets, filters, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from payments.models import Booking, Payment
from payments.serializers import BookingSerializer, PaymentSerializer
from users.serializers import *
from assignments.serializers import AssignmentSerializer
from tourism.serializers import TourPlanSerializer
from support.serializers import SupportTicketSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from reviews.serializers import ReviewSerializer

from .models import (
    UserActivityLog, DailySiteStatistics, TourBookingStatistic,
    TutorBookingStatistic, GuideBookingStatistic,
    FeedbackSummary, SystemNotification
)
from .serializers import (
    UserActivityLogSerializer, DailySiteStatisticsSerializer,
    TourBookingStatisticSerializer, TutorBookingStatisticSerializer,
    GuideBookingStatisticSerializer, FeedbackSummarySerializer,
    SystemNotificationSerializer
)

User = get_user_model()


# ---------------- Admin Dashboard ----------------
class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        all_bookings = Booking.objects.all()
        total_income = sum(b.amount_paid for b in all_bookings if b.status == "paid")

        return Response({
            "total_users": User.objects.count(),
            "total_bookings": all_bookings.count(),
            "total_income": total_income,
            "bookings": BookingSerializer(all_bookings, many=True).data,
            "payments": PaymentSerializer(Payment.objects.all(), many=True).data,
            "reports": ReportSerializer(Report.objects.all(), many=True).data,
            "notifications": NotificationSerializer(notifications, many=True).data
        })


# ---------------- Tutor Dashboard ----------------
class TutorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'tutor_profile'):
            return Response({'error': 'Not a tutor'}, status=403)

        tutor = request.user.tutor_profile
        notifications = Notification.objects.filter(user=request.user, is_read=False)

        return Response({
            "profile": TutorProfileSerializer(tutor).data,
            "bookings": BookingSerializer(tutor.bookings.all(), many=True).data,
            "payments": PaymentSerializer(tutor.tutor_payments.all(), many=True).data,
            "reviews": ReviewSerializer(tutor.reviews.all(), many=True).data,
            "notifications": NotificationSerializer(notifications, many=True).data
        })


# ---------------- Guide Dashboard ----------------
class GuideDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'guide_profile'):
            return Response({'error': 'Not a guide'}, status=403)

        guide = request.user.guide_profile
        notifications = Notification.objects.filter(user=request.user, is_read=False)

        return Response({
            "profile": GuideProfileSerializer(guide).data,
            "tours": TourSerializer(guide.tours.all(), many=True).data,
            "payments": PaymentSerializer(guide.guide_payments.all(), many=True).data,
            "reviews": ReviewSerializer(guide.reviews.all(), many=True).data,
            "notifications": NotificationSerializer(notifications, many=True).data
        })


# ---------------- Learner Dashboard ----------------
class LearnerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'learner_profile'):
            return Response({'error': 'Not a learner'}, status=403)

        learner = request.user.learner_profile
        notifications = Notification.objects.filter(user=request.user, is_read=False)

        return Response({
            "profile": LearnerProfileSerializer(learner).data,
            "assignments": AssignmentSerializer(learner.learner_assignments.all(), many=True).data,
            "payments": PaymentSerializer(learner.payments.all(), many=True).data,
            "bookings": BookingSerializer(learner.bookings.all(), many=True).data,
            "notifications": NotificationSerializer(notifications, many=True).data
        })


# ---------------- Visitor Dashboard ----------------
class VisitorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'visitor_profile'):
            return Response({'error': 'Not a visitor'}, status=403)

        visitor = request.user.visitor_profile
        notifications = Notification.objects.filter(user=request.user, is_read=False)

        return Response({
            "profile": VisitorProfileSerializer(visitor).data,
            "tour_bookings": BookingSerializer(visitor.tour_bookings.all(), many=True).data,
            "payments": PaymentSerializer(visitor.payments.all(), many=True).data,
            "reviews": ReviewSerializer(visitor.reviews.all(), many=True).data,
            "notifications": NotificationSerializer(notifications, many=True).data
        })


# ---------------- Analytics & Admin Stats ----------------
class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserActivityLog.objects.select_related('user').all().order_by('-timestamp')
    serializer_class = UserActivityLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user__id', 'action']
    search_fields = ['description']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class DailySiteStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailySiteStatistics.objects.all().order_by('-date')
    serializer_class = DailySiteStatisticsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'date': ['gte', 'lte']}
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class TourBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourBookingStatistic.objects.all().order_by('-date')
    serializer_class = TourBookingStatisticSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'tour_type', 'location']
    search_fields = ['location']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class TutorBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TutorBookingStatistic.objects.select_related('tutor').all().order_by('-date')
    serializer_class = TutorBookingStatisticSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'subject', 'tutor__id']
    search_fields = ['subject']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class GuideBookingStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuideBookingStatistic.objects.select_related('guide').all().order_by('-date')
    serializer_class = GuideBookingStatisticSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'region', 'guide__id']
    search_fields = ['region']
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class FeedbackSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeedbackSummary.objects.all().order_by('-date')
    serializer_class = FeedbackSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'date': ['gte', 'lte']}
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]


class SystemNotificationViewSet(viewsets.ModelViewSet):
    queryset = SystemNotification.objects.prefetch_related('recipients').all().order_by('-created_at')
    serializer_class = SystemNotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return self.queryset.filter(recipients=user)
