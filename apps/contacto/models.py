from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone


class ContactReason(TimeStampedModel):
    name = models.CharField('motivo', max_length=80, help_text='Ej.: Genética, Productos, Calidad y bioseguridad.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True,
                                    help_text='Desactiva un motivo para quitarlo del formulario sin borrar los mensajes asociados.')

    class Meta:
        verbose_name = 'motivo de consulta'
        verbose_name_plural = 'motivos de consulta'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


class ContactMessage(TimeStampedModel):
    """Mensaje recibido desde el formulario de contacto. Los datos enviados no se editan en el admin."""

    name = models.CharField('nombre', max_length=120)
    company = models.CharField('empresa', max_length=150, blank=True)
    position = models.CharField('cargo', max_length=120, blank=True)
    city = models.CharField('ciudad', max_length=100, blank=True)
    phone = models.CharField('teléfono', max_length=30, blank=True, validators=[validate_phone])
    whatsapp = models.CharField('WhatsApp', max_length=30, blank=True, validators=[validate_phone])
    email = models.EmailField('correo')
    # PROTECT: un motivo con mensajes no se borra (se desactiva) para no perder la clasificación.
    reason = models.ForeignKey(ContactReason, on_delete=models.PROTECT, null=True, blank=True,
                               related_name='messages', verbose_name='motivo')
    message = models.TextField('consulta', max_length=3000)
    privacy_accepted = models.BooleanField('aceptó la política de privacidad', default=False)
    is_read = models.BooleanField('leído', default=False)
    is_answered = models.BooleanField('respondido', default=False)
    is_archived = models.BooleanField('archivado', default=False)

    class Meta:
        verbose_name = 'mensaje recibido'
        verbose_name_plural = 'mensajes recibidos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} <{self.email}>'
