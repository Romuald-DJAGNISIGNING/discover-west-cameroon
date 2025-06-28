from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from .models import (
    UserActivityLog, DailySiteStatistics, TourBookingStatistic, TutorBookingStatistic,
    GuideBookingStatistic, FeedbackSummary, SystemNotification, DashboardStat, DashboardWidget
)
# Import demo models from cross-apps for dashboard integration
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
from assignments.models import Assignment

User = get_user_model()

class DashboardAppTests(APITestCase):
    def setUp(self):
        # Users
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@westcameroon.com",
            phone_number="+237600000025",
            password="adminpass",
            role="admin"
        )
        self.tutor = User.objects.create_user(
            username="tutor",
            email="tutor@westcameroon.com",
            phone_number="+237600000026",
            password="tutorpass",
            role="tutor"
        )
        self.guide = User.objects.create_user(
            username="guide",
            email="guide@westcameroon.com",
            phone_number="+237600000027",
            password="guidepass",
            role="guide"
        )
        self.learner = User.objects.create_user(
            username="learner",
            email="learner@westcameroon.com",
            phone_number="+237600000028",
            password="learnerpass",
            role="learner"
        )
        self.visitor = User.objects.create_user(
            username="visitor",
            email="visitor@westcameroon.com",
            phone_number="+237600000029",
            password="visitorpass",
            role="visitor"
        )

        # Villages, Attractions, Festivals
        self.village = Village.objects.create(name="Bafoussam", department="Mifi", description="Heart of West", population=500000)
        self.attraction = TouristicAttraction.objects.create(name="Chute de la Métché", description="Waterfall", village=self.village, added_by=self.admin)
        self.festival = Festival.objects.create(
            name="Ngouon", description="Cultural festival", type="cultural", 
            start_date="2025-12-10", end_date="2025-12-15", location="Bafoussam", 
            village=self.village, main_language="Fe'fe'", is_annual=True, added_by=self.admin
        )

        # Assignments, Sessions, Tutorials, Quizzes, Reviews, Reports, Support, Payments
        self.assignment = Assignment.objects.create(
            title="History Assignment",
            description="Complete the history assignment",
            assigned_by=self.tutor,
            assigned_to=self.learner,
            due_date=timezone.now() + timedelta(days=5),
            assignment_type="tutoring",
            is_active=True
        )
        self.session = CustomSession.objects.create(
            session_type='tour_guide',
            tutor_or_guide=self.guide,
            learner_or_visitor=self.visitor,
            topic_or_location="Village Tour",
            scheduled_time=timezone.now() + timedelta(days=1),
            duration_minutes=60,
            status='confirmed'
        )
        self.tutorial = Tutorial.objects.create(
            title="Discover Bamena", category=None, description="Learn Bamena history", content="...", created_by=self.tutor, is_published=True
        )
        self.quiz_result = QuizAttempt.objects.create(user=self.learner, quiz=None, score=95, date_taken=timezone.now())
        self.review = Review.objects.create(user=self.visitor, title="Great Place", rating=5, content="Loved Ngouon!", created_at=timezone.now())
        self.report = Report.objects.create(user=self.visitor, title="Spam", description="Wrong info", created_at=timezone.now())
        self.support = SupportTicket.objects.create(subject="Need help", message="How to book?", created_by=self.visitor)
        self.booking = Booking.objects.create(learner_or_visitor=self.learner, tutor=self.tutor, booking_type="tutorial")
        self.payment = PaymentTransaction.objects.create(
            user=self.learner, method=None, amount=10000, currency="XAF", status="success", reference="REF-001", purpose="booking"
        )
        self.payout = Payout.objects.create(guide_or_tutor=self.tutor, amount=5000, related_booking=self.booking, status="paid")
        self.notification = Notification.objects.create(user=self.visitor, message="Welcome!", notification_type="info", is_read=False)
        self.daily_stats = DailySiteStatistics.objects.create(date=timezone.now().date(), new_users=1, active_users=3, total_bookings=2)
        self.feedback_summary = FeedbackSummary.objects.create(date=timezone.now().date(), average_rating=4.7, total_feedback=10, positive_feedback=9, negative_feedback=1)
        self.sys_notification = SystemNotification.objects.create(title="Platform Update", message="New features", notification_type="info")
        self.sys_notification.recipients.add(self.visitor)
        self.stat = DashboardStat.objects.create(stat_name="Users", value=5)
        self.widget = DashboardWidget.objects.create(user=self.admin, widget_type="stat", config={"type": "users"})

    def test_admin_dashboard_view(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("admin-dashboard")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("recent_users", resp.data)
        self.assertIn("stats", resp.data)
        self.assertIn("widgets", resp.data)

    def test_visitor_dashboard_view(self):
        self.client.force_authenticate(user=self.visitor)
        url = reverse("visitor-dashboard")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("recent_activity", resp.data)
        self.assertIn("popular_villages", resp.data)
        self.assertIn("notifications", resp.data)

    def test_learner_dashboard_view(self):
        self.client.force_authenticate(user=self.learner)
        url = reverse("learner-dashboard")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("enrolled_tutorials", resp.data)
        self.assertIn("quiz_results", resp.data)
        self.assertIn("recent_payments", resp.data)

    def test_tutor_dashboard_view(self):
        self.client.force_authenticate(user=self.tutor)
        url = reverse("tutor-dashboard")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("my_bookings", resp.data)
        self.assertIn("earnings", resp.data)
        self.assertIn("assignments", resp.data)

    def test_guide_dashboard_view(self):
        self.client.force_authenticate(user=self.guide)
        url = reverse("guide-dashboard")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("recent_bookings", resp.data)
        self.assertIn("earnings", resp.data)

    def test_welcome_dashboard_view(self):
        url = reverse("welcome-dashboard")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("featured_village", resp.data)
        self.assertIn("site_stats", resp.data)
        self.assertIn("testimonials", resp.data)

    def test_what_about_us_view(self):
        url = reverse("what-about-us")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("title", resp.data)
        self.assertIn("mission", resp.data)
        self.assertIn("team", resp.data)

    def test_contact_us_view(self):
        url = reverse("contact-us")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("email", resp.data)
        self.assertIn("phone", resp.data)
        self.assertIn("support_link", resp.data)

    def test_activity_log_api(self):
        self.client.force_authenticate(user=self.learner)
        UserActivityLog.objects.create(user=self.learner, action="login", description="Logged in")
        url = reverse("activitylog-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(any(log["action"] == "login" for log in resp.data))

    def test_dashboard_widget_api(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("dashboardwidget-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)
        # Test create
        data = {"widget_type": "stat", "config": {"type": "bookings"}}
        resp2 = self.client.post(url, data)
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(resp2.data["widget_type"], "stat")

    def test_system_notification_api(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("systemnotification-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(any(n["title"] == "Platform Update" for n in resp.data))
        # Mark as read
        notif_id = self.sys_notification.id
        mark_url = reverse("systemnotification-mark-read", args=[notif_id])
        resp2 = self.client.post(mark_url)
        self.assertEqual(resp2.status_code, 200)

    def test_feedback_summary_api(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("feedbacksummary-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(any(f["average_rating"] == 4.7 for f in resp.data))

    def test_permissions(self):
        # Normal user cannot access admin stats APIs
        self.client.force_authenticate(user=self.learner)
        url = reverse("dailysitestats-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        url = reverse("dashboardstat-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)