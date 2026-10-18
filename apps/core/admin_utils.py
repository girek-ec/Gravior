from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html


def image_preview(image, height=60):
    """Miniatura para listados y formularios del admin; vacío si no hay imagen."""
    if not image:
        return '—'
    return format_html('<img src="{}" style="max-height:{}px;max-width:200px;border-radius:4px;" alt="">',
                       image.url, height)


class SingletonAdminMixin:
    """Admin de un modelo singleton: sin crear un segundo registro ni borrar el existente."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        opts = self.model._meta
        instance = self.model.objects.first()
        if instance:
            return redirect(reverse(f'admin:{opts.app_label}_{opts.model_name}_change', args=[instance.pk]))
        return redirect(reverse(f'admin:{opts.app_label}_{opts.model_name}_add'))
