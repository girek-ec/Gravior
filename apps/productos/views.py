from django.views.generic import TemplateView


class ProductListView(TemplateView):
    template_name = 'gravior/productos.html'
