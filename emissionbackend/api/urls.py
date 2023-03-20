from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^projects/$', views.getProjects),
    url(r'^projects/([0-9]+)$', views.getProject),
    url(r'^userprofile/$', views.UserProfileAPI),
    url(r'^projectusers/([0-9]+)$', views.ProjectUsersAPI)
]