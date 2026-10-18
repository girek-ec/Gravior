from django.http import Http404
from django.views import View


class PendingDetailView(View):
    """Ruta de detalle reservada: responde 404 hasta que su bloque implemente el modelo."""

    def get(self, request, *args, **kwargs):
        raise Http404


class SeoMixin:
    """Pasa seo_title / seo_description del objeto principal; base.html usa los generales si están vacíos."""

    def get_seo_object(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_seo_object()
        context['seo_title'] = getattr(obj, 'seo_title', '')
        context['seo_description'] = getattr(obj, 'seo_description', '')
        return context
