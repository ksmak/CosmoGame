from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """CustomUser admin."""
    list_display = (
        'username',
        'email',
        'is_active',
        'registration_date',
        'change_date'
    )
    list_filter = ('username', )
    search_fields = ('username', )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2', 'email')
        }),
        (_('Permissions'), {
            'classes': ('wide', ),
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (None, {
            'classes': ('wide', ),
            'fields': ('activation_code', 'registration_date', 'change_date')
        })
    )
    fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password', 'email')
        }),
        (_('Permissions'), {
            'classes': ('wide', ),
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (None, {
            'classes': ('wide', ),
            'fields': ('activation_code', 'registration_date', 'change_date')
        })
    )
    readonly_fields = ('activation_code', 'registration_date',
                       'change_date', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)
