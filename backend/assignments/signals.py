from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment, AssignmentSubmission
from django.core.mail import send_mail
from django.conf import settings

# --- EMAIL Notification Utility ---
def notify_user_email(user, subject, message):
    if user.email:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

# --- IN-APP Notification Utility ---
def in_app_notify(user, subject, message):
    # Replace this with your actual in-app notification logic
    # Example using django-notifications-hq:
    # from notifications.signals import notify
    # notify.send(sender=None, recipient=user, verb=subject, description=message)
    # Or with your custom Notification model:
    # Notification.objects.create(user=user, subject=subject, message=message)
    print(f"[IN-APP NOTIFY] To: {user.username} | {subject} | {message}")

# --- ASSIGNMENT CREATED: Notify Learner ---
@receiver(post_save, sender=Assignment)
def notify_learner_assignment_created(sender, instance, created, **kwargs):
    if created:
        learner = instance.assigned_to
        subject = f"New Assignment: {instance.title}"
        message = (
            f"Hello {learner.username},\n\n"
            f"You have received a new assignment: '{instance.title}'.\n"
            f"Description: {instance.description}\n"
            f"Due Date: {instance.due_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Assigned by: {instance.assigned_by.username}\n\n"
            f"Please log in to your dashboard to view and submit your work."
        )
        notify_user_email(learner, subject, message)
        in_app_notify(learner, subject, message)

# --- SUBMISSION CREATED: Notify Tutor/Guide ---
@receiver(post_save, sender=AssignmentSubmission)
def notify_tutor_submission_created(sender, instance, created, **kwargs):
    if created:
        tutor = instance.assignment.assigned_by
        subject = f"New Submission for: {instance.assignment.title}"
        message = (
            f"Hello {tutor.username},\n\n"
            f"{instance.student.username} has submitted work for the assignment: '{instance.assignment.title}'.\n"
            f"Please review and grade the submission."
        )
        notify_user_email(tutor, subject, message)
        in_app_notify(tutor, subject, message)

# --- SUBMISSION GRADED: Notify Learner ---
@receiver(post_save, sender=AssignmentSubmission)
def notify_learner_graded(sender, instance, **kwargs):
    # Notify learner if their submission has just been graded
    if instance.grade is not None and instance.feedback:
        learner = instance.student
        subject = f"Assignment Graded: {instance.assignment.title}"
        message = (
            f"Hello {learner.username},\n\n"
            f"Your submission for '{instance.assignment.title}' has been graded.\n"
            f"Grade: {instance.grade}\n"
            f"Feedback: {instance.feedback}\n\n"
            f"Check your dashboard for more details."
        )
        notify_user_email(learner, subject, message)
        in_app_notify(learner, subject, message)