from django.views.generic import TemplateView


class QualityView(TemplateView):
    template_name = 'calidad/calidad_bioseguridad.html'
