from django.contrib import admin
from .models import CustomSession, SessionMaterial, SessionFeedback, InAppNotification

@admin.register(CustomSession)
class CustomSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "session_type",
        "tutor_or_guide",
        "learner_or_visitor",
        "topic_or_location",
        "scheduled_time",
        "status",
        "is_confirmed",
        "is_paid",
    )
    list_filter = ("session_type", "status", "is_confirmed", "is_paid", "scheduled_time")
    search_fields = ("topic_or_location", "tutor_or_guide__username", "learner_or_visitor__username")
    ordering = ("-scheduled_time",)

@admin.register(SessionMaterial)
class SessionMaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "title", "uploaded_by", "uploaded_at")
    search_fields = ("title", "session__topic_or_location", "uploaded_by__username")

@admin.register(SessionFeedback)
class SessionFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "author", "rating", "created_at")
    search_fields = ("session__topic_or_location", "author__username", "comment")

@admin.register(InAppNotification)
class InAppNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "is_read", "url")
    search_fields = ("user__username", "message")
    list_filter = ("is_read", "created_at")