from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class DailySiteStatistics(models.Model):
    date = models.DateField(unique=True)
    new_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    total_bookings = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    total_festivals = models.PositiveIntegerField(default=0)
    total_events = models.PositiveIntegerField(default=0)
    total_tour_bookings = models.PositiveIntegerField(default=0)
    total_tutor_bookings = models.PositiveIntegerField(default=0)
    total_guide_bookings = models.PositiveIntegerField(default=0)

class TourBookingStatistic(models.Model):
    date = models.DateField()
    tour_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bookings_count = models.PositiveIntegerField(default=0)

class TutorBookingStatistic(models.Model):
    date = models.DateField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    bookings_count = models.PositiveIntegerField(default=0)

class GuideBookingStatistic(models.Model):
    date = models.DateField()
    guide = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    bookings_count = models.PositiveIntegerField(default=0)

class FeedbackSummary(models.Model):
    date = models.DateField()
    average_rating = models.FloatField()
    total_feedback = models.PositiveIntegerField(default=0)
    positive_feedback = models.PositiveIntegerField(default=0)
    negative_feedback = models.PositiveIntegerField(default=0)

class SystemNotification(models.Model):
    NOTIF_TYPES = [
        ('info', _("Info")),
        ('warning', _("Warning")),
        ('success', _("Success")),
        ('error', _("Error")),
    ]
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='info')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    recipients = models.ManyToManyField(User, blank=True, related_name="system_notifications")

class DashboardStat(models.Model):
    stat_name = models.CharField(max_length=100)
    value = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=100, blank=True)

class DashboardWidget(models.Model):
    WIDGET_TYPES = [
        ('stat', _("Statistic")),
        ('map', _("Map")),
        ('calendar', _("Calendar")),
        ('weather', _("Weather")),
        ('reviews', _("Reviews")),
        ('featured', _("Featured")),
        ('gallery', _("Gallery")),
        ('leaderboard', _("Leaderboard")),
        ('phrase', _("Language Phrase")),
        ('event', _("Event")),
        ('custom', _("Custom")),
        ('assignments', _("Assignments")),
        ('sessions', _("Sessions")),
        ('payments', _("Payments")),
        ('support', _("Support")),
        ('quizzes', _("Quizzes")),
        ('reports', _("Reports")),
        ('notifications', _("Notifications")),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dashboard_widgets")
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPES)
    config = models.JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)