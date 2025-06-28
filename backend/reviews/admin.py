from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "title", "village", "attraction", "festival", "hosting_family", "social_immersion", "created_at")
    list_filter = ("rating", "village", "attraction", "festival", "hosting_family", "social_immersion")
    search_fields = ("title", "content", "user__username")