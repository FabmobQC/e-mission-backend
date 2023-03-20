from django.test import TestCase

from projects.models import Project
from .models import UserProfile


class UserProfileTestCase(TestCase):

    def test_create_userprofile(self):
        project1 = Project.objects.create()
        user1 = UserProfile.objects.create(uuid='f94f8d80-50db-4fb1-b08e-2984da52e34a',
                            email='myemail@business.com', project=project1)

        assert user1.project.id == project1.id