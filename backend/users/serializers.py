from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

User = get_user_model()

class UserRegistrationSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    role = serializers.ChoiceField(choices=[('learner', 'Learner'),('visitor', 'Visitor'), ('tutor', 'Tutor'), ('guide', 'Touristic Guide')])
    location = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    id_card = serializers.ImageField(required=False, allow_null=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'full_name': self.validated_data.get('full_name', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'password1': self.validated_data.get('password1', ''),
            'gender': self.validated_data.get('gender', ''),
            'role': self.validated_data.get('role', ''),
            'location': self.validated_data.get('location', ''),
            'profile_picture': self.validated_data.get('profile_picture', None),
            'id_card': self.validated_data.get('id_card', None),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.full_name = self.cleaned_data.get('full_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.gender = self.cleaned_data.get('gender')
        user.role = self.cleaned_data.get('role')
        user.location = self.cleaned_data.get('location')
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            user.profile_picture = profile_picture
        id_card = self.cleaned_data.get('id_card')
        if id_card:
            user.id_card = id_card
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'email', 'phone_number', 'profile_picture', 'id_card',
            'gender', 'role', 'location', 'is_active', 'is_staff', 'date_joined'
        ]
        read_only_fields = ['is_active', 'is_staff', 'date_joined']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'profile_picture', 'gender', 'role', 'location', 'id_card']