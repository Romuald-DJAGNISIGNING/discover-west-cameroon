from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'full_name', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'role', 'is_active', 'gender')
    search_fields = ('email', 'username', 'full_name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'full_name', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'profile_picture', 'id_card', 'gender', 'role', 'location')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'phone_number', 'password1', 'password2', 'role')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)