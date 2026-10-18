from django.utils.html import format_html


def image_preview(image, height=60):
    """Miniatura para listados y formularios del admin; vacío si no hay imagen."""
    if not image:
        return '—'
    return format_html('<img src="{}" style="max-height:{}px;max-width:200px;border-radius:4px;" alt="">',
                       image.url, height)
