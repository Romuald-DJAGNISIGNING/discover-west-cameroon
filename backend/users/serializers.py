

from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'username', 'full_name', 'phone_number', 'profile_picture',
            'id_card', 'gender', 'role', 'location', 'is_active', 'is_staff', 'date_joined'
        )
        read_only_fields = ('is_active', 'is_staff', 'date_joined')


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    role = serializers.ChoiceField(choices=[('student', 'Student'), ('tutor', 'Tutor'), ('guide', 'Touristic Guide')])
    location = serializers.CharField(required=False, allow_blank=True)
    id_card = serializers.ImageField(required=True)
    profile_picture = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'username': self.validated_data.get('username', ''),
            'full_name': self.validated_data.get('full_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'gender': self.validated_data.get('gender', ''),
            'role': self.validated_data.get('role', ''),
            'location': self.validated_data.get('location', ''),
            'id_card': self.validated_data.get('id_card'),
            'profile_picture': self.validated_data.get('profile_picture'),
        })
        return data


class CustomLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email_or_phone'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials.")
