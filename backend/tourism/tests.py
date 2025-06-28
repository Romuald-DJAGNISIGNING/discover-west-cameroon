from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from villages.models import Village
from .models import (
    TouristicAttraction, SocialImmersionExperience, HostingFamilyExperience,
    TourismActivity, TouristFeedback, TouristComment, SharedTouristMedia
)
from PIL import Image
from io import BytesIO

User = get_user_model()

def create_test_image():
    file = BytesIO()
    image = Image.new('RGB', (100, 100), 'white')
    image.save(file, 'jpeg')
    file.seek(0)
    return file

class TourismAppTests(APITestCase):
    def setUp(self):
        self.tutor = User.objects.create_user(
            username="tutor",
            email="tutor@westcameroon.com",
            phone_number="+237600000026",
            password="tutorpass",
            role="tutor"
        )
        self.guide = User.objects.create_user(
            username="guide",
            email="guide@westcameroon.com",
            phone_number="+237600000027",
            password="guidepass",
            role="guide"
        )
        self.learner = User.objects.create_user(
            username="learner",
            email="learner@westcameroon.com",
            phone_number="+237600000028",
            password="learnerpass",
            role="learner"
        )
        self.village = Village.objects.create(
            name="Dschang",
            department="Menoua",
            description="University town.",
            population=200000,
        )
        self.attraction = TouristicAttraction.objects.create(
            name="Museum of Civilization",
            description="Showcase of Cameroon's cultures.",
            village=self.village,
            latitude=5.45,
            longitude=10.05,
            added_by=self.tutor
        )
        self.immersion = SocialImmersionExperience.objects.create(
            title="Bamileke Life",
            description="Live with locals, learn the culture.",
            village=self.village,
            start_date="2025-07-01",
            end_date="2025-07-10",
            host_family="Foumbotsop Family",
            activities="Farming, Storytelling",
            live_cooking=True,
            added_by=self.tutor
        )
        self.family = HostingFamilyExperience.objects.create(
            family_name="Nana Family",
            description="Warm welcoming Bamileke family.",
            village=self.village,
            address="Rue du marché, Dschang",
            can_host=4,
            live_cooking=True,
            added_by=self.guide
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_attraction(self):
        self.authenticate(self.tutor)
        url = reverse('attraction-list')
        data = {
            "name": "Lac Baleng",
            "description": "A beautiful crater lake.",
            "village": self.village.id,
            "latitude": 5.12345,
            "longitude": 10.12345
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(TouristicAttraction.objects.filter(name="Lac Baleng").exists())

    def test_learner_cannot_create_attraction(self):
        self.authenticate(self.learner)
        url = reverse('attraction-list')
        data = {
            "name": "Chutes de la Menoua",
            "description": "Waterfalls.",
            "village": self.village.id,
            "latitude": 5.12,
            "longitude": 10.12
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_add_feedback_comment_and_media_to_attraction(self):
        self.authenticate(self.learner)
        # Test feedback
        url = reverse('attraction-add-feedback', args=[self.attraction.id])
        data = {"content": "Amazing!", "rating": 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        
        # Test comment
        url = reverse('attraction-add-comment', args=[self.attraction.id])
        data = {"content": "Great for families."}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        
        # Test media
        url = reverse('attraction-add-media', args=[self.attraction.id])
        image_file = create_test_image()
        image = SimpleUploadedFile(
            name='test.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )
        response = self.client.post(
            url,
            {'image': image, 'caption': 'Test caption'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 201, msg=response.data)

    def test_feedback_stars(self):
        self.authenticate(self.learner)
        url = reverse('attraction-add-feedback', args=[self.attraction.id])
        data = {"content": "Nice", "rating": 3}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        feedback = TouristFeedback.objects.first()
        self.assertEqual(feedback.rating, 3)
        self.assertEqual(feedback.content, "Nice")

    def test_activities_linking(self):
        self.authenticate(self.guide)
        url = reverse('tourismactivity-list')
        data = {
            "name": "Guided Tour",
            "description": "Learn about Bamileke culture.",
            "attraction": self.attraction.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        
        data = {
            "name": "Cooking Class",
            "description": "Make ndolé.",
            "immersion": self.immersion.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        
        data = {
            "name": "Harvest Festival",
            "description": "Participate in festival.",
            "family": self.family.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_family_experience_feedback(self):
        self.authenticate(self.learner)
        url = reverse('hostingfamily-add-feedback', args=[self.family.id])
        data = {"content": "Very welcoming!", "rating": 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_social_immersion_feedback_comment_media(self):
        self.authenticate(self.learner)
        # Test feedback
        url = reverse('socialimmersion-add-feedback', args=[self.immersion.id])
        data = {"content": "Life changing", "rating": 4}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        
        # Test comment
        url = reverse('socialimmersion-add-comment', args=[self.immersion.id])
        data = {"content": "I learned so much!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        
        # Test media
        url = reverse('socialimmersion-add-media', args=[self.immersion.id])
        image_file = create_test_image()
        image = SimpleUploadedFile(
            name='test.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )
        response = self.client.post(
            url,
            {'image': image, 'caption': 'Test caption'},
            format='multipart'
        )
        self.assertEqual(response.status_code, 201, msg=response.data)