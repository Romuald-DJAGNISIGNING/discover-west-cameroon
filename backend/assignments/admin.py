from django.contrib import admin
from .models import Assignment, AssignmentSubmission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignment_type', 'assigned_by', 'assigned_to', 'due_date', 'is_active', 'created_at')
    list_filter = ('assignment_type', 'assigned_by', 'assigned_to', 'due_date', 'is_active')
    search_fields = ('title', 'description', 'assigned_by__username', 'assigned_to__username')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade', 'is_active')
    list_filter = ('assignment', 'student', 'is_active')
    search_fields = ('assignment__title', 'student__username', 'comment')