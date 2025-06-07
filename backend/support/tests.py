# support/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import SupportTicket

User = get_user_model()

class SupportTicketTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@gmail.com',
            username='user1',
            phone_number='+237612345678',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_support_ticket(self):
        data = {
            'subject': 'Test Issue',
            'message': 'There is an issue with the app.',
            'category': 'technical',  
        }
        response = self.client.post('/api/support/tickets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SupportTicket.objects.count(), 1)
        ticket = SupportTicket.objects.get()
        self.assertEqual(ticket.subject, data['subject'])
        self.assertEqual(ticket.user, self.user)

    def test_list_support_tickets(self):
        SupportTicket.objects.create(user=self.user, subject='Issue 1', message='Message 1', category='bug')
        SupportTicket.objects.create(user=self.user, subject='Issue 2', message='Message 2', category='feature')

        response = self.client.get('/api/support/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_support_ticket_status(self):
        ticket = SupportTicket.objects.create(user=self.user, subject='Issue 1', message='Message 1', category='bug')
        data = {'status': 'in_progress'}
        response = self.client.patch(f'/api/support/tickets/{ticket.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'in_progress')
