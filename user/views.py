from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


from user import models as  mod
from user import serializers as serializer
from rest_framework import viewsets, mixins, filters, status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView

class UserProfileViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    model = mod.UserProfile
    serializer_class = serializer.UserProfileSerializer
    queryset = mod.UserProfile.objects.all()
