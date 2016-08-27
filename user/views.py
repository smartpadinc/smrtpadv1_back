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
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()

class UserViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = User
    serializer_class = serializer.UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        if 'email' in request.data:
            user = User.objects.filter(email=request.data['email'])
            if len(user) > 0:
                return Response({'responseMsg': "Email address already exists!", 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                super(UserViewSet, self).create(request, *args, **kwargs)
                request.data['password'], request.data['csrfmiddlewaretoken'] = None, None

                return Response({'responseMsg': "Successfully Created!", 'data': request.data, 'success': 'true'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'responseMsg': "Email field is required.", 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    model = mod.UserProfile
    serializer_class = serializer.UserProfileSerializer
    queryset = mod.UserProfile.objects.all()
