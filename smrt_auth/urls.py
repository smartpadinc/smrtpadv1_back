from django.conf.urls import url, include
from rest_framework import routers
from smrt_auth import views as authview

internal_routers = routers.DefaultRouter()

urlpatterns = [
    url(r'^login$', authview.Login.as_view(), name="auth.login"),
    url(r'^logout$', authview.RevokeSession.as_view(), name="auth.logout"),
]

urlpatterns += internal_routers.urls
