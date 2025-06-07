from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'subject', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('category', 'status', 'created_at', 'updated_at')
    search_fields = ('user__email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
