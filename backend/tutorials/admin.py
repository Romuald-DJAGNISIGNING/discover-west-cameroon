from django.contrib import admin
from .models import Tutorial, TutorialCategory, TutorialStep

@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(TutorialStep)
class TutorialStepAdmin(admin.ModelAdmin):
    list_display = ('tutorial', 'step_number', 'title')
    search_fields = ('tutorial__title', 'title', 'content')
    list_filter = ('tutorial',)
    ordering = ('tutorial', 'step_number')
