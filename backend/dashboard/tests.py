from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class DashboardAPITests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.login(username='adminuser', password='adminpass')

    def test_user_activity_log_list(self):
        response = self.client.get('/dashboard/user-activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_daily_statistics_view(self):
        response = self.client.get('/dashboard/daily-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tour_booking_statistics(self):
        response = self.client.get('/dashboard/tour-bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tutor_booking_statistics(self):
        response = self.client.get('/dashboard/tutor-bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_guide_booking_statistics(self):
        response = self.client.get('/dashboard/guide-bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feedback_summary_statistics(self):
        response = self.client.get('/dashboard/feedback-summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_system_notification_creation(self):
        payload = {
            "message": "This is a test system notification.",
            "level": "info"
        }
        response = self.client.post('/dashboard/system-notifications/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_system_notification_retrieve(self):
        # Create a notification first
        payload = {
            "message": "Retrieve this notification.",
            "level": "warning"
        }
        post_response = self.client.post('/dashboard/system-notifications/', payload)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        notification_id = post_response.data['id']
        get_response = self.client.get(f'/dashboard/system-notifications/{notification_id}/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access_denied(self):
        self.client.logout()
        response = self.client.get('/dashboard/daily-stats/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
