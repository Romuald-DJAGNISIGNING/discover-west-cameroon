from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SupportTicket(models.Model):
    CATEGORY_CHOICES = [
        ('technical', _("Technical Issue")),
        ('account', _("Account Issue")),
        ('general', _("General Inquiry")),
    ]

    STATUS_CHOICES = [
        ('open', _("Open")),
        ('in_progress', _("In Progress")),
        ('closed', _("Closed")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name=_("User")
    )
    subject = models.CharField(_("Subject"), max_length=255)
    message = models.TextField(_("Message"))
    category = models.CharField(
        _("Category"),
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=STATUS_CHOICES,
        default='open'
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Support Ticket")
        verbose_name_plural = _("Support Tickets")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.user.email}"


class SupportReply(models.Model):
    ticket = models.ForeignKey(
        'SupportTicket',
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name="Support Ticket"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    def __str__(self):
        return f"Reply by {self.user} on ticket #{self.ticket.id}"

    class Meta:
        verbose_name = "Support Reply"
        verbose_name_plural = "Support Replies"
        ordering = ['-created_at']

