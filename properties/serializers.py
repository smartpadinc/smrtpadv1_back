from django.contrib.auth.models import User
from rest_framework import serializers
from properties import models as model

class UnitPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = model.UnitProperty
        exclude = ('property_code','date_created','last_modified_by','last_modified')
