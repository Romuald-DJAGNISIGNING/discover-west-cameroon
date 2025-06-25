from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tutorial
from notifications.tasks import notify_user
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Tutorial)
def notify_admin_new_tutorial(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            notify_user.delay(
                user_id=admin.id,
                subject="New Tutorial Submitted",
                message=f"{instance.author} submitted a new tutorial: {instance.title}",
                in_app_title="New Tutorial Submission",
                in_app_type="info",
                link="/admin/tutorials/"
            )
