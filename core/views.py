from django.http import Http404
from django.views import View
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'core/index.html'


class PendingDetailView(View):
    """Ruta de detalle reservada: responde 404 hasta que su bloque implemente el modelo."""

    def get(self, request, *args, **kwargs):
        raise Http404
