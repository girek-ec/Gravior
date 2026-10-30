from django.db import models

from apps.core.models import SlugFromNameMixin, TimeStampedModel
from apps.core.validators import image_validators


class FacilityCategory(SlugFromNameMixin, TimeStampedModel):
    name = models.CharField('categoría', max_length=60, help_text='Ej.: Infraestructura, Bioseguridad, Tecnología.')
    slug = models.SlugField('identificador', max_length=80, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el nombre. Se usa en el filtro de la galería.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'categoría de instalaciones'
        verbose_name_plural = 'categorías'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


class Facility(SlugFromNameMixin, TimeStampedModel):
    """Instalación o elemento institucional de la galería. No publicar capacidad exacta ni datos estratégicos."""

    slug_source = 'title'

    # PROTECT: no se borra una categoría que tiene instalaciones (sección 21.3).
    category = models.ForeignKey(FacilityCategory, on_delete=models.PROTECT, related_name='facilities',
                                 verbose_name='categoría')
    title = models.CharField('título', max_length=120)
    slug = models.SlugField('identificador', max_length=140, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el título. Reservado para una futura página de detalle.')
    summary = models.TextField('texto breve', max_length=200)
    description = models.TextField('descripción ampliada', blank=True)
    main_image = models.ImageField('imagen principal', upload_to='facilities/', validators=image_validators(3),
                                   help_text='Recomendado 800 × 635 px. Máx. 3 MB. Usar fotografías propias o autorizadas.')
    public_location = models.CharField(
        'ubicación pública', max_length=120, blank=True,
        help_text='Solo si es publicable (por ejemplo, la provincia). No publicar ubicaciones sensibles.')
    video_url = models.URLField('video', max_length=500, blank=True, help_text='Enlace de YouTube o Vimeo.')
    is_featured = models.BooleanField('destacado', default=False)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'instalación'
        verbose_name_plural = 'instalaciones'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title


class FacilityGallery(TimeStampedModel):
    # CASCADE: las fotos dependen de su instalación (sección 21.3).
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='gallery', verbose_name='instalación')
    image = models.ImageField('fotografía', upload_to='facilities/gallery/', validators=image_validators(3),
                              help_text='Máx. 3 MB. Se abre en la galería al hacer clic en la instalación.')
    caption = models.CharField('pie de foto', max_length=150, blank=True)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'fotografía'
        verbose_name_plural = 'galería'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.caption or f'Foto de {self.facility}'
