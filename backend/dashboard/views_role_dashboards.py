from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.db.models import Sum, Avg
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Import all app models for integration
from assignments.models import Assignment
from custom_sessions.models import CustomSession
from festivals.models import Festival
from notifications.models import Notification
from payments.models import PaymentTransaction, Booking, Payout
from quizzes.models import QuizAttempt
from reports.models import Report
from reviews.models import Review
from support.models import SupportTicket
from tourism.models import TouristicAttraction
from tutorials.models import Tutorial
from users.models import CustomUser as AppUser
from villages.models import Village

from .models import (
    UserActivityLog, DailySiteStatistics, TourBookingStatistic, TutorBookingStatistic,
    GuideBookingStatistic, FeedbackSummary, SystemNotification, DashboardWidget
)

User = get_user_model()

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {
            "recent_users": list(AppUser.objects.order_by('-date_joined').values('email', 'date_joined')[:5]),
            "recent_notifications": list(SystemNotification.objects.order_by('-created_at').values('title', 'created_at')[:5]),
            "stats": {
                "total_users": AppUser.objects.count(),
                "active_today": DailySiteStatistics.objects.order_by('-date').first().active_users if DailySiteStatistics.objects.exists() else 0,
                "total_bookings": DailySiteStatistics.objects.aggregate(total=Sum("total_bookings"))["total"] or 0,
                "total_reviews": DailySiteStatistics.objects.aggregate(total=Sum("total_reviews"))["total"] or 0,
                "average_feedback": FeedbackSummary.objects.aggregate(avg=Avg("average_rating"))["avg"] or 0,
                "total_payments": PaymentTransaction.objects.filter(status="success").aggregate(total=Sum("amount"))["total"] or 0,
                "pending_reports": Report.objects.filter(status="pending").count(),
                "pending_support_tickets": SupportTicket.objects.filter(status__in=["open", "in_progress"]).count(),
                "assignments_due": Assignment.objects.filter(status="pending").count(),
                "custom_sessions_today": CustomSession.objects.filter(date=DailySiteStatistics.objects.order_by('-date').first().date).count() if DailySiteStatistics.objects.exists() else 0,
            },
            "widgets": [
                {"type": "map", "config": {"show": "all_villages"}},
                {"type": "leaderboard", "config": {"top": "guides"}},
                {"type": "weather", "config": {"region": "West Cameroon"}},
                {"type": "payments", "config": {}},
                {"type": "assignments", "config": {"status": "pending"}},
                {"type": "support", "config": {"status": "open"}},
                {"type": "reports", "config": {"status": "pending"}},
            ],
        }
        return Response(data, status=status.HTTP_200_OK)

class VisitorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "recent_activity": list(UserActivityLog.objects.filter(user=request.user).order_by('-timestamp').values("action", "description", "timestamp")[:5]),
            "recommended_tours": list(TouristicAttraction.objects.order_by('-id').values("name", "description", "village__name")[:3]),
            "popular_villages": list(Village.objects.order_by('-population').values("name", "description", "population")[:3]),
            "upcoming_festivals": list(Festival.objects.order_by('start_date').values("name", "start_date", "location")[:3]),
            "recent_reviews": list(Review.objects.order_by('-created_at').values("title", "rating", "content")[:3]),
            "assignments": list(Assignment.objects.filter(user=request.user).order_by('-due_date').values("title", "due_date", "status")[:3]),
            "custom_sessions": list(CustomSession.objects.filter(users=request.user).order_by('-date').values("title", "date", "status")[:3]),
            "notifications": list(Notification.objects.filter(user=request.user, is_read=False).values("message", "created_at")[:3]),
            "widgets": [
                {"type": "featured", "config": {"model": "Festival"}},
                {"type": "calendar", "config": {}},
                {"type": "phrase", "config": {"lang": "Fe'fe'"}},
                {"type": "weather", "config": {"region": "West Cameroon"}},
                {"type": "quizzes", "config": {}},
            ],
        }
        return Response(data, status=status.HTTP_200_OK)

class LearnerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "enrolled_tutorials": list(Tutorial.objects.filter(is_published=True).values("title", "category__name", "created_at")[:5]),
            "quiz_results": list(QuizAttempt.objects.filter(user=request.user).order_by('-date_taken').values("quiz__title", "score", "date_taken")[:5]),
            "recent_payments": list(PaymentTransaction.objects.filter(user=request.user).order_by('-created').values("amount", "currency", "status", "created")[:3]),
            "upcoming_bookings": list(Booking.objects.filter(learner_or_visitor=request.user).order_by('-created_at').values("booking_type", "created_at")[:3]),
            "assignments": list(Assignment.objects.filter(user=request.user).order_by('-due_date').values("title", "due_date", "status")[:3]),
            "custom_sessions": list(CustomSession.objects.filter(users=request.user).order_by('-date').values("title", "date", "status")[:3]),
            "widgets": [
                {"type": "gallery", "config": {"filter": "recent"}},
                {"type": "stat", "config": {"type": "payment"}},
                {"type": "quizzes", "config": {}},
                {"type": "assignments", "config": {"user": request.user.id}},
            ],
        }
        return Response(data, status=status.HTTP_200_OK)

class TutorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "is_tutor") or not getattr(request.user, "is_tutor", False):
            return Response({"detail": _("Not authorized as a tutor.")}, status=status.HTTP_403_FORBIDDEN)
        data = {
            "my_bookings": list(Booking.objects.filter(tutor=request.user).order_by('-created_at').values("learner_or_visitor__email", "booking_type", "created_at")[:5]),
            "earnings": Payout.objects.filter(guide_or_tutor=request.user, status="paid").aggregate(total=Sum("amount"))["total"] or 0,
            "pending_payouts": Payout.objects.filter(guide_or_tutor=request.user, status="pending").count(),
            "my_reviews": list(Review.objects.filter(user=request.user).order_by('-created_at').values("title", "rating", "content")[:3]),
            "assignments": list(Assignment.objects.filter(user=request.user).order_by('-due_date').values("title", "due_date", "status")[:3]),
            "custom_sessions": list(CustomSession.objects.filter(users=request.user).order_by('-date').values("title", "date", "status")[:3]),
            "widgets": [
                {"type": "stat", "config": {"type": "earnings"}},
                {"type": "leaderboard", "config": {"top": "tutors"}},
                {"type": "assignments", "config": {"user": request.user.id}},
                {"type": "support", "config": {"user": request.user.id}},
            ],
        }
        return Response(data, status=status.HTTP_200_OK)

class GuideDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "is_guide") or not getattr(request.user, "is_guide", False):
            return Response({"detail": _("Not authorized as a guide.")}, status=status.HTTP_403_FORBIDDEN)
        bookings = Booking.objects.filter(guide=request.user).order_by('-created_at')[:5]
        data = {
            "recent_bookings": list(bookings.values("learner_or_visitor__email", "booking_type", "created_at")),
            "earnings": Payout.objects.filter(guide_or_tutor=request.user, status="paid").aggregate(total=Sum("amount"))["total"] or 0,
            "pending_payouts": Payout.objects.filter(guide_or_tutor=request.user, status="pending").count(),
            "my_reviews": list(Review.objects.filter(user=request.user).order_by('-created_at').values("title", "rating", "content")[:3]),
            "assignments": list(Assignment.objects.filter(user=request.user).order_by('-due_date').values("title", "due_date", "status")[:3]),
            "custom_sessions": list(CustomSession.objects.filter(users=request.user).order_by('-date').values("title", "date", "status")[:3]),
            "widgets": [
                {"type": "calendar", "config": {"type": "my_bookings"}},
                {"type": "stat", "config": {"type": "earnings"}},
                {"type": "support", "config": {"user": request.user.id}},
            ],
        }
        return Response(data, status=status.HTTP_200_OK)