from django.test import TestCase
from django.utils import timezone
from users.models import CustomUser
from .models import CustomSession

class CustomSessionModelTest(TestCase):

    def setUp(self):
        self.tutor = CustomUser.objects.create_user(
            email='tutor@gmail.com',
            username='tutor1',
            phone_number='+237600000001',
            password='strongpass123',
            full_name='Tutor One',
            gender='male',
            role='tutor',
        )
        self.student = CustomUser.objects.create_user(
            email='student@gmail.com',
            username='student1',
            phone_number='+237600000002',
            password='strongpass123',
            full_name='Student One',
            gender='female',
            role='student',
        )

    def test_create_session(self):
        session = CustomSession.objects.create(
            tutor_or_guide=self.tutor,
            student_or_visitor=self.student,
            session_type='educational',
            topic_or_location='History of Cameroon',
            scheduled_time=timezone.now() + timezone.timedelta(days=1),
            duration_minutes=90,
            location='Buea Library',
            notes='Bring textbooks.'
        )
        expected_str = f"{session.session_type.title()} Session with {session.tutor_or_guide.username} on {session.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(session), expected_str)
        self.assertFalse(session.is_confirmed)
