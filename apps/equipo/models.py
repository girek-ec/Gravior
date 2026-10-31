from django.db import models

from apps.core.models import SlugFromNameMixin, TimeStampedModel
from apps.core.validators import image_validators, validate_phone

PRIVATE_DATA_HELP = 'Solo si la persona autorizó publicarlo. Si se deja vacío no se muestra en la web.'


class TeamMember(SlugFromNameMixin, TimeStampedModel):
    """Integrante que se muestra públicamente. No publicar nombres, cargos ni datos personales sin aprobación."""

    name = models.CharField('nombre', max_length=120)
    slug = models.SlugField('identificador', max_length=140, unique=True, blank=True,
                            help_text='Se genera automáticamente desde el nombre. Útil si luego existe una página de detalle.')
    position = models.CharField('cargo', max_length=120)
    specialty = models.CharField('especialidad', max_length=120, blank=True)
    short_bio = models.TextField('resumen', max_length=400, help_text='Texto breve aprobado por la persona.')
    biography = models.TextField('biografía completa', blank=True,
                                 help_text='Aún no se muestra en la web (no hay página de detalle).')
    photo = models.ImageField('fotografía', upload_to='team/', validators=image_validators(2),
                              help_text='Vertical, recomendado 600 × 832 px. Máx. 2 MB. Solo fotos autorizadas.')
    email = models.EmailField('correo', blank=True, help_text=PRIVATE_DATA_HELP)
    phone = models.CharField('teléfono', max_length=30, blank=True, validators=[validate_phone], help_text=PRIVATE_DATA_HELP)
    linkedin_url = models.URLField('perfil de LinkedIn', max_length=300, blank=True, help_text=PRIVATE_DATA_HELP)
    is_featured = models.BooleanField('mostrar en Inicio', default=False)
    order = models.PositiveIntegerField('orden', default=0)
    is_active = models.BooleanField('activo', default=True)

    class Meta:
        verbose_name = 'integrante'
        verbose_name_plural = 'miembros del equipo técnico'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name

    @property
    def phone_link(self):
        digits = ''.join(ch for ch in self.phone if ch.isdigit())
        return ('+' + digits if self.phone.strip().startswith('+') else digits) if digits else ''
