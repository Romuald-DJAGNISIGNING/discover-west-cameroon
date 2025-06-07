from django.contrib import admin
from .models import Assignment, AssignmentSubmission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_by', 'assigned_to', 'due_date', 'created_at')
    list_filter = ('assigned_by', 'assigned_to', 'due_date')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')
    list_filter = ('assignment', 'student')
