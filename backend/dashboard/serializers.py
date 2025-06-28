from rest_framework import serializers
from .models import (
    UserActivityLog, DailySiteStatistics, TourBookingStatistic, TutorBookingStatistic,
    GuideBookingStatistic, FeedbackSummary, SystemNotification, DashboardStat, DashboardWidget
)

class UserActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = UserActivityLog
        fields = "__all__"

class DailySiteStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySiteStatistics
        fields = "__all__"

class TourBookingStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBookingStatistic
        fields = "__all__"

class TutorBookingStatisticSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField()
    class Meta:
        model = TutorBookingStatistic
        fields = "__all__"

class GuideBookingStatisticSerializer(serializers.ModelSerializer):
    guide = serializers.StringRelatedField()
    class Meta:
        model = GuideBookingStatistic
        fields = "__all__"

class FeedbackSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackSummary
        fields = "__all__"

class SystemNotificationSerializer(serializers.ModelSerializer):
    recipients = serializers.StringRelatedField(many=True)
    class Meta:
        model = SystemNotification
        fields = "__all__"

class DashboardStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStat
        fields = "__all__"

class DashboardWidgetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = DashboardWidget
        fields = "__all__"