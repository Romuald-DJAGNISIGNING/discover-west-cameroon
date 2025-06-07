from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import Report

class ReportTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user@gmail.com',
            username='testuser',
            phone_number='+237612345678',
            full_name='Test User',
            password='password123',
            gender='male',
            role='student',
        )
        self.admin = CustomUser.objects.create_superuser(
            email='admin@gmail.com',
            username='adminuser',
            phone_number='+237699999999',
            full_name='Admin User',
            password='adminpass',
            gender='male',
            role='student'
        )

    def test_create_report(self):
        self.client.login(email='user@gmail.com', password='password123')
        url = reverse('create-report')
        data = {
            'reported_user': self.admin.id,  # or any valid user id
            'reason': 'other',               # must be one of the choices
            'description': 'There is a bug when loading a certain tour guide.'
        }
        response = self.client.post(url, data)
        print(response.status_code, response.data)  # For debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_reports_as_admin(self):
        self.client.login(email='admin@gmail.com', password='adminpass')
        url = reverse('list-reports')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reports_as_user_forbidden(self):
        self.client.login(email='user@gmail.com', password='password123')
        url = reverse('list-reports')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
