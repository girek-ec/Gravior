from django.views.generic import TemplateView

from .models import Partner


class PartnerView(TemplateView):
    template_name = 'gravior/aliados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partners = list(Partner.objects.filter(is_active=True))
        context.update(
            partners=partners,
            # El carrusel muestra solo aliados con reseña aprobada.
            carousel_partners=[partner for partner in partners if partner.description],
            hero_partner=next((partner for partner in partners if partner.image), None),
        )
        return context
