from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication & Registration
    path('auth/', include('dj_rest_auth.urls')),  # Login, logout, password change/reset
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Sign-up
    path('accounts/', include('allauth.urls')),  # Handles Google OAuth flow

    # Custom app routes (modular API endpoints)
    path('api/users/', include('users.urls')),
    path('api/custom_sessions/', include('custom_sessions.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/festivals/', include('festivals.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/support/', include('support.urls')),
    path('api/tourism/', include('tourism.urls')),
    path('api/tutorials/', include('tutorials.urls')),
    path('api/villages/', include('villages.urls')),
]

# Static & Media serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
