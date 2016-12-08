from django.conf.urls import *
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
admin.autodiscover()

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/user/', include('user.urls')),
    url(r'^api/properties/', include('properties.urls')),
    url(r'^api/swagger/', schema_view),
]
