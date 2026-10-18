from django.views.generic import TemplateView

from apps.inicio.models import Differential, Statistic


class AboutView(TemplateView):
    template_name = 'gravior/nosotros.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            differentials=Differential.objects.filter(is_active=True, show_about=True),
            statistics=Statistic.objects.filter(is_active=True, show_about=True),
        )
        return context
