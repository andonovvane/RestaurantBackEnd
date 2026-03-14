from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ('date_joined',)

    # when create new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'table_id')}
         ),
    )

    # when editing useers
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'table_id', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Groups', {'fields': ('groups',)}),
    )

    # shows in user list
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'role', 'table_id')
    ordering = ('email',)


# Register the custom user model
admin.site.register(User, CustomUserAdmin)
