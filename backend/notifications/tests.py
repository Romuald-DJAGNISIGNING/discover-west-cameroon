from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.notification = Notification.objects.create(
            recipient=self.user,
            title='Booking Confirmed',
            message='Your booking has been confirmed successfully.',
            notification_type='success'
        )

    def test_notification_creation(self):
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(self.notification.recipient, self.user)
        self.assertEqual(self.notification.title, 'Booking Confirmed')
        self.assertFalse(self.notification.read)

    def test_mark_as_read(self):
        self.notification.read = True
        self.notification.save()
        self.assertTrue(Notification.objects.get(pk=self.notification.pk).read)

# --- Additional API tests for notifications ---

class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', email='api@example.com', password='apipass')
        self.client.force_authenticate(user=self.user)
        self.notification = Notification.objects.create(
            recipient=self.user,
            title='API Notification',
            message='This is an API notification.',
            notification_type='info'
        )

    def test_list_notifications(self):
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_notification(self):
        url = reverse('notification-detail', args=[self.notification.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Notification')

    def test_mark_notification_as_read(self):
        url = reverse('notification-detail', args=[self.notification.id])
        response = self.client.patch(url, {'read': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)
