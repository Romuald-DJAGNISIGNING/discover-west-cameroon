from django.contrib import admin
from .models import (
    Festival, FestivalMedia, FestivalFact, FestivalComment, FestivalBookmark,
    FestivalAttendance, FestivalFeedback
)

class FestivalMediaInline(admin.TabularInline):
    model = FestivalMedia
    extra = 1

class FestivalFactInline(admin.TabularInline):
    model = FestivalFact
    extra = 1

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "village", "start_date", "is_annual", "average_rating", "popularity_score")
    inlines = [FestivalMediaInline, FestivalFactInline]
    search_fields = ("name", "description", "village__name")

admin.site.register(FestivalComment)
admin.site.register(FestivalBookmark)
admin.site.register(FestivalAttendance)
admin.site.register(FestivalFeedback)