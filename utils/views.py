from django.views.generic.base import TemplateView

class APIHomePageView(TemplateView):

    template_name = "api-root.html"

    def get_context_data(self, **kwargs):
        pass
