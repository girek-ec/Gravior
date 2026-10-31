import re
from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.db import models

from .validators import (
    MaxFileSizeValidator,
    image_validators,
    validate_favicon_extension,
    validate_link,
    validate_phone,
)


class TimeStampedModel(models.Model):
    """Trazabilidad administrativa común (sección 5 del documento de arquitectura)."""

    created_at = models.DateTimeField('creado', auto_now_add=True)
    updated_at = models.DateTimeField('actualizado', auto_now=True)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    """Modelo del que debe existir una sola instancia (sección 21.1)."""

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if not self.pk and type(self).objects.exists():
            raise ValidationError(f'Ya existe un registro de {self._meta.verbose_name}; edita el existente.')

    @classmethod
    def get_current(cls):
        return cls.objects.first()


class SiteConfiguration(SingletonModel, TimeStampedModel):
    """Singleton con la identidad y los datos corporativos del sitio."""

    company_name = models.CharField('nombre comercial', max_length=120)
    legal_name = models.CharField('razón social', max_length=200, blank=True,
                                  help_text='Solo si se decide publicarla.')
    logo = models.ImageField(
        'logo principal', upload_to='site/', validators=image_validators(1),
        help_text='PNG con fondo transparente para fondos claros. Recomendado: 164 × 43 px (o el doble para pantallas retina). Máx. 1 MB.')
    logo_white = models.ImageField(
        'logo para fondos oscuros', upload_to='site/', blank=True, validators=image_validators(1),
        help_text='Versión clara del logo para el menú lateral y el pie de página. Mismas medidas que el logo principal.')
    isotype = models.ImageField(
        'isotipo', upload_to='site/', blank=True, validators=image_validators(1),
        help_text='Elemento gráfico de la marca. PNG cuadrado, recomendado 512 × 512 px.')
    favicon = models.ImageField(
        'favicon', upload_to='site/', blank=True,
        validators=[validate_favicon_extension, MaxFileSizeValidator(0.5)],
        help_text='Icono de la pestaña del navegador. PNG o ICO cuadrado de 32 × 32 o 64 × 64 px.')
    short_description = models.TextField(
        'descripción corporativa breve',
        help_text='Una o dos frases sobre qué es GRAVIOR.')
    phone = models.CharField('teléfono principal', max_length=30, blank=True, validators=[validate_phone])
    whatsapp_number = models.CharField(
        'número de WhatsApp', max_length=30, validators=[validate_phone],
        help_text='Con código de país, por ejemplo +593 99 000 0000.')
    whatsapp_message = models.CharField(
        'mensaje inicial de WhatsApp', max_length=200, blank=True,
        help_text='Texto que aparece escrito al abrir el chat.')
    whatsapp_enabled = models.BooleanField('mostrar botón de WhatsApp', default=True)
    main_email = models.EmailField('correo general', blank=True)
    address = models.CharField('dirección', max_length=255, blank=True,
                               help_text='Solo si es publicable.')
    city = models.CharField('ciudad', max_length=100, blank=True)
    province = models.CharField('provincia', max_length=100, blank=True)
    country = models.CharField('país', max_length=100, blank=True)
    business_hours = models.CharField('horario de atención', max_length=200, blank=True)
    google_maps_url = models.URLField('enlace a Google Maps', max_length=500, blank=True)
    copyright_text = models.CharField(
        'texto de copyright', max_length=200,
        help_text='Se muestra en el pie de página antes del nombre comercial, por ejemplo "Copyright 2026".')
    default_seo_title = models.CharField(
        'título SEO general', max_length=70, blank=True,
        help_text='Título por defecto de las páginas (máx. 70 caracteres).')
    default_seo_description = models.TextField(
        'descripción SEO general', max_length=300, blank=True,
        help_text='Descripción por defecto para buscadores (ideal 150–160 caracteres).')

    class Meta:
        verbose_name = 'configuración general'
        verbose_name_plural = 'configuración general'

    def __str__(self):
        return self.company_name

    @staticmethod
    def _digits(value):
        return re.sub(r'\D', '', value or '')

    @property
    def phone_link(self):
        digits = self._digits(self.phone)
        if not digits:
            return ''
        return '+' + digits if self.phone.strip().startswith('+') else digits

    @property
    def whatsapp_url(self):
        """URL de wa.me solo si el botón está activo y hay número."""
        return self.whatsapp_link()

    def whatsapp_link(self, subject=''):
        """URL de wa.me con el mensaje inicial y, opcionalmente, el tema de la consulta (p. ej. un producto)."""
        digits = self._digits(self.whatsapp_number)
        if not (self.whatsapp_enabled and digits):
            return ''
        message = ' – '.join(part for part in (self.whatsapp_message, subject) if part)
        url = f'https://wa.me/{digits}'
        if message:
            url += f'?text={quote(message)}'
        return url

    @property
    def location_text(self):
        return ', '.join(part for part in (self.address, self.city, self.province, self.country) if part)


