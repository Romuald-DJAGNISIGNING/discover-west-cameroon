from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserActivityLog(models.Model):
    """
    Logs user activity across the platform.
    """
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view_festival', 'Viewed Festival'),
        ('view_tourism', 'Viewed Tourism Spot'),
        ('book_tour', 'Booked Tour'),
        ('book_tutor', 'Booked Tutor'),
        ('book_guide', 'Booked Guide'),
        ('post_review', 'Posted Review'),
        ('submit_report', 'Submitted Report'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"


class DailySiteStatistics(models.Model):
    """
    Stores daily aggregated platform statistics.
    """
    date = models.DateField(default=timezone.now, unique=True)
    new_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)

    total_bookings = models.PositiveIntegerField(default=0)
    total_tour_bookings = models.PositiveIntegerField(default=0)
    total_tutor_bookings = models.PositiveIntegerField(default=0)
    total_guide_bookings = models.PositiveIntegerField(default=0)

    total_reviews = models.PositiveIntegerField(default=0)
    total_reports = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Stats for {self.date}"


class TourBookingStatistic(models.Model):
    """
    Tracks per-tour booking stats by location or type.
    """
    date = models.DateField(default=timezone.now)
    tour_type = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bookings_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('date', 'tour_type', 'location')
        ordering = ['-date']

    def __str__(self):
        return f"Tour bookings on {self.date} - {self.tour_type or 'Any'} @ {self.location or 'All'}: {self.bookings_count}"


class TutorBookingStatistic(models.Model):
    """
    Tracks bookings per tutor and subject.
    """
    date = models.DateField(default=timezone.now)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_booking_stats')
    subject = models.CharField(max_length=255, blank=True, null=True)
    bookings_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('date', 'tutor', 'subject')
        ordering = ['-date']

    def __str__(self):
        return f"Tutor {self.tutor.email} on {self.date} - {self.subject or 'All'}: {self.bookings_count}"


class GuideBookingStatistic(models.Model):
    """
    Tracks bookings made for local guides.
    """
    date = models.DateField(default=timezone.now)
    guide = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guide_booking_stats')
    region = models.CharField(max_length=255, blank=True, null=True)
    bookings_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('date', 'guide', 'region')
        ordering = ['-date']

    def __str__(self):
        return f"Guide {self.guide.email} on {self.date} - {self.region or 'All'}: {self.bookings_count}"


class FeedbackSummary(models.Model):
    """
    Captures daily feedback metrics.
    """
    date = models.DateField(default=timezone.now)
    average_rating = models.FloatField(default=0.0)
    total_feedback = models.PositiveIntegerField(default=0)
    positive_feedback = models.PositiveIntegerField(default=0)
    negative_feedback = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Feedback for {self.date} - Avg: {self.average_rating}"


class SystemNotification(models.Model):
    """
    System-generated messages for users or admins.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    created_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(User, related_name='notifications', blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type.title()} - {self.title}"

class DashboardStat(models.Model):
    """
    General statistics for the dashboard.
    """
    stat_name = models.CharField(max_length=100, unique=True)
    value = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['stat_name']

    def __str__(self):
        return f"{self.stat_name}: {self.value}"
