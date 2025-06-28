import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import PaymentTransaction
from django.utils import timezone
from .backends import STRIPE_API_KEY
import os
import stripe

# Stripe Webhook Example
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'charge.succeeded':
        charge = event['data']['object']
        tx = PaymentTransaction.objects.filter(external_id=charge['id']).first()
        if tx:
            tx.status = "success"
            tx.updated = timezone.now()
            tx.save()
    return HttpResponse(status=200)

# PayPal Webhook Example
@csrf_exempt
def paypal_webhook(request):
    data = json.loads(request.body)
    resource = data.get("resource", {})
    event_type = data.get("event_type", "")
    
    if event_type == "CHECKOUT.ORDER.APPROVED":
        tx = PaymentTransaction.objects.filter(external_id=resource.get("id")).first()
        if tx:
            tx.status = "success"
            tx.updated = timezone.now()
            tx.save()
    elif event_type == "PAYMENT.CAPTURE.DENIED":
        tx = PaymentTransaction.objects.filter(external_id=resource.get("id")).first()
        if tx:
            tx.status = "failed"
            tx.updated = timezone.now()
            tx.save()
    return HttpResponse(status=200)

# MTN Mobile Money Webhook Example (Callback URL)
@csrf_exempt
def mtn_webhook(request):
    data = json.loads(request.body)
    reference = data.get("externalId") or data.get("referenceId")
    status_str = data.get("status", "").upper()
    
    tx = PaymentTransaction.objects.filter(reference=reference).first()
    if tx:
        if status_str == "SUCCESSFUL":
            tx.status = "success"
        elif status_str == "FAILED":
            tx.status = "failed"
        elif status_str == "PENDING":
            tx.status = "pending"
        tx.updated = timezone.now()
        tx.save()
    return HttpResponse(status=200)

# Orange Money Webhook Example (Notification URL)
@csrf_exempt
def orange_webhook(request):
    data = json.loads(request.body)
    order_id = data.get("order_id")
    status_str = data.get("status", "").upper()
    
    tx = PaymentTransaction.objects.filter(reference=order_id).first()
    if tx:
        if status_str in ["PAID", "SUCCESS", "SUCCESSFUL"]:
            tx.status = "success"
        elif status_str in ["CANCELLED", "FAILED"]:
            tx.status = "failed"
        elif status_str == "PENDING":
            tx.status = "pending"
        tx.updated = timezone.now()
        tx.save()
    return HttpResponse(status=200)