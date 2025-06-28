from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL

SESSION_TYPE_CHOICES = (
    ('tutoring', _("Tutoring")),
    ('tour_guide', _("Tour Guide")),
)

SESSION_STATUS_CHOICES = (
    ('pending', _("Pending")),
    ('confirmed', _("Confirmed")),
    ('in_progress', _("In Progress")),
    ('completed', _("Completed")),
    ('cancelled', _("Cancelled")),
    ('no_show', _("No Show")),
)

RECURRENCE_CHOICES = (
    ('none', _("None")),
    ('daily', _("Daily")),
    ('weekly', _("Weekly")),
    ('monthly', _("Monthly")),
)

class CustomSession(models.Model):
    session_type = models.CharField(
        _("Session Type"),
        max_length=50,
        choices=SESSION_TYPE_CHOICES
    )
    tutor_or_guide = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hosted_sessions',
        verbose_name=_("Tutor or Guide")
    )
    learner_or_visitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attending_sessions',
        verbose_name=_("Learner or Visitor")
    )
    topic_or_location = models.CharField(
        _("Topic or Location"),
        max_length=255,
        help_text=_("Topic for tutoring or location for guide session")
    )
    scheduled_time = models.DateTimeField(_("Scheduled Time"))
    duration_minutes = models.PositiveIntegerField(_("Duration (minutes)"))
    location = models.CharField(_("Location"), max_length=255, blank=True, null=True)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    is_confirmed = models.BooleanField(_("Is Confirmed"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=SESSION_STATUS_CHOICES,
        default='pending'
    )
    cancellation_reason = models.TextField(_("Cancellation Reason"), blank=True, null=True)
    external_link = models.URLField(_("External Link (e.g., Zoom/Meet)"), blank=True, null=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(_("Is Paid"), default=False)
    recurrence = models.CharField(
        _("Recurrence"),
        max_length=10,
        choices=RECURRENCE_CHOICES,
        default='none'
    )
    recurrence_end_date = models.DateField(_("Recurrence End Date"), blank=True, null=True)
    can_communicate = models.BooleanField(_("Allow Messaging"), default=True)
    can_share_materials = models.BooleanField(_("Allow Sharing Materials"), default=True)

    class Meta:
        ordering = ['-scheduled_time']
        verbose_name = _("Custom Session")
        verbose_name_plural = _("Custom Sessions")

    def __str__(self):
        return f"{self.get_session_type_display()} Session with {self.tutor_or_guide.username} on {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def end_time(self):
        return self.scheduled_time + timezone.timedelta(minutes=self.duration_minutes)

    def mark_confirmed(self):
        self.is_confirmed = True
        self.status = 'confirmed'
        self.save(update_fields=['is_confirmed', 'status', 'updated_at'])

    def mark_completed(self):
        self.status = 'completed'
        self.save(update_fields=['status', 'updated_at'])

    def mark_cancelled(self, reason=""):
        self.status = 'cancelled'
        self.cancellation_reason = reason
        self.save(update_fields=['status', 'cancellation_reason', 'updated_at'])

    def mark_no_show(self):
        self.status = 'no_show'
        self.save(update_fields=['status', 'updated_at'])

    def mark_paid(self):
        self.is_paid = True
        self.save(update_fields=['is_paid', 'updated_at'])

    def is_active(self):
        return self.status in ['pending', 'confirmed', 'in_progress']

    def can_accept_feedback(self):
        """Check if session is in a state that can accept feedback"""
        return self.status == 'completed'


class SessionMaterial(models.Model):
    session = models.ForeignKey(
        CustomSession, 
        on_delete=models.CASCADE, 
        related_name='materials', 
        verbose_name=_("Session")
    )
    title = models.CharField(_("Title"), max_length=255)
    file = models.FileField(_("File"), upload_to="session_materials/")
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="uploaded_materials"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = _("Session Material")
        verbose_name_plural = _("Session Materials")

    def __str__(self):
        return f"{self.title} for {self.session}"


class SessionFeedback(models.Model):
    session = models.ForeignKey(
        CustomSession,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name=_("Session")
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Author")
    )
    rating = models.PositiveSmallIntegerField(
        _("Rating"), 
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text=_("1 to 5 stars")
    )
    comment = models.TextField(_("Comment"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        unique_together = ('session', 'author')
        ordering = ['-created_at']
        verbose_name = _("Session Feedback")
        verbose_name_plural = _("Session Feedbacks")

    def __str__(self):
        return f"{self.rating}★ Feedback by {self.author.username} for {self.session}"


class InAppNotification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inapp_notifications'
    )
    message = models.CharField(max_length=512)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("In-App Notification")
        verbose_name_plural = _("In-App Notifications")

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"