from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Assignment, AssignmentSubmission
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class AssignmentPermissionsTests(APITestCase):
    def setUp(self):
        self.tutor = User.objects.create_user(
            username="tutor",
            email="tutor@example.com",
            phone_number="+237600000001",
            password="pw",
            role="tutor"
        )
        self.guide = User.objects.create_user(
            username="guide",
            email="guide@example.com",
            phone_number="+237600000002",
            password="pw",
            role="guide"
        )
        self.learner = User.objects.create_user(
            username="learner",
            email="learner@example.com",
            phone_number="+237600000003",
            password="pw",
            role="learner"
        )
        self.other_learner = User.objects.create_user(
            username="otherlearner",
            email="otherlearner@example.com",
            phone_number="+237600000004",
            password="pw",
            role="learner"
        )
        self.visitor = User.objects.create_user(
            username="visitor",
            email="visitor@example.com",
            phone_number="+237600000005",
            password="pw",
            role="visitor"
        )

        # Tutor assigns to learner
        self.tutor_assignment = Assignment.objects.create(
            title="Essay",
            description="Write an essay.",
            due_date=timezone.now() + timedelta(days=3),
            assignment_type="tutoring",
            assigned_by=self.tutor,
            assigned_to=self.learner,
            is_active=True
        )
        # Guide assigns to learner
        self.guide_assignment = Assignment.objects.create(
            title="Tour Reflection",
            description="Describe your tour experience.",
            due_date=timezone.now() + timedelta(days=2),
            assignment_type="tour",
            assigned_by=self.guide,
            assigned_to=self.learner,
            is_active=True
        )

    def tearDown(self):
        Assignment.objects.all().delete()
        AssignmentSubmission.objects.all().delete()
        User.objects.all().delete()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # ---- Learner permissions ----

    def test_learner_sees_own_assignments(self):
        self.authenticate(self.learner)
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)  # Handle pagination
        self.assertEqual(len(data), 2)
        for assignment in data:
            self.assertEqual(assignment['assigned_to'], self.learner.id)

    def test_learner_cannot_see_others_assignments(self):
        self.authenticate(self.other_learner)
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 0)

    def test_learner_can_submit_assignment(self):
        self.authenticate(self.learner)
        url = reverse('assignmentsubmission-list')
        with open(__file__, "rb") as testfile:
            data = {
                "assignment": self.tutor_assignment.id,
                "file": testfile,
            }
            response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 201)
        submission = AssignmentSubmission.objects.get(assignment=self.tutor_assignment, student=self.learner)
        self.assertEqual(submission.assignment, self.tutor_assignment)
        self.assertEqual(submission.student, self.learner)

    def test_learner_sees_only_own_submissions(self):
        AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment, 
            student=self.learner, 
            file="test1.txt",
            is_active=True
        )
        AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment,
            student=self.other_learner,
            file="test2.txt",
            is_active=True
        )
        self.authenticate(self.learner)
        url = reverse('assignmentsubmission-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['student'], self.learner.id)

    def test_learner_cannot_grade_submission(self):
        self.authenticate(self.learner)
        submission = AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment,
            student=self.learner,
            file="test3.txt",
            is_active=True
        )
        url = reverse('assignmentsubmission-grade', args=[submission.id])
        response = self.client.patch(url, {"grade": 18, "feedback": "Good job"}, format="json")
        self.assertEqual(response.status_code, 403)

    # ---- Tutor/Guide permissions ----

    def test_tutor_sees_assigned_assignments(self):
        self.authenticate(self.tutor)
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['assigned_by'], self.tutor.id)

    def test_guide_sees_assigned_assignments(self):
        self.authenticate(self.guide)
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['assigned_by'], self.guide.id)

    def test_tutor_sees_submissions_for_their_assignment(self):
        AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment,
            student=self.learner,
            file="essay.txt",
            is_active=True
        )
        AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment,
            student=self.other_learner,
            file="essay2.txt",
            is_active=True
        )
        self.authenticate(self.tutor)
        url = reverse('assignmentsubmission-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 2)
        self.assertTrue(all(sub['assignment'] == self.tutor_assignment.id for sub in data))

    def test_tutor_can_grade_submission(self):
        submission = AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment,
            student=self.learner,
            file="essay.txt",
            is_active=True
        )
        self.authenticate(self.tutor)
        url = reverse('assignmentsubmission-grade', args=[submission.id])
        data = {"grade": 17.5, "feedback": "Nice work"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(float(submission.grade), 17.5)
        self.assertEqual(submission.feedback, "Nice work")

    def test_guide_cannot_grade_unrelated_submission(self):
        submission = AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment,
            student=self.learner,
            file="essay.txt",
            is_active=True
        )
        self.authenticate(self.guide)
        url = reverse('assignmentsubmission-grade', args=[submission.id])
        data = {"grade": 10}
        response = self.client.patch(url, data, format="json")
        self.assertIn(response.status_code, [403, 404])
        if response.status_code == 404:
            self.assertTrue(AssignmentSubmission.objects.filter(id=submission.id).exists())

    def test_tutor_can_list_submissions_for_assignment(self):
        AssignmentSubmission.objects.create(
            assignment=self.tutor_assignment,
            student=self.learner,
            file="t1.txt",
            is_active=True
        )
        self.authenticate(self.tutor)
        url = reverse('assignment-submissions', args=[self.tutor_assignment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))
        self.assertGreaterEqual(len(response.data), 1)

    # ---- Visitor permissions ----

    def test_visitor_cannot_see_assignments(self):
        self.authenticate(self.visitor)
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 0)

  