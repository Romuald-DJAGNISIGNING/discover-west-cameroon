from django.core.mail import send_mail
import requests

def send_sms(phone_number, message):
    # Integrate with real SMS API.
    # Example: requests.post('https://api.smsprovider.com/send', data={...})
    print(f"[SMS] To: {phone_number} | Message: {message}")

def send_email(subject, message, recipient_email):
    send_mail(subject, message, 'no-reply@discoverwestcm.com', [recipient_email])