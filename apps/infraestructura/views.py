from django.views.generic import TemplateView


class FacilityListView(TemplateView):
    template_name = 'gravior/instalaciones.html'
