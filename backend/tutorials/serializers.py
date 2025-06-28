from rest_framework import serializers
from .models import Tutorial, TutorialCategory, TutorialComment

class TutorialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialCategory
        fields = "__all__"

class TutorialCommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = TutorialComment
        fields = ["id", "comment", "created_at", "user", "user_username", "tutorial"]
        read_only_fields = ["id", "created_at", "user", "user_username", "tutorial"]

class TutorialSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    comments = TutorialCommentSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    
    class Meta:
        model = Tutorial
        fields = "__all__"