from django.db import models
from django.conf import settings

REPORT_REASON_CHOICES = (
    ('abuse', 'Abuse'),
    ('harassment', 'Harassment'),
    ('spam', 'Spam'),
    ('fraud', 'Fraud'),
    ('other', 'Other'),
)

REPORT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('reviewed', 'Reviewed'),
    ('resolved', 'Resolved'),
    ('dismissed', 'Dismissed'),
)

class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made'
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_received'
    )
    reason = models.CharField(max_length=50, choices=REPORT_REASON_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Report from {self.reporter.email} against {self.reported_user.email}"
