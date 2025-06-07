

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Tutorial, TutorialStep

User = get_user_model()

class TutorialTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@gmail.com',
            username='user1',
            phone_number='+237612345678',
            password='testpass123',
            full_name='Test User',
            gender='male',
            role='student'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_tutorial(self):
        response = self.client.post('/api/tutorials/', {
            'title': 'How to Explore Bafut Palace',
            'description': 'A detailed guide to exploring the Bafut Royal Palace.',
            'language': 'English',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutorial.objects.count(), 1)

    def test_create_tutorial_step(self):
        tutorial = Tutorial.objects.create(
            author=self.user,
            title='How to Visit Lake Awing',
            description='Guide on visiting Lake Awing',
            language='English'
        )
        response = self.client.post('/api/tutorial-steps/', {
            'tutorial': tutorial.id,
            'title': 'Step 1',
            'content': 'Take a bike from Bamenda to Awing',
            'order': 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TutorialStep.objects.count(), 1)
