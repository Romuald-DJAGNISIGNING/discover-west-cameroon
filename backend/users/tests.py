from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email='test@gmail.com',
            username='testuser',
            phone_number='+237612345678',
            password='testpass123',
            full_name='Test User',
            gender='male',
            role='student'
        )
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'student')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@gmail.com',
            username='adminuser',
            phone_number='+237612345679',
            password='adminpass123',
            full_name='Admin User',
            gender='female',
            role='tutor'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)