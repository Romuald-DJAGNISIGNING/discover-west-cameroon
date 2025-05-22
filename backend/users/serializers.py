from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
import os

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'email',
            'phone_number',
            'password',
            'confirm_password',
            'profile_picture',
            'id_card',
            'gender',
            'role',
            'location',
        ]

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only Gmail addresses are accepted.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        # Assign default profile picture if not provided
        if not validated_data.get('profile_picture'):
            validated_data['profile_picture'] = os.path.join(
                'profile_pics',
                getattr(settings, 'DEFAULT_PROFILE_PIC', 'default_profile_pic.jpg')
            )

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
