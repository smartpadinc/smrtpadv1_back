import json
from django.contrib.auth.models import User
from rest_framework import serializers
from user import models as model


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField('get_user_profile')

    def get_user_profile(self, obj):
        try:
           query = model.UserProfile.objects.values().get(user=obj.id)

           del query["userprofile"]
           del query["date_created"]
           del query["last_modified_by_id"]
           del query["last_modified"]

           return query

        except model.UserProfile.DoesNotExist:
           return {}

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email','profile',)
        write_only_fields = ('password',)
        read_only_fields = ('last_login','date_joined')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.UserProfile
        read_only_fields = ('date_created','last_modified_by','last_modified')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Organization
        exclude = ('date_created','last_modified_by','last_modified')
