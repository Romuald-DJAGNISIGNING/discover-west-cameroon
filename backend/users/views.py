from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, RegisterSerializer

from django.utils import translation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

User = get_user_model()

# View to get current user info
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

# Base register view for reuse
class BaseRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        role = getattr(self, 'role', None)
        user = serializer.save()
        if role:
            user.role = role
            user.save()
        return user

# Role-based signup views
class RegisterLearnerView(BaseRegisterView):
    role = 'learner'

class RegisterTutorView(BaseRegisterView):
    role = 'tutor'

class RegisterGuideView(BaseRegisterView):
    role = 'guide'

class RegisterVisitorView(BaseRegisterView):
    role = 'visitor'

# Fallback registration (if needed)
class RegisterUserView(BaseRegisterView):
    pass

# List all users (admin only)
class CustomUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CustomUserSerializer

# Get or update current user's data
class CustomUserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

@csrf_exempt
def set_language(request):
    """
    Endpoint to switch language (session or cookie).
    Accepts POST: { 'language': 'en' or 'fr' }
    """
    if request.method == 'POST':
        lang_code = request.POST.get('language')
        next_url = request.POST.get('next', '/')

        if lang_code and lang_code in dict(settings.LANGUAGES).keys():
            if hasattr(request, 'session'):
                request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
            response = JsonResponse({'message': 'Language changed', 'language': lang_code})
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response

        return JsonResponse({'error': 'Invalid language code'}, status=400)

    return JsonResponse({'error': 'POST request required'}, status=405)

# --- Custom Error Message for Unauthorized Access ---

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_auth_guard(request):
    return Response({"message": "Welcome to the dashboard"})
