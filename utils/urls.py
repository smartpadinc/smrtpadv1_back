from django.conf.urls import url, include
from rest_framework import routers
from utils import views as utilview

internal_routers = routers.DefaultRouter()

urlpatterns = [
    url(r'', utilview.APIHomePageView.as_view(), name='api-home'),
]

urlpatterns += internal_routers.urls
