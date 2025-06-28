import requests
import uuid
import os
from decimal import Decimal
from django.conf import settings

# Load secrets from environment or settings
MTN_MOMO_API_USER = os.getenv("MTN_MOMO_API_USER", getattr(settings, "MTN_MOMO_API_USER", ""))
MTN_MOMO_API_KEY = os.getenv("MTN_MOMO_API_KEY", getattr(settings, "MTN_MOMO_API_KEY", ""))
MTN_MOMO_SUBSCRIPTION_KEY = os.getenv("MTN_MOMO_SUBSCRIPTION_KEY", getattr(settings, "MTN_MOMO_SUBSCRIPTION_KEY", ""))
MTN_MOMO_ENV = os.getenv("MTN_MOMO_ENV", getattr(settings, "MTN_MOMO_ENV", "sandbox"))
MTN_MOMO_BASE_URL = os.getenv("MTN_MOMO_BASE_URL", getattr(settings, "MTN_MOMO_BASE_URL", "https://sandbox.momodeveloper.mtn.com"))

ORANGE_MONEY_API_KEY = os.getenv("ORANGE_MONEY_API_KEY", getattr(settings, "ORANGE_MONEY_API_KEY", ""))
ORANGE_MONEY_API_SECRET = os.getenv("ORANGE_MONEY_API_SECRET", getattr(settings, "ORANGE_MONEY_API_SECRET", ""))
ORANGE_MONEY_BASE_URL = os.getenv("ORANGE_MONEY_BASE_URL", getattr(settings, "ORANGE_MONEY_BASE_URL", "https://api.orange.com"))

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", getattr(settings, "STRIPE_API_KEY", ""))
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", getattr(settings, "PAYPAL_CLIENT_ID", ""))
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", getattr(settings, "PAYPAL_CLIENT_SECRET", ""))
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL", getattr(settings, "PAYPAL_BASE_URL", "https://api.sandbox.paypal.com"))


class MTNMobileMoneyBackend:
    """
    Backend for MTN Mobile Money Cameroon.
    Docs: https://momodeveloper.mtn.com/docs/services/collection/operations
    """

    def get_access_token(self):
        url = f"{MTN_MOMO_BASE_URL}/collection/token/"
        headers = {
            "Ocp-Apim-Subscription-Key": MTN_MOMO_SUBSCRIPTION_KEY
        }
        resp = requests.post(url, auth=(MTN_MOMO_API_USER, MTN_MOMO_API_KEY), headers=headers)
        resp.raise_for_status()
        return resp.json()["access_token"]

    def process_payment(self, transaction):
        access_token = self.get_access_token()
        url = f"{MTN_MOMO_BASE_URL}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Reference-Id": transaction.reference,
            "X-Target-Environment": MTN_MOMO_ENV,
            "Ocp-Apim-Subscription-Key": MTN_MOMO_SUBSCRIPTION_KEY,
            "Content-Type": "application/json",
        }
        body = {
            "amount": str(transaction.amount),
            "currency": transaction.currency,
            "externalId": transaction.reference,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": transaction.metadata.get("payer_phone"),  # Must be set
            },
            "payerMessage": transaction.description or "Payment",
            "payeeNote": "Discover West Cameroon"
        }
        resp = requests.post(url, json=body, headers=headers)
        resp.raise_for_status()
        return resp.status_code == 202  # 202 Accepted means request initiated

    def check_status(self, transaction):
        access_token = self.get_access_token()
        url = f"{MTN_MOMO_BASE_URL}/collection/v1_0/requesttopay/{transaction.reference}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": MTN_MOMO_ENV,
            "Ocp-Apim-Subscription-Key": MTN_MOMO_SUBSCRIPTION_KEY,
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        status = resp.json().get("status")
        return status  # "PENDING", "SUCCESSFUL", "FAILED"


