from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PaymentTransaction, Payout
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=PaymentTransaction)
def send_payment_notification(sender, instance, created, **kwargs):
    if instance.status == "success":
        Notification.objects.create(
            recipient=instance.user,
            title=f"Payment Successful - {instance.reference}",
            message=f"Your payment of {instance.amount} {instance.currency} for {instance.get_purpose_display()} was successful.",
            notification_type="in_app",
            event_type="payment_success",
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )
    elif instance.status == "failed":
        Notification.objects.create(
            recipient=instance.user,
            title=f"Payment Failed - {instance.reference}",
            message=f"Your payment of {instance.amount} {instance.currency} failed.",
            notification_type="in_app",
            event_type="payment_failed",
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )

@receiver(post_save, sender=Payout)
def send_payout_notification(sender, instance, created, **kwargs):
    if instance.status == "paid":
        Notification.objects.create(
            recipient=instance.guide_or_tutor,
            title=f"Payout Received - {instance.related_booking.id}",
            message=f"You have been paid {instance.amount} XAF for booking #{instance.related_booking.id}.",
            notification_type="in_app",
            event_type="payout_success",
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )