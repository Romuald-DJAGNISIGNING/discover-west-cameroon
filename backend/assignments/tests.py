

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Assignment, AssignmentSubmission

User = get_user_model()

class AssignmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tutor = User.objects.create_user(
            email='tutor@gmail.com',
            username='tutor1',
            phone_number='+237612345678',
            password='pass1234',
            role='tutor'
        )
        self.student = User.objects.create_user(
            email='student@gmail.com',
            username='student1',
            phone_number='+237612345679',
            password='pass1234',
            role='student'
        )
        self.client.force_authenticate(user=self.tutor)

    def test_create_assignment(self):
        url = reverse('assignment-create')
        data = {
            'title': 'Test Assignment',
            'description': 'This is a test assignment.',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Assignment.objects.get().title, 'Test Assignment')

    def test_list_assignments(self):
        Assignment.objects.create(title='Assignment 1', description='Desc 1', created_by=self.tutor)
        Assignment.objects.create(title='Assignment 2', description='Desc 2', created_by=self.tutor)
        url = reverse('assignment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class AssignmentSubmissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tutor = User.objects.create_user(
            email='tutor@gmail.com',
            username='tutor1',
            phone_number='+237612345678',
            password='pass1234',
            role='tutor'
        )
        self.student = User.objects.create_user(
            email='student@gmail.com',
            username='student1',
            phone_number='+237612345679',
            password='pass1234',
            role='student'
        )
        self.assignment = Assignment.objects.create(title='Test Assignment', description='Desc', created_by=self.tutor)
        self.client.force_authenticate(user=self.student)

    def test_create_submission(self):
        url = reverse('submission-create')
        data = {
            'assignment': self.assignment.id,
            'content': 'My submission content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssignmentSubmission.objects.count(), 1)
        self.assertEqual(AssignmentSubmission.objects.get().content, 'My submission content')

    def test_list_submissions(self):
        AssignmentSubmission.objects.create(assignment=self.assignment, student=self.student, content='Content 1')
        AssignmentSubmission.objects.create(assignment=self.assignment, student=self.student, content='Content 2')
        url = reverse('submission-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
