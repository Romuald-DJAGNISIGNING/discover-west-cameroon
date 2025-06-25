from django.contrib import admin
from .models import CustomSession

@admin.register(CustomSession)
class CustomSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'session_type',
        'tutor_or_guide',
        'learner_or_visitor',
        'topic_or_location',
        'scheduled_time',
        'duration_minutes',
        'is_confirmed',
        'created_at',
    )
    list_filter = ('session_type', 'is_confirmed', 'scheduled_time')
    search_fields = (
        'topic_or_location',
        'tutor_or_guide__username',
        'learner_or_visitor__username',
    )
