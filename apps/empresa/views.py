from django.views.generic import TemplateView

from apps.core.views import SeoMixin
from apps.inicio.models import Differential, Statistic

from .models import AboutPage, CorporateValue


class AboutView(SeoMixin, TemplateView):
    template_name = 'gravior/nosotros.html'

    def get_seo_object(self):
        return self.about

    def get_context_data(self, **kwargs):
        self.about = AboutPage.get_current()
        context = super().get_context_data(**kwargs)
        context.update(
            about=self.about,
            corporate_values=CorporateValue.objects.filter(is_active=True),
            differentials=Differential.objects.filter(is_active=True, show_about=True),
            statistics=Statistic.objects.filter(is_active=True, show_about=True),
        )
        return context
