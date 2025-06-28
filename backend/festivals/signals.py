# Notify users when a festival is added, attended, or feedback given
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Festival, FestivalAttendance, FestivalFeedback

def in_app_notify(user, subject, message):
    print(f"[IN-APP NOTIFY] To: {user.username} | {subject} | {message}")

@receiver(post_save, sender=Festival)
def notify_festival_added(sender, instance, created, **kwargs):
    if created and instance.added_by:
        subject = f"Festival Added: {instance.name}"
        message = f"Thank you for contributing the festival '{instance.name}'!"
        in_app_notify(instance.added_by, subject, message)

@receiver(post_save, sender=FestivalAttendance)
def notify_festival_attendance(sender, instance, created, **kwargs):
    if created:
        subject = f"Festival Attendance: {instance.festival.name}"
        message = f"You have registered to attend '{instance.festival.name}'."
        in_app_notify(instance.user, subject, message)
        # Notify the booked tutor/guide if any
        if instance.booked_tutor_guide:
            in_app_notify(instance.booked_tutor_guide, "You were booked!", f"{instance.user.username} booked you for {instance.festival.name}.")

@receiver(post_save, sender=FestivalFeedback)
def notify_feedback_given(sender, instance, created, **kwargs):
    if created:
        subject = f"Festival Feedback: {instance.attendance.festival.name}"
        message = f"Thank you for your feedback and rating on {instance.attendance.festival.name}!"
        in_app_notify(instance.attendance.user, subject, message)