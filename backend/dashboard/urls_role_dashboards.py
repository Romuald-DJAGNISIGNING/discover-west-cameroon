from django.urls import path
from .views_role_dashboards import (
    AdminDashboardView, VisitorDashboardView, LearnerDashboardView,
    TutorDashboardView, GuideDashboardView
)

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('visitor/', VisitorDashboardView.as_view(), name='visitor-dashboard'),
    path('learner/', LearnerDashboardView.as_view(), name='learner-dashboard'),
    path('tutor/', TutorDashboardView.as_view(), name='tutor-dashboard'),
    path('guide/', GuideDashboardView.as_view(), name='guide-dashboard'),
]