from rest_framework import serializers
from .models import Assignment, AssignmentSubmission

class AssignmentSerializer(serializers.ModelSerializer):
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at', 'due_date',
            'assignment_type', 'assigned_by', 'assigned_by_username', 'assigned_to', 'assigned_to_username',
            'attachment', 'external_link', 'is_active'
        ]
        read_only_fields = ('created_at', 'updated_at', 'assigned_by', 'assigned_by_username')

    def validate(self, data):
        request = self.context.get('request')
        assigned_by = data.get('assigned_by') or getattr(self.instance, 'assigned_by', None) or request.user
        assigned_to = data.get('assigned_to') or getattr(self.instance, 'assigned_to', None)
        assignment_type = data.get('assignment_type') or getattr(self.instance, 'assignment_type', None)

        # Only tutors or guides can assign, only learners can be assigned
        if assignment_type == 'tutoring':
            if getattr(assigned_by, 'role', None) != 'tutor':
                raise serializers.ValidationError("Assigned by must be a tutor for tutoring assignments.")
        elif assignment_type == 'tour':
            if getattr(assigned_by, 'role', None) != 'guide':
                raise serializers.ValidationError("Assigned by must be a guide for tour assignments.")
        if getattr(assigned_to, 'role', None) != 'learner':
            raise serializers.ValidationError("Only a learner can be assigned an assignment.")
        return data

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'assignment_title', 'student', 'student_username',
            'submitted_at', 'file', 'comment', 'grade', 'feedback', 'is_active'
        ]
        read_only_fields = ('submitted_at', 'student', 'student_username')

    def validate(self, data):
        student = data.get('student') or self.context['request'].user
        if getattr(student, 'role', None) != 'learner':
            raise serializers.ValidationError("Only learners can submit assignments.")
        return data