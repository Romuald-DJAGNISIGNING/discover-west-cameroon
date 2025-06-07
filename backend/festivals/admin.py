from django.contrib import admin
from .models import Festival

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_date', 'end_date', 'is_featured')
    search_fields = ('name', 'location', 'description')
    list_filter = ('is_featured', 'start_date')
