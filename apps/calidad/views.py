from django.db.models import Prefetch
from django.views.generic import TemplateView

from apps.core.views import SeoMixin

from .models import QualityArea, QualityPage, QualityStep


def active_areas():
    return QualityArea.objects.filter(is_active=True).prefetch_related(
        Prefetch('steps', queryset=QualityStep.objects.filter(is_active=True), to_attr='active_steps'))


class QualityView(SeoMixin, TemplateView):
    template_name = 'gravior/servicios.html'

    def get_seo_object(self):
        return self.quality_page

    def get_context_data(self, **kwargs):
        self.quality_page = QualityPage.get_current()
        context = super().get_context_data(**kwargs)
        areas = list(active_areas())
        context.update(
            quality_page=self.quality_page,
            quality_areas=areas,
            # Contadores de la maqueta calculados con el contenido publicado (no son cifras comerciales).
            areas_count=len(areas),
            steps_per_area=max((len(area.active_steps) for area in areas), default=0),
        )
        return context
