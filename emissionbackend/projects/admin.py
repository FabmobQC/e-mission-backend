from django.contrib import admin

from projects.models import Project, Form, FormURL, Notification, NotificationTitles, NotificationMessages

admin.site.register(Project)
admin.site.register(Form)
admin.site.register(FormURL)
admin.site.register(Notification)
admin.site.register(NotificationTitles)
admin.site.register(NotificationMessages)
