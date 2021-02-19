from django.views.generic.base import TemplateView


class IndexTemplateView(TemplateView):
    def get_template_names(self):
        template_name = "employeeapi/index.html"
        return template_name
