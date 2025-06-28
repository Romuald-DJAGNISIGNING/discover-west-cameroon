from django.urls import path
from . import views_classic

urlpatterns = [
    path('classic/', views_classic.report_list, name='report_list'),
    path('classic/<int:pk>/', views_classic.report_detail, name='report_detail'),
    path('classic/create/', views_classic.report_create, name='report_create'),
    path('classic/<int:pk>/edit/', views_classic.report_edit, name='report_edit'),
    path('classic/<int:pk>/review/', views_classic.report_review, name='report_review'),
]