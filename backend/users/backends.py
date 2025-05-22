from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneEmailUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                phone_number=username
            ) if username.isdigit() else User.objects.get(
                email=username
            ) if '@' in username else User.objects.get(
                username=username
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
