from rest_framework import serializers
from .models import SupportTicket

class SupportTicketSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = SupportTicket
        fields = [
            'id',
            'user',
            'user_email',
            'subject',
            'message',
            'category',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_email', 'created_at', 'updated_at']
