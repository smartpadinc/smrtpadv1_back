from django.test import TestCase

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from django.contrib.auth.models import User
from user import models as usermod


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
            'login'   : '/api/auth/login',
            'logout'  : '/api/auth/logout',
        }
        self.data = {
            'username'      : '',
            'password'      : 'Test',
            'first_name'    : 'Test',
            'last_name'     : 'Test',
            'email'         : '',
        }


        def test_authenticate_user(self):
            data = {
                'username': 'testuser',
                'password': 'testing'
            }

            response = self.client.post(self.url['login'], self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['success'], True)
