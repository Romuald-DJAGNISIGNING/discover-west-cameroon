from django.db import models
from django.conf import settings
from villages.models import Village
from tourism.models import TouristicAttraction
from festivals.models import Festival

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('bug', 'Bug/Issue'),
        ('suggestion', 'Suggestion'),
        ('abuse', 'Abuse/Violation'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='feedback')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    title = models.CharField(max_length=255)
    description = models.TextField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Optional links to other apps for context
    village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.SET_NULL, related_name="reports")
    attraction = models.ForeignKey(TouristicAttraction, null=True, blank=True, on_delete=models.SET_NULL, related_name="reports")
    festival = models.ForeignKey(Festival, null=True, blank=True, on_delete=models.SET_NULL, related_name="reports")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    resolution_comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type} - {self.title}"