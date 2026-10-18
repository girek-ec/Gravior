from django.db import models

from apps.core.models import TimeStampedModel, unique_slug
from apps.core.validators import image_validators, pdf_validators

ICON_HELP = ('Clase de icono incluida en la plantilla (Bootstrap Icons, Font Awesome o Line Icons), '
             'por ejemplo "bi bi-graph-up-arrow".')


class GeneticLine(TimeStampedModel):
    name = models.CharField('nombre comercial', max_length=120)
    slug = models.SlugField(
        'identificador para URL', max_length=140, unique=True, blank=True,
        help_text='Se genera automáticamente desde el nombre. Cámbialo solo si es necesario: es parte de la URL.')
    brand_name = models.CharField('marca genética', max_length=80, blank=True)
    brand_logo = models.ImageField(
        'logo de la marca', upload_to='genetics/brands/', blank=True, validators=image_validators(1),
        help_text='Solo logos autorizados por la marca y sin modificar. PNG transparente, aprox. 197 × 87 px.')
    summary = models.TextField('resumen', max_length=300, help_text='Texto breve para tarjetas y el inicio.')
    description = models.TextField('descripción amplia')
    main_image = models.ImageField('imagen principal', upload_to='genetics/', validators=image_validators(3),
                                   help_text='Vertical, recomendado 578 × 691 px. Máx. 3 MB.')
    secondary_image = models.ImageField('imagen secundaria', upload_to='genetics/', blank=True,
                                        validators=image_validators(3),
                                        help_text='Fondo de las tarjetas de características. 600 × 672 px.')
    application = models.TextField('aplicación / uso', blank=True)
    is_featured = models.BooleanField('destacar en Inicio', default=False)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)
    seo_title = models.CharField('título SEO', max_length=70, blank=True)
    seo_description = models.TextField('descripción SEO', max_length=300, blank=True)

    class Meta:
        verbose_name = 'línea genética'
        verbose_name_plural = 'líneas genéticas'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        super().save(*args, **kwargs)


class GeneticFeature(TimeStampedModel):
    # CASCADE: una característica no tiene sentido sin su línea (sección 21.3).
    genetic_line = models.ForeignKey(GeneticLine, on_delete=models.CASCADE, related_name='features',
                                     verbose_name='línea genética')
    title = models.CharField('título', max_length=80, help_text='Ej.: Uniformidad, eficiencia.')
    description = models.TextField('descripción', max_length=300, help_text='Solo texto aprobado.')
    icon_class = models.CharField('clase del icono', max_length=100, blank=True, help_text=ICON_HELP)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'característica'
        verbose_name_plural = 'características'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title


class GeneticDocument(TimeStampedModel):
    class DocumentType(models.TextChoices):
        DATASHEET = 'ficha', 'Ficha técnica'
        MANUAL = 'manual', 'Manual'
        GUIDE = 'guia', 'Guía'
        COMMERCIAL = 'comercial', 'Comercial'
        OTHER = 'otro', 'Otro'

    # PROTECT: documentación publicada; no se borra por accidente al eliminar la línea (sección 21.3).
    genetic_line = models.ForeignKey(GeneticLine, on_delete=models.PROTECT, related_name='documents',
                                     verbose_name='línea genética')
    title = models.CharField('título del documento', max_length=150)
    document_type = models.CharField('tipo', max_length=20, choices=DocumentType.choices)
    file = models.FileField('archivo PDF', upload_to='genetics/documents/', validators=pdf_validators(10),
                            help_text='Solo PDF aprobado para distribución. Máx. 10 MB.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'documento'
        verbose_name_plural = 'documentos'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title
