from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from swagger_custom_generator.schema_generator import MySchemaGenerator

class SwaggerSchemaView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = MySchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
