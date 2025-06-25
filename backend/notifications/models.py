from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings


User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('booking', _("Booking")),
        ('payment', _("Payment")),
        ('support', _("Support")),
        ('review', _("Review")),
        ('generic', _("Generic")),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_recipients',  # <-- make this unique
        verbose_name=_("Recipient")
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name=_("Actor")
    )
    verb = models.CharField(_("Verb"), max_length=255)  # e.g. 'booked', 'paid', 'replied'
    target = models.CharField(_("Target"), max_length=255, null=True, blank=True)  # e.g. tutor name, guide name
    action_object = models.CharField(_("Action Object"), max_length=255, null=True, blank=True)  # optional details
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    read = models.BooleanField(_("Read"), default=False)
    type = models.CharField(
        _("Type"),
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='generic'
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return f'{self.recipient.username} - {self.verb} - {self.target}'       


