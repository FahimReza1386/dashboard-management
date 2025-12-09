# Django Imports
from django.contrib import admin

# Third-Party Imports
from unfold.admin import ModelAdmin

# Locale Imports
from accounts.models.users import Users


@admin.register(Users)
class UsersAdmin(ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )
    search_fields = ('email', 'first_name', 'last_name', 'national_code', 'phone_number')
    list_filter = ('is_active', 'is_staff')
    ordering = ('-id',)
    
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'national_code', 'phone_number', 'avatar')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        # ('Important Dates', {
        #     'fields': ('created_at', 'updated_at')
        # }),
    )