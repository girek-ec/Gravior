from django.db.models import Prefetch
from django.views.generic import TemplateView

from apps.core.views import SeoMixin

from .models import GeneticDocument, GeneticFeature, GeneticLine


def active_lines():
    return GeneticLine.objects.filter(is_active=True).prefetch_related(
        Prefetch('features', queryset=GeneticFeature.objects.filter(is_active=True), to_attr='active_features'),
        Prefetch('documents', queryset=GeneticDocument.objects.filter(is_active=True), to_attr='active_documents'),
    )


class GeneticLineListView(SeoMixin, TemplateView):
    """Listado de líneas; usa el SEO general (no hay página propia en el modelo de datos)."""

    template_name = 'gravior/genetica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genetic_lines'] = active_lines()
        return context
