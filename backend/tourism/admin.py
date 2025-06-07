from django.contrib import admin
from .models import (
    Category, Attraction, LocalSite, TourPlan, TourActivity, TourReview, TourCategory,
    TourPhoto, TourGuide, TourTransport, TourTransportBooking, TourEvent, TourEventRegistration,
    TourFeedback, TourItinerary, TourMap, TourSafetyInfo, TourWeatherInfo,
    TourCulturalExperience, TourCulturalExperienceBooking, TourCulturalExperienceReview
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'added_by')
    search_fields = ('name', 'location')
    list_filter = ('category',)

@admin.register(LocalSite)
class LocalSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'added_by')
    search_fields = ('name', 'location')

@admin.register(TourPlan)
class TourPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'guide', 'price', 'duration_days', 'created_at')
    search_fields = ('title', 'guide__username')
    filter_horizontal = ('attractions',)

@admin.register(TourActivity)
class TourActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'attraction', 'date', 'time', 'created_by')
    search_fields = ('title', 'attraction__name')
    list_filter = ('date',)

@admin.register(TourReview)
class TourReviewAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'user', 'rating', 'created_at')
    search_fields = ('attraction__name', 'user__username')
    list_filter = ('rating', 'created_at')

@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(TourPhoto)
class TourPhotoAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'caption', 'uploaded_by', 'created_at')
    search_fields = ('caption', 'attraction__name', 'uploaded_by__username')

@admin.register(TourGuide)
class TourGuideAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'available')
    search_fields = ('user__username', 'expertise')
    list_filter = ('available',)

@admin.register(TourTransport)
class TourTransportAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'available')
    search_fields = ('name',)
    list_filter = ('available',)

@admin.register(TourTransportBooking)
class TourTransportBookingAdmin(admin.ModelAdmin):
    list_display = ('transport', 'user', 'date', 'time', 'created_at')
    search_fields = ('transport__name', 'user__username')
    list_filter = ('date',)

@admin.register(TourEvent)
class TourEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'created_by')
    search_fields = ('title', 'location', 'created_by__username')
    list_filter = ('date',)

@admin.register(TourEventRegistration)
class TourEventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registered_at')
    search_fields = ('event__title', 'user__username')

@admin.register(TourFeedback)
class TourFeedbackAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'user', 'rating', 'created_at')
    search_fields = ('attraction__name', 'user__username', 'feedback_text')
    list_filter = ('rating',)

@admin.register(TourItinerary)
class TourItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'created_by__username')
    filter_horizontal = ('attractions',)

@admin.register(TourMap)
class TourMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'created_by__username')
    filter_horizontal = ('attractions',)

@admin.register(TourSafetyInfo)
class TourSafetyInfoAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'created_by', 'created_at')
    search_fields = ('attraction__name', 'created_by__username')

@admin.register(TourWeatherInfo)
class TourWeatherInfoAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'average_temperature', 'best_visit_season', 'created_by', 'created_at')
    search_fields = ('attraction__name', 'best_visit_season', 'created_by__username')

@admin.register(TourCulturalExperience)
class TourCulturalExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'attraction', 'date', 'time', 'price', 'available_slots', 'booked_slots', 'is_active')
    search_fields = ('title', 'attraction__name', 'created_by__username')
    list_filter = ('is_active', 'date')

@admin.register(TourCulturalExperienceBooking)
class TourCulturalExperienceBookingAdmin(admin.ModelAdmin):
    list_display = ('experience', 'user', 'booked_at', 'number_of_slots')
    search_fields = ('experience__title', 'user__username')

@admin.register(TourCulturalExperienceReview)
class TourCulturalExperienceReviewAdmin(admin.ModelAdmin):
    list_display = ('experience', 'user', 'rating', 'created_at')
    search_fields = ('experience__title', 'user__username')
    list_filter = ('rating', 'created_at')
