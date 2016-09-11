from properties import models as  mod
from properties import serializers as serializer
from rest_framework import viewsets, mixins, filters, status, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from django.contrib import admin
admin.autodiscover()

import string, random

class UnitPropertySearchViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    model = mod.UnitProperty
    serializer_class = serializer.UnitPropertySerializer
    allowed_methods = ('GET',)

    def get_queryset(self):
        query = mod.UnitProperty.objects.all()
        if IsAdminUser():
            query = mod.UnitProperty.objects.all()

        return query


class UnitPropertyManageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    model = mod.UnitProperty
    serializer_class = serializer.UnitPropertySerializer
    allowed_methods = ('POST','PATCH',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response({'responseMsg': "Successfully added property.", 'success': 'true'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'responseMsg': 'Request failed due to field errors.', 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        query = mod.UnitProperty.objects.all()
        if IsAdminUser():
            query = mod.UnitProperty.objects.all()

        return query
