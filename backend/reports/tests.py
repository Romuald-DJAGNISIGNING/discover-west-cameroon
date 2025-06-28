from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from villages.models import Village
from tourism.models import TouristicAttraction
from festivals.models import Festival
from .models import Report

User = get_user_model()

class ReportsAppTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            phone_number='+237600000013',
            password='pw',
            role='admin',
            is_superuser=True
        )
        self.tutor = User.objects.create_user(
            username='tutor',
            email='tutor@example.com',
            phone_number='+237600000014',
            password='pw',
            role='tutor'
        )
        self.learner = User.objects.create_user(
            username='learner',
            email='learner@example.com',
            phone_number='+237600000015',
            password='pw',
            role='learner'
        )
        self.village = Village.objects.create(name="Bana", department="Hauts-Plateaux", description="Bana village", population=20000)
        self.attraction = TouristicAttraction.objects.create(name="Bana Falls", description="Beautiful falls", village=self.village, added_by=self.tutor)
        self.festival = Festival.objects.create(
            name="Bana Festival", description="Annual fest", type="cultural",
            start_date="2025-08-01", end_date="2025-08-03", location="Bana", village=self.village, main_language="Fe'fe'", is_annual=True, added_by=self.tutor
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_report(self):
        self.authenticate(self.learner)
        url = reverse('report-list')
        data = {
            "type": "suggestion",
            "title": "Improve signage",
            "description": "More signs are needed.",
            "village": self.village.id
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Report.objects.filter(title="Improve signage").exists())

    def test_filter_reports(self):
        self.authenticate(self.learner)
        Report.objects.create(type="abuse", title="Spam", description="Spam found", reported_by=self.learner, village=self.village)
        url = reverse('report-list')
        resp = self.client.get(url, {"type": "abuse"})
        self.assertEqual(resp.status_code, 200)
        
        # Handle both list and paginated responses
        if isinstance(resp.data, list):
            results = resp.data
        else:
            results = resp.data.get('results', [])
        
        self.assertTrue(any(r["type"] == "abuse" for r in results),
                       msg="No abuse reports found in filtered results")

    def test_admin_can_review_and_resolve(self):
        report = Report.objects.create(type="bug", title="Broken bench", description="Bench broken", reported_by=self.learner, attraction=self.attraction)
        self.authenticate(self.admin)
        review_url = reverse('report-review', args=[report.id])
        resp = self.client.post(review_url, {"resolution_comment": "Noted"})
        self.assertEqual(resp.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, "reviewed")
        resolve_url = reverse('report-resolve', args=[report.id])
        resp = self.client.post(resolve_url, {"resolution_comment": "Fixed"})
        self.assertEqual(resp.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, "resolved")

    def test_owner_can_edit_title_and_description_only(self):
        report = Report.objects.create(type="feedback", title="Old", description="Desc", reported_by=self.learner, festival=self.festival)
        self.authenticate(self.learner)
        url = reverse('report-detail', args=[report.id])
        print(f"Request data: { {'title': 'New', 'description': 'Updated'} }")  # Debug
        resp = self.client.patch(
            url, 
            {"title": "New", "description": "Updated"},
            format='json'
        )
        print(f"Response status: {resp.status_code}")  # Debug
        print(f"Response content: {resp.content}")  # Debug
        self.assertEqual(resp.status_code, 200)

    def test_permission_logic(self):
        from .permissions import IsAdminReviewerOrOwnerOrReadOnly
        perm = IsAdminReviewerOrOwnerOrReadOnly()
        request = self.client.patch('/').wsgi_request
        request.user = self.learner
        request.data = {'title': 'New'}
        
        # Create a mock view and object
        class MockView:
            pass
        report = Report.objects.create(
            type="feedback", 
            title="Old", 
            reported_by=self.learner
        )
        
        # Should return True for owner editing allowed fields
        self.assertTrue(
            perm.has_object_permission(request, MockView(), report),
            "Owner should be able to edit their report"
        )