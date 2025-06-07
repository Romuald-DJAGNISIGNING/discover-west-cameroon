from django.contrib import admin
from .models import Village, Attraction, LocalSite

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'population', 'tourism_status', 'featured')
    search_fields = ('name', 'location', 'language')
    list_filter = ('tourism_status', 'featured', 'language')
    ordering = ('name',)

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'village', 'attraction_type', 'tourist_rating')
    search_fields = ('name', 'village__name')
    list_filter = ('attraction_type', 'village')
    ordering = ('name',)

@admin.register(LocalSite)
class LocalSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'village', 'site_type')
    search_fields = ('name', 'village__name')
    list_filter = ('site_type', 'village')
    ordering = ('name',)
