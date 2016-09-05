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
from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()

class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = User
    serializer_class = serializer.UserSerializer
    queryset = User.objects.all()
    allowed_methods = ('GET','POST','PATCH',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=False)

        if serializer.is_valid():

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

        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            super(UserViewSet, self).partial_update(request, *args, **kwargs)
            return Response({'responseMsg': "Successfully Created!", 'data': request.data, 'success': 'true'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
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
                u.save()
                return Response({'responseMsg': "Successfully changed account password.", 'success': 'true'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'responseMsg': "Invalid password.", 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = mod.UserProfile
    serializer_class = serializer.UserProfileSerializer
    queryset = mod.UserProfile.objects.all()
