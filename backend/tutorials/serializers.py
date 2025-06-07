# tutorials/serializers.py

from rest_framework import serializers
from .models import Tutorial, TutorialStep

class TutorialStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialStep
        fields = ['id', 'title', 'content', 'step_number']


class TutorialSerializer(serializers.ModelSerializer):
    steps = TutorialStepSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model = Tutorial
        fields = ['id', 'author', 'author_name', 'title', 'description', 'video_url', 'created_at', 'updated_at', 'steps']
        read_only_fields = ['author', 'created_at', 'updated_at']
