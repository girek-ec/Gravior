from django.views.generic import TemplateView

from .models import Differential, HeroSlide, ProcessStep, Statistic


class HomeView(TemplateView):
    template_name = 'gravior/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            hero_slides=HeroSlide.objects.filter(is_active=True),
            differentials=Differential.objects.filter(is_active=True, show_home=True),
            statistics=Statistic.objects.filter(is_active=True, show_home=True),
            process_steps=ProcessStep.objects.filter(is_active=True),
        )
        return context
