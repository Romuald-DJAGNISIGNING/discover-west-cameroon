from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "title", "notification_type", "event_type", 
                   "content_object", "is_read", "created_at", "delivery_status")
    list_filter = ("notification_type", "event_type", "is_read", "delivery_status", "created_at")
    search_fields = ("recipient__username", "title", "message")
    readonly_fields = ("content_object",)