from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def inquiry_url(context, subject=''):
    """Destino de los botones de consulta: WhatsApp si está activo en la configuración; si no, Contacto."""
    config = context.get('site_config')
    whatsapp = config.whatsapp_link(subject) if config else ''
    return whatsapp or reverse('contacto:index')


@register.filter
def slice_columns(items, columns=2):
    """Reparte una lista en `columns` columnas (la primera recibe el sobrante), omitiendo las vacías."""
    items = list(items)
    columns = max(int(columns), 1)
    size = -(-len(items) // columns) if items else 0
    return [items[i:i + size] for i in range(0, len(items), size)] if size else []
