from django.test import TestCase

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from django.contrib.auth.models import User

# OAUTH TOOLKIT
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import USER_SETTINGS as oauth2_settings


class UserAuthTestCase(TestCase):
    # initialiaze token/auth
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()

        self.url = {
            'user'    : '/api/user/account',
            'login'   : '/api/auth/login',
            'logout'  : '/api/auth/logout',
        }
        self.data = {
            'username'      : 'Test',
            'password'      : 'Test',
            'first_name'    : 'Test',
            'last_name'     : 'Test',
            'email'         : 'leoangelo.dia123@gmail.com',
            'user_type'     : 2
        }

        # Mock new application - this will be the provider
        Application.objects.create(user=self.user,client_type="confidential", authorization_grant_type="password", name="default")

        # Register new test user
        self.client.post(self.url['user'], self.data, format='json')

    def test_authenticate_user(self):
        response = self.client.post(self.url['login'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

    def test_authenticate_invalid_user(self):
        self.data['username']   = 'Test1'
        self.data['password']   = 'Test1'
        response = self.client.post(self.url['login'], self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], False)

    def test_logout_with_session(self):
        res = self.client.post(self.url['login'], self.data, format='json')
        response = self.client.post(self.url['logout'], **{
            'Authorization': 'Bearer ' + res.data['data']['access_token']
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

    def test_logout_no_session(self):
        res = self.client.post(self.url['login'], self.data, format='json')
        response = self.client.post(self.url['logout'], **{
            'Authorization': 'Bearer ' + res.data['data']['access_token'] + "123"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_must_be_included_on_login_response(self):
        response = self.client.post(self.url['login'], self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(('user' in response.data['data']), True)
