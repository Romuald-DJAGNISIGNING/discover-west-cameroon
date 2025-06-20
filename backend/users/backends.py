# users/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneEmailUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(phone_number=username)
            except CustomUser.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
