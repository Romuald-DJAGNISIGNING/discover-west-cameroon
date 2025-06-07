from rest_framework import serializers
from .models import Report
from users.models import CustomUser
from users.serializers import CustomUserSerializer

class ReportSerializer(serializers.ModelSerializer):
    reporter = CustomUserSerializer(read_only=True)
    reported_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Report
        fields = [
            'id',
            'reporter',
            'reported_user',
            'reason',
            'description',
            'status',
            'created_at',
            'reviewed_at'
        ]
        read_only_fields = ['status', 'created_at', 'reviewed_at']
