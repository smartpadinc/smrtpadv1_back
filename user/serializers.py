import json
from django.contrib.auth.models import User
from rest_framework import serializers
from user import models as model


class UserSerializer(serializers.ModelSerializer):

    # def validate_email(self,value):
    #     raise serializers.ValidationError("Validation is working")
    #     return value
    profile = serializers.SerializerMethodField('get_user_profile')

    def get_user_profile(self, obj):
        #profile_queryset = model.UserProfile.objects.all().filter(user=request.user, status='A')
        #serializer = AccountUserActiveSerializer(instance=accounts_queryset, many=True, context=self.context)
        #query = model.UserProfile.objects.all().filter(user=obj.id)
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
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email','profile')
        write_only_fields = ('password',)
        read_only_fields = ('last_login','date_joined')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.UserProfile
        read_only_fields = ('userprofile','date_created','last_modified_by')
