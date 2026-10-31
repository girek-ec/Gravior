from django.db import models

from apps.core.models import SlugFromNameMixin, TimeStampedModel
from apps.core.validators import image_validators


class Partner(SlugFromNameMixin, TimeStampedModel):
    """Aliado o respaldo estratégico publicado con autorización (logo oficial sin modificar)."""

    name = models.CharField('nombre', max_length=120)
    slug = models.SlugField('identificador', max_length=140, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el nombre.')
    logo = models.ImageField(
        'logo oficial', upload_to='partners/', validators=image_validators(1),
        help_text='Solo el logo oficial autorizado, sin modificar sus colores ni proporciones. '
                  'PNG con fondo transparente, recomendado 300 × 120 px. Máx. 1 MB.')
    description = models.TextField('reseña de la relación', max_length=400, blank=True,
                                   help_text='Solo texto aprobado por ambas partes. Aparece en el carrusel de Aliados.')
    alliance_type = models.CharField('tipo de relación', max_length=80, blank=True,
                                     help_text='Ej.: Genética, Soporte técnico, Tecnología.')
    website = models.URLField('sitio web oficial', max_length=300, blank=True)
    image = models.ImageField('imagen adicional', upload_to='partners/images/', blank=True,
                              validators=image_validators(2),
                              help_text='Imagen cuadrada para el carrusel (se recorta en círculo), 300 × 300 px. '
                                        'Si se deja vacía se usa el logo.')
    is_featured = models.BooleanField('destacado', default=False,
                                      help_text='Reservado para una sección de aliados en el inicio (la maqueta actual no la tiene).')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'aliado estratégico'
        verbose_name_plural = 'aliados estratégicos'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name
