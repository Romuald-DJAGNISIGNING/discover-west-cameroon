

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Quiz, Question, Choice

User = get_user_model()

class QuizModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@gmail.com",
            username="admin",
            phone_number="+237612345678",
            password="adminpass",
            full_name="Admin User"
        )
        self.quiz = Quiz.objects.create(
            title="Culture Quiz",
            description="Test your knowledge about West Cameroon culture",
            created_by=self.user
        )

    def test_quiz_creation(self):
        self.assertEqual(self.quiz.title, "Culture Quiz")
        self.assertEqual(str(self.quiz), "Culture Quiz")

class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="trad@gmail.com",
            username="trad",
            phone_number="+237612345679",
            password="tradpass",
            full_name="Trad User"
        )
        self.quiz = Quiz.objects.create(
            title="Traditions",
            description="Traditional Practices",
            created_by=self.user
        )
        self.question = Question.objects.create(quiz=self.quiz, text="What is the most celebrated festival?")

    def test_question_creation(self):
        self.assertEqual(self.question.text, "What is the most celebrated festival?")
        self.assertEqual(str(self.question), "Question for Traditions")

class ChoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="music@gmail.com",
            username="music",
            phone_number="+237612345680",
            password="musicpass",
            full_name="Music User"
        )
        self.quiz = Quiz.objects.create(
            title="Music",
            description="Traditional Music",
            created_by=self.user
        )
        self.question = Question.objects.create(quiz=self.quiz, text="What is the name of the traditional xylophone?")
        self.choice = Choice.objects.create(question=self.question, text="Balafon", is_correct=True)

    def test_choice_creation(self):
        self.assertEqual(self.choice.text, "Balafon")
        self.assertTrue(self.choice.is_correct)
        self.assertEqual(str(self.choice), "Balafon")
