from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentMethodViewSet,
    PaymentTransactionViewSet,
    PaymentReceiptViewSet,
    BookingViewSet,
    PayoutViewSet,
)
from .webhooks import (
    stripe_webhook,
    paypal_webhook,
    mtn_webhook,
    orange_webhook,
)

router = DefaultRouter()
router.register(r'methods', PaymentMethodViewSet, basename="paymentmethod")
router.register(r'bookings', BookingViewSet, basename="booking")
router.register(r'transactions', PaymentTransactionViewSet, basename="paymenttransaction")
router.register(r'receipts', PaymentReceiptViewSet, basename="paymentreceipt")
router.register(r'payouts', PayoutViewSet, basename="payout")

urlpatterns = [
    path('', include(router.urls)),
    
    # Payment actions
    path('transactions/<int:transaction_id>/initiate/', 
         PaymentTransactionViewSet.as_view({'post': 'initiate'}), 
         name='paymenttransaction-initiate'),
    path('transactions/<int:transaction_id>/cancel/', 
         PaymentTransactionViewSet.as_view({'post': 'cancel'}), 
         name='paymenttransaction-cancel'),

    # Webhooks
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('webhooks/paypal/', paypal_webhook, name='paypal-webhook'),
    path('webhooks/mtn/', mtn_webhook, name='mtn-webhook'),
    path('webhooks/orange/', orange_webhook, name='orange-webhook'),
]