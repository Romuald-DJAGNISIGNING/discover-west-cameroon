

from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.CustomSessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/<int:pk>/', views.CustomSessionDetailView.as_view(), name='session-detail'),
    path('sessions/<int:pk>/confirm/', views.ConfirmSessionView.as_view(), name='session-confirm'),
]

