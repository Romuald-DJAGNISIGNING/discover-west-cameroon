from django.contrib import admin
from .models import TutorialCategory, Tutorial, TutorialComment

@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "created_by", "created_at")
    list_filter = ("category", "is_published", "village", "attraction", "festival")
    search_fields = ("title", "description")
    raw_id_fields = ("created_by",)

@admin.register(TutorialComment)
class TutorialCommentAdmin(admin.ModelAdmin):
    list_display = ("tutorial", "user", "created_at")
    search_fields = ("tutorial__title", "user__username", "comment")