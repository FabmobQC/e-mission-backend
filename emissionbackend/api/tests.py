from django.test import TestCase
from django.contrib.auth import get_user_model

from projects.models import Project
from userprofile.models import UserProfile

from rest_framework.test import APIClient


class UserProfileTestCase(TestCase):

    project1 = ""

    def setUp(self):

        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", username="testuser", password="foo")
        
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.project1 = Project.objects.create()

        UserProfile.objects.create(uuid='f94f8d80-50db-4fb1-b08e-2984da52e34a',
                            email='myemail@business.com', project=self.project1)

        UserProfile.objects.create(uuid='7d5b8250-5f8f-4ffc-b521-019690e1402e',
                            email='myemail2@business.com', project=self.project1)        

    def test_add_user_profile(self):
        client = APIClient()

        data = {
            'uuid': 'f94f8d80-50db-4fb1-b08e-2984da52e34a',
            'email': 'myemail@business.com', 
            'project': str(self.project1.id)
        }

        response = client.post('/api/userprofile/', data, format='json')
        
        assert response.status_code == 201

    def test_get_project_user_profiles_no_authentication(self):
        client = APIClient()

        response = client.get(f'/api/projectusers/{self.project1.id}')
        
        assert response.status_code == 403

    def test_get_project_user_profiles_authenticated(self):

        client = APIClient()


        client.login(username='testuser', password='foo')

        response = client.get(f'/api/projectusers/{self.project1.id}')
        
        assert response.status_code == 200