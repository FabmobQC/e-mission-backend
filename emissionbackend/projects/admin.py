from django.contrib import admin

from projects.models import Project, Form, FormURL, Notification, NotificationTitles, NotificationMessages, ProjectMode, ProjectPurpose
from projects.models import Mode, ModeTranslation
from projects.models import Purpose, PurposeTranslation
from projects.models import Email, EmailSubjects, EmailMessages


class ProjectModeInline(admin.TabularInline):
    model = ProjectMode
    extra = 1


class ProjectPurposeInline(admin.TabularInline):
    model = ProjectPurpose
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectModeInline, ProjectPurposeInline)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Form)
admin.site.register(FormURL)
admin.site.register(Notification)
admin.site.register(NotificationTitles)
admin.site.register(NotificationMessages)
admin.site.register(Mode)
admin.site.register(ModeTranslation)
admin.site.register(Purpose)
admin.site.register(PurposeTranslation)
admin.site.register(Email)
admin.site.register(EmailSubjects)
admin.site.register(EmailMessages)
