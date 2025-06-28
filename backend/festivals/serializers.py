from rest_framework import serializers
from .models import (
    Festival, FestivalMedia, FestivalFact, FestivalComment,
    FestivalBookmark, FestivalAttendance, FestivalFeedback
)
from django.contrib.auth import get_user_model

User = get_user_model()

class FestivalMediaSerializer(serializers.ModelSerializer):
    festival = serializers.PrimaryKeyRelatedField(queryset=Festival.objects.all())
    
    class Meta:
        model = FestivalMedia
        fields = ['id', 'festival', 'image', 'video_url', 'caption', 'created_at']
        read_only_fields = ['created_at']
        extra_kwargs = {
            'image': {'required': False},
            'video_url': {'required': False},
            'caption': {'required': False}
        }

class FestivalFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalFact
        fields = ['id', 'fact', 'source', 'created_at']
        read_only_fields = ['created_at']
        extra_kwargs = {
            'fact': {'required': True},
            'festival': {'required': True}
        }

class FestivalCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = FestivalComment
        fields = ['id', 'user', 'festival', 'comment', 'created_at']
        read_only_fields = ['user', 'festival', 'created_at']
        extra_kwargs = {
            'comment': {'required': True}
        }

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'role': obj.user.role
        }

class FestivalBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalBookmark
        fields = ['id', 'user', 'festival', 'created_at']
        read_only_fields = ['user', 'created_at']


class FestivalAttendanceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    booked_tutor_guide = serializers.SerializerMethodField()
    festival = serializers.PrimaryKeyRelatedField(queryset=Festival.objects.all())

    class Meta:
        model = FestivalAttendance
        fields = [
            'id', 'user', 'festival', 'status', 'booked_tutor_guide',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'role': obj.user.role
        }

    def get_booked_tutor_guide(self, obj):
        if obj.booked_tutor_guide:
            return {
                'id': obj.booked_tutor_guide.id,
                'username': obj.booked_tutor_guide.username,
                'role': obj.booked_tutor_guide.role
            }
        return None


class FestivalFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FestivalFeedback
        fields = [
            'id', 'attendance', 'festival', 'feedback_text', 'rating',
            'image', 'video_url', 'experience', 'created_at', 'updated_at'
        ]
        read_only_fields = ['attendance', 'festival', 'created_at', 'updated_at']
        extra_kwargs = {
            'rating': {'min_value': 1, 'max_value': 5, 'required': True},
            'feedback_text': {'required': True},
            'image': {'required': False},
            'video_url': {'required': False}
        }

    def get_booked_tutor_guide(self, obj):
        if obj.booked_tutor_guide:
            return {
                'id': obj.booked_tutor_guide.id,
                'username': obj.booked_tutor_guide.username,
                'role': obj.booked_tutor_guide.role
            }
        return None

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'role': obj.user.role
        }

class FestivalSerializer(serializers.ModelSerializer):
    media = FestivalMediaSerializer(many=True, read_only=True)
    facts = FestivalFactSerializer(many=True, read_only=True)
    comments = FestivalCommentSerializer(many=True, read_only=True)
    attendances_count = serializers.IntegerField(
        source='attendances.count',
        read_only=True
    )
    average_rating = serializers.SerializerMethodField()
    popularity_score = serializers.SerializerMethodField()
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = [
            'id', 'name', 'description', 'type', 'start_date', 'end_date',
            'location', 'village', 'main_language', 'main_ethnic_group',
            'traditional_foods', 'main_activities', 'is_annual', 'website',
            'added_by', 'created_at', 'updated_at', 'media', 'facts',
            'comments', 'attendances_count', 'average_rating', 'popularity_score'
        ]
        read_only_fields = ['added_by', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        return obj.average_rating

    def get_popularity_score(self, obj):
        return obj.popularity_score

    def get_added_by(self, obj):
        if obj.added_by:
            return {
                'id': obj.added_by.id,
                'username': obj.added_by.username,
                'role': obj.added_by.role
            }
        return None