from django.conf.urls import url, include
from rest_framework import routers
from properties import views as propview

internal_routers = routers.DefaultRouter()

internal_routers.register(r'search', propview.UnitPropertySearchViewSet, 'properties-search')
internal_routers.register(r'manage', propview.UnitPropertyManageViewSet, 'properties-manage')

urlpatterns = internal_routers.urls
