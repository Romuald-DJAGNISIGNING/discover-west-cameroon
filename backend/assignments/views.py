from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer

class IsLearner(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'learner'

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, 'role', None) in ('tutor', 'guide')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, 'role', None) in ('tutor', 'guide')

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Assignment.objects.filter(is_active=True)
        
        if getattr(user, 'role', None) == 'learner':
            return queryset.filter(assigned_to=user)
        elif getattr(user, 'role', None) == 'tutor':
            return queryset.filter(assigned_by=user, assignment_type='tutoring')
        elif getattr(user, 'role', None) == 'guide':
            return queryset.filter(assigned_by=user, assignment_type='tour')
        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def submissions(self, request, pk=None):
        assignment = self.get_object()
        if assignment.assigned_by != request.user and assignment.assigned_to != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        
        submissions = assignment.submissions.filter(is_active=True)
        serializer = AssignmentSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSubmissionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['grade', 'partial_update', 'update']:
            return [permissions.IsAuthenticated(), IsStaffOrReadOnly()]
        else:
            return [permissions.IsAuthenticated(), IsLearner()]

    def get_queryset(self):
        user = self.request.user
        queryset = AssignmentSubmission.objects.filter(is_active=True)
        
        if getattr(user, 'role', None) == 'learner':
            return queryset.filter(student=user)
        elif getattr(user, 'role', None) == 'tutor':
            return queryset.filter(assignment__assigned_by=user, assignment__assignment_type='tutoring')
        elif getattr(user, 'role', None) == 'guide':
            return queryset.filter(assignment__assigned_by=user, assignment__assignment_type='tour')
        return queryset.none()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = super().get_object()
        
        # Additional permission check for staff roles
        user = self.request.user
        if getattr(user, 'role', None) in ('tutor', 'guide'):
            if user != obj.assignment.assigned_by:
                self.permission_denied(self.request)
        return obj

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsStaffOrReadOnly])
    def grade(self, request, pk=None):
        submission = self.get_object()
        if submission.assignment.assigned_by != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        
        grade = request.data.get('grade')
        feedback = request.data.get('feedback')
        
        if grade is not None:
            submission.grade = grade
        if feedback is not None:
            submission.feedback = feedback
        
        submission.save()
        return Response(AssignmentSubmissionSerializer(submission).data)