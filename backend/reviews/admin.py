from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user_email', 'target_type', 'target_id', 'rating', 'short_comment', 'parent_id', 'created_at'
    )
    search_fields = ('user__email', 'target_type', 'comment')
    list_filter = ('rating', 'target_type', 'created_at')
    ordering = ('-created_at',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def short_comment(self, obj):
        return (obj.comment[:40] + '...') if obj.comment and len(obj.comment) > 40 else obj.comment
    short_comment.short_description = 'Comment'

    def parent_id(self, obj):
        return obj.parent.id if obj.parent else None
    parent_id.short_description = 'Parent Review ID'
