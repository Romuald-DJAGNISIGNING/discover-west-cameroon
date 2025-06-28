from .settings import *  # Import all regular settings

# Override settings for testing
PAYMENT_BACKENDS = {
    'mtn': 'payments.backends.MTNMobileMoneyBackend',
    'orange': 'payments.backends.OrangeMoneyBackend',
    'card': 'payments.backends.StripeBackend',
    'paypal': 'payments.backends.PayPalBackend',
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use faster password hasher for tests
AUTH_PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use SQLite in-memory database for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable logging during tests
LOGGING_CONFIG = None

DEBUG = True  # Ensure debug is on for tests
SECRET_KEY = 'fake-key-for-testing'  # Add a test secret key

# Disable external API calls during tests
CINETPAY_API_KEY = ''
CINETPAY_SITE_ID = ''
ORANGE_MONEY_API_KEY = ''
MTN_MOMO_API_KEY = ''
PAYPAL_CLIENT_ID = ''
PAYPAL_SECRET = ''
STRIPE_API_KEY = ''

# Disable email sending during tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable Celery during tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
