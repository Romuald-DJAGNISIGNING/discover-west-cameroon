from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


SESSION_TYPE_CHOICES = (
    ('tutoring', _("Tutoring")),
    ('tour_guide', _("Tour Guide")),
)

class CustomSession(models.Model):
    session_type = models.CharField(
        _("Session Type"),
        max_length=50,
        choices=SESSION_TYPE_CHOICES
    )
    tutor_or_guide = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_sessions',
        verbose_name=_("Tutor or Guide")
    )
    learner_or_visitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=[
            ('pending', _("Pending")),
            ('completed', _("Completed")),
            ('cancelled', _("Cancelled")),
        ],
        default='pending'
    )

    class Meta:
        ordering = ['-scheduled_time']
        verbose_name = _("Custom Session")
        verbose_name_plural = _("Custom Sessions")

    def __str__(self):
        return f"{self.session_type.title()} {_('Session with')} {self.tutor_or_guide.username} {_('on')} {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
