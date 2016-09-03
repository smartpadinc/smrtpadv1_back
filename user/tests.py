from django.test import TestCase

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from django.contrib.auth.models import User

# Create your tests here.

class UserManagementTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()

        self.url = {
            'user' : '/api/user-management/users/',
        }
        self.data = {
            'username'      : '',
            'password'      : 'Test',
            'first_name'    : 'Test',
            'last_name'     : 'Test',
            'email'         : '',
        }

    def test_add_new_valid_account_authorized(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Test'
        self.data['email']      = 'leoangelo.dia123@gmail.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_new_valid_account_unauthorized(self):
        self.data['username']   = 'Test2'
        self.data['email']      = 'leoangelo.dia123@gmail.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_new_valid_account_duplicate_email(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'anothertest'
        self.data['email']      = 'test1234@test.com'

        self.client.post(self.url['user'], self.data, format='json')

        self.data['username']   = 'Test3'
        self.data['email']      = 'test1234@test.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_new_invalid_account_authorized(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Invalid Username'
        self.data['email']      = 'leoangelo.dia123@gmail.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