class OrangeMoneyBackend:
    """
    Backend for Orange Money Cameroon.
    Docs: https://developer.orange.com/apis/orange-money-web-payment-cm/
    """

    def get_access_token(self):
        url = f"{ORANGE_MONEY_BASE_URL}/oauth/v2/token"
        headers = {"Authorization": f"Basic {ORANGE_MONEY_API_KEY}:{ORANGE_MONEY_API_SECRET}"}
        data = {"grant_type": "client_credentials"}
        resp = requests.post(url, headers=headers, data=data)
        resp.raise_for_status()
        return resp.json()["access_token"]

    def process_payment(self, transaction):
        access_token = self.get_access_token()
        url = f"{ORANGE_MONEY_BASE_URL}/omcoreapis/1.0.2/mp/init"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "merchant_key": ORANGE_MONEY_API_KEY,
            "currency": transaction.currency,
            "order_id": transaction.reference,
            "amount": str(transaction.amount),
            "return_url": transaction.metadata.get("return_url", "https://yourdomain.com/payment/orange/return/"),
            "cancel_url": transaction.metadata.get("cancel_url", "https://yourdomain.com/payment/orange/cancel/"),
            "notif_url": transaction.metadata.get("notif_url", "https://yourdomain.com/payment/orange/notify/"),
            "lang": "fr"
        }
        resp = requests.post(url, json=body, headers=headers)
        resp.raise_for_status()
        return resp.json()  # Contains payment_url, token, etc.

    def check_status(self, transaction):
        # Orange Money status check is usually via a notification webhook
        # or via querying the order status endpoint if available.
        # Implement as per your Orange account documentation.
        # Return values: "INITIATED", "SUCCESSFUL", "FAILED", "CANCELLED"
        return transaction.status  # Placeholder


class StripeBackend:
    """
    Backend for Credit Card payments via Stripe.
    Docs: https://stripe.com/docs/api
    """
    def __init__(self):
        import stripe
        stripe.api_key = STRIPE_API_KEY
        self.stripe = stripe

    def process_payment(self, transaction):
        # Transaction must have metadata['stripe_token'] set by the frontend
        token = transaction.metadata.get("stripe_token")
        if not token:
            raise ValueError("Missing Stripe token in transaction metadata.")
        charge = self.stripe.Charge.create(
            amount=int(Decimal(transaction.amount) * 100),  # Stripe expects cents
            currency=transaction.currency.lower(),
            description=transaction.description or "Discover West Cameroon Payment",
            source=token
        )
        transaction.external_id = charge.id
        if charge.status == "succeeded":
            transaction.status = "success"
        else:
            transaction.status = "failed"
        transaction.save()
        return charge.status == "succeeded"

    def check_status(self, transaction):
        charge = self.stripe.Charge.retrieve(transaction.external_id)
        return charge.status  # "succeeded", "pending", "failed", etc.


class PayPalBackend:
    """
    Backend for PayPal payments.
    Docs: https://developer.paypal.com/docs/api/overview/
    """
    def get_access_token(self):
        resp = requests.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
            headers={"Accept": "application/json"}
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

    def process_payment(self, transaction):
        access_token = self.get_access_token()
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": transaction.reference,
                "amount": {
                    "currency_code": transaction.currency,
                    "value": str(transaction.amount)
                }
            }],
            "application_context": {
                "return_url": transaction.metadata.get("return_url", "https://yourdomain.com/payment/paypal/return/"),
                "cancel_url": transaction.metadata.get("cancel_url", "https://yourdomain.com/payment/paypal/cancel/")
            }
        }
        resp = requests.post(url, json=body, headers=headers)
        resp.raise_for_status()
        order = resp.json()
        transaction.external_id = order.get("id")
        transaction.save()
        return order  # Contains approval_url, etc.

    def check_status(self, transaction):
        access_token = self.get_access_token()
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{transaction.external_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json().get("status")  # E.g. "COMPLETED", "CREATED", etc.

# Backend registry
PAYMENT_BACKENDS = {
    'mtn': MTNMobileMoneyBackend(),
    'orange': OrangeMoneyBackend(),
    'card': StripeBackend(),
    'paypal': PayPalBackend(),
}

def process_payment(transaction):
    backend = PAYMENT_BACKENDS.get(transaction.method.name)
    if not backend:
        raise ValueError(f"No backend for payment method: {transaction.method.name}")
    return backend.process_payment(transaction)

def check_payment_status(transaction):
    backend = PAYMENT_BACKENDS.get(transaction.method.name)
    if not backend:
        raise ValueError(f"No backend for payment method: {transaction.method.name}")
    return backend.check_status(transaction)