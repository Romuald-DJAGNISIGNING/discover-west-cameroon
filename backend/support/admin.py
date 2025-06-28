from django.contrib import admin
from .models import SupportTicket, SupportMessage

class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 1

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "priority", "status", "village", "attraction", "festival", "created_by", "assigned_to", "created_at")
    list_filter = ("priority", "status", "village", "attraction", "festival")
    search_fields = ("subject", "message", "created_by__username", "assigned_to__username")
    inlines = [SupportMessageInline]

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ("ticket", "user", "created_at")
    search_fields = ("ticket__subject", "user__username", "message")