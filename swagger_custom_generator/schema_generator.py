from rest_framework.schemas import SchemaGenerator


class MySchemaGenerator(SchemaGenerator):
    title = 'REST API Index'

    def get_link(self, path, method, view):
        link = super(MySchemaGenerator, self).get_link(path, method, view)
        link._fields += self.get_core_fields(view)
        return link

    def get_core_fields(self, view):
        return getattr(view, 'coreapi_fields', ())
