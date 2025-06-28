from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from villages.models import Village
from tourism.models import TouristicAttraction
from festivals.models import Festival
from .models import SupportTicket, SupportMessage

User = get_user_model()

class SupportAppTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            phone_number='+237600000009',
            password='pw',
            role='admin',
            is_superuser=True
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            phone_number='+237600000010',
            password='pw',
            role='learner'
        )
        self.village = Village.objects.create(name="Dschang", department="Menoua", description="Dschang desc", population=120000)
        self.attraction = TouristicAttraction.objects.create(name="Dschang Lake", description="Lake desc", village=self.village, added_by=self.admin)
        self.festival = Festival.objects.create(
            name="Dschang Fest", description="Fest desc", type="cultural",
            start_date="2025-09-10", end_date="2025-09-12", location="Dschang", village=self.village, main_language="Yemba", is_annual=True, added_by=self.admin
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_ticket(self):
        self.authenticate(self.user)
        url = reverse('supportticket-list')
        data = {
            "subject": "Help needed",
            "message": "I can't book.",
            "priority": "urgent",
            "village": self.village.id,
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(SupportTicket.objects.filter(subject="Help needed").exists())

    def test_add_message_to_ticket(self):
        ticket = SupportTicket.objects.create(subject="Q", message="M", created_by=self.user)
        self.authenticate(self.user)
        url = reverse('supportticket-add-message', args=[ticket.id])
        data = {"message": "Reply"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(ticket.messages.count(), 1)

    def test_admin_can_assign_and_resolve(self):
        ticket = SupportTicket.objects.create(subject="Assign me", message="msg", created_by=self.user)
        self.authenticate(self.admin)
        assign_url = reverse('supportticket-assign', args=[ticket.id])
        resp = self.client.post(assign_url, {"assigned_to": self.admin.id})
        self.assertEqual(resp.status_code, 200)
        ticket.refresh_from_db()
        self.assertEqual(ticket.assigned_to, self.admin)
        resolve_url = reverse('supportticket-resolve', args=[ticket.id])
        resp = self.client.post(resolve_url, {"resolution": "Done"})
        self.assertEqual(resp.status_code, 200)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "resolved")
        self.assertEqual(ticket.resolution, "Done")