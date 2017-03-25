from django.contrib.auth.models import User
from rest_framework import serializers
from user import models as model

import time

class UserAccountListSerializer(serializers.ModelSerializer):

    # http://stackoverflow.com/questions/22264368/how-to-override-django-unique-error-message-for-username-in-custom-userchangef
    # first_name = serializers.CharField(
    #     unique=True,
    #     min_length=5,
    #     error_messages={
    #         "unique": u"Dapat Unique!",
    #         "blank": "Password cannot be empty.",
    #         "min_length": "Password too short.",
    #     },
    #)

    profile = serializers.SerializerMethodField('get_user_profile')

    def get_user_profile(self, obj):
        try:
           query = model.UserProfile.objects.values().get(user=obj.id)

           del query["last_modified_by_id"]

           return query

        except model.UserProfile.DoesNotExist:
           return {}

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','profile')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('last_login','date_joined')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.UserProfile
        exclude = ('userprofile','date_created','last_modified_by','last_modified','user','user_type')

class AccountChangePasswordSerializer(serializers.ModelSerializer):
     new_password = serializers.CharField(required=True, max_length=32)

     class Meta:
         model = User
         fields = ('password','new_password',)

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.Organization
        exclude = ('date_created','last_modified_by','last_modified')
