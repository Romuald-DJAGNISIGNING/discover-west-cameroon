from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'username', 'full_name', 'phone_number', 'role',
        'gender', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_active', 'role', 'gender')
    search_fields = ('email', 'username', 'full_name', 'phone_number')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': (
                'username', 'full_name', 'phone_number', 'gender', 'role', 'location'
            )
        }),
        ('Media', {'fields': ('profile_picture', 'id_card')}),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'full_name', 'phone_number', 'gender', 'role',
                'location', 'profile_picture', 'id_card', 'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )

