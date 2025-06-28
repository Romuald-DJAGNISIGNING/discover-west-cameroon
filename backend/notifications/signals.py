from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from .utils import send_sms, send_email

User = get_user_model()

@receiver(post_save, sender=Notification)
def handle_notification_delivery(sender, instance, created, **kwargs):
    if created and instance.notification_type in ["email", "sms"]:
        # Decide delivery method and send
        if instance.notification_type == "sms":
            phone = getattr(instance.recipient, "phone_number", None)
            # You must have phone_number on user profile
            if phone:
                try:
                    send_sms(phone, instance.message)
                    instance.delivery_status = "sent"
                except Exception as e:
                    instance.delivery_status = "failed"
            else:
                instance.delivery_status = "failed"
        elif instance.notification_type == "email":
            email = getattr(instance.recipient, "email", None)
            if email:
                try:
                    send_email(instance.title, instance.message, email)
                    instance.delivery_status = "sent"
                except Exception as e:
                    instance.delivery_status = "failed"
            else:
                instance.delivery_status = "failed"
        instance.save(update_fields=["delivery_status"])