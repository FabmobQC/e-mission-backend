from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from userprofile.models import Server, User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ('token', 'email', 'get_projects',
                    'is_active', 'is_superuser')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if not obj:  # add_fieldsets
            fieldsets = (
                ("Authentication", {
                 'fields': ('email', 'password1', 'password2',)}),
                ("Personal ino", {
                 'fields': ('first_name', 'last_name', 'server',)}),
            )
        else:
            fieldsets = (
                ("Authentication",
                    {'fields': ('email', 'password',)}),
                ("Personal ino",
                    {'fields': ('first_name', 'last_name', 'server',)}),
                ("Permissions", {
                 'fields': ('groups', 'user_permissions',)}),
                ("Activity", {
                 'fields': ('is_active', 'last_login', 'date_joined',)}),
            )
        return fieldsets

    @admin.display(description='Projects')
    def get_projects(self, obj):
        return "|".join([p.id for p in obj.projects.all()])


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    class Meta:
        model = Server
        fields = '__all__'
    list_display = ('id', 'url', 'max_users')
