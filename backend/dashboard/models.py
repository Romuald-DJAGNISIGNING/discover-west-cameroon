from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


User = get_user_model()





class UserActivityLog(models.Model):
    """
    Logs user activity across the platform.
    """
    ACTION_CHOICES = [
        ('login', _("Login")),
        ('logout', _("Logout")),
        ('view_festival', _("Viewed Festival")),
        ('view_tourism', _("Viewed Tourism Spot")),
        ('book_tour', _("Booked Tour")),
        ('book_tutor', _("Booked Tutor")),
        ('book_guide', _("Booked Guide")),
        ('post_review', _("Posted Review")),
        ('submit_report', _("Submitted Report")),
        ('other', _("Other")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs', verbose_name=_("User"))
    action = models.CharField(_("Action"), max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(_("Description"), blank=True, null=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("User Activity Log")
        verbose_name_plural = _("User Activity Logs")

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"


class DailySiteStatistics(models.Model):
    """
    Stores daily aggregated platform statistics.
    """
    date = models.DateField(_("Date"), default=timezone.now, unique=True)
    new_users = models.PositiveIntegerField(_("New Users"), default=0)
    active_users = models.PositiveIntegerField(_("Active Users"), default=0)

    total_bookings = models.PositiveIntegerField(_("Total Bookings"), default=0)
    total_tour_bookings = models.PositiveIntegerField(_("Total Tour Bookings"), default=0)
    total_tutor_bookings = models.PositiveIntegerField(_("Total Tutor Bookings"), default=0)
    total_guide_bookings = models.PositiveIntegerField(_("Total Guide Bookings"), default=0)

    total_reviews = models.PositiveIntegerField(_("Total Reviews"), default=0)
    total_reports = models.PositiveIntegerField(_("Total Reports"), default=0)

    class Meta:
        ordering = ['-date']
        verbose_name = _("Daily Site Statistic")
        verbose_name_plural = _("Daily Site Statistics")

    def __str__(self):
        return f"{_('Stats for')} {self.date}"


class TourBookingStatistic(models.Model):
    """
    Tracks per-tour booking stats by location or type.
    """
    date = models.DateField(_("Date"), default=timezone.now)
    tour_type = models.CharField(_("Tour Type"), max_length=100, blank=True, null=True)
    location = models.CharField(_("Location"), max_length=255, blank=True, null=True)
    bookings_count = models.PositiveIntegerField(_("Bookings Count"), default=0)

    class Meta:
        unique_together = ('date', 'tour_type', 'location')
        ordering = ['-date']
        verbose_name = _("Tour Booking Statistic")
        verbose_name_plural = _("Tour Booking Statistics")

    def __str__(self):
        return f"{_('Tour bookings on')} {self.date} - {self.tour_type or _('Any')} @ {self.location or _('All')}: {self.bookings_count}"


class TutorBookingStatistic(models.Model):
    """
    Tracks bookings per tutor and subject.
    """
    date = models.DateField(_("Date"), default=timezone.now)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_booking_stats', verbose_name=_("Tutor"))
    subject = models.CharField(_("Subject"), max_length=255, blank=True, null=True)
    bookings_count = models.PositiveIntegerField(_("Bookings Count"), default=0)

    class Meta:
        unique_together = ('date', 'tutor', 'subject')
        ordering = ['-date']
        verbose_name = _("Tutor Booking Statistic")
        verbose_name_plural = _("Tutor Booking Statistics")

    def __str__(self):
        return f"{_('Tutor')} {self.tutor.email} {_('on')} {self.date} - {self.subject or _('All')}: {self.bookings_count}"


class GuideBookingStatistic(models.Model):
    """
    Tracks bookings made for local guides.
    """
    date = models.DateField(_("Date"), default=timezone.now)
    guide = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guide_booking_stats', verbose_name=_("Guide"))
    region = models.CharField(_("Region"), max_length=255, blank=True, null=True)
    bookings_count = models.PositiveIntegerField(_("Bookings Count"), default=0)

    class Meta:
        unique_together = ('date', 'guide', 'region')
        ordering = ['-date']
        verbose_name = _("Guide Booking Statistic")
        verbose_name_plural = _("Guide Booking Statistics")

    def __str__(self):
        return f"{_('Guide')} {self.guide.email} {_('on')} {self.date} - {self.region or _('All')}: {self.bookings_count}"


class FeedbackSummary(models.Model):
    """
    Captures daily feedback metrics.
    """
    date = models.DateField(_("Date"), default=timezone.now)
    average_rating = models.FloatField(_("Average Rating"), default=0.0)
    total_feedback = models.PositiveIntegerField(_("Total Feedback"), default=0)
    positive_feedback = models.PositiveIntegerField(_("Positive Feedback"), default=0)
    negative_feedback = models.PositiveIntegerField(_("Negative Feedback"), default=0)

    class Meta:
        ordering = ['-date']
        verbose_name = _("Feedback Summary")
        verbose_name_plural = _("Feedback Summaries")

    def __str__(self):
        return f"{_('Feedback for')} {self.date} - {_('Avg')}: {self.average_rating}"


class SystemNotification(models.Model):
    """
    System-generated messages for users or admins.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('info', _("Info")),
        ('warning', _("Warning")),
        ('error', _("Error")),
        ('success', _("Success")),
    ]

    title = models.CharField(_("Title"), max_length=255)
    message = models.TextField(_("Message"))
    notification_type = models.CharField(_("Notification Type"), max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='system_notifications',
        blank=True,
        verbose_name=_("Recipients")
    )
    is_read = models.BooleanField(_("Is Read"), default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("System Notification")
        verbose_name_plural = _("System Notifications")

    def __str__(self):
        return f"{self.notification_type.title()} - {self.title}"


class DashboardStat(models.Model):
    """
    General statistics for the dashboard.
    """
    stat_name = models.CharField(_("Stat Name"), max_length=100, unique=True)
    value = models.PositiveIntegerField(_("Value"), default=0)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)
    label = models.CharField(_("Label"), max_length=255, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)

    class Meta:
        ordering = ['stat_name']
        verbose_name = _("Dashboard Stat")
        verbose_name_plural = _("Dashboard Stats")

    def __str__(self):
        return f"{self.stat_name}: {self.value}"
