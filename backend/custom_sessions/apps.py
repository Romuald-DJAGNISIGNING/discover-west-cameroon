

from django.apps import AppConfig

class CustomSessionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_sessions'
    verbose_name = "Custom Sessions"
    label = 'custom_sessions'
