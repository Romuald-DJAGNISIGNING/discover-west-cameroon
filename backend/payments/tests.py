

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Payment

User = get_user_model()

class PaymentTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@gmail.com",
            username="testuser",
            phone_number="+237612345678",
            password="strongpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_payment(self):
        url = reverse('payment-list')
        data = {
            "amount": "5000.00",
            "payment_method": "MTN Mobile Money",
            "transaction_id": "TXN1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get().user, self.user)

    def test_get_payments(self):
        Payment.objects.create(
            user=self.user,
            amount=5000.00,
            payment_method="Orange Money",
            transaction_id="TXN9876543210"
        )
        url = reverse('payment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
