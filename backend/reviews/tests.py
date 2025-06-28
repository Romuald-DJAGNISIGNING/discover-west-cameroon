from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from villages.models import Village
from tourism.models import TouristicAttraction, HostingFamilyExperience, SocialImmersionExperience
from festivals.models import Festival
from .models import Review

User = get_user_model()

class ReviewsAppTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            phone_number='+237600000011',
            password='pw',
            role='learner'
        )
        self.user2 = User.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            phone_number='+237600000012',
            password='pw',
            role='learner'
        )
        self.village = Village.objects.create(name="Bandjoun", department="Koung-Khi", description="Bandjoun desc", population=70000)
        self.attraction = TouristicAttraction.objects.create(name="Bandjoun Museum", description="Museum", village=self.village, added_by=self.user)
        self.festival = Festival.objects.create(name="Bandjoun Fest", description="Fest desc", type="cultural",
                                               start_date="2025-08-10", end_date="2025-08-12",
                                               location="Bandjoun", village=self.village, main_language="Ghomala", is_annual=True, added_by=self.user)
        self.family = HostingFamilyExperience.objects.create(family_name="Family X", description="Kind family", village=self.village, address="123", can_host=3, live_cooking=True, added_by=self.user)
        self.immersion = SocialImmersionExperience.objects.create(title="Immersion X", description="Immersion desc", village=self.village, start_date="2025-09-01", end_date="2025-09-03", host_family="Family X", activities="Cooking", live_cooking=True, added_by=self.user)

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_review_village(self):
        self.authenticate(self.user)
        url = reverse('review-list')
        data = {
            "rating": 5, "title": "Great village", "content": "Loved it!",
            "village": self.village.id
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Review.objects.filter(village=self.village, user=self.user).exists())

    def test_unique_review_per_user_per_target(self):
        self.authenticate(self.user)
        url = reverse('review-list')
        data = {
            "rating": 4, "title": "Nice museum", "content": "Worth visiting.",
            "attraction": self.attraction.id
        }
        # First post should succeed
        self.client.post(url, data)
        
        # Second post should fail with validation error
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("You have already reviewed this attraction.", str(response.content))

    def test_edit_review(self):
        self.authenticate(self.user)
        review = Review.objects.create(user=self.user, rating=3, title="Ok", content="Ok", festival=self.festival)
        url = reverse('review-detail', args=[review.id])
        data = {"title": "Updated", "content": "Much better", "rating": 4}
        resp = self.client.patch(url, data)
        self.assertEqual(resp.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.title, "Updated")
        self.assertEqual(review.rating, 4)

    def test_other_user_cannot_edit(self):
        review = Review.objects.create(user=self.user, rating=3, title="No edit", content="No edit", hosting_family=self.family)
        self.authenticate(self.user2)
        url = reverse('review-detail', args=[review.id])
        data = {"title": "Hacked"}
        resp = self.client.patch(url, data)
        self.assertEqual(resp.status_code, 403)