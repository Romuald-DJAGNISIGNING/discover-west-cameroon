from django.db import models
from django.conf import settings
from villages.models import Village
from tourism.models import TouristicAttraction
from festivals.models import Festival

class SupportTicket(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    subject = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='support_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Optional linkage for context
    village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.SET_NULL, related_name="support_tickets")
    attraction = models.ForeignKey(TouristicAttraction, null=True, blank=True, on_delete=models.SET_NULL, related_name="support_tickets")
    festival = models.ForeignKey(Festival, null=True, blank=True, on_delete=models.SET_NULL, related_name="support_tickets")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    resolution = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject} ({self.get_status_display()})"

class SupportMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    attachment = models.FileField(upload_to='support/attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)