from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


REPORT_REASON_CHOICES = (
    ('abuse', _("Abuse")),
    ('harassment', _("Harassment")),
    ('spam', _("Spam")),
    ('fraud', _("Fraud")),
    ('other', _("Other")),
)

REPORT_STATUS_CHOICES = (
    ('pending', _("Pending")),
    ('reviewed', _("Reviewed")),
    ('resolved', _("Resolved")),
    ('dismissed', _("Dismissed")),
)

class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made',
        verbose_name=_("Reporter")
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_received',
        verbose_name=_("Reported User")
    )
    reason = models.CharField(_("Reason"), max_length=50, choices=REPORT_REASON_CHOICES)
    description = models.TextField(_("Description"))
    status = models.CharField(_("Status"), max_length=20, choices=REPORT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    reviewed_at = models.DateTimeField(_("Reviewed At"), blank=True, null=True)

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ['-created_at']

    def __str__(self):
        return _("Report from %(reporter)s against %(reported_user)s") % {
            "reporter": self.reporter.email,
            "reported_user": self.reported_user.email,
        }
