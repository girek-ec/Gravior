from django.db.models import Prefetch
from django.views.generic import TemplateView

from .models import Facility, FacilityCategory, FacilityGallery


class FacilityListView(TemplateView):
    """Galería de instalaciones con filtro por categoría en el navegador (isotope de Crafto)."""

    template_name = 'gravior/instalaciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facilities'] = (
            Facility.objects.filter(is_active=True, category__is_active=True)
            .select_related('category')
            .prefetch_related(Prefetch('gallery', queryset=FacilityGallery.objects.filter(is_active=True),
                                       to_attr='active_gallery'))
        )
        context['facility_categories'] = FacilityCategory.objects.filter(
            is_active=True, facilities__is_active=True).distinct()
        return context
