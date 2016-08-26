from django.conf.urls import url, include
from rest_framework import routers
from user import views as userview

api_routers = routers.DefaultRouter()


api_routers.register(r'users', userview.UserViewSet, 'users')

urlpatterns = api_routers.urls

# http://tutorial.djangogirls.org/en/django_urls/

"""
test_routers = routers.DefaultRouter()
test_routers.register(r'sample-url1', userview.UserProfileViewSet, 'user-profile')
urlpatterns += test_routers.urls
"""

"""
from . import views
urlpatterns = [
    url(r'^sample-url/$', views.index, name='index'),
]
"""
