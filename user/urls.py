from django.conf.urls import url, include
from rest_framework import routers
from user import views as userview

internal_routers = routers.DefaultRouter()

internal_routers.register(r'account', userview.UserViewSet, 'users')
internal_routers.register(r'profile', userview.UserProfileViewSet, 'user-profile')
internal_routers.register(r'organization', userview.OrganizationViewSet, 'organization')

urlpatterns = internal_routers.urls

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
