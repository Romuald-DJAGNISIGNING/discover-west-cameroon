from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class PhoneEmailUsernameBackend(ModelBackend):
    """
    Custom authentication backend.
    Allows login with email, username, or phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username:
            try:
                if '@' in username:
                    user = UserModel.objects.get(email__iexact=username)
                elif username.isdigit():
                    user = UserModel.objects.get(phone_number=username)
                else:
                    user = UserModel.objects.get(username__iexact=username)
            except UserModel.DoesNotExist:
                return None
            if user and user.check_password(password):
                return user
        return None