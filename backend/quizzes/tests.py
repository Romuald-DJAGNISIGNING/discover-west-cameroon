from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from villages.models import Village
from tourism.models import TouristicAttraction
from .models import Quiz, Question, Choice, QuizAttempt, QuestionResponse

User = get_user_model()

class QuizAppTests(APITestCase):
    def setUp(self):
        # Users
        self.tutor = User.objects.create_user(
            username='tutor',
            email='tutor@example.com',
            phone_number='+237600000019',
            password='pw',
            role='tutor'
        )
        self.learner = User.objects.create_user(
            username='learner',
            email='learner@example.com',
            phone_number='+237600000020',
            password='pw',
            role='learner'
        )
        self.village = Village.objects.create(name="Bafoussam", department="Mifi", description="Capital", population=10000)
        self.attraction = TouristicAttraction.objects.create(
            name="Museum", description="Museum desc", village=self.village, added_by=self.tutor
        )
        self.client.force_authenticate(user=self.tutor)
        # Create a quiz
        self.quiz = Quiz.objects.create(title="Village Quiz", description="Test", village=self.village, created_by=self.tutor)
        self.q1 = Question.objects.create(quiz=self.quiz, text="Largest city?", type="mcq", order=1)
        self.c1 = Choice.objects.create(question=self.q1, text="Bafoussam", is_correct=True)
        self.c2 = Choice.objects.create(question=self.q1, text="Foumban", is_correct=False)
        self.q2 = Question.objects.create(quiz=self.quiz, text="Describe a festival.", type="open", order=2)
        self.q3 = Question.objects.create(quiz=self.quiz, text="Select foods", type="multi", order=3)
        self.c3 = Choice.objects.create(question=self.q3, text="Koki", is_correct=True)
        self.c4 = Choice.objects.create(question=self.q3, text="Ndolé", is_correct=True)
        self.c5 = Choice.objects.create(question=self.q3, text="Pizza", is_correct=False)

    def test_quiz_list(self):
        url = reverse('quiz-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        
        # Handle both paginated and non-paginated responses
        data = resp.data['results'] if 'results' in resp.data else resp.data
        self.assertTrue(any([quiz['title'] == "Village Quiz" for quiz in data]))

    def test_create_quiz_by_tutor(self):
        url = reverse('quiz-list')
        data = {
            "title": "Tourism Quiz",
            "description": "Quiz desc",
            "village": self.village.id
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)

    def test_quiz_detail_view(self):
        url = reverse('quiz-detail', args=[self.quiz.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], "Village Quiz")

    def test_learner_cannot_create_quiz(self):
        self.client.force_authenticate(user=self.learner)
        url = reverse('quiz-list')
        data = {"title": "Fail Quiz"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 403)
        # Adding this to be more explicit about expected error
        self.assertIn('permission', resp.data['detail'].lower()) 

    def test_attempt_quiz_and_submit(self):
        self.client.force_authenticate(user=self.learner)
        url = reverse('quiz-start', args=[self.quiz.id])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        attempt_id = resp.data['attempt_id']
        submit_url = reverse('quizattempt-submit', args=[attempt_id])
        # All correct
        data = {
            "responses": [
                {"question": self.q1.id, "selected_choices": [self.c1.id]},
                {"question": self.q2.id, "text_answer": "Ngouon Festival"},
                {"question": self.q3.id, "selected_choices": [self.c3.id, self.c4.id]}
            ]
        }
        resp = self.client.post(submit_url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        attempt = QuizAttempt.objects.get(id=attempt_id)
        self.assertTrue(attempt.score > 0)

    def test_tutor_adds_feedback(self):
        self.client.force_authenticate(user=self.learner)
        start_url = reverse('quiz-start', args=[self.quiz.id])
        resp = self.client.post(start_url)
        attempt_id = resp.data["attempt_id"]
        submit_url = reverse('quizattempt-submit', args=[attempt_id])
        self.client.post(submit_url, {"responses": []}, format='json')
        self.client.force_authenticate(user=self.tutor)
        feedback_url = reverse('quizattempt-feedback', args=[attempt_id])
        resp = self.client.post(feedback_url, {"feedback": "Well done"})
        self.assertEqual(resp.status_code, 200)
        attempt = QuizAttempt.objects.get(id=attempt_id)
        self.assertEqual(attempt.feedback, "Well done")