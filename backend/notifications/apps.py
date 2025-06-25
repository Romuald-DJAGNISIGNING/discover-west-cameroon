from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = 'Notifications'
    label = 'notifications'

    def ready(self):
        import notifications.signals  # Ensures signals like auto-send on event load when app is ready

