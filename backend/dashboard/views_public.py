from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from villages.models import Village
from festivals.models import Festival
from tourism.models import TouristicAttraction
from tutorials.models import Tutorial
from users.models import CustomUser as AppUser

class WelcomeDashboardView(APIView):
    permission_classes = []  # Public endpoint

    def get(self, request):
        featured_village = Village.objects.order_by('-population').values('name', 'description', 'population').first()
        featured_festival = Festival.objects.order_by('start_date').values('name', 'start_date', 'location').first()
        featured_attraction = TouristicAttraction.objects.order_by('-id').values('name', 'description', 'village__name').first()
        featured_tutorial = Tutorial.objects.order_by('-created_at').values('title', 'category__name', 'created_at').first()
        site_stats = {
            "registered_users": AppUser.objects.count(),
            "total_festivals": Festival.objects.count(),
            "total_touristic_attractions": TouristicAttraction.objects.count(),
            "total_tutorials": Tutorial.objects.count(),
        }
        testimonials = [
            _("Discover West Cameroon made my trip unforgettable! — A happy traveler"),
            _("The guides and tutors are top-notch! — A satisfied learner"),
        ]
        platform_news = [
            _("Welcome to our new dashboard experience!"),
            _("Check out the latest events and book your place."),
        ]
        return Response({
            "featured_village": featured_village,
            "featured_festival": featured_festival,
            "featured_attraction": featured_attraction,
            "featured_tutorial": featured_tutorial,
            "site_stats": site_stats,
            "testimonials": testimonials,
            "platform_news": platform_news,
        }, status=status.HTTP_200_OK)

class WhatAboutUsView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({
            "title": _("About Discover West Cameroon"),
            "mission": _("To celebrate, preserve, and share the rich cultural and natural heritage of the West Cameroon region."),
            "vision": _("A world where the culture, traditions, and beauty of West Cameroon are recognized, respected, and enjoyed by all."),
            "team": [
                {"name": "Romuald DJAGNISIGNING", "role": _("Founder & Architect")},
                {"name": _("Your Team Members"), "role": _("Collaborators & Guides")},
            ],
            "region_focus": _("West Cameroon Region: its villages, festivals, languages, and natural wonders."),
            "history": _("Created in 2025 to empower locals and travelers with authentic discovery experiences.")
        }, status=status.HTTP_200_OK)

class ContactUsView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({
            "email": "contact@discoverwestcameroon.com",
            "phone": "+237 6XX-XXX-XXX",
            "support_link": "/support/classic/",
            "address": _("Bafoussam, West Cameroon"),
            "social": [
                {"platform": "Facebook", "url": "https://facebook.com/discoverwestcameroon"},
                {"platform": "Instagram", "url": "https://instagram.com/discoverwestcameroon"},
            ]
        }, status=status.HTTP_200_OK)