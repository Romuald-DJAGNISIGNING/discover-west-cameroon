from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Review

User = get_user_model()

class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@gmail.com",
            username="testuser",
            full_name="Test User",
            phone_number="+237612345678",
            password="testpass123"
        )
        self.review = Review.objects.create(
            user=self.user,
            comment="This is a great tour!",
            rating=5,
            target_type="guide",
            target_id=1
        )

    def test_review_creation(self):
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(self.review.comment, "This is a great tour!")

    def test_nested_reply(self):
        reply = Review.objects.create(
            user=self.user,
            comment="Thanks for the feedback!",
            rating=5,
            target_type="guide",
            target_id=1,
            parent=self.review
        )
        self.assertEqual(reply.parent, self.review)
        self.assertEqual(self.review.replies.count(), 1)
