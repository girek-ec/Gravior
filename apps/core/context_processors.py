from django.templatetags.static import static

from .models import CallToAction, CorporateEmail, SiteConfiguration, SocialNetwork

# Imágenes de la maqueta usadas mientras no se carguen las oficiales en la configuración general.
FALLBACK_LOGO = 'crafto/images/demo-gym-and-fitness-logo-black.png'
FALLBACK_LOGO_WHITE = 'crafto/images/demo-gym-and-fitness-logo-white.png'
FALLBACK_FAVICON = 'crafto/images/favicon.png'


def _image_url(image, fallback):
    return image.url if image else static(fallback)


def site(request):
    """Datos corporativos globales para header, footer, WhatsApp y SEO por defecto.

    Funciona aunque todavía no exista la configuración: las variables quedan vacías.
    """
    if request.path.startswith('/admin/'):
        return {}
    config = SiteConfiguration.get_current()
    return {
        'site_config': config,
        'corporate_emails': list(CorporateEmail.objects.filter(is_active=True)),
        'social_networks': list(SocialNetwork.objects.filter(is_active=True)),
        'whatsapp_url': config.whatsapp_url if config else '',
        # Llamados a la acción por identificador: {{ ctas.header_contact.button_text }}
        'ctas': {cta.code: cta for cta in CallToAction.objects.filter(is_active=True)},
        'logo_url': _image_url(config and config.logo, FALLBACK_LOGO),
        'logo_white_url': _image_url(config and config.logo_white, FALLBACK_LOGO_WHITE),
        'favicon_url': _image_url(config and config.favicon, FALLBACK_FAVICON),
    }
