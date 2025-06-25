
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'verb', 'target', 'type', 'timestamp', 'read')
    list_filter = ('type', 'read', 'timestamp')
    search_fields = ('recipient__username', 'actor__username', 'verb', 'target')
    ordering = ('-timestamp',)
