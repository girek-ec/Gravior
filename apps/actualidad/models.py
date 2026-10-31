from django.db import models
from django.utils import timezone

from apps.core.models import SlugFromNameMixin, TimeStampedModel
from apps.core.validators import image_validators


class PostCategory(SlugFromNameMixin, TimeStampedModel):
    name = models.CharField('categoría', max_length=60)
    slug = models.SlugField('identificador', max_length=80, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el nombre. Se usa en el filtro de Actualidad.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'categoría de publicaciones'
        verbose_name_plural = 'categorías'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


class PublishedPostQuerySet(models.QuerySet):
    def published(self):
        """Publicadas, con fecha ya cumplida y categoría activa."""
        return self.filter(is_published=True, published_at__lte=timezone.now(), category__is_active=True)


class Post(SlugFromNameMixin, TimeStampedModel):
    slug_source = 'title'

    # PROTECT: no se borra una categoría que tiene publicaciones (sección 21.3).
    category = models.ForeignKey(PostCategory, on_delete=models.PROTECT, related_name='posts',
                                 verbose_name='categoría')
    title = models.CharField('título', max_length=160)
    slug = models.SlugField('identificador para URL', max_length=180, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el título. Es parte de la URL: /actualidad/<identificador>/.')
    excerpt = models.TextField('resumen', max_length=300, help_text='Texto breve para las tarjetas y la cita del artículo.')
    content = models.TextField(
        'contenido',
        help_text='Texto plano. Separa los párrafos con una línea en blanco. No se interpreta HTML: se muestra tal cual.')
    main_image = models.ImageField('imagen principal', upload_to='blog/', validators=image_validators(3),
                                   help_text='Horizontal, recomendado 1600 × 920 px. Máx. 3 MB.')
    thumbnail = models.ImageField('miniatura', upload_to='blog/thumbnails/', blank=True, validators=image_validators(1),
                                  help_text='Imagen de la tarjeta, 600 × 430 px. Si se deja vacía se usa la imagen principal.')
    author = models.CharField('autor', max_length=120, blank=True, help_text='Solo si se publica.')
    published_at = models.DateTimeField('fecha de publicación', default=timezone.now,
                                        help_text='Una fecha futura deja la publicación programada (no visible hasta entonces).')
    is_featured = models.BooleanField('destacar en Inicio', default=False,
                                      help_text='Reservado para una sección de actualidad en el inicio (la maqueta actual no la tiene).')
    is_published = models.BooleanField('publicado', default=True)
    seo_title = models.CharField('título SEO', max_length=70, blank=True,
                                 help_text='Si se deja vacío se usa el título.')
    seo_description = models.TextField('descripción SEO', max_length=300, blank=True,
                                       help_text='Si se deja vacía se usa el resumen.')

    objects = PublishedPostQuerySet.as_manager()

    class Meta:
        verbose_name = 'publicación'
        verbose_name_plural = 'noticias y artículos'
        ordering = ['-published_at', '-pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('actualidad:detail', kwargs={'slug': self.slug})

    @property
    def card_image(self):
        return self.thumbnail or self.main_image

    @property
    def paragraphs(self):
        """Párrafos del contenido (separados por líneas en blanco)."""
        blocks = [block.strip() for block in self.content.replace('\r\n', '\n').split('\n\n')]
        return [block for block in blocks if block]
