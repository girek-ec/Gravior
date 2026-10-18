from django.urls import reverse
from django.views.generic import TemplateView

from apps.calidad.views import active_areas
from apps.empresa.models import AboutPage
from apps.genetica.models import GeneticLine

from .models import Differential, HeroSlide, ProcessStep, Statistic

SOLUTION_TABS_MAX = 5
KNOWLEDGE_AREAS_MAX = 3


def solution_tabs():
    """Pestañas "Genética / soluciones" del inicio (sección 18): líneas destacadas y áreas de calidad.

    Cada pestaña es un dict con la misma forma para que el Bloque C pueda sumar productos.
    """
    tabs = []
    for line in GeneticLine.objects.filter(is_active=True, is_featured=True):
        tabs.append({
            'label': line.name, 'title': line.summary, 'text': line.application,
            'focus': line.brand_name, 'image': line.main_image, 'url': reverse('genetica:index'),
        })
    for area in active_areas()[:max(SOLUTION_TABS_MAX - len(tabs), 0)]:
        tabs.append({
            'label': area.name, 'title': area.description, 'text': '',
            'focus': '', 'image': area.image, 'url': reverse('calidad:index'),
        })
    return tabs[:SOLUTION_TABS_MAX]


class HomeView(TemplateView):
    template_name = 'gravior/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            hero_slides=HeroSlide.objects.filter(is_active=True),
            differentials=Differential.objects.filter(is_active=True, show_home=True),
            statistics=Statistic.objects.filter(is_active=True, show_home=True),
            process_steps=ProcessStep.objects.filter(is_active=True),
            about=AboutPage.get_current(),
            solution_tabs=solution_tabs(),
            knowledge_areas=active_areas()[:KNOWLEDGE_AREAS_MAX],
        )
        return context
