from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Booking, Payment, Payout
from notifications.utils import create_notification
from notifications.tasks import notify_user
from .utils import mark_tutorial_payment_complete


@receiver(pre_save, sender=Payment)
def prevent_duplicate_notifications(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Payment.objects.get(pk=instance.pk)
            instance._send_payment_notification = previous.status != instance.status
        except Payment.DoesNotExist:
            instance._send_payment_notification = True
    else:
        instance._send_payment_notification = True


@receiver(post_save, sender=Payment)
def payment_notification(sender, instance, created, **kwargs):
    should_notify = getattr(instance, "_send_payment_notification", True)
    if (created or should_notify) and instance.status == "completed":
        user = instance.payer

        # Send in-app and email notification (retry enabled in Celery)
        notify_user.apply_async(
            kwargs={
                'user_id': user.id,
                'subject': "Payment Successful",
                'message': f"Your payment of {instance.amount} FCFA has been received.",
                'html_template': "emails/payment_received.html",
                'context': {"payment": instance},
                'in_app_title': "Payment Confirmed",
                'in_app_type': "success",
                'link': f"/dashboard/{user.role}/payments/"
            },
            retry=True,
            retry_policy={
                'max_retries': 3,
                'interval_start': 0,
                'interval_step': 10,
                'interval_max': 30,
            }
        )

        # Grant tutorial access if it's a tutorial payment
        mark_tutorial_payment_complete(instance)


@receiver(post_save, sender=Booking)
def notify_admin_on_booking(sender, instance, created, **kwargs):
    if created:
        # Notify admin in-app
        create_notification(
            recipient=None,
            title="New Booking Created",
            message=f"{instance.user} booked {instance.tutor or instance.guide} for {instance.booking_type}."
        )

        # Email alert
        send_mail(
            subject="New Booking Alert",
            message=f"A new booking was made by {instance.user}.\nDetails: {instance}",
            from_email="admin@discoverwestcameroon.com",
            recipient_list=["admin@discoverwestcameroon.com"],
            fail_silently=True,
        )


@receiver(post_save, sender=Payout)
def payout_notification(sender, instance, **kwargs):
    if instance.status == "paid":
        notify_user.apply_async(
            kwargs={
                'user_id': instance.guide_or_tutor.id,
                'subject': "Payout Received",
                'message': f"You've received a payout of {instance.amount} FCFA.",
                'html_template': "emails/payout_received.html",
                'context': {"payout": instance},
                'in_app_title': "Payout Confirmed 💰",
                'in_app_type': "success",
                'link': f"/dashboard/{instance.guide_or_tutor.role}/payouts/"
            },
            retry=True,
            retry_policy={
                'max_retries': 3,
                'interval_start': 0,
                'interval_step': 10,
                'interval_max': 30,
            }
        )