class CorporateEmail(TimeStampedModel):
    class EmailType(models.TextChoices):
        INFO = 'info', 'Información'
        COMMERCIAL = 'comercial', 'Comercial'
        SALES = 'ventas', 'Ventas'
        ADMIN = 'administracion', 'Administración'
        OTHER = 'otro', 'Otro'

    label = models.CharField('etiqueta', max_length=60,
                             help_text='Ej.: Información, Comercial, Ventas, Administración.')
    email = models.EmailField('correo')
    email_type = models.CharField('tipo', max_length=20, choices=EmailType.choices, blank=True,
                                  help_text='Clasificación interna.')
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'correo corporativo'
        verbose_name_plural = 'correos corporativos'
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.label} <{self.email}>'


class SocialNetwork(TimeStampedModel):
    name = models.CharField('nombre', max_length=60)
    icon_class = models.CharField(
        'clase del icono', max_length=100, blank=True,
        help_text='Icono de Font Awesome incluido en la plantilla, por ejemplo "fa-brands fa-facebook-f", '
                  '"fa-brands fa-instagram", "fa-brands fa-linkedin-in", "fa-brands fa-youtube".')
    url = models.URLField('URL oficial', max_length=500)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'red social'
        verbose_name_plural = 'redes sociales'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


class CallToAction(TimeStampedModel):
    code = models.SlugField(
        'identificador', max_length=60, unique=True,
        help_text='Lo usa la plantilla para ubicar el llamado: header_contact (botón del encabezado), '
                  'home_process (sección de proceso del inicio), about_contact (Nosotros). '
                  'No lo cambies salvo indicación del equipo técnico.')
    title = models.CharField('título', max_length=150)
    text = models.TextField('texto de apoyo', blank=True)
    button_text = models.CharField('texto del botón', max_length=60,
                                   help_text='Ej.: Hablar con un asesor.')
    button_url = models.CharField('enlace del botón', max_length=500, validators=[validate_link],
                                  help_text='Ruta interna (/contacto/) o enlace completo (https://, mailto:, tel:).')
    image = models.ImageField('imagen', upload_to='site/cta/', blank=True, validators=image_validators(2),
                              help_text='Opcional. JPG o PNG, máx. 2 MB.')
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'llamado a la acción'
        verbose_name_plural = 'llamados a la acción'
        ordering = ['code']

    def __str__(self):
        return f'{self.title} ({self.code})'


def unique_slug(instance, value, field_name='slug', max_length=None):
    """Slug único a partir de `value`; agrega -2, -3… si ya existe en el modelo."""
    from django.utils.text import slugify
    max_length = max_length or instance._meta.get_field(field_name).max_length
    base = (slugify(value) or 'item')[:max_length]
    slug, n = base, 2
    queryset = type(instance).objects.exclude(pk=instance.pk)
    while queryset.filter(**{field_name: slug}).exists():
        suffix = f'-{n}'
        slug = f'{base[:max_length - len(suffix)]}{suffix}'
        n += 1
    return slug


class SlugFromNameMixin:
    """Genera el slug desde `slug_source` (por defecto `name`) solo si está vacío.

    El slug queda estable aunque luego se edite el nombre (sección 21.2).
    """

    slug_source = 'name'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, getattr(self, self.slug_source))
        super().save(*args, **kwargs)
