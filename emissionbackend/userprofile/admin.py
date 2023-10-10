from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from userprofile.models import Server, User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ('token', 'username', 'email', 'project', 'server',
                    'is_active', 'is_superuser')
    ordering = ('email',)
    required_fields = ('email', 'username')

    def get_fieldsets(self, request, obj=None):
        if not obj:  # add_fieldsets
            fieldsets = (
                ("Authentication", {
                 'fields': ('username', 'email', 'password1', 'password2',)}),
                ("Personal ino", {
                 'fields': ('first_name', 'last_name', 'server',)}),
            )
        else:
            fieldsets = (
                ("Authentication",
                    {'fields': ('username', 'email', 'password',)}),
                ("Personal ino",
                    {'fields': ('first_name', 'last_name', 'server',)}),
                ("Permissions", {
                 'fields': ('groups', 'user_permissions',)}),
                ("Activity", {
                 'fields': ('is_active', 'last_login', 'date_joined',)}),
            )
        return fieldsets


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    class Meta:
        model = Server
        fields = '__all__'
    list_display = ('id', 'url', 'max_users')
    required_fields = ('url', 'max_users', 'project')
