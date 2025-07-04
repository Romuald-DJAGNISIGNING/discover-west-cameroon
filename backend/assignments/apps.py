from django.apps import AppConfig

class AssignmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignments'
    verbose_name = 'Assignments Management'
    label = 'assignments'

    def ready(self):
        import assignments.signals
