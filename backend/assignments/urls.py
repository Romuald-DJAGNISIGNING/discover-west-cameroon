

from django.urls import path
from .views import (
    AssignmentListView,
    AssignmentCreateView,
    AssignmentDetailView,
    AssignmentSubmissionCreateView,
    AssignmentSubmissionListView,
    AssignmentSubmissionDetailView,
)

urlpatterns = [
    path('assignments/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    
    path('submissions/', AssignmentSubmissionListView.as_view(), name='submission-list'),
    path('submissions/create/', AssignmentSubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/', AssignmentSubmissionDetailView.as_view(), name='submission-detail'),
]
