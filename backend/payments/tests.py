from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import (
    PaymentMethod,
    PaymentTransaction,
    PaymentReceipt,
    Booking,
    Payout,
)
import uuid
from unittest.mock import patch
from django.conf import settings

User = get_user_model()

class PaymentsAppTest(APITestCase):
    def setUp(self):
        settings.TESTING = True  # Add this line for test environment
        
        # Create test users with all required fields
        self.user = User.objects.create_user(
            email='user@test.com',
            username='testuser',
            phone_number='+237600000001',
            password='testpass123',
            full_name='Test User',
            gender='male',
            role='learner'
        )
        self.tutor = User.objects.create_user(
            email='tutor@test.com',
            username='testtutor',
            phone_number='+237600000002',
            password='tutorpass123',
            full_name='Test Tutor',
            gender='female',
            role='tutor'
        )
        self.guide = User.objects.create_user(
            email='guide@test.com',
            username='testguide',
            phone_number='+237600000003',
            password='guidepass123',
            full_name='Test Guide',
            gender='male',
            role='guide'
        )
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            username='adminuser',
            phone_number='+237600000004',
            password='adminpass123',
            full_name='Admin User',
            gender='female',
            role='admin'
        )

        # Create payment methods
        self.mtn = PaymentMethod.objects.create(name="mtn", description="MTN Mobile Money")
        self.orange = PaymentMethod.objects.create(name="orange", description="Orange Money")
        self.card = PaymentMethod.objects.create(name="card", description="Credit Card")
        self.paypal = PaymentMethod.objects.create(name="paypal", description="PayPal")

        # Create bookings
        self.tutorial_booking = Booking.objects.create(
            learner_or_visitor=self.user,
            tutor=self.tutor,
            booking_type="tutorial"
        )
        self.tour_booking = Booking.objects.create(
            learner_or_visitor=self.user,
            guide=self.guide,
            booking_type="tour"
        )

        # Get content type for bookings
        self.booking_content_type = ContentType.objects.get_for_model(Booking)

        # Create test transactions with complete metadata
        self.tx_mtn = PaymentTransaction.objects.create(
            user=self.user,
            method=self.mtn,
            amount=5000,
            currency="XAF",
            status="pending",
            reference="mtn-ref-001",
            purpose="booking",
            metadata={
                "payer_phone": "671234567",
                "description": "Test payment"
            },
            content_type=self.booking_content_type,
            object_id=self.tutorial_booking.id
        )
        
        self.tx_stripe = PaymentTransaction.objects.create(
            user=self.user,
            method=self.card,
            amount=2000,
            currency="XAF",
            status="pending",
            reference="stripe-ref-001",
            purpose="booking",
            metadata={
                "stripe_token": "tok_visa_test",
                "description": "Test payment"
            },
            external_id="stripe_charge_id_123",
            content_type=self.booking_content_type,
            object_id=self.tutorial_booking.id
        )
        
        self.tx_paypal = PaymentTransaction.objects.create(
            user=self.user,
            method=self.paypal,
            amount=3000,
            currency="XAF",
            status="pending",
            reference="paypal-ref-001",
            purpose="booking",
            metadata={
                "return_url": "https://example.com/return",
                "cancel_url": "https://example.com/cancel",
                "description": "Test payment"
            },
            external_id="paypal_order_id_456",
            content_type=self.booking_content_type,
            object_id=self.tutorial_booking.id
        )
        
        self.tx_orange = PaymentTransaction.objects.create(
            user=self.user,
            method=self.orange,
            amount=4000,
            currency="XAF",
            status="pending",
            reference="orange-ref-001",
            purpose="booking",
            metadata={
                "notif_url": "https://example.com/notify",
                "return_url": "https://example.com/return",
                "description": "Test payment"
            },
            content_type=self.booking_content_type,
            object_id=self.tutorial_booking.id
        )

    def tearDown(self):
        settings.TESTING = False  # Reset testing flag

    def test_payment_method_list(self):
        url = reverse("paymentmethod-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # 4 payment methods created
        method_names = [method['name'] for method in response.data]
        self.assertIn('mtn', method_names)
        self.assertIn('orange', method_names)

    def test_create_booking(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("booking-list")
        data = {
            "learner_or_visitor": self.user.id,
            "tutor": self.tutor.id,
            "booking_type": "tutorial",
            "guide": None  # Explicitly set guide to None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["learner_or_visitor"], self.user.id)
        self.assertEqual(response.data["booking_type"], "tutorial")

    def test_user_can_create_payment_transaction(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("paymenttransaction-list")
        data = {
            "method_id": self.mtn.id,
            "amount": "10000.00",
            "currency": "XAF",
            "purpose": "booking",
            "description": "Payment for tutorial booking",
            "metadata": {
                "payer_phone": "671234567",
                "note": "Test payment"
            },
            "content_type": self.booking_content_type.id,
            "object_id": self.tutorial_booking.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(response.data["method"]["name"], "mtn")
        self.assertEqual(response.data["amount"], "10000.00")

    @patch("payments.backends.process_payment", return_value=True)
    def test_initiate_payment(self, mock_process_payment):
        self.client.force_authenticate(user=self.user)
        
        url = reverse("paymenttransaction-initiate", args=[self.tx_mtn.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tx_mtn.refresh_from_db()
        self.assertEqual(self.tx_mtn.status, "success")
        self.assertTrue(PaymentReceipt.objects.filter(transaction=self.tx_mtn).exists())
        
        # Verify booking is marked as paid
        self.tutorial_booking.refresh_from_db()
        self.assertTrue(self.tutorial_booking.is_paid_to_admin)

    def test_cannot_initiate_non_pending_payment(self):
        self.client.force_authenticate(user=self.user)
        
        # Update transaction to completed status
        self.tx_mtn.status = "success"
        self.tx_mtn.save()
        
        url = reverse("paymenttransaction-initiate", args=[self.tx_mtn.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Transaction already processed.")

    def test_cancel_payment(self):
        self.client.force_authenticate(user=self.user)
        
        url = reverse("paymenttransaction-cancel", args=[self.tx_orange.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tx_orange.refresh_from_db()
        self.assertEqual(self.tx_orange.status, "cancelled")

    def test_cannot_cancel_non_pending_payment(self):
        self.client.force_authenticate(user=self.user)
        
        # Update transaction to completed status
        self.tx_orange.status = "success"
        self.tx_orange.save()
        
        url = reverse("paymenttransaction-cancel", args=[self.tx_orange.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Cannot cancel. Transaction already processed.")

    def test_payment_receipt_creation(self):
        self.client.force_authenticate(user=self.user)
        
        # Create receipt
        receipt = PaymentReceipt.objects.create(transaction=self.tx_stripe)
        
        # Test receipt access
        url = reverse("paymentreceipt-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(receipt.id), [str(r['id']) for r in response.data['results']])

    def test_admin_can_create_payout(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("payout-list")
        data = {
            "guide_or_tutor": self.tutor.id,
            "amount": "4000.00",
            "related_booking": self.tutorial_booking.id,
            "note": "Payment for tutorial services"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payout = Payout.objects.get(id=response.data["id"])
        self.assertEqual(payout.status, "paid")
        self.assertEqual(payout.paid_by_admin, self.admin)
        
        # Verify booking is marked as paid to service provider
        self.tutorial_booking.refresh_from_db()
        self.assertTrue(self.tutorial_booking.is_paid_to_service_provider)

    def test_regular_user_cannot_mark_payout_as_paid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("payout-list")
        data = {
            "guide_or_tutor": self.tutor.id,
            "amount": "4000.00",
            "related_booking": self.tutorial_booking.id,
            "note": "User attempt to payout"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payout = Payout.objects.get(id=response.data["id"])
        self.assertEqual(payout.status, "pending")
        self.assertIsNone(payout.paid_by_admin)

    def test_user_can_only_see_own_transactions(self):
        # Create a transaction for another user
        other_tx = PaymentTransaction.objects.create(
            user=self.tutor,
            method=self.orange,
            amount="6000.00",
            currency="XAF",
            status="success",
            reference="other-tx-001",
            purpose="booking",
            metadata={
                "notif_url": "https://example.com/notify",
                "return_url": "https://example.com/return"
            }
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse("paymenttransaction-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see our own transactions
        tx_ids = [tx['id'] for tx in response.data['results']]
        self.assertNotIn(other_tx.id, tx_ids)

    def test_admin_can_see_all_transactions(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("paymenttransaction-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see all transactions
        self.assertGreaterEqual(len(response.data['results']), 4)

class WebhookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='webhook@test.com',
            username='webhookuser',
            phone_number='+237600000005',
            password='webhookpass',
            full_name='Webhook User',
            gender='male',
            role='learner'
        )
        
        self.mtn = PaymentMethod.objects.create(name="mtn", description="MTN Mobile Money")
        self.orange = PaymentMethod.objects.create(name="orange", description="Orange Money")
        self.card = PaymentMethod.objects.create(name="card", description="Credit Card")
        self.paypal = PaymentMethod.objects.create(name="paypal", description="PayPal")
        
        # Create test transactions with complete metadata
        self.tx_mtn = PaymentTransaction.objects.create(
            user=self.user,
            method=self.mtn,
            amount=5000,
            currency="XAF",
            status="pending",
            reference="mtn-ref-001",
            purpose="booking",
            metadata={"payer_phone": "671234567"}
        )
        self.tx_stripe = PaymentTransaction.objects.create(
            user=self.user,
            method=self.card,
            amount=2000,
            currency="XAF",
            status="pending",
            reference="stripe-ref-001",
            purpose="booking",
            metadata={"stripe_token": "tok_test"},
            external_id="stripe_charge_id_123"
        )
        self.tx_paypal = PaymentTransaction.objects.create(
            user=self.user,
            method=self.paypal,
            amount=3000,
            currency="XAF",
            status="pending",
            reference="paypal-ref-001",
            purpose="booking",
            metadata={
                "return_url": "https://example.com/return",
                "cancel_url": "https://example.com/cancel"
            },
            external_id="paypal_order_id_456"
        )
        self.tx_orange = PaymentTransaction.objects.create(
            user=self.user,
            method=self.orange,
            amount=4000,
            currency="XAF",
            status="pending",
            reference="orange-ref-001",
            purpose="booking",
            metadata={
                "notif_url": "https://example.com/notify",
                "return_url": "https://example.com/return"
            }
        )

    @patch("payments.webhooks.STRIPE_API_KEY", "sk_test_fake")
    @patch("stripe.Webhook.construct_event")
    def test_stripe_webhook_success(self, mock_construct_event):
        mock_construct_event.return_value = {
            "type": "charge.succeeded",
            "data": {"object": {"id": self.tx_stripe.external_id}}
        }
        
        url = reverse("stripe-webhook")
        response = self.client.post(
            url, 
            data="{}", 
            content_type="application/json", 
            HTTP_STRIPE_SIGNATURE="dummy"
        )
        
        self.assertEqual(response.status_code, 200)
        self.tx_stripe.refresh_from_db()
        self.assertEqual(self.tx_stripe.status, "success")

    def test_paypal_webhook_success(self):
        url = reverse("paypal-webhook")
        event = {
            "event_type": "CHECKOUT.ORDER.APPROVED",
            "resource": {"id": self.tx_paypal.external_id}
        }
        response = self.client.post(url, data=event, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.tx_paypal.refresh_from_db()
        self.assertEqual(self.tx_paypal.status, "success")

    def test_paypal_webhook_failed(self):
        url = reverse("paypal-webhook")
        event = {
            "event_type": "PAYMENT.CAPTURE.DENIED",
            "resource": {"id": self.tx_paypal.external_id}
        }
        response = self.client.post(url, data=event, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.tx_paypal.refresh_from_db()
        self.assertEqual(self.tx_paypal.status, "failed")

    def test_mtn_webhook_success(self):
        url = reverse("mtn-webhook")
        payload = {
            "externalId": self.tx_mtn.reference,
            "status": "SUCCESSFUL"
        }
        response = self.client.post(url, data=payload, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.tx_mtn.refresh_from_db()
        self.assertEqual(self.tx_mtn.status, "success")

    def test_orange_webhook_success(self):
        url = reverse("orange-webhook")
        payload = {
            "order_id": self.tx_orange.reference,
            "status": "PAID"
        }
        response = self.client.post(url, data=payload, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.tx_orange.refresh_from_db()
        self.assertEqual(self.tx_orange.status, "success")

class PaymentsAppIntegrationTest(APITestCase):
    def setUp(self):
        settings.TESTING = True
        
        self.user = User.objects.create_user(
            email='user2@test.com',
            username='testuser2',
            phone_number='+237600000006',
            password='testpass123',
            full_name='Test User 2',
            gender='female',
            role='learner'
        )
        self.admin = User.objects.create_superuser(
            email='admin2@test.com',
            username='adminuser2',
            phone_number='+237600000007',
            password='adminpass123',
            full_name='Admin User 2',
            gender='male',
            role='admin'
        )
        
        self.mtn = PaymentMethod.objects.create(name="mtn", description="MTN Mobile Money")
        self.orange = PaymentMethod.objects.create(name="orange", description="Orange Money")
        self.card = PaymentMethod.objects.create(name="card", description="Credit Card")
        self.paypal = PaymentMethod.objects.create(name="paypal", description="PayPal")

        self.booking = Booking.objects.create(
            learner_or_visitor=self.user,
            tutor=None,
            booking_type="tour"
        )

        self.booking_content_type = ContentType.objects.get_for_model(Booking)

        # Define test payment data with complete metadata
        self.mtn_payment_data = {
            "method_id": self.mtn.id,
            "amount": "10000.00",
            "currency": "XAF",
            "purpose": "booking",
            "description": "Booking payment via MTN",
            "metadata": {
                "payer_phone": "671234567",
                "note": "Test payment"
            },
            "content_type": self.booking_content_type.id,
            "object_id": self.booking.id
        }
        
        self.orange_payment_data = {
            "method_id": self.orange.id,
            "amount": "15000.00",
            "currency": "XAF",
            "purpose": "booking",
            "description": "Booking payment via Orange",
            "metadata": {
                "notif_url": "https://example.com/notify",
                "return_url": "https://example.com/return",
                "phone": "691234567"
            },
            "content_type": self.booking_content_type.id,
            "object_id": self.booking.id
        }
        
        self.card_payment_data = {
            "method_id": self.card.id,
            "amount": "20000.00",
            "currency": "XAF",
            "purpose": "booking",
            "description": "Booking payment via Credit Card",
            "metadata": {
                "stripe_token": "tok_visa_test",
                "note": "Test payment"
            },
            "content_type": self.booking_content_type.id,
            "object_id": self.booking.id
        }
        
        self.paypal_payment_data = {
            "method_id": self.paypal.id,
            "amount": "25000.00",
            "currency": "XAF",
            "purpose": "booking",
            "description": "Booking payment via PayPal",
            "metadata": {
                "return_url": "https://example.com/success",
                "cancel_url": "https://example.com/cancel",
                "note": "Test payment"
            },
            "content_type": self.booking_content_type.id,
            "object_id": self.booking.id
        }

    def tearDown(self):
        settings.TESTING = False

    @patch("payments.backends.MTNMobileMoneyBackend.process_payment", return_value=True)
    def test_process_payment_backend_success_mtn(self, mock_mtn_backend):
        """Test MTN Mobile Money payment processing"""
        self.client.force_authenticate(user=self.user)
        
        # Create transaction
        url = reverse("paymenttransaction-list")
        response = self.client.post(url, self.mtn_payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Initiate payment
        transaction_id = response.data["id"]
        initiate_url = reverse("paymenttransaction-initiate", args=[transaction_id])
        response = self.client.post(initiate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_mtn_backend.called)
        
        # Verify transaction status updated
        transaction = PaymentTransaction.objects.get(id=transaction_id)
        self.assertEqual(transaction.status, "success")

    @patch("payments.backends.OrangeMoneyBackend.process_payment", return_value={"payment_url": "https://orange.com/pay"})
    def test_process_payment_backend_success_orange(self, mock_orange_backend):
        """Test Orange Money payment processing"""
        self.client.force_authenticate(user=self.user)
        
        # Create transaction
        url = reverse("paymenttransaction-list")
        response = self.client.post(url, self.orange_payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Initiate payment
        transaction_id = response.data["id"]
        initiate_url = reverse("paymenttransaction-initiate", args=[transaction_id])
        response = self.client.post(initiate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_orange_backend.called)
        
        # Verify transaction status updated
        transaction = PaymentTransaction.objects.get(id=transaction_id)
        self.assertEqual(transaction.status, "success")

    @patch("payments.backends.StripeBackend.process_payment", return_value=True)
    def test_process_payment_backend_success_stripe(self, mock_stripe_backend):
        """Test Stripe (Credit Card) payment processing"""
        self.client.force_authenticate(user=self.user)
        
        # Create transaction
        url = reverse("paymenttransaction-list")
        response = self.client.post(url, self.card_payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Initiate payment
        transaction_id = response.data["id"]
        initiate_url = reverse("paymenttransaction-initiate", args=[transaction_id])
        response = self.client.post(initiate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_stripe_backend.called)
        
        # Verify transaction status updated
        transaction = PaymentTransaction.objects.get(id=transaction_id)
        self.assertEqual(transaction.status, "success")

    @patch("payments.backends.PayPalBackend.process_payment", return_value={"id": "PAY-123", "status": "APPROVED"})
    def test_process_payment_backend_success_paypal(self, mock_paypal_backend):
        """Test PayPal payment processing"""
        self.client.force_authenticate(user=self.user)
        
        # Create transaction
        url = reverse("paymenttransaction-list")
        response = self.client.post(url, self.paypal_payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Initiate payment
        transaction_id = response.data["id"]
        initiate_url = reverse("paymenttransaction-initiate", args=[transaction_id])
        response = self.client.post(initiate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_paypal_backend.called)
        
        # Verify transaction status updated
        transaction = PaymentTransaction.objects.get(id=transaction_id)
        self.assertEqual(transaction.status, "success")