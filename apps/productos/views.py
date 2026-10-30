from django.db.models import Prefetch
from django.views.generic import TemplateView

from .models import Product, ProductCategory, ProductDocument, ProductFeature


def active_products():
    return (Product.objects.filter(is_active=True, category__is_active=True)
            .select_related('category')
            .prefetch_related(
                Prefetch('features', queryset=ProductFeature.objects.filter(is_active=True), to_attr='active_features'),
                Prefetch('documents', queryset=ProductDocument.objects.filter(is_active=True),
                         to_attr='active_documents'),
            ))


class ProductListView(TemplateView):
    """Catálogo informativo con filtro por categoría (?categoria=<slug>). Usa el SEO general."""

    template_name = 'gravior/productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = list(ProductCategory.objects.filter(is_active=True, products__is_active=True).distinct())
        selected = next((c for c in categories if c.slug == self.request.GET.get('categoria')), None)
        products = active_products()
        if selected:
            products = products.filter(category=selected)
        context.update(
            product_categories=categories,
            selected_category=selected,
            products=products,
            # La lista "Una propuesta integral" usa las categorías con descripción, en dos columnas.
            category_highlights=[c for c in ProductCategory.objects.filter(is_active=True) if c.description],
        )
        return context
