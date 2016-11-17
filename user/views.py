from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

from user import models as  mod
from user import serializers as serializer
#from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasReadWriteScope, TokenHasScope
from rest_framework import viewsets, mixins, filters, status, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from django.contrib import admin
admin.autodiscover()

import string, random

class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = User
    serializer_class = serializer.UserSerializer
    allowed_methods = ('GET','POST','PATCH',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=False)

        if serializer.is_valid():

            if 'email' in request.data:

                # Check if email already exists
                user = User.objects.filter(email=request.data['email'])
                if len(user) > 0:
                    return Response({'responseMsg': "Email address already exists!", 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
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

                        return Response({'responseMsg': "Successfully Created!", 'data': request.data, 'success': 'true'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'responseMsg': "Email field is required.", 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'responseMsg': "Successfully Created!", 'data': request.data, 'success': 'true'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # Permissions: show only the details of authorized_user unless the user is admin

        query = User.objects.filter(username=self.request.user)
        if IsAdminUser():
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
                return Response({'responseMsg': "Successfully changed account password.", 'success': 'true'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'responseMsg': "Invalid password.", 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = mod.UserProfile
    serializer_class = serializer.UserProfileSerializer
    allowed_methods = ('GET','POST','PATCH',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=False)
        self.request.data['user_id'] = self.request.user.id

        if serializer.is_valid():
            serializer.save()
            return Response({'responseMsg': "Successfully changed user profile.", 'success': 'true'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'responseMsg': 'User has already existing profile. Update it instead.', 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        query = mod.UserProfile.objects.filter(user_id=self.request.user.id)
        if IsAdminUser():
            query = mod.UserProfile.objects.all()

        return query

class OrganizationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = mod.Organization
    serializer_class = serializer.OrganizationSerializer
    allowed_methods = ('GET','POST','PATCH',)

    def get_queryset(self):
        query = mod.Organization.objects.all()
        if IsAdminUser():
            query = mod.Organization.objects.all()

        return query
