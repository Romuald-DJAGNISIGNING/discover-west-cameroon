from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Village, VillageImage, VillageComment

User = get_user_model()

class VillageImageSerializer(serializers.ModelSerializer):
    village = serializers.PrimaryKeyRelatedField(queryset=Village.objects.all(), required=False)
    
    class Meta:
        model = VillageImage
        fields = "__all__"
        extra_kwargs = {
            'image': {
                'required': True,
                'allow_null': False,
                'use_url': True
            }
        }

class VillageCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    village = serializers.PrimaryKeyRelatedField(queryset=Village.objects.all(), required=False)
    user_username = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = VillageComment
        fields = "__all__"

class VillageSerializer(serializers.ModelSerializer):
    images = VillageImageSerializer(many=True, read_only=True)
    comments = VillageCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Village
        fields = "__all__"