

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notifications.tasks import notify_user

User = get_user_model()

@receiver(post_save, sender=User)
def welcome_new_user(sender, instance, created, **kwargs):
    if created:
        notify_user.delay(
            user_id=User.id,
            subject="Welcome to Discover West Cameroon",
            message="Thanks for joining! Explore festivals, book guides, and more.",
            html_template="emails/welcome_email.html",
            context={"user": instance},
            in_app_title="Welcome 🎉",
            in_app_type="info",
            link=f"/dashboard/{instance.role}/"
        )
