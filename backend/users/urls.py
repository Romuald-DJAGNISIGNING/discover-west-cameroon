

from django.urls import path
from .views import (
    CustomUserListView,
    CustomUserDetailView,
    CurrentUserView,
    RegisterUserView
)

urlpatterns = [
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('', CustomUserListView.as_view(), name='user-list'),
    path('<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
]
