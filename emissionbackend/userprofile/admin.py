from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from userprofile.models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ('email', 'get_projects', 'is_active', 'is_superuser')
    ordering = ('email',)

    @admin.display(description='Projects')
    def get_projects(self, obj):
        return "|".join([p.id for p in obj.projects.all()])
