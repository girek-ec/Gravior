from django.views.generic import TemplateView


class PostListView(TemplateView):
    template_name = 'actualidad/actualidad.html'
