

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@gmail.com',
            'username': 'testuser',
            'full_name': 'Test User',
            'phone_number': '+237612345678',
            'gender': 'male',
            'role': 'student',
            'location': 'Buea',
        }

    def test_create_user_with_gmail(self):
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            phone_number=self.user_data['phone_number'],
            password='strongpassword123',
            full_name=self.user_data['full_name'],
            gender=self.user_data['gender'],
            role=self.user_data['role'],
            location=self.user_data['location']
        )
        self.assertEqual(user.email, 'testuser@gmail.com')
        self.assertTrue(user.check_password('strongpassword123'))

    def test_reject_non_gmail_email(self):
        with self.assertRaises(ValidationError):
            user = User(
                email='wrongemail@yahoo.com',
                username='wronguser',
                phone_number='+237612345679',
                full_name='Wrong User',
                gender='female',
                role='guide',
                location='Dschang'
            )
            user.full_clean()  # Trigger validation

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@gmail.com',
            username='admin',
            phone_number='+237612345680',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
