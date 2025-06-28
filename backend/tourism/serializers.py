from rest_framework import serializers
from .models import (
    TouristicAttraction, SocialImmersionExperience, HostingFamilyExperience,
    TourismActivity, TouristFeedback, TouristComment, SharedTouristMedia
)

class SharedTouristMediaSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = SharedTouristMedia
        fields = "__all__"
        extra_kwargs = {
            'user': {'required': False},
            'attraction': {'required': False},
            'immersion': {'required': False},
            'family': {'required': False},
            'image': {'required': False},
            'video': {'required': False},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TouristCommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = TouristComment
        fields = "__all__"
        extra_kwargs = {
            'user': {'required': False},
            'attraction': {'required': False},
            'immersion': {'required': False},
            'family': {'required': False}
        }

class TouristFeedbackSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    stars = serializers.SerializerMethodField()
    
    def get_stars(self, obj):
        return "★" * obj.rating + "☆" * (5 - obj.rating)
    
    class Meta:
        model = TouristFeedback
        fields = "__all__"
        extra_kwargs = {
            'content': {'required': True},
            'rating': {'required': True},
            'user': {'required': False},
            'attraction': {'required': False},
            'immersion': {'required': False},
            'family': {'required': False}
        }

class TourismActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourismActivity
        fields = "__all__"

class HostingFamilyExperienceSerializer(serializers.ModelSerializer):
    feedbacks = TouristFeedbackSerializer(many=True, read_only=True)
    comments = TouristCommentSerializer(many=True, read_only=True)
    shared_media = SharedTouristMediaSerializer(many=True, read_only=True)
    activities = TourismActivitySerializer(many=True, read_only=True)
    class Meta:
        model = HostingFamilyExperience
        fields = "__all__"

class SocialImmersionExperienceSerializer(serializers.ModelSerializer):
    feedbacks = TouristFeedbackSerializer(many=True, read_only=True)
    comments = TouristCommentSerializer(many=True, read_only=True)
    shared_media = SharedTouristMediaSerializer(many=True, read_only=True)
    activities = TourismActivitySerializer(many=True, read_only=True)
    class Meta:
        model = SocialImmersionExperience
        fields = "__all__"

class TouristicAttractionSerializer(serializers.ModelSerializer):
    feedbacks = TouristFeedbackSerializer(many=True, read_only=True)
    comments = TouristCommentSerializer(many=True, read_only=True)
    shared_media = SharedTouristMediaSerializer(many=True, read_only=True)
    activities = TourismActivitySerializer(many=True, read_only=True)
    class Meta:
        model = TouristicAttraction
        fields = "__all__"