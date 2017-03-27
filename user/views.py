from utils.email import SendEmail  as emailSender
from django.core.signing import Signer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# USER
from user import models as mod
from user import serializers as serializer
from user import filters as filtr
from user.permissions import DefaultPermissions as perm

# DRF
#from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasReadWriteScope, TokenHasScope
from rest_framework import viewsets, mixins, filters, status, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import datetime, timedelta

import logging, string, random, requests, time, hashlib
logger = logging.getLogger(__name__)

CHAR_POOL = string.ascii_letters + string.digits + string.punctuation
SAFE_POOL = string.ascii_letters + string.digits

class UserAccountList(APIView):
    """
        Endpoint for getting user account details
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializer.UserAccountListSerializer

    def get(self, request, pk=None):

        try:
            user_id = pk if pk else request.user.id
            instance = User.objects.get(pk=user_id)
            srlzr = serializer.UserAccountListSerializer(instance)

            return Response({'data': srlzr.data, 'success': True}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'success': False, 'responseMsg': "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)

class UserAccount(APIView):
    """
     Endpoint for registering user
    """
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    serializer_class = serializer.UserSerializer

    def post(self, request):
        # make the request POST mutable so that we can alter the response
        request.POST._mutable = True

        srlzr = serializer.UserSerializer(data=request.data, many=False)

        if srlzr.is_valid():
            if 'email' in request.data:
                # Check if email already exists
                user = User.objects.filter(email=request.data['email'])
                if len(user) > 0:
                    return Response({'responseMsg': "Email address already exists!", 'success': False}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Create new user
                    srlzr.save()

                    # Add profile to newly added user
                    user_type = (request.data['user_type'] if 'user_type' in request.data else 1)
                    user = User.objects.get(email=request.data['email'])

                    if user is not None:
                        # Generate random password for 1st time users if there are no password in request
                        random_password          = ''.join((random.choice(CHAR_POOL)) for x in range(15))
                        request.data['password'] = (request.data['password'] if 'password' in request.data else random_password)

                        # Set encrypted user_password
                        user.set_password(request.data['password'])
                        user.save()

                        # Create User Profile
                        profile = mod.UserProfile()
                        profile.user_id     = user.id
                        profile.user_type   = user_type
                        profile.first_name  = user.first_name
                        profile.last_name   = user.last_name
                        profile.save()

                        # Remove password and csrfmiddlewaretoken in return data
                        request.data['password'], request.data['csrfmiddlewaretoken'] = None, None

                        """
                            Send Email
                        """
                        emailSender.send('welcome', {
                            'recipient_list' : (request.data['email'],),
                            'context': {
                                'first_name': user.first_name,
                                'password'  : random_password
                            }
                        })

                        return Response({'responseMsg': "Successfully Created!", 'data': request.data, 'success': True}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'responseMsg': 'Request failed due to field errors.', 'success': False, 'errors': srlzr.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'responseMsg': "Email field is required.", 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': False, 'errors': srlzr.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    """
     Endpoint for updating account profile
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializer.UserProfileSerializer

    def patch(self, request, user_id, format=None):

        if int(user_id) != int(request.user.id):
            return Response({'responseMsg': 'Request failed. User mismatch.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        request.POST._mutable = True
        instance = mod.UserProfile.objects.get(user_id=request.user.id)
        srlzr = serializer.UserProfileSerializer(instance, data=request.data, partial=True)

        if srlzr.is_valid():
            srlzr.save()

            user = User.objects.get(pk=self.request.user.id)
            user.first_name = request.data['first_name']
            user.last_name  = request.data['last_name']
            user.save()

            return Response({'responseMsg': "Successfully Updated!", 'data': request.data, 'success': True}, status=status.HTTP_200_OK)

        return Response({'responseMsg': 'Request failed due to field errors.', 'success': False, 'errors': srlzr.errors}, status=status.HTTP_400_BAD_REQUEST)

class AccountChangePassword(APIView):
    """
        Endpoint for changing user password
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializer.AccountChangePasswordSerializer

    def post(self, request, format=None):

        instance = User.objects.get(pk=request.user.id)
        srlzr = serializer.AccountChangePasswordSerializer(instance, data=request.data, partial=True)

        if srlzr.is_valid() and 'new_password' in request.data and 'password' in request.data:
            if instance.check_password(request.data['password']):
                instance.set_password(request.data['new_password'])
                instance.save()
                return Response({'responseMsg': "Successfully changed account password.", 'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'responseMsg': "Invalid password.", 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class AccountResetPasswordConfirm(APIView):
    """
        Reset password with confirmation_key
    """
    serializer_class = serializer.AccountResetPasswordConfirmSerializer

    def post(self, request, format=None):
        srlzr = serializer.AccountResetPasswordConfirmSerializer(data=request.data)

        if srlzr.is_valid():

            try:
                signer = Signer()
                signed_key   = signer.unsign(request.data['confirmation_key'])
                confirmation = mod.AccountResetPassword.objects.get(signed_key=signed_key)

                return Response({'responseMsg': "Successfully changed account password.", 'success': True}, status=status.HTTP_200_OK)

            except Exception:
                return Response({'responseMsg': "Invalid confirmation key", 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

class AccountResetPasswordInquiry(APIView):
    """
        Send reset password request
    """
    serializer_class = serializer.AccountResetPasswordSerializer

    def post(self, request, format=None):

        if 'email_address' in request.data:

            """
                Register resetpassword key to be sent on email if the user exists, else, ignore.
                If there's pending/active reset password key and the user issued a reset password request
                again, just update the most recent data.
            """
            try:
                signer = Signer()
                rands  = ''.join((random.choice(SAFE_POOL)) for x in range(20))
                signed = signer.sign(rands)
                user   = User.objects.get(email=request.data['email_address'])

                obj, created = mod.AccountResetPassword.objects.update_or_create(
                    user=user, status='A',
                    defaults={'hash_key': signed, 'signed_key': rands},
                )

                """
                    Send Email
                """
                emailSender.send('forgot-password', {
                    'recipient_list' : (request.data['email_address'],),
                    'context': {'confirmation_key':signed},
                })

            except Exception:
                pass

            return Response({'responseMsg': "We sent a reset password link to your email.", 'success': True}, status=status.HTTP_200_OK)


class OrganizationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = mod.Organization
    serializer_class = serializer.OrganizationSerializer
    allowed_methods = ('GET','POST','PATCH',)

    def create(self, request, *args, **kwargs):
        # make the request POST mutable so that we can alter the response
        request.POST._mutable = True

        serializer = self.get_serializer(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response({'responseMsg': "Successfully added new organization.", 'success': True}, status=status.HTTP_201_CREATED)

        else:
            return Response({'responseMsg': "Request failed due to field errors.", 'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        query = mod.Organization.objects.all()

        if perm.isAdmin(self):
            query = mod.Organization.objects.all()

        return query


"""
class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = User
    serializer_class = serializer.UserSerializer
    allowed_methods = ('GET','POST','PATCH',)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        # make the request POST mutable so that we can alter the response
        request.POST._mutable = True

        serializer = self.get_serializer(data=request.data, many=False)

        if serializer.is_valid():

            if 'email' in request.data:
                # Check if email already exists
                user = User.objects.filter(email=request.data['email'])
                if len(user) > 0:
                    return Response({'responseMsg': "Email address already exists!", 'success': False}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Create new user
                    serializer.save()

                    # Add profile to newly added user
                    user_type = (request.data['user_type'] if 'user_type' in request.data else 1)
                    user = User.objects.get(email=request.data['email'])

                    if user is not None:
                        # Generate random password for 1st time users if there are no password in request
                        chars                    = string.ascii_letters + string.digits + string.punctuation
                        random_password          = ''.join((random.choice(chars)) for x in range(15))
                        request.data['password'] = (request.data['password'] if 'password' in request.data else random_password)

                        # Set encrypted user_password
                        user.set_password(request.data['password'])
                        user.save()

                        # Create User Profile
                        profile = mod.UserProfile()
                        profile.user_id     = user.id
                        profile.user_type   = user_type
                        profile.first_name  = user.first_name
                        profile.last_name   = user.last_name
                        profile.save()

                        # Remove password and csrfmiddlewaretoken in return data
                        request.data['password'], request.data['csrfmiddlewaretoken'] = None, None

                        return Response({'responseMsg': "Successfully Created!", 'data': request.data, 'success': True}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'responseMsg': 'Request failed due to field errors.', 'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'responseMsg': "Email field is required.", 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        # make the request POST mutable so that we can alter the response
        request.POST._mutable = True

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            userprofile = mod.UserProfile.objects.filter(user_id=self.request.user.id)[:1].get()
            userprofile.first_name = (request.data['first_name'] if 'first_name' in request.data else userprofile.first_name)
            userprofile.last_name  = (request.data['last_name'] if 'last_name' in request.data else userprofile.last_name)
            userprofile.save()

            request.data['user_id'] = userprofile.user_id

            return Response({'responseMsg': "Successfully Updated!", 'data': request.data, 'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        query = User.objects.filter(username=self.request.user)
        if perm.isAdmin(self):
            query = User.objects.all()

        return query

    @list_route(methods=['patch'],)
    def change_password(self, request, pk=None):
        user = User.objects.get(pk=self.request.user.id)

        if user is not None and 'old_password' in request.data and 'new_password' in request.data:

            old  = self.request.data['old_password']
            new  = self.request.data['new_password']

            if user.check_password(old):
                user.set_password(new)
                user.save()
                return Response({'responseMsg': "Successfully changed account password.", 'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'responseMsg': "Invalid password.", 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
"""
