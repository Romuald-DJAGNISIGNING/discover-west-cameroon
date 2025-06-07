from django.contrib import admin
from .models import (
    UserActivityLog,
    DailySiteStatistics,
    TourBookingStatistic,
    TutorBookingStatistic,
    GuideBookingStatistic,
    FeedbackSummary,
    SystemNotification,
    DashboardStat,
)

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__email', 'action', 'description')
    list_filter = ('action', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(DailySiteStatistics)
class DailySiteStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'new_users', 'active_users', 'total_bookings', 'total_reviews', 'total_reports')
    search_fields = ('date',)
    ordering = ('-date',)
    list_filter = ('date',)

@admin.register(TourBookingStatistic)
class TourBookingStatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'tour_type', 'location', 'bookings_count')
    search_fields = ('tour_type', 'location')
    list_filter = ('date', 'tour_type', 'location')
    ordering = ('-date',)

@admin.register(TutorBookingStatistic)
class TutorBookingStatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'tutor', 'subject', 'bookings_count')
    search_fields = ('tutor__email', 'subject')
    list_filter = ('date', 'subject')
    ordering = ('-date',)

@admin.register(GuideBookingStatistic)
class GuideBookingStatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'guide', 'region', 'bookings_count')
    search_fields = ('guide__email', 'region')
    list_filter = ('date', 'region')
    ordering = ('-date',)

@admin.register(FeedbackSummary)
class FeedbackSummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'average_rating', 'total_feedback', 'positive_feedback', 'negative_feedback')
    search_fields = ('date',)
    ordering = ('-date',)
    list_filter = ('date',)

@admin.register(SystemNotification)
class SystemNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'created_at', 'is_read')
    search_fields = ('title', 'message')
    list_filter = ('notification_type', 'is_read', 'created_at')
    ordering = ('-created_at',)
    filter_horizontal = ('recipients',)

@admin.register(DashboardStat)
class DashboardStatAdmin(admin.ModelAdmin):
    list_display = ('stat_name', 'label', 'value', 'last_updated')
    search_fields = ('stat_name', 'label')
    list_filter = ('last_updated',)
    ordering = ('stat_name',)
    readonly_fields = ('stat_name', 'label', 'value', 'last_updated', 'description')
    fieldsets = (
        (None, {
            'fields': ('stat_name', 'label', 'value', 'last_updated', 'description')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

