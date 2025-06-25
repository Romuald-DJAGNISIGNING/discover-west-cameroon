from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.apps import apps

from .tasks import notify_user  # Use the actual function name

User = get_user_model()

def get_booking_model():
    return apps.get_model('payments', 'Booking')

def get_payment_model():
    return apps.get_model('payments', 'Payment')

def get_support_reply_model():
    # Fix: Use SupportReply, not SupportMessage
    return apps.get_model('support', 'SupportReply')

@receiver(post_save, sender=None)
def notify_on_booking(sender, instance, created, **kwargs):
    Booking = get_booking_model()
    if sender is Booking and created:
        user = getattr(instance, 'user', None)
        service_provider = getattr(instance, 'tutor', None) or getattr(instance, 'guide', None)
        if service_provider:
            notify_user(
                recipient_id=service_provider.id,
                actor_id=user.id if user else None,
                verb="You have a new booking",
                target=str(instance),
                type="booking"
            )

@receiver(post_save, sender=None)
def notify_admin_on_payment(sender, instance, created, **kwargs):
    Payment = get_payment_model()
    if sender is Payment and created:
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            notify_user(
                recipient_id=admin_user.id,
                actor_id=instance.payer.id,
                verb=f"made a payment of {instance.amount} XAF",
                target=str(instance),
                type="payment"
            )

@receiver(post_save, sender=None)
def notify_user_on_support_reply(sender, instance, created, **kwargs):
    SupportReply = get_support_reply_model()
    if sender is SupportReply and created:
        ticket = getattr(instance, 'ticket', None)
        user = getattr(ticket, 'user', None) if ticket else None
        if user:
            notify_user(
                recipient_id=user.id,
                actor_id=None,  # Admin or system
                verb="replied to your support request",
                target=str(instance),
                type="support"
            )
