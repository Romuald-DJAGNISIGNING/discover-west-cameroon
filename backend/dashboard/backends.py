
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardBackend(ModelBackend):
    """
    Custom backend for dashboard-specific authentication or permission checks,
    if needed in the future.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Use default authentication for now
        return super().authenticate(request, username, password, **kwargs)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
