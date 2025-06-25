from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SupportReply  # Direct import to avoid get_model issues
from notifications.tasks import notify_user

@receiver(post_save, sender=SupportReply)
def support_reply_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.ticket.user

        notify_user.delay(
            user_id=user.id,
            subject="Support Reply",
            message=f"New reply: {instance.message[:80]}...",
            html_template="emails/support_reply.html",
            context={"reply": instance},
            in_app_title="Support Reply",
            in_app_type="info",
            link=f"/dashboard/{user.role}/support/{instance.ticket.id}/"
        )
