from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    stars = serializers.SerializerMethodField()
    
    def get_stars(self, obj):
        return "★" * obj.rating + "☆" * (5 - obj.rating)
    
    def validate(self, data):
        # Check for existing review by this user for the same target
        user = self.context['request'].user
        attraction = data.get('attraction')
        village = data.get('village')
        festival = data.get('festival')
        hosting_family = data.get('hosting_family')
        social_immersion = data.get('social_immersion')
        
        if attraction:
            if Review.objects.filter(user=user, attraction=attraction).exists():
                raise serializers.ValidationError("You have already reviewed this attraction.")
        elif village:
            if Review.objects.filter(user=user, village=village).exists():
                raise serializers.ValidationError("You have already reviewed this village.")
        elif festival:
            if Review.objects.filter(user=user, festival=festival).exists():
                raise serializers.ValidationError("You have already reviewed this festival.")
        elif hosting_family:
            if Review.objects.filter(user=user, hosting_family=hosting_family).exists():
                raise serializers.ValidationError("You have already reviewed this hosting family.")
        elif social_immersion:
            if Review.objects.filter(user=user, social_immersion=social_immersion).exists():
                raise serializers.ValidationError("You have already reviewed this social immersion.")
        
        return data
    
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ('user', 'created_at', 'updated_at')