from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
import os


# Choices
GENDER_CHOICES = (
    ('male', _("Male")),
    ('female', _("Female")),
    ('other', _("Other")),
)

USER_ROLE_CHOICES = (
    ('student', _("Student")),
    ('tutor', _("Tutor")),
    ('guide', _("Touristic Guide")),
)

def validate_gmail(value):
    if not value.lower().endswith('@gmail.com'):
        raise ValidationError(_("Only Gmail addresses are allowed."))

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))
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
    username = models.CharField(_("Username"), max_length=150, unique=True)
    full_name = models.CharField(_("Full Name"), max_length=255)
    email = models.EmailField(_("Email Address"), unique=True, validators=[validate_gmail])
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+237612345678'. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(_("Phone Number"), validators=[phone_regex], max_length=17, unique=True)
    
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to='profile_pics/',
        default=os.path.join('profile_pics', getattr(settings, 'DEFAULT_PROFILE_PIC', 'default.jpg'))
    )
    id_card = models.ImageField(_("ID Card"), upload_to='id_cards/', blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=10, choices=GENDER_CHOICES)
    role = models.CharField(_("Role"), max_length=50, choices=USER_ROLE_CHOICES)
    location = models.CharField(_("Location"), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'full_name']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.username

