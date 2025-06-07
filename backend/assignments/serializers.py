from rest_framework import serializers
from .models import Assignment, AssignmentSubmission
from users.models import CustomUser

class AssignmentSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    assigned_to = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'created_at', 'due_date', 'created_by', 'assigned_to']

class AssignmentCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'assigned_to']

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    assignment = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'submitted_at', 'file', 'grade', 'feedback']

class AssignmentSubmissionCreateSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())

    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'file']
