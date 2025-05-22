from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
import os

# Choices
GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

USER_ROLE_CHOICES = (
    ('student', 'Student'),
    ('tutor', 'Tutor'),
    ('guide', 'Touristic Guide'),
)

def validate_gmail(value):
    if not value.lower().endswith('@gmail.com'):
        raise ValidationError("Only Gmail addresses are allowed.")

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, phone_number, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[validate_gmail])
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+237612345678'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default=os.path.join('profile_pics', getattr(settings, 'DEFAULT_PROFILE_PIC', 'default.jpg'))
    )
    id_card = models.ImageField(upload_to='id_cards/')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)  # For Tour Guides or Student's home

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'full_name']

    def __str__(self):
        return self.email
