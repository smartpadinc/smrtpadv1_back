from django.contrib.auth.models import User
from rest_framework import serializers
from user import models as model

class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, max_length=32)
