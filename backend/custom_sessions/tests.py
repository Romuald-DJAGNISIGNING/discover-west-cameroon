from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import CustomSession, SessionMaterial, SessionFeedback, InAppNotification
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class CustomSessionsAPITests(APITestCase):
    def setUp(self):
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

        self.tutoring_session = CustomSession.objects.create(
            session_type='tutoring',
            tutor_or_guide=self.tutor,
            learner_or_visitor=self.learner,
            topic_or_location="Bamileke Art",
            scheduled_time=timezone.now() + timedelta(days=1),
            duration_minutes=60,
            status='pending'
        )
        self.tour_session = CustomSession.objects.create(
            session_type='tour_guide',
            tutor_or_guide=self.guide,
            learner_or_visitor=self.visitor,
            topic_or_location="Foumban Palace Tour",
            scheduled_time=timezone.now() + timedelta(days=2),
            duration_minutes=120,
            status='pending'
        )

    def tearDown(self):
        CustomSession.objects.all().delete()
        User.objects.all().delete()
        SessionFeedback.objects.all().delete()
        InAppNotification.objects.all().delete()
        SessionMaterial.objects.all().delete()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_tutoring_session_as_learner(self):
        self.authenticate(self.learner)
        url = reverse("customsession-list")
        data = {
            "session_type": "tutoring",
            "tutor_or_guide_id": self.tutor.id,
            "topic_or_location": "Learn Ghomala",
            "scheduled_time": (timezone.now() + timedelta(days=4)).isoformat(),
            "duration_minutes": 90,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["topic_or_location"], "Learn Ghomala")
        self.assertEqual(response.data["learner_or_visitor"], self.learner.id)

    def test_create_tour_guide_session_as_visitor(self):
        self.authenticate(self.visitor)
        url = reverse("customsession-list")
        data = {
            "session_type": "tour_guide",
            "tutor_or_guide_id": self.guide.id,
            "topic_or_location": "Tour of Bamenda Grassfields",
            "scheduled_time": (timezone.now() + timedelta(days=3)).isoformat(),
            "duration_minutes": 180,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["topic_or_location"], "Tour of Bamenda Grassfields")
        self.assertEqual(response.data["learner_or_visitor"], self.visitor.id)

    def test_confirm_session(self):
        self.authenticate(self.tutor)
        url = reverse("customsession-confirm", args=[self.tutoring_session.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.tutoring_session.refresh_from_db()
        self.assertEqual(self.tutoring_session.status, "confirmed")

    def test_confirm_tour_session(self):
        self.authenticate(self.guide)
        url = reverse("customsession-confirm", args=[self.tour_session.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.tour_session.refresh_from_db()
        self.assertEqual(self.tour_session.status, "confirmed")

    def test_complete_session(self):
        self.tutoring_session.status = "confirmed"
        self.tutoring_session.save()
        self.authenticate(self.tutor)
        url = reverse("customsession-complete", args=[self.tutoring_session.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.tutoring_session.refresh_from_db()
        self.assertEqual(self.tutoring_session.status, "completed")

    def test_cancel_session(self):
        self.authenticate(self.tutor)
        url = reverse("customsession-cancel", args=[self.tutoring_session.id])
        reason = "Unexpected event"
        response = self.client.post(url, {"reason": reason})
        self.assertEqual(response.status_code, 200)
        self.tutoring_session.refresh_from_db()
        self.assertEqual(self.tutoring_session.status, "cancelled")
        self.assertEqual(self.tutoring_session.cancellation_reason, reason)

    def test_no_show_session(self):
        self.authenticate(self.tutor)
        url = reverse("customsession-no-show", args=[self.tutoring_session.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.tutoring_session.refresh_from_db()
        self.assertEqual(self.tutoring_session.status, "no_show")

    def test_upload_material(self):
        self.authenticate(self.tutor)
        url = reverse("sessionmaterial-list")
        with open(__file__, "rb") as testfile:
            data = {
                "session": self.tutoring_session.id,
                "title": "Art Sample",
                "file": testfile,
            }
            response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SessionMaterial.objects.count(), 1)

    def test_upload_material_to_tour_session(self):
        self.authenticate(self.guide)
        url = reverse("sessionmaterial-list")
        with open(__file__, "rb") as testfile:
            data = {
                "session": self.tour_session.id,
                "title": "Tour Brochure",
                "file": testfile,
            }
            response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        material = SessionMaterial.objects.get(session=self.tour_session)
        self.assertEqual(material.title, "Tour Brochure")

    def test_give_feedback(self):
        # Complete the session first
        self.tutoring_session.status = 'completed'
        self.tutoring_session.save()
        
        self.authenticate(self.learner)
        url = reverse("sessionfeedback-list")
        data = {
            "session": self.tutoring_session.id,
            "rating": 5,
            "comment": "Wonderful experience!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(SessionFeedback.objects.count(), 1)
        feedback = SessionFeedback.objects.first()
        self.assertEqual(feedback.author, self.learner)
        self.assertEqual(feedback.session, self.tutoring_session)
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.comment, "Wonderful experience!")

    def test_feedback_on_tour_session(self):
        # Complete the session first
        self.tour_session.status = 'completed'
        self.tour_session.save()
        
        self.authenticate(self.visitor)
        url = reverse("sessionfeedback-list")
        data = {
            "session": self.tour_session.id,
            "rating": 4,
            "comment": "Wonderful palace and history!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(SessionFeedback.objects.count(), 1)
        feedback = SessionFeedback.objects.first()
        self.assertEqual(feedback.author, self.visitor)
        self.assertEqual(feedback.session, self.tour_session)
        self.assertEqual(feedback.rating, 4)
        self.assertEqual(feedback.comment, "Wonderful palace and history!")
        self.assertTrue(InAppNotification.objects.filter(user=self.guide).exists())
        self.assertTrue(InAppNotification.objects.filter(user=self.visitor).exists())

    def test_inapp_notification_on_feedback(self):
        # Complete the session first
        self.tutoring_session.status = 'completed'
        self.tutoring_session.save()
        
        self.authenticate(self.learner)
        url = reverse("sessionfeedback-list")
        data = {
            "session": self.tutoring_session.id,
            "rating": 5,
            "comment": "Great!"
        }
        self.client.post(url, data)
        self.assertTrue(InAppNotification.objects.filter(user=self.tutor).exists())
        self.assertTrue(InAppNotification.objects.filter(user=self.learner).exists())

    def test_fetch_user_notifications(self):
        InAppNotification.objects.create(user=self.tutor, message="Test notification")
        self.authenticate(self.tutor)
        url = reverse("inappnotification-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_sessions_list(self):
        self.authenticate(self.tutor)
        url = reverse("customsession-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_session_detail(self):
        self.authenticate(self.learner)
        url = reverse("customsession-detail", args=[self.tutoring_session.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.tutoring_session.id)

    def test_update_session_notes_and_location(self):
        self.authenticate(self.tutor)
        url = reverse("customsession-detail", args=[self.tutoring_session.id])
        data = {
            "notes": "Bring sketchbook and pencils.",
            "location": "Bafoussam Art Center"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.tutoring_session.refresh_from_db()
        self.assertEqual(self.tutoring_session.notes, "Bring sketchbook and pencils.")
        self.assertEqual(self.tutoring_session.location, "Bafoussam Art Center")

    def test_recurrence_fields(self):
        self.authenticate(self.learner)
        url = reverse("customsession-list")
        data = {
            "session_type": "tutoring",
            "tutor_or_guide_id": self.tutor.id,
            "topic_or_location": "Weekly Bamileke Dance",
            "scheduled_time": (timezone.now() + timedelta(days=5)).isoformat(),
            "duration_minutes": 60,
            "recurrence": "weekly",
            "recurrence_end_date": (timezone.now() + timedelta(days=40)).date().isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["recurrence"], "weekly")
        self.assertIsNotNone(response.data["recurrence_end_date"])

    def test_permissions_flags(self):
        self.authenticate(self.tutor)
        url = reverse("customsession-detail", args=[self.tutoring_session.id])
        data = {"can_communicate": False, "can_share_materials": False}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.tutoring_session.refresh_from_db()
        self.assertFalse(self.tutoring_session.can_communicate)
        self.assertFalse(self.tutoring_session.can_share_materials)

    def test_mark_paid(self):
        self.authenticate(self.tutor)
        self.tutoring_session.mark_paid()
        self.tutoring_session.refresh_from_db()
        self.assertTrue(self.tutoring_session.is_paid)

    def test_external_link_and_price_fields(self):
        self.authenticate(self.tutor)
        url = reverse("customsession-detail", args=[self.tutoring_session.id])
        data = {
            "external_link": "https://zoom.us/j/123456789",
            "price": "15000.00",
            "is_paid": True
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.tutoring_session.refresh_from_db()
        self.assertEqual(str(self.tutoring_session.price), "15000.00")
        self.assertEqual(self.tutoring_session.external_link, "https://zoom.us/j/123456789")
        self.assertTrue(self.tutoring_session.is_paid)

    def test_unique_feedback_per_session_author(self):
        # Complete the session first
        self.tutoring_session.status = 'completed'
        self.tutoring_session.save()
        
        self.authenticate(self.learner)
        url = reverse("sessionfeedback-list")
        data = {
            "session": self.tutoring_session.id,
            "rating": 5,
            "comment": "Very good"
        }
        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED, response1.data)
        self.assertEqual(SessionFeedback.objects.count(), 1)
        
        # Try to submit feedback again for the same session
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SessionFeedback.objects.count(), 1)
        self.assertIn("already submitted", str(response2.data['non_field_errors'][0]))

    def test_cannot_create_session_without_required_fields(self):
        self.authenticate(self.learner)
        url = reverse("customsession-list")
        data = {
            "session_type": "tutoring",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_upload_material_without_file(self):
        self.authenticate(self.tutor)
        url = reverse("sessionmaterial-list")
        data = {
            "session": self.tutoring_session.id,
            "title": "Missing file"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_notification_mark_as_read(self):
        note = InAppNotification.objects.create(user=self.tutor, message="Mark me read", is_read=False)
        self.authenticate(self.tutor)
        url = reverse("inappnotification-detail", args=[note.id])
        response = self.client.patch(url, {"is_read": True})
        self.assertEqual(response.status_code, 200)
        note.refresh_from_db()
        self.assertTrue(note.is_read)

    def test_session_end_time_property(self):
        end_time = self.tutoring_session.end_time
        expected = self.tutoring_session.scheduled_time + timedelta(minutes=self.tutoring_session.duration_minutes)
        self.assertEqual(end_time, expected)

    def test_is_active_property(self):
        self.tutoring_session.status = 'pending'
        self.assertTrue(self.tutoring_session.is_active())
        self.tutoring_session.status = 'confirmed'
        self.assertTrue(self.tutoring_session.is_active())
        self.tutoring_session.status = 'in_progress'
        self.assertTrue(self.tutoring_session.is_active())
        self.tutoring_session.status = 'cancelled'
        self.assertFalse(self.tutoring_session.is_active())
        self.tutoring_session.status = 'completed'
        self.assertFalse(self.tutoring_session.is_active())
        self.tutoring_session.status = 'no_show'
        self.assertFalse(self.tutoring_session.is_active())

    def test_str_methods(self):
        self.assertIn("Tutoring Session with", str(self.tutoring_session))
        
        material = SessionMaterial.objects.create(
            session=self.tutoring_session, 
            title="Brochure", 
            file="dummy.pdf", 
            uploaded_by=self.tutor
        )
        self.assertIn("Brochure for", str(material))
        
        feedback = SessionFeedback.objects.create(
            session=self.tutoring_session, 
            author=self.learner, 
            rating=5
        )
        self.assertIn("★ Feedback by", str(feedback))
        
        note = InAppNotification.objects.create(
            user=self.tutor, 
            message="Hello"
        )
        self.assertIn(f"Notification for {self.tutor.username}", str(note))