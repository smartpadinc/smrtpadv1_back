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
            'user'                  : '/api/user/account/',
            'user_change_password'  : '/api/user/account/change_password/',
            'user_profile'          : '/api/user/profile/',
            'organization'          : '/api/user/organization/',
        }
        self.data = {
            'username'      : '',
            'password'      : 'Test',
            'first_name'    : 'Test',
            'last_name'     : 'Test',
            'email'         : '',
        }

    def test_get_user_account(self):
        self.client.login(username='testuser', password='testing')
        response = self.client.get(self.url['user'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_new_valid_account_authorized(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Test'
        self.data['email']      = 'leoangelo.dia123@gmail.com'
        self.data['user_type']  = 2

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'true')

    def test_ensure_correct_field_value_onsave(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Test'
        self.data['email']      = 'leoangelo.dia123@gmail.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rd = response.data['data']
        self.assertEqual(rd['username'], self.data['username'])
        self.assertEqual(rd['email'], self.data['email'])
        self.assertEqual(rd['first_name'], self.data['first_name'])
        self.assertEqual(rd['last_name'], self.data['last_name'])
        self.assertEqual(response.data['success'], 'true')

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
        self.assertEqual(response.data['success'], 'false')

    def test_add_new_valid_account_duplicate_username(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'anothertest'
        self.data['email']      = 'test1234@test.com'

        self.client.post(self.url['user'], self.data, format='json')

        self.data['username']   = 'anothertest'
        self.data['email']      = 'test12345@test.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], 'false')

    def test_add_new_invalid_account_authorized(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Invalid Username'
        self.data['email']      = 'leoangelo.dia123@gmail.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], 'false')

    def test_change_password(self):
        self.client.login(username='testuser', password='testing')

        data = {
            "old_password" : 'testing',
            "new_password" : 'demo1234',
        }

        response = self.client.patch(self.url['user_change_password'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'true')

    def test_change_invalid_password(self):
        self.client.login(username='testuser', password='testing')

        data = {
            "old_password" : 'testing123',
            "new_password" : 'demo1234',
        }

        response = self.client.patch(self.url['user_change_password'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], 'false')

    def test_get_user_profile(self):
        self.client.login(username='testuser', password='testing')
        response = self.client.get(self.url['user_profile'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_add_new_profile(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Test'
        self.data['email']      = 'leoangelo.dia123@gmail.com'
        self.data['first_name'] = 'Leo'
        self.data['last_name']  = 'Diaz'
        self.data['user_type']  = 2
        self.client.post(self.url['user'], self.data, format='json')

        response = self.client.get(self.url['user_profile'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_organization(self):
        self.client.login(username='testuser', password='testing')
        response = self.client.get(self.url['organization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
