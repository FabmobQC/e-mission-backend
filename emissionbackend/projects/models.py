from django.db import models


TIMEZONES = [
    ('Montreal', 'America/Montreal'),
    ('Toronto', 'America/Toronto'),
]

LANGUAGES = [
    ('fr', 'Francais'),
    ('en', 'English')
]

class FormURL(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    url = models.URLField(max_length=200)

    def __str__(self):
        return f'{str(self.url)}'

class Form(models.Model):
    id = models.AutoField(primary_key=True)
    urls = models.ManyToManyField(FormURL)
    is_active = models.BooleanField(default=True)
    day = models.IntegerField(default=0)
    display_time = models.TimeField()

    def __str__(self):
        return f'{str(self.day)}-{str(self.display_time)}-{str(self.urls.all()[0])}'


class NotificationTitles(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{str(self.language)}-{str(self.title)}'

class NotificationMessages(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    body = models.CharField(max_length=200)

    def __str__(self):
        return f'{str(self.language)}-{str(self.body)}'

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.IntegerField(default=1)
    display_time = models.TimeField()
    titles = models.ManyToManyField(NotificationTitles, related_name="notification_titles")
    messages = models.ManyToManyField(NotificationMessages, related_name="notification_messages")

    def __str__(self):
        return f'{str(self.day)}-{str(self.display_time)}-{str(self.titles.all()[0])}'
    
class EmailSubjects(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{str(self.language)}-{str(self.title)}'

class EmailMessages(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    body = models.CharField(max_length=200)

    def __str__(self):
        return f'{str(self.language)}-{str(self.body)}'

class Email(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.IntegerField(default=1)
    display_time = models.TimeField()
    subjects = models.ManyToManyField(EmailSubjects, related_name="notification_titles")
    messages = models.ManyToManyField(EmailMessages, related_name="notification_messages")

    def __str__(self):
        return f'{str(self.day)}-{str(self.display_time)}-{str(self.subjects.all()[0])}'
    
class ModeTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    value = models.CharField(max_length=200)
    
class Mode(models.Model):
    id = models.AutoField(primary_key=True)
    mode_translations = models.ManyToManyField(ModeTranslation, related_name="mode_translations")

class PurposeTranslation(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    value = models.CharField(max_length=200)

class Purpose(models.Model):
    id = models.AutoField(primary_key=True)
    purpose_translations = models.ManyToManyField(PurposeTranslation, related_name="purpose_translations")

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name_fr = models.CharField(max_length=250)
    name_en = models.CharField(max_length=250)
    server_url = models.URLField(max_length=200)
    timezone = models.CharField(max_length=10, choices=TIMEZONES)
    main_form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="main_form", null=True, blank=True)
    daily_forms = models.ManyToManyField(Form, related_name="daily_forms", blank=True)
    daily_notifications = models.ManyToManyField(Notification, related_name="daily_notifications", blank=True)
    daily_emails = models.ManyToManyField(Email, related_name="daily_emails", blank=True)
    modes = models.ManyToManyField(Mode, blank=True)
    purposes = models.ManyToManyField(Purpose, blank=True)

    def __str__(self):
        return f'{str(self.id)}-{str(self.name_en)}'