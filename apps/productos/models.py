from django.db import models

from apps.core.models import SlugFromNameMixin, TimeStampedModel
from apps.core.validators import image_validators, pdf_validators


class ProductCategory(SlugFromNameMixin, TimeStampedModel):
    name = models.CharField('categoría', max_length=80)
    slug = models.SlugField('identificador', max_length=100, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el nombre. Se usa en el filtro del catálogo.')
    description = models.TextField('descripción', max_length=300, blank=True)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'categoría de productos'
        verbose_name_plural = 'categorías'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


class Product(SlugFromNameMixin, TimeStampedModel):
    """Producto o solución del catálogo informativo: sin precio, carrito, stock ni pago."""

    # PROTECT: no se borra una categoría que tiene productos (sección 21.3).
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products',
                                 verbose_name='categoría')
    name = models.CharField('nombre', max_length=120,
                            help_text='Se muestra en grande en la tarjeta del catálogo: preferir nombres cortos (una o dos palabras).')
    slug = models.SlugField('identificador para URL', max_length=140, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el nombre. Reservado para la futura página de detalle.')
    brand = models.CharField('marca', max_length=80, blank=True, help_text='Solo si aplica. Aún no se muestra en la web (no hay página de detalle).')
    reference = models.CharField('código / referencia', max_length=40, blank=True)
    summary = models.TextField('resumen', max_length=200, help_text='Texto breve para la tarjeta del catálogo.')
    description = models.TextField('descripción completa', help_text='Aún no se muestra en la web (no hay página de detalle).')
    main_image = models.ImageField('imagen principal', upload_to='products/', validators=image_validators(3),
                                   help_text='Horizontal, recomendado 960 × 640 px. Máx. 3 MB.')
    application = models.TextField('aplicación', blank=True, help_text='Aún no se muestra en la web (no hay página de detalle).')
    benefits = models.TextField('beneficios', blank=True, help_text='Aún no se muestra en la web (no hay página de detalle).')
    inquiry_button_text = models.CharField(
        'texto del botón de consulta', max_length=40, blank=True,
        help_text='Ej.: Solicitar información. Abre WhatsApp si está activo en la configuración general; si no, Contacto.')
    is_featured = models.BooleanField('destacar', default=False, help_text='Aparece en las pestañas del inicio.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)
    seo_title = models.CharField('título SEO', max_length=70, blank=True)
    seo_description = models.TextField('descripción SEO', max_length=300, blank=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


class ProductFeature(TimeStampedModel):
    # CASCADE: una característica no existe sin su producto.
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features', verbose_name='producto')
    title = models.CharField('título', max_length=80)
    description = models.TextField('contenido', max_length=300)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'característica'
        verbose_name_plural = 'características'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title


class ProductDocument(TimeStampedModel):
    class DocumentType(models.TextChoices):
        DATASHEET = 'ficha', 'Ficha técnica'
        CATALOG = 'catalogo', 'Catálogo'
        MANUAL = 'manual', 'Manual'
        CERTIFICATE = 'certificado', 'Certificado'
        OTHER = 'otro', 'Otro'

    # PROTECT: documentación publicada; no se borra por accidente al eliminar el producto.
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='documents', verbose_name='producto')
    title = models.CharField('título', max_length=150)
    document_type = models.CharField('tipo', max_length=20, choices=DocumentType.choices)
    file = models.FileField('archivo PDF', upload_to='products/documents/', validators=pdf_validators(10),
                            help_text='Solo PDF aprobado para distribución. Máx. 10 MB.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'documento'
        verbose_name_plural = 'documentos'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title
