from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', include('utils.urls', namespace='baseview')),
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/user/', include('user.urls')),
    url(r'^api/auth/', include('smrt_auth.urls')),
    #url(r'^api/properties/', include('properties.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
