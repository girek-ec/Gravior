from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import image_validators, validate_link

ICON_HELP = ('Clase de icono incluida en la plantilla (Bootstrap Icons, Font Awesome o Line Icons), '
             'por ejemplo "bi bi-shield-check" o "line-icon-Gear-2".')


class HeroSlide(TimeStampedModel):
    eyebrow = models.CharField('etiqueta superior', max_length=80, blank=True,
                               help_text='Texto corto sobre el título, junto a la etiqueta destacada.')
    title = models.CharField('título principal', max_length=80,
                             help_text='Breve: idealmente menos de 40 caracteres.')
    highlight_text = models.CharField('texto destacado', max_length=30, blank=True,
                                      help_text='Etiqueta oscura antes de la etiqueta superior, ej.: GRAVIOR, TECNOLOGÍA.')
    description = models.TextField('descripción breve', max_length=220)
    desktop_image = models.ImageField(
        'imagen de escritorio', upload_to='hero/', validators=image_validators(5),
        help_text='Fondo del slide. JPG horizontal de 1920 × 1100 px, máx. 5 MB.')
    mobile_image = models.ImageField(
        'imagen móvil', upload_to='hero/', blank=True, validators=image_validators(3),
        help_text='Versión opcional para celulares (pantallas de hasta 778 px). Recomendado: 778 × 900 px. Si se deja vacía se usa la imagen de escritorio.')
    thumbnail = models.ImageField(
        'miniatura', upload_to='hero/', blank=True, validators=image_validators(1),
        help_text='Fondo del botón "Siguiente". 400 × 180 px. Si se deja vacía se usa la imagen de escritorio.')
    primary_button_text = models.CharField('texto del botón 1', max_length=40, blank=True)
    primary_button_url = models.CharField('enlace del botón 1', max_length=500, blank=True, validators=[validate_link])
    secondary_button_text = models.CharField('texto del botón 2', max_length=40, blank=True)
    secondary_button_url = models.CharField(
        'enlace del botón 2', max_length=500, blank=True, validators=[validate_link],
        help_text='Se usa si no hay video. Si hay video, el botón 2 abre el video.')
    video_url = models.URLField('video', max_length=500, blank=True,
                                help_text='Enlace de YouTube o Vimeo que abre el botón 2 en una ventana emergente.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'slide principal'
        verbose_name_plural = 'slider principal'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title

    @property
    def secondary_link(self):
        return self.video_url or self.secondary_button_url


class Differential(TimeStampedModel):
    title = models.CharField('título', max_length=80, help_text='Ej.: Calidad, Bioseguridad, Eficiencia.')
    description = models.TextField('descripción', max_length=300, help_text='Mensaje breve.')
    icon_class = models.CharField('clase del icono', max_length=100, blank=True, help_text=ICON_HELP)
    image = models.ImageField('imagen', upload_to='home/differentials/', blank=True, validators=image_validators(1),
                              help_text='Icono o imagen cuadrada de 114 × 114 px. Si existe, reemplaza al icono en el inicio.')
    show_home = models.BooleanField('mostrar en Inicio', default=True)
    show_about = models.BooleanField('mostrar en Nosotros', default=True)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'diferencial'
        verbose_name_plural = 'diferenciales'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title


class Statistic(TimeStampedModel):
    title = models.CharField('nombre del indicador', max_length=60)
    value = models.PositiveIntegerField('valor', help_text='Solo números enteros, sin puntos ni comas.')
    prefix = models.CharField('prefijo', max_length=10, blank=True)
    suffix = models.CharField('sufijo', max_length=10, blank=True, help_text='Ej.: +, %, años.')
    description = models.CharField('contexto breve', max_length=150, blank=True)
    show_home = models.BooleanField('mostrar en Inicio', default=True)
    show_about = models.BooleanField('mostrar en Nosotros', default=True)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True,
                                    help_text='Publicar solo cifras oficiales aprobadas por GRAVIOR.')

    class Meta:
        verbose_name = 'indicador'
        verbose_name_plural = 'indicadores'
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.title}: {self.prefix}{self.value}{self.suffix}'


class ProcessStep(TimeStampedModel):
    number = models.CharField('número', max_length=5, help_text='Ej.: 01, 02, 03.')
    title = models.CharField('nombre de la etapa', max_length=60)
    description = models.TextField('explicación breve', max_length=300)
    icon_class = models.CharField('clase del icono', max_length=100, blank=True, help_text=ICON_HELP)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'etapa del proceso'
        verbose_name_plural = 'proceso de trabajo'
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.number} · {self.title}'
