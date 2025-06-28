from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer, UserProfileUpdateSerializer
)
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

# Registration endpoint (overrides dj_rest_auth)
class CustomRegisterView(RegisterView):
    serializer_class = UserRegistrationSerializer

# Login endpoint (overrides dj_rest_auth)
class CustomLoginView(LoginView):
    serializer_class = UserLoginSerializer

# User profile view (GET current user)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Update profile view (PATCH/PUT)
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

# List all users (admin/staff only)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]