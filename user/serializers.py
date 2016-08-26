from django.contrib.auth.models import User
from rest_framework import serializers
from user import models as model


class UserSerializer(serializers.ModelSerializer):

    # def validate_email(self,value):
    #     raise serializers.ValidationError("Validation is working")
    #     return value

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('last_login','date_joined')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.UserProfile
        fields = ('first_name', 'middle_name','last_name')
