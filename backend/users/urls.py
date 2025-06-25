from django.urls import path
from .views import (
    CustomUserListView,
    CustomUserDetailView,
    CurrentUserView,
    RegisterUserView,
    RegisterLearnerView,
    RegisterTutorView,
    RegisterGuideView,
    RegisterVisitorView,
    dashboard_auth_guard,
)

urlpatterns = [
    # 🔐 Authenticated user info
    path('me/', CurrentUserView.as_view(), name='current-user'),

    # 👤 General + role-based registration
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('register/learner/', RegisterLearnerView.as_view(), name='register-learner'),
    path('register/tutor/', RegisterTutorView.as_view(), name='register-tutor'),
    path('register/guide/', RegisterGuideView.as_view(), name='register-guide'),
    path('register/visitor/', RegisterVisitorView.as_view(), name='register-visitor'),

    # 🛡️ API auth check for frontend redirects
    path('auth-guard/', dashboard_auth_guard, name='dashboard-auth-guard'),

    # 🛠️ Admin access
    path('', CustomUserListView.as_view(), name='user-list'),
    path('<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
]
