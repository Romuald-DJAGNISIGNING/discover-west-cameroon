
from django.db import models
from django.conf import settings
from django.utils import timezone

SESSION_TYPE_CHOICES = (
    ('tutoring', 'Tutoring'),
    ('tour_guide', 'Tour Guide'),
)

class CustomSession(models.Model):
    session_type = models.CharField(max_length=50, choices=SESSION_TYPE_CHOICES)
    tutor_or_guide = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_sessions')
    student_or_visitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attending_sessions')
    topic_or_location = models.CharField(max_length=255, help_text="Topic for tutoring or location for guide session")
    scheduled_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    location = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_time']
        verbose_name = "Custom Session"
        verbose_name_plural = "Custom Sessions"

    def __str__(self):
        return f"{self.session_type.title()} Session with {self.tutor_or_guide.username} on {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
