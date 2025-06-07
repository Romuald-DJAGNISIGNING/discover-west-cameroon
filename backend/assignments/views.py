from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Assignment, AssignmentSubmission
from .serializers import (
    AssignmentSerializer, AssignmentCreateSerializer,
    AssignmentSubmissionSerializer, AssignmentSubmissionCreateSerializer
)
from users.models import CustomUser

class AssignmentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        user = self.request.user
        # If user is tutor/guide, show assignments assigned by them
        if user.role in ['tutor', 'guide']:
            return Assignment.objects.filter(assigned_by=user)
        # If user is student, show assignments assigned to them
        return Assignment.objects.filter(assigned_to=user)

class AssignmentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class AssignmentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()

class AssignmentSubmissionCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSubmissionCreateSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class AssignmentSubmissionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        # Tutors/guides see submissions for assignments they assigned
        if user.role in ['tutor', 'guide']:
            return AssignmentSubmission.objects.filter(assignment__assigned_by=user)
        # Students see their own submissions
        return AssignmentSubmission.objects.filter(student=user)

class AssignmentSubmissionDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSubmissionSerializer
    queryset = AssignmentSubmission.objects.all()

    def patch(self, request, *args, **kwargs):
        # Allow tutors/guides to grade and give feedback
        submission = self.get_object()
        user = request.user
        if user.role in ['tutor', 'guide'] and submission.assignment.assigned_by == user:
            grade = request.data.get('grade')
            feedback = request.data.get('feedback')
            if grade is not None:
                submission.grade = grade
            if feedback is not None:
                submission.feedback = feedback
            submission.save()
            serializer = self.get_serializer(submission)
            return Response(serializer.data)
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentCreateSerializer
        return AssignmentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
