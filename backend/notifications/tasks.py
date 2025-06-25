from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@shared_task
def send_html_email_task(subject, recipient_email, template_name, context={}, from_email=None):
    """
    Sends an HTML email using a template.
    """
    from_email = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@discoverwestcameroon.com')
    try:
        html_content = render_to_string(template_name, context)
        text_content = context.get('message') or 'You have a new message.'

        email = EmailMultiAlternatives(subject, text_content, from_email, [recipient_email])
        email.attach_alternative(html_content, "text/html")
        email.send()
        return f"Email sent to {recipient_email}"
    except Exception as e:
        return f"Email send failed: {str(e)}"

@shared_task
def create_in_app_notification_task(user_id, title, message, notification_type='info', link=None):
    """
    Creates an in-app notification for a user.
    """
    try:
        user = User.objects.get(pk=user_id)
        Notification.objects.create(
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link or '',
            created_at=timezone.now()
        )
        return f"Notification created for {user.username}"
    except User.DoesNotExist:
        return f"User with ID {user_id} not found."
    except Exception as e:
        return f"Notification error: {str(e)}"

@shared_task
def notify_user(
    user_id,
    subject,
    message,
    html_template=None,
    context={},
    in_app_title=None,
    in_app_type="info",
    link=None
):
    """
    Unified notification: email + in-app.
    """
    try:
        user = User.objects.get(pk=user_id)

        # Email
        if html_template:
            send_html_email_task.delay(
                subject=subject,
                recipient_email=user.email,
                template_name=html_template,
                context=context
            )
        else:
            send_html_email_task.delay(
                subject=subject,
                recipient_email=user.email,
                template_name='emails/default.html',
                context={'message': message}
            )

        # In-App
        create_in_app_notification_task.delay(
            user_id=user_id,
            title=in_app_title or subject,
            message=message,
            notification_type=in_app_type,
            link=link
        )
        return f"Notification queued for user {user.username}"

    except User.DoesNotExist:
        return f"User with ID {user_id} does not exist."
