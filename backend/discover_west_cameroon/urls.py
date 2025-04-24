from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/custom_sessions/', include('custom_sessions.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/tutorials/', include('tutorials.urls')),
    path('api/tourism/', include('tourism.urls')),
    path('api/villages/', include('villages.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/festivals/', include('festivals.urls')),
    path('api/support/', include('support.urls')),

 # Social login
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
