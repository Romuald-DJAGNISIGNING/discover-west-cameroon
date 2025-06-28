from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pw", email="user@email.com", role="learner", phone_number="+237623456789")
        self.tutor = User.objects.create_user(username="tutor", password="pw", email="tutor@email.com", role="tutor", phone_number="+237653456789")
        self.client.force_authenticate(user=self.user)
        Notification.objects.create(
            recipient=self.user,
            notification_type="in_app",
            event_type="festival_new",
            title="New Festival Added",
            message="Discover the new festival in your area!"
        )

    def test_list_notifications(self):
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_unread_notifications(self):
        url = reverse('notification-unread')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(not n['is_read'] for n in response.data))

    def test_mark_single_read(self):
        notif = Notification.objects.filter(recipient=self.user).first()
        url = reverse('notification-mark-read', args=[notif.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_mark_all_read(self):
        url = reverse('notification-mark-all-read')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Notification.objects.filter(recipient=self.user, is_read=False).exists())

    def test_clear_all_notifications(self):
        url = reverse('notification-clear-all')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Notification.objects.filter(recipient=self.user).exists())