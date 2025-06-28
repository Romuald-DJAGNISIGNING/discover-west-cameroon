from django.contrib import admin
from .models import (
    TouristicAttraction, SocialImmersionExperience, HostingFamilyExperience,
    TourismActivity, TouristFeedback, TouristComment, SharedTouristMedia
)

@admin.register(TouristicAttraction)
class TouristicAttractionAdmin(admin.ModelAdmin):
    list_display = ("name", "village", "added_by", "created_at")
    search_fields = ("name", "village__name")

@admin.register(SocialImmersionExperience)
class SocialImmersionAdmin(admin.ModelAdmin):
    list_display = ("title", "village", "start_date", "end_date", "added_by")
    search_fields = ("title", "village__name")

@admin.register(HostingFamilyExperience)
class HostingFamilyAdmin(admin.ModelAdmin):
    list_display = ("family_name", "village", "can_host", "added_by")
    search_fields = ("family_name", "village__name")

@admin.register(TourismActivity)
class TourismActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "attraction", "immersion", "family", "added_by")
    search_fields = ("name",)

@admin.register(TouristFeedback)
class TouristFeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "attraction", "immersion", "family", "created_at")
    search_fields = ("user__username",)

@admin.register(TouristComment)
class TouristCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "attraction", "immersion", "family", "created_at")
    search_fields = ("user__username",)

@admin.register(SharedTouristMedia)
class SharedTouristMediaAdmin(admin.ModelAdmin):
    list_display = ("user", "attraction", "immersion", "family", "created_at")
    search_fields = ("user__username",)