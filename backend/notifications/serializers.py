from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    actor_username = serializers.CharField(source='actor.username', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'recipient_username',
            'actor',
            'actor_username',
            'verb',
            'target',
            'description',
            'type',
            'is_read',
            'timestamp',
        ]
        read_only_fields = ['id', 'recipient', 'timestamp']
