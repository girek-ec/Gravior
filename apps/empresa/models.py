from django.db import models

from apps.core.models import SingletonModel, TimeStampedModel
from apps.core.validators import image_validators

ICON_HELP = ('Clase de icono incluida en la plantilla (Bootstrap Icons, Font Awesome o Line Icons), '
             'por ejemplo "bi bi-shield-check".')


class AboutPage(SingletonModel, TimeStampedModel):
    """Contenido corporativo principal (Quiénes somos). Una sola instancia."""

    page_title = models.CharField('título de página', max_length=80)
    intro = models.TextField('introducción', max_length=300,
                             help_text='Frase principal de la cabecera de Nosotros y del bloque "Sobre GRAVIOR" del inicio.')
    company_description = models.TextField('descripción de la empresa', help_text='Qué es y qué hace GRAVIOR.')
    purpose = models.TextField('propósito', blank=True)
    mission = models.TextField('misión', blank=True)
    vision = models.TextField('visión', blank=True)
    value_proposition = models.TextField('propuesta de valor')
    client_commitment = models.TextField('compromiso con clientes', blank=True)
    main_image = models.ImageField(
        'imagen principal', upload_to='about/', validators=image_validators(3),
        help_text='Horizontal, recomendado 1920 × 980 px. Máx. 3 MB.')
    secondary_image = models.ImageField(
        'imagen secundaria', upload_to='about/', blank=True, validators=image_validators(3),
        help_text='Vertical, recomendado 578 × 649 px. Máx. 3 MB.')
    corporate_video_url = models.URLField('video corporativo', max_length=500, blank=True,
                                          help_text='Enlace de YouTube o Vimeo.')
    seo_title = models.CharField('título SEO', max_length=70, blank=True,
                                 help_text='Si se deja vacío se usa el de la configuración general.')
    seo_description = models.TextField('descripción SEO', max_length=300, blank=True,
                                       help_text='Si se deja vacía se usa la de la configuración general.')

    class Meta:
        verbose_name = 'quiénes somos'
        verbose_name_plural = 'quiénes somos'

    def __str__(self):
        return self.page_title


class CorporateValue(TimeStampedModel):
    name = models.CharField('nombre', max_length=80)
    description = models.TextField('descripción', max_length=300)
    icon_class = models.CharField('clase del icono', max_length=100, blank=True, help_text=ICON_HELP)
    image = models.ImageField('imagen', upload_to='about/values/', blank=True, validators=image_validators(2),
                              help_text='Recomendado 600 × 440 px. Máx. 2 MB.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'valor corporativo'
        verbose_name_plural = 'valores corporativos'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name
