from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, BookingViewSet, PayoutViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'payouts', PayoutViewSet, basename='payout')

urlpatterns = [
    path('', include(router.urls)),
]
