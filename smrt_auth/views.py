from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings

# USER
from smrt_auth import serializers as serializer
from user.serializers import UserProfileSerializer
from user.models import UserProfile

# DRF
#from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasReadWriteScope, TokenHasScope
from rest_framework import viewsets, mixins, filters, status, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

# OAUTH TOOLKIT
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import USER_SETTINGS as oauth2_settings

from datetime import datetime, timedelta

import logging, string, random, requests
logger = logging.getLogger(__name__)

class Login(APIView):
    serializer_class = serializer.AuthSerializer

    def post(self, request):
        if 'username' in request.data and 'password' in request.data:
            user = authenticate(username=request.data['username'], password=request.data['password'])

            if user is not None:

                # get the default application details e.g clien_id, client_secret
                application = Application.objects.get(name="default")

                # Set expiration - default to 30mins
                expiration  = timezone.now() + timedelta(seconds=oauth2_settings['ACCESS_TOKEN_EXPIRE_SECONDS'])

                # Delete previous access/refresh token
                AccessToken.objects.filter(user=user, application=application).delete()
                RefreshToken.objects.filter(user=user, application=application).delete()

                access_token = AccessToken.objects.create(
                    user=user,
                    scope='',
                    expires=expiration,
                    token=''.join((random.choice(string.ascii_letters+string.digits)) for x in range(50)),
                    application=application ,
                )
                access_token.save()

                refresh_token = RefreshToken(
                    user=user,
                    token=''.join((random.choice(string.ascii_letters+string.digits)) for x in range(50)),
                    application=application,
                    access_token=access_token
                )
                refresh_token.save()

                try:
                    instance = UserProfile.objects.get(user_id=user.id)
                    srlzr = UserProfileSerializer(instance)
                except UserProfile.DoesNotExist:
                    srlzr = None

                data = {
                    'access_token'      : access_token.token,
                    'token_expiration'  : oauth2_settings['ACCESS_TOKEN_EXPIRE_SECONDS'],
                    'user'              : srlzr.data if srlzr is not None else {}
                }

                return Response({'responseMsg': "Authentication successful!", 'success': True, 'data': data}, status=status.HTTP_200_OK)
            else:
                return Response({'responseMsg': "Invalid username or password", 'success': False}, status=status.HTTP_200_OK)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class RevokeSession(APIView):
    """
        Endpoint for revoking user session
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk=None):
        user = User.objects.get(pk=request.user.id)

        if user is not None:

            # get the default application details e.g clien_id, client_secret
            application = Application.objects.get(name="default")

            # Delete all access/refresh token
            AccessToken.objects.filter(user=user, application=application).delete()
            RefreshToken.objects.filter(user=user, application=application).delete()

            return Response({'success': True, 'responseMsg': "User successfully logout"}, status=status.HTTP_200_OK)

        else:
            return Response({'success': False, 'responseMsg': "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)
