from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from userprofile.models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ('email', 'username',
                    'project', 'is_active', 'is_superuser')
