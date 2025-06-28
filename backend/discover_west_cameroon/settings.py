import os
from pathlib import Path
from decouple import config, Csv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='localhost,127.0.0.1')

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# CORS Settings
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv(), default='')
    CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='')

# APPLICATIONS
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Auth & Social
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'corsheaders',
    'social_django',

    # Local apps
    'users',
    'custom_sessions',
    'tutorials',
    'villages',
    'support',
    'assignments',
    'quizzes',
    'dashboard',
    'festivals',
    'payments',
    'reports',
    'reviews',
    'tourism',
    'notifications',
]

SITE_ID = 1
AUTH_USER_MODEL = 'users.CustomUser'

# MIDDLEWARE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'discover_west_cameroon.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'discover_west_cameroon.wsgi.application'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# AUTHENTICATION BACKENDS
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.PhoneEmailUsernameBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# SOCIAL AUTH (Google)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_CLIENT_ID', default='')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_CLIENT_SECRET', default='')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default=''),
            'secret': config('GOOGLE_CLIENT_SECRET', default=''),
            'key': ''
        }
    }
}

# Payment Gateways
ORANGE_MONEY_API_KEY = config('ORANGE_MONEY_API_KEY', default='')
MTN_MOMO_API_KEY = config('MTN_MOMO_API_KEY', default='')
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID', default='')
PAYPAL_SECRET = config('PAYPAL_SECRET', default='')
STRIPE_API_KEY = config('STRIPE_API_KEY', default='')

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Africa/Douala'
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
]
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / 'locale']

# STATIC & MEDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT FILES
DEFAULT_PROFILE_PIC = 'default_profile_pic.jpg'
DEFAULT_PROFILE_PICTURE = 'defaults/default_profile.jpg'

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT Settings
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'
JWT_AUTH_SECURE = not DEBUG
JWT_AUTH_HTTPONLY = True
JWT_AUTH_SAMESITE = 'Lax' if DEBUG else 'Strict'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# Authentication URLs
LOGIN_URL = 'rest_login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'rest_login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='no-reply@discoverwestcameroon.com')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# ALLAUTH & ACCOUNT SETTINGS
CCOUNT_LOGIN_METHODS = ['email', 'username']
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_RATE_LIMITS = {
    'login_failed': '5/5m'  # 5 attempts per 5 minutes
}
ACCOUNT_EMAIL_VERIFICATION = config('ACCOUNT_EMAIL_VERIFICATION', default='optional')
ACCOUNT_SESSION_REMEMBER = True

SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False

# REST AUTH
REST_AUTH = {
    'REGISTER_SERIALIZER': 'users.serializers.UserRegistrationSerializer',
    'LOGIN_SERIALIZER': 'users.serializers.UserLoginSerializer',
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer',
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
    'JWT_AUTH_REFRESH_COOKIE': 'refresh',
    'JWT_AUTH_COOKIE': 'access',
    'SESSION_LOGIN': False,
    'OLD_PASSWORD_FIELD_ENABLED': True,
}

# JAZZMIN ADMIN
JAZZMIN_SETTINGS = {
    "site_title": "Discover West Cameroon Admin",
    "site_header": "Discover West Cameroon",
    "site_brand": "Discover West Cameroon",
    "site_logo": "defaults/west_cameroun_logo.png",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to Discover West Cameroon Administration",
    "copyright": "Discover West Cameroon",
    "search_model": ["users.CustomUser", "villages.Village", "festivals.Festival", "tourism.TouristicAttraction"],
    "user_avatar": "profile_picture",
    "topmenu_links": [
        {"name": "Website", "url": "https://discoverwestcameroon.com", "new_window": True},
        {"model": "users.CustomUser"},
        {"model": "villages.Village"},
        {"model": "festivals.Festival"},
        {"model": "tourism.TouristicAttraction"},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "mailto:support@discoverwestcameroon.com"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["auth"],
    "order_with_respect_to": [
        "users", "villages", "festivals", "tourism",
        "reports", "payments", "reviews", "dashboard",
    ],
    "icons": {
        "users": "fas fa-users",
        "villages": "fas fa-map-marker-alt",
        "festivals": "fas fa-drum",
        "tourism": "fas fa-tree",
        "reports": "fas fa-file-alt",
        "payments": "fas fa-credit-card",
        "reviews": "fas fa-star",
        "dashboard": "fas fa-tachometer-alt",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "minty",
    "dark_mode_theme": "darkly",
}