from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportCreateView.as_view(), name='create-report'),
    path('all/', views.ReportListView.as_view(), name='list-reports'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
]
