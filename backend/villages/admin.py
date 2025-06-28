from django.contrib import admin
from .models import Village, VillageImage, VillageComment

class VillageImageInline(admin.TabularInline):
    model = VillageImage
    extra = 1

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "population", "tourism_status")
    search_fields = ("name", "department", "main_languages")
    inlines = [VillageImageInline]

admin.site.register(VillageImage)
admin.site.register(VillageComment)