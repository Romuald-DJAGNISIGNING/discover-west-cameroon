

from rest_framework import serializers
from .models import CustomSession
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'full_name', 'role']

class CustomSessionSerializer(serializers.ModelSerializer):
    tutor_or_guide = CustomUserSerializer(read_only=True)
    student_or_visitor = CustomUserSerializer(read_only=True)
    tutor_or_guide_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='tutor_or_guide', write_only=True
    )
    student_or_visitor_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='student_or_visitor', write_only=True
    )

    class Meta:
        model = CustomSession
        fields = [
            'id', 'session_type', 'topic_or_location', 'scheduled_time',
            'duration_minutes', 'location', 'notes', 'is_confirmed',
            'tutor_or_guide', 'student_or_visitor',
            'tutor_or_guide_id', 'student_or_visitor_id',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_confirmed']
