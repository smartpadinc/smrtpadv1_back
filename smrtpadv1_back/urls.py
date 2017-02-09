from django.conf.urls import *
from django.contrib import admin
from swagger_custom_generator.swagger_view import SwaggerSchemaView
admin.autodiscover()

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^docs2/', SwaggerSchemaView.as_view()),
    #url(r'^docs2/', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/user/', include('user.urls')),
    url(r'^api/properties/', include('properties.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
