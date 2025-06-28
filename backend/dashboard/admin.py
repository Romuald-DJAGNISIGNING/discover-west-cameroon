from django.contrib import admin
from .models import (
    UserActivityLog, DailySiteStatistics, TourBookingStatistic, TutorBookingStatistic,
    GuideBookingStatistic, FeedbackSummary, SystemNotification, DashboardStat, DashboardWidget
)

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'timestamp')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__email', 'action', 'description')

@admin.register(DailySiteStatistics)
class DailySiteStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'new_users', 'active_users', 'total_bookings')
    list_filter = ('date',)
    search_fields = ('date',)

@admin.register(TourBookingStatistic)
class TourBookingStatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'tour_type', 'location', 'bookings_count')
    list_filter = ('date', 'tour_type', 'location')
    search_fields = ('tour_type', 'location')

@admin.register(TutorBookingStatistic)
class TutorBookingStatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'tutor', 'subject', 'bookings_count')
    list_filter = ('date', 'subject', 'tutor')
    search_fields = ('tutor__email', 'subject')

@admin.register(GuideBookingStatistic)
class GuideBookingStatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'guide', 'region', 'bookings_count')
    list_filter = ('date', 'region', 'guide')
    search_fields = ('guide__email', 'region')

@admin.register(FeedbackSummary)
class FeedbackSummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'average_rating', 'total_feedback', 'positive_feedback', 'negative_feedback')
    list_filter = ('date',)
    search_fields = ('date',)

@admin.register(SystemNotification)
class SystemNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'created_at', 'is_read')
    list_filter = ('notification_type', 'created_at', 'is_read')
    search_fields = ('title', 'message')
    filter_horizontal = ('recipients',)

@admin.register(DashboardStat)
class DashboardStatAdmin(admin.ModelAdmin):
    list_display = ('stat_name', 'value', 'last_updated', 'label')
    list_filter = ('stat_name',)
    search_fields = ('stat_name', 'label')

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'widget_type', 'created')
    list_filter = ('widget_type', 'created', 'user')
    search_fields = ('widget_type', 'user__email')