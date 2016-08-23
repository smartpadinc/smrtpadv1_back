from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sample-url/$', views.index, name='index'),
]
