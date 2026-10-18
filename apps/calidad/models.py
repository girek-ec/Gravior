from django.db import models

from apps.core.models import SingletonModel, TimeStampedModel, unique_slug
from apps.core.validators import image_validators, validate_link

ICON_HELP = ('Clase de icono incluida en la plantilla (Bootstrap Icons, Font Awesome o Line Icons), '
             'por ejemplo "line-icon-Gear-2".')


class QualityPage(SingletonModel, TimeStampedModel):
    """Discurso principal de Calidad y bioseguridad. Una sola instancia."""

    page_title = models.CharField('título', max_length=80)
    intro = models.TextField('introducción', max_length=300, help_text='Frase principal de la cabecera.')
    description = models.TextField('descripción principal')
    main_image = models.ImageField('imagen principal', upload_to='quality/', validators=image_validators(3),
                                   help_text='Horizontal, recomendado 960 × 640 px. Máx. 3 MB.')
    quality_commitment = models.TextField('compromiso de calidad', blank=True)
    biosecurity_approach = models.TextField('enfoque de bioseguridad', blank=True)
    cta_text = models.CharField('texto del llamado a la acción', max_length=150, blank=True)
    cta_url = models.CharField('enlace del llamado a la acción', max_length=500, blank=True, validators=[validate_link],
                               help_text='Ruta interna (/contacto/) o enlace completo.')
    seo_title = models.CharField('título SEO', max_length=70, blank=True,
                                 help_text='Si se deja vacío se usa el de la configuración general.')
    seo_description = models.TextField('descripción SEO', max_length=300, blank=True,
                                       help_text='Si se deja vacía se usa la de la configuración general.')

    class Meta:
        verbose_name = 'página de calidad y bioseguridad'
        verbose_name_plural = 'página de calidad y bioseguridad'

    def __str__(self):
        return self.page_title


class QualityArea(TimeStampedModel):
    name = models.CharField('nombre del área', max_length=60)
    slug = models.SlugField('identificador', max_length=80, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el nombre.')
    description = models.TextField('descripción', max_length=400)
    icon_class = models.CharField('clase del icono', max_length=100, blank=True, help_text=ICON_HELP)
    image = models.ImageField('imagen', upload_to='quality/areas/', blank=True, validators=image_validators(2),
                              help_text='Recomendado 960 × 640 px. Máx. 2 MB.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'área'
        verbose_name_plural = 'áreas'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        super().save(*args, **kwargs)


class QualityStep(TimeStampedModel):
    # CASCADE: las etapas dependen de su área (sección 21.3).
    quality_area = models.ForeignKey(QualityArea, on_delete=models.CASCADE, related_name='steps',
                                     verbose_name='área')
    number = models.CharField('numeración', max_length=10, blank=True, help_text='Ej.: 01, 02.')
    title = models.CharField('título', max_length=100)
    description = models.TextField('descripción', max_length=500)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'etapa'
        verbose_name_plural = 'etapas / procesos'
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.number} {self.title}'.strip()
