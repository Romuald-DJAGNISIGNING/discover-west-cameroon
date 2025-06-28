from django.urls import path
from .views import (
    CustomRegisterView, CustomLoginView, UserProfileView, UserProfileUpdateView, UserListView
)

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='rest_register'),
    path('login/', CustomLoginView.as_view(), name='rest_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('all/', UserListView.as_view(), name='all_users'),
]