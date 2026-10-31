from django.views.generic import TemplateView

from .models import TeamMember


class TeamView(TemplateView):
    """Equipo técnico: el primer integrante va en la tarjeta destacada y el resto en la grilla."""

    template_name = 'gravior/equipo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members = list(TeamMember.objects.filter(is_active=True))
        context.update(
            team_members=members,
            lead_member=members[0] if members else None,
            other_members=members[1:],
        )
        return context
