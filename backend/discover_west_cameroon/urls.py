from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # API Documentation (if you add DRF Spectacular or similar later)
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Health check endpoint
    path('health/', include('health_check.urls')),
]

# Internationalized URLs
urlpatterns += i18n_patterns(
    # Authentication endpoints
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),
    
    # API endpoints
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
    path('api/tutorials/', include('tutorials.urls')),  # Simplified include without namespace
    path('api/villages/', include('villages.urls')),
    path('api/notifications/', include('notifications.urls')),
    
    # JWT Token Refresh
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
)

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns