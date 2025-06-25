from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.tasks import notify_user

def get_booking_model():
    from django.apps import apps
    return apps.get_model('payments', 'Booking')

@receiver(post_save, sender=None)
def booking_created_notification(sender, instance, created, **kwargs):
    Booking = get_booking_model()
    if sender is Booking and created:
        learner = instance.learner
        guide_or_tutor = getattr(instance, 'tutor', None) or getattr(instance, 'guide', None)

        notify_user.delay(
            user_id=learner.id,
            subject="Booking Confirmed",
            message=f"Your booking with {guide_or_tutor.get_full_name()} is confirmed.",
            html_template="emails/booking_confirmation.html",
            context={"booking": instance},
            in_app_title="Booking Successful",
            in_app_type="success",
            link=f"/dashboard/learner/bookings/{instance.id}/"
        )
