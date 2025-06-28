from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import PaymentTransaction
from .backends import process_payment, check_payment_status

class InitiatePaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, transaction_id):
        try:
            transaction = PaymentTransaction.objects.get(id=transaction_id, user=request.user)
        except PaymentTransaction.DoesNotExist:
            return Response({"detail": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = process_payment(transaction)
            return Response({"detail": "Payment initiated.", "result": result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Payment initiation failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class CheckPaymentStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, transaction_id):
        try:
            transaction = PaymentTransaction.objects.get(id=transaction_id, user=request.user)
        except PaymentTransaction.DoesNotExist:
            return Response({"detail": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            status_result = check_payment_status(transaction)
            return Response({"status": status_result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Status check failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)