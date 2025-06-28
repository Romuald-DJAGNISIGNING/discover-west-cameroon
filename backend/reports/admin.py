from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("type", "title", "status", "village", "attraction", "festival", "reported_by", "reviewed_by", "created_at")
    list_filter = ("type", "status", "village", "attraction", "festival")
    search_fields = ("title", "description", "reported_by__username", "reviewed_by__username")