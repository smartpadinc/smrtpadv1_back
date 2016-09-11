from django.conf.urls import url, include
from rest_framework import routers
from properties import views as propview

internal_routers = routers.DefaultRouter()


internal_routers.register(r'account', userview.UserViewSet, 'users')

urlpatterns = internal_routers.urls
