from django.db import models
from projects.models import Project

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField()
    email = models.EmailField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)