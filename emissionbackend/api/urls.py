from django.urls import re_path
from django.urls.conf import include
from api import views as api_views
from userprofile import views as user_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename="users")
router.register(r'projects', api_views.ProjectViewSet, basename="projects")
router.register(r'projects_cfg', api_views.ConfigurationViewSet,
                basename="projects_cfg")

urlpatterns = [
    re_path(
        r'^projectusers/([0-9]+)$',
        api_views.ProjectUsersAPI
    ),
    re_path('^login/',
            user_views.LoginView.as_view(),
            name='login'
            ),
    re_path('^logout/',
            user_views.LogoutView.as_view(),
            name='logout'
            ),

    re_path('', include(router.urls)),
]
