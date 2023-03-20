from django.test import TestCase

from projects.models import Project
from userprofile.models import UserProfile

from rest_framework.test import APIClient

class UserProfileTestCase(TestCase):

    project1 = ""

    def setUp(self):

        self.project1 = Project.objects.create()


    def test_add_user_profile(self):
        client = APIClient()

        data = {
            'uuid': 'f94f8d80-50db-4fb1-b08e-2984da52e34a',
            'email': 'myemail@business.com', 
            'project': str(self.project1.id)
        }

        response = client.post('/api/userprofile/', data, format='json')
        
        assert response.status_code == 201