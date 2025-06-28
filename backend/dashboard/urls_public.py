from django.urls import path
from .views_public import WelcomeDashboardView, WhatAboutUsView, ContactUsView

urlpatterns = [
    path('welcome/', WelcomeDashboardView.as_view(), name='welcome-dashboard'),
    path('about/', WhatAboutUsView.as_view(), name='what-about-us'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
]