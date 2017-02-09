from django.conf.urls import url, include
from rest_framework import routers
from user import views as userview

internal_routers = routers.DefaultRouter()

#internal_routers.register(r'account', userview.UserViewSet, 'users')
#internal_routers.register(r'profile', userview.UserProfileViewSet, 'user-profile')
internal_routers.register(r'organization', userview.OrganizationViewSet, 'organization')

urlpatterns = [
    url(r'^sample-url/$', userview.index, name='index'),

    url(r'^account$', userview.UserAccountList.as_view(), name="user.register"),
    url(r'^register$', userview.UserAccount.as_view(), name="user.register"),
    url(r'^profile/(?P<pk>[0-9]+)/$', userview.UserProfile.as_view(), name="user.profile"),
    url(r'^change_password/(?P<pk>[0-9]+)/$', userview.AccountChangePassword.as_view(), name="change.password"),
]

urlpatterns += internal_routers.urls


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
