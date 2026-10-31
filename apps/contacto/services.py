"""Servicios del formulario de contacto: límite de envíos por IP y aviso por correo."""

import logging

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.urls import reverse

from apps.core.models import CorporateEmail, SiteConfiguration

logger = logging.getLogger(__name__)

COMMERCIAL_TYPES = (CorporateEmail.EmailType.COMMERCIAL, CorporateEmail.EmailType.SALES)


def client_ip(request):
    """IP del cliente. Se usa REMOTE_ADDR: detrás de un proxy hay que configurarlo en el despliegue."""
    return request.META.get('REMOTE_ADDR', '') or 'desconocida'


def rate_limit_exceeded(request):
    """Cuenta los envíos por IP en la caché de Django y avisa si se superó el límite de la ventana."""
    limit = getattr(settings, 'CONTACT_RATE_LIMIT', 5)
    window = getattr(settings, 'CONTACT_RATE_WINDOW', 3600)
    key = f'contacto:envios:{client_ip(request)}'
    cache.add(key, 0, timeout=window)
    try:
        attempts = cache.incr(key)
    except ValueError:  # la clave expiró entre add() e incr()
        cache.set(key, 1, timeout=window)
        attempts = 1
    return attempts > limit


def notification_recipients():
    """Correos del equipo comercial: CorporateEmail comerciales/ventas activos, luego todos los activos,
    luego el correo general de la configuración. Nunca se muestran en la página."""
    active = CorporateEmail.objects.filter(is_active=True)
    recipients = list(active.filter(email_type__in=COMMERCIAL_TYPES).values_list('email', flat=True))
    if not recipients:
        recipients = list(active.values_list('email', flat=True))
    if not recipients:
        config = SiteConfiguration.get_current()
        if config and config.main_email:
            recipients = [config.main_email]
    return recipients


def notify_new_message(message, request=None):
    """Envía el aviso con el mailer por defecto (MAILERS). Si falla, se registra y no se interrumpe al usuario."""
    recipients = notification_recipients()
    if not recipients:
        logger.warning('Mensaje de contacto %s sin destinatarios configurados para el aviso.', message.pk)
        return False
    admin_url = reverse('admin:contacto_contactmessage_change', args=[message.pk])
    if request is not None:
        admin_url = request.build_absolute_uri(admin_url)
    lines = [
        'Nuevo mensaje desde el formulario de contacto del sitio web.',
        '',
        f'Nombre: {message.name}',
        f'Correo: {message.email}',
        f'Empresa: {message.company or "—"}',
        f'Cargo: {message.position or "—"}',
        f'Ciudad: {message.city or "—"}',
        f'Teléfono: {message.phone or "—"}',
        f'WhatsApp: {message.whatsapp or "—"}',
        f'Motivo: {message.reason or "—"}',
        '',
        'Consulta:',
        message.message,
        '',
        f'Ver en el administrador: {admin_url}',
    ]
    subject = f'Nuevo mensaje de contacto: {message.name}'[:150]
    try:
        EmailMessage(subject, '\n'.join(lines), settings.DEFAULT_FROM_EMAIL, recipients,
                     reply_to=[message.email]).send()
    except Exception:  # noqa: BLE001 - el mensaje ya quedó guardado; el error se registra para soporte
        logger.exception('No se pudo enviar el aviso del mensaje de contacto %s.', message.pk)
        return False
    return True
