from django.core.mail import send_mail
from django.conf import settings
from .models import InAppNotification
import os

def send_email_notification(users, subject, message):
    recipient_list = [u.email for u in users if getattr(u, 'email', None)]
    if recipient_list:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@discovercameroon.com'),
            recipient_list=recipient_list,
            fail_silently=True,
        )

def send_sms_notification(users, message):
    try:
        from twilio.rest import Client
        TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', os.environ.get("TWILIO_ACCOUNT_SID"))
        TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', os.environ.get("TWILIO_AUTH_TOKEN"))
        TWILIO_FROM_NUMBER = getattr(settings, 'TWILIO_FROM_NUMBER', os.environ.get("TWILIO_FROM_NUMBER"))
        if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER):
            return
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for user in users:
            phone_number = getattr(user, 'phone_number', None)
            if phone_number:
                try:
                    client.messages.create(
                        body=message,
                        from_=TWILIO_FROM_NUMBER,
                        to=phone_number
                    )
                except Exception as e:
                    print(f"SMS to {phone_number} failed: {e}")
    except ImportError:
        pass

def send_push_notification(users, message, title="Discover West Cameroon"):
    try:
        from pyfcm import FCMNotification
        FCM_API_KEY = getattr(settings, 'FCM_API_KEY', os.environ.get("FCM_API_KEY"))
        if not FCM_API_KEY:
            return
        push_service = FCMNotification(api_key=FCM_API_KEY)
        for user in users:
            device_token = getattr(user, 'device_token', None)
            if device_token:
                try:
                    push_service.notify_single_device(
                        registration_id=device_token,
                        message_title=title,
                        message_body=message
                    )
                except Exception as e:
                    print(f"Push notification to {device_token} failed: {e}")
    except ImportError:
        pass

def send_inapp_notification(users, message, url=None):
    for user in users:
        InAppNotification.objects.create(
            user=user,
            message=message,
            url=url
        )

def notify_users(users, message, subject="Discover West Cameroon Session Update", url=None,
                 channels=("email", "inapp", "sms", "push")):
    if "email" in channels:
        send_email_notification(users, subject, message)
    if "sms" in channels:
        send_sms_notification(users, message)
    if "push" in channels:
        send_push_notification(users, message, title=subject)
    if "inapp" in channels:
        send_inapp_notification(users, message, url=url)