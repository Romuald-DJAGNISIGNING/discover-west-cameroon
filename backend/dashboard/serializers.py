from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    UserActivityLog,
    DailySiteStatistics,
    TourBookingStatistic,
    TutorBookingStatistic,
    GuideBookingStatistic,
    FeedbackSummary,
    SystemNotification
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserActivityLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'action', 'description', 'timestamp']


class DailySiteStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySiteStatistics
        fields = [
            'id', 'date', 'new_users', 'active_users',
            'total_bookings', 'total_tour_bookings',
            'total_tutor_bookings', 'total_guide_bookings',
            'total_reviews', 'total_reports'
        ]


class TourBookingStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBookingStatistic
        fields = ['id', 'date', 'tour_type', 'location', 'bookings_count']


class TutorBookingStatisticSerializer(serializers.ModelSerializer):
    tutor = UserSerializer(read_only=True)

    class Meta:
        model = TutorBookingStatistic
        fields = ['id', 'date', 'tutor', 'subject', 'bookings_count']


class GuideBookingStatisticSerializer(serializers.ModelSerializer):
    guide = UserSerializer(read_only=True)

    class Meta:
        model = GuideBookingStatistic
        fields = ['id', 'date', 'guide', 'region', 'bookings_count']


class FeedbackSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackSummary
        fields = [
            'id', 'date', 'average_rating',
            'total_feedback', 'positive_feedback', 'negative_feedback'
        ]


class SystemNotificationSerializer(serializers.ModelSerializer):
    recipients = UserSerializer(many=True, read_only=True)

    class Meta:
        model = SystemNotification
        fields = [
            'id', 'title', 'message',
            'notification_type', 'created_at', 'recipients', 'is_read'
        ]
