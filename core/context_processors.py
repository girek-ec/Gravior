from .models import CallToAction, CorporateEmail, SiteConfiguration, SocialNetwork


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
    }
