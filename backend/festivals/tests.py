from django.urls import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import (
    Festival, FestivalAttendance, FestivalFeedback, FestivalBookmark,
    FestivalComment, FestivalMedia, FestivalFact
)
from datetime import date
import io

User = get_user_model()

def get_star_rating(rating):
    """Return a string with 'rating' filled stars."""
    return "★" * rating

class FestivalAppTests(APITestCase):
    def setUp(self):
        # Create users
        self.tutor = User.objects.create_user(
            username="tutor",
            email="tutor@example.com",
            phone_number="+237600000021",
            password="pw123",
            role="tutor"
        )
        self.learner = User.objects.create_user(
            username="learner",
            email="learner@example.com",
            phone_number="+237600000022",
            password="pw123",
            role="learner"
        )
        self.guide = User.objects.create_user(
            username="guide",
            email="guide@example.com",
            phone_number="+237600000023",
            password="pw123",
            role="guide"
        )
        self.visitor = User.objects.create_user(
            username="visitor",
            email="visitor@example.com",
            phone_number="+237600000024",
            password="pw123",
            role="visitor"
        )
        # Create a festival
        self.festival = Festival.objects.create(
            name="Ngouon",
            description="Bamoun Royal Festival",
            type="traditional",
            start_date=date(2025, 12, 5),
            end_date=date(2025, 12, 12),
            location="Foumban",
            main_language="Bamoun",
            is_annual=True,
            added_by=self.tutor,
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_festival_list_and_detail(self):
        url = reverse('festival-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)
        url = reverse('festival-detail', args=[self.festival.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Ngouon")
        # Rating and popularity must be present
        self.assertIn('average_rating', response.data)
        self.assertIn('popularity_score', response.data)

    def test_tutor_can_create_festival(self):
        self.authenticate(self.tutor)
        url = reverse('festival-list')
        data = {
            "name": "Msem Todjom",
            "description": "Bafoussam harvest festival",
            "type": "traditional",
            "start_date": "2025-08-15",
            "location": "Bafoussam",
            "main_language": "Ghomala",
            "is_annual": True,
            "added_by": self.tutor.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Festival.objects.filter(name="Msem Todjom").exists())

    def test_learner_cannot_create_festival(self):
        self.authenticate(self.learner)
        url = reverse('festival-list')
        data = {
            "name": "Msem Baham",
            "description": "Harvest festival",
            "type": "traditional",
            "start_date": "2025-09-10",
            "location": "Baham",
            "main_language": "Fe'fe'",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_bookmark_and_unbookmark_festival(self):
        self.authenticate(self.learner)
        url = reverse('festival-bookmark', args=[self.festival.id])
        # Bookmark
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "bookmarked")
        self.assertTrue(FestivalBookmark.objects.filter(festival=self.festival, user=self.learner).exists())
        # Unbookmark
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], "unbookmarked")
        self.assertFalse(FestivalBookmark.objects.filter(festival=self.festival, user=self.learner).exists())

    def test_comment_on_festival(self):
        self.authenticate(self.visitor)
        url = reverse('festival-comments', args=[self.festival.id])
        data = {"comment": "Very interesting!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FestivalComment.objects.count(), 1)
        self.assertEqual(FestivalComment.objects.first().comment, "Very interesting!")
        # Get comments - now checking for proper paginated response
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)  # For paginated responses

    def test_tutor_can_add_media_and_fact(self):
        self.authenticate(self.tutor)
        # Festival Media
        url = reverse('festivalmedia-list')
        # Create a valid small image file
        from PIL import Image
        import io
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)
        uploaded_file = SimpleUploadedFile(
            "test.jpg",
            image_file.read(),
            content_type="image/jpeg"
        )
        data = {
            'festival': self.festival.id, 
            'caption': 'Royal Dance', 
            'image': uploaded_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FestivalMedia.objects.count(), 1)
        obj = FestivalMedia.objects.first()
        self.assertTrue(obj.image)

        # Festival Fact
        url = reverse('festivalfact-list')
        data = {
            'festival': self.festival.id, 
            'fact': 'Ngouon is centuries old.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FestivalFact.objects.count(), 1)

    def test_learner_cannot_add_media_or_fact(self):
        self.authenticate(self.learner)
        url = reverse('festivalmedia-list')
        image_file = SimpleUploadedFile("test2.jpg", b"file_content", content_type="image/jpeg")
        data = {'festival': self.festival.id, 'caption': 'Learner tries', 'image': image_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 403)
        url = reverse('festivalfact-list')
        data = {'festival': self.festival.id, 'fact': 'Learner tries'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_attendance_and_feedback_flow_with_media_and_star_rating(self):
        # Learner attends festival
        self.authenticate(self.learner)
        url = reverse('festival-attendances', args=[self.festival.id])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 201)
        attendance_id = response.data['id']
        self.assertTrue(FestivalAttendance.objects.filter(id=attendance_id, user=self.learner).exists())
        attendance = FestivalAttendance.objects.get(id=attendance_id)

        # Confirm attendance
        url = reverse('festivalattendance-update-status', args=[attendance_id])
        response = self.client.patch(url, {'status': 'confirmed'})
        self.assertEqual(response.status_code, 200)
        attendance.refresh_from_db()
        self.assertEqual(attendance.status, 'confirmed')

        # Create a valid small image file
        from PIL import Image
        import io
        image = Image.new('RGB', (100, 100), color='blue')
        image_file = io.BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)
        uploaded_file = SimpleUploadedFile(
            "feedback.jpg",
            image_file.read(),
            content_type="image/jpeg"
        )

        # Add feedback/experience with rating and media
        url = reverse('festivalattendance-feedback', args=[attendance_id])
        feedback_data = {
            "feedback_text": "It was amazing!",
            "rating": 5,
            "experience": "Loved the dances and food.",
            "image": uploaded_file
        }
        response = self.client.post(url, feedback_data, format='multipart')
        self.assertEqual(response.status_code, 201)  # First submission should be 201 Created
        self.assertEqual(FestivalFeedback.objects.count(), 1)
        feedback = FestivalFeedback.objects.first()
        # Assert star rating
        star_str = get_star_rating(feedback.rating)
        self.assertEqual(star_str, "★★★★★")
        self.assertEqual(feedback.feedback_text, "It was amazing!")
        self.assertTrue(feedback.image)

        # Learner cannot post feedback again (should update instead)
        # Create new image for the update
        image = Image.new('RGB', (100, 100), color='green')
        image_file = io.BytesIO()
        image.save(image_file, 'jpeg')
        image_file.seek(0)
        updated_file = SimpleUploadedFile(
            "updated.jpg",
            image_file.read(),
            content_type="image/jpeg"
        )
        
        updated_data = {
            "feedback_text": "Updated feedback!",
            "rating": 4,
            "experience": "Still great but not perfect.",
            "image": updated_file
        }
        response = self.client.post(url, updated_data, format='multipart')
        self.assertEqual(response.status_code, 200)  # Update should return 200 OK
        feedback.refresh_from_db()
        self.assertEqual(feedback.feedback_text, "Updated feedback!")
        self.assertEqual(feedback.rating, 4)

    def test_booking_tutor_or_guide(self):
        # Learner books a guide for the festival
        self.authenticate(self.learner)
        url = reverse('festival-attendances', args=[self.festival.id])
        data = {"booked_tutor_guide": self.guide.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        attendance = FestivalAttendance.objects.get(id=response.data['id'])
        self.assertEqual(attendance.booked_tutor_guide, self.guide)

    def test_only_attendance_owner_can_give_feedback(self):
        # Learner attends festival
        self.authenticate(self.learner)
        url = reverse('festival-attendances', args=[self.festival.id])
        response = self.client.post(url, {})
        attendance_id = response.data['id']
        url = reverse('festivalattendance-feedback', args=[attendance_id])
        feedback_data = {
            "feedback_text": "Great!",
            "rating": 4,
            "experience": "Nice.",
        }
        response = self.client.post(url, feedback_data)
        self.assertIn(response.status_code, [200, 201])
        # Another user tries to update feedback
        self.authenticate(self.visitor)
        response = self.client.post(url, feedback_data)
        self.assertEqual(response.status_code, 403)

    def test_festival_popularity_and_rating_with_stars(self):
        # Two users attend and rate the festival
        self.authenticate(self.learner)
        url = reverse('festival-attendances', args=[self.festival.id])
        att1 = self.client.post(url, {})
        att1_id = att1.data['id']
        self.client.patch(reverse('festivalattendance-update-status', args=[att1_id]), {'status': 'confirmed'})
        self.client.post(reverse('festivalattendance-feedback', args=[att1_id]), {
            "feedback_text": "Awesome!",
            "rating": 5,
            "experience": "Great!"
        })
        self.authenticate(self.visitor)
        att2 = self.client.post(url, {})
        att2_id = att2.data['id']
        self.client.patch(reverse('festivalattendance-update-status', args=[att2_id]), {'status': 'confirmed'})
        self.client.post(reverse('festivalattendance-feedback', args=[att2_id]), {
            "feedback_text": "Nice!",
            "rating": 3,
            "experience": "Enjoyed the food."
        })
        self.festival.refresh_from_db()
        # Check average_rating and popularity_score
        url = reverse('festival-detail', args=[self.festival.id])
        response = self.client.get(url)
        self.assertIn('average_rating', response.data)
        self.assertAlmostEqual(response.data['average_rating'], 4.0, places=1)
        self.assertIn('popularity_score', response.data)
        # popularity_score = confirmed_attendances * (average_rating / 5.0)
        self.assertAlmostEqual(response.data['popularity_score'], 2 * (4.0 / 5.0), places=2)
        # Check star string
        star_str = get_star_rating(round(response.data['average_rating']))
        self.assertEqual(star_str, "★★★★")