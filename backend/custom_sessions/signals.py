
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomSession
from notifications.tasks import notify_user

@receiver(post_save, sender=CustomSession)
def session_completed_notification(sender, instance, created, **kwargs):
    if instance.status == "completed":
        notify_user.delay(
            user_id=instance.user.id,
            subject="Session Completed",
            message=f"Your session with ID {instance.id} has ended.",
            html_template="emails/session_completed.html",
            context={"session": instance},
            in_app_title="Session Completed ✅",
            in_app_type="info",
            link=f"/dashboard/{instance.user.role}/sessions/"
        )
