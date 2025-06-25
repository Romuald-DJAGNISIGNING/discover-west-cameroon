from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Payment, Booking, Payout
from .serializers import PaymentSerializer, BookingSerializer, PayoutSerializer
from .utils import create_payment_for_tutorial

# Fix: Import IsOwnerOrAdmin only if it exists, otherwise define it here
try:
    from users.permissions import IsOwnerOrAdmin
except ImportError:
    from rest_framework.permissions import BasePermission

    class IsOwnerOrAdmin(BasePermission):
        """
        Custom permission to only allow owners of an object or admins to access it.
        """
        def has_object_permission(self, request, view, obj):
            return (
                request.user and 
                (request.user.is_staff or obj == request.user or getattr(obj, 'user', None) == request.user)
            )

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(payer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(payer=self.request.user)

    @action(detail=False, methods=['post'], url_path='make-payment')
    def make_payment(self, request):
        tutorial_id = request.data.get('tutorial_id')
        if not tutorial_id:
            return Response({'detail': 'Tutorial ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        from tutorials.models import Tutorial  # local import to avoid circular import
        try:
            tutorial = Tutorial.objects.get(pk=tutorial_id)
        except Tutorial.DoesNotExist:
            return Response({'detail': 'Tutorial not found.'}, status=status.HTTP_404_NOT_FOUND)

        payment = create_payment_for_tutorial(request.user, tutorial)
        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        # Fix: Use correct field for filtering bookings by user
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        # Fix: Use correct field for saving the user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_as_paid(self, request, pk=None):
        booking = self.get_object()
        booking.is_paid_to_admin = True
        booking.save()
        return Response({'status': 'Booking marked as paid to admin'})


class PayoutViewSet(viewsets.ModelViewSet):
    serializer_class = PayoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payout.objects.all()
        return Payout.objects.filter(guide_or_tutor=user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def trigger_payout(self, request, pk=None):
        payout = self.get_object()
        if payout.status == 'paid':
            return Response({'detail': 'Payout already completed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        payout.status = 'paid'
        payout.save()
        return Response({'status': 'Payout triggered and marked as paid.'})
