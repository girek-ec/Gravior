from django.views.generic import TemplateView


class TeamView(TemplateView):
    template_name = 'equipo/equipo.html'


class PartnerView(TemplateView):
    template_name = 'equipo/aliados.html'
