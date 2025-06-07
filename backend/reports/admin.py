from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'reporter_email', 'reported_user_email', 'reason', 'status', 'created_at', 'reviewed_at'
    )
    list_filter = ('reason', 'status', 'created_at', 'reviewed_at')
    search_fields = (
        'reporter__email', 'reported_user__email', 'description'
    )
    ordering = ('-created_at',)

    def reporter_email(self, obj):
        return obj.reporter.email
    reporter_email.short_description = 'Reporter Email'

    def reported_user_email(self, obj):
        return obj.reported_user.email
    reported_user_email.short_description = 'Reported User Email'
