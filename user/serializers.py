from rest_framework import serializers
from user import models as model

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = model.UserProfile
        fields = ('first_name', 'middle_name','last_name')
