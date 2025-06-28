from django.urls import path
from .webhooks import stripe_webhook, paypal_webhook, mtn_webhook, orange_webhook

urlpatterns = [
    path('stripe/', stripe_webhook, name='stripe-webhook'),
    path('paypal/', paypal_webhook, name='paypal-webhook'),
    path('mtn/', mtn_webhook, name='mtn-webhook'),
    path('orange/', orange_webhook, name='orange-webhook'),
]