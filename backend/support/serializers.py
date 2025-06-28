from rest_framework import serializers
from .models import SupportTicket, SupportMessage

class SupportMessageSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = SupportMessage
        fields = "__all__"

class SupportTicketSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    assigned_to_username = serializers.CharField(source="assigned_to.username", read_only=True)
    messages = SupportMessageSerializer(many=True, read_only=True)
    class Meta:
        model = SupportTicket
        fields = "__all__"