from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ("in_app", "In-app"),
        ("email", "Email"),
        ("sms", "SMS"),
    )
    EVENT_TYPE_CHOICES = (
        ("festival_new", "New Festival"),
        ("festival_attendance", "Festival Attendance"),
        ("festival_feedback", "Festival Feedback"),
        ("tutor_booked", "Tutor/Guide Booked"),
        ("assignment", "Assignment"),
        ("quiz", "Quiz"),
        ("payment_success", "Payment Success"),
        ("payment_failed", "Payment Failed"),
        ("payout_success", "Payout Success"),
        ("custom", "Custom"),
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")
    notification_type = models.CharField(max_length=16, choices=NOTIFICATION_TYPE_CHOICES, default="in_app")
    event_type = models.CharField(max_length=32, choices=EVENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    url = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=32, choices=(("pending","Pending"),("sent","Sent"),("failed","Failed")), default="pending")
    
    # Generic foreign key for related objects
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} - {self.title} ({self.notification_type})"

    def get_absolute_url(self):
        if self.event_type == "payment_success" and self.content_object:
            return f"/payments/transactions/{self.content_object.id}/"
        elif self.event_type == "payout_success" and self.content_object:
            return f"/payments/payouts/{self.content_object.id}/"
        return self.url