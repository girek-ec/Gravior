from django.views.generic import TemplateView


class PostListView(TemplateView):
    template_name = 'gravior/actualidad.html'


class PostDetailView(TemplateView):
    """Muestra la maqueta del detalle para cualquier slug; en el bloque E pasa a DetailView de Post."""

    template_name = 'gravior/actualidad-detalle.html'
