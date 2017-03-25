from django.test import TestCase

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from django.contrib.auth.models import User
from user import models as usermod

import json

class UserTestCase(TestCase):
    # initialiaze token/auth
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()

        self.url = {
            'user'                   : '/api/user/account',
            'user_change_password'   : '/api/user/change_password',
            'user_profile'           : '/api/user/profile/',
            'reset_password_inquiry' : '/api/user/reset_password/inquiry',
            'organization'           : '/api/organization',
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
        response = self.client.get(self.url['user'] + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_new_valid_account_authorized(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Test'
        self.data['email']      = 'leoangelo.dia123@gmail.com'
        self.data['user_type']  = 2

        response = self.client.post(self.url['user'], self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], True)

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
        self.assertEqual(response.data['success'], True)

    def test_add_new_valid_account_duplicate_email(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'anothertest'
        self.data['email']      = 'test1234@test.com'

        self.client.post(self.url['user'], self.data, format='json')

        self.data['username']   = 'Test3'
        self.data['email']      = 'test1234@test.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)

    def test_add_new_valid_account_duplicate_username(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'anothertest'
        self.data['email']      = 'test1234@test.com'

        self.client.post(self.url['user'], self.data, format='json')

        self.data['username']   = 'anothertest'
        self.data['email']      = 'test12345@test.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)

    def test_add_new_invalid_account_authorized(self):
        self.client.login(username='testuser', password='testing')

        self.data['username']   = 'Invalid Username'
        self.data['email']      = 'leoangelo.dia123@gmail.com'

        response = self.client.post(self.url['user'], self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)

    def test_change_password(self):
        self.client.login(username='testuser', password='testing')

        data = {
            "password" : 'testing',
            "new_password" : 'demo1234',
        }

        response = self.client.post(self.url['user_change_password'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

    def test_change_invalid_password(self):
        self.client.login(username='testuser', password='testing')

        data = {
            "password" : 'testing123',
            "new_password" : 'demo1234',
        }

        response = self.client.post(self.url['user_change_password'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)

    def test_get_user_profile(self):
        self.client.login(username='testuser', password='testing')
        response = self.client.get(self.url['user'] + '/{}'.format(str(self.user.id)) )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        self.client.login(username='testuser', password='testing')

        self.data['first_name'] = 'Leo'
        self.data['last_name']  = 'Diaz'

        address = [
            {'line1' : 'address line 1'},
            {'line2' : 'address line 2'}
        ]

        profile = usermod.UserProfile()
        profile.user_id     = self.user.id
        profile.user_type   = 1
        profile.first_name  = 'Leo'
        profile.middle_name = 'L'
        profile.birthdate   = '1991-01-01'
        profile.mobile_no   = '6586954125'
        profile.address     = json.dumps(address)
        profile.city        = 'Makati'
        profile.state       = 'Manila'
        profile.country     = 'PH'
        profile.zip_code    = '1234'
        profile.identification_type = '1'
        profile.identification_no   = '123456'
        profile.img_url     = 'http://imgur.com/gallery/ggWm4'
        profile.fb_url      = 'https://www.facebook.com/prinsipeleo'

        profile.save()

        response = self.client.patch(self.url['user_profile'] + "{}/".format(str(self.user.id)), self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_inquiry(self):
          self.data['email_address'] = "testuser@test.com"
          self.client.post(self.url['reset_password_inquiry'], self.data, format='json')

          count = usermod.AccountResetPassword.objects.filter(user=self.user,status='A').count()

          self.assertEqual(count, 1)

    def test_reset_password_inquiry_invalid_user(self):
          self.data['email_address'] = "testuser123@test.com"
          self.client.post(self.url['reset_password_inquiry'], self.data, format='json')

          count = usermod.AccountResetPassword.objects.filter(user=self.user,status='A').count()

          self.assertEqual(count, 0)
