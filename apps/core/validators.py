"""Validadores compartidos para archivos subidos y enlaces administrables."""

import re

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.utils.deconstruct import deconstructible

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']
FAVICON_EXTENSIONS = ['png', 'ico']

validate_image_extension = FileExtensionValidator(
    allowed_extensions=IMAGE_EXTENSIONS,
    message='Formato no permitido. Usa JPG, PNG o WEBP.',
)

validate_favicon_extension = FileExtensionValidator(
    allowed_extensions=FAVICON_EXTENSIONS,
    message='Formato no permitido. Usa PNG o ICO.',
)


@deconstructible
class MaxFileSizeValidator:
    """Rechaza archivos más pesados que `max_mb` megabytes."""

    def __init__(self, max_mb):
        self.max_mb = max_mb

    def __call__(self, file):
        if file and file.size > self.max_mb * 1024 * 1024:
            raise ValidationError(
                'El archivo pesa %(size).1f MB; el máximo permitido es %(max)s MB.',
                params={'size': file.size / (1024 * 1024), 'max': self.max_mb},
            )

    def __eq__(self, other):
        return isinstance(other, MaxFileSizeValidator) and self.max_mb == other.max_mb


def image_validators(max_mb=2):
    return [validate_image_extension, MaxFileSizeValidator(max_mb)]


LINK_PATTERN = re.compile(r'^(/|#|https?://|mailto:|tel:)')


def validate_link(value):
    """Acepta rutas internas (/contacto/), anclas (#seccion) o enlaces http(s), mailto: y tel:."""
    if value and not LINK_PATTERN.match(value):
        raise ValidationError(
            'Usa una ruta interna que empiece con "/" (por ejemplo /contacto/), un ancla "#" '
            'o un enlace completo que empiece con https://, mailto: o tel:.'
        )


validate_phone = RegexValidator(
    regex=r'^\+?[\d\s()-]{7,20}$',
    message='Escribe solo números, espacios y opcionalmente el prefijo +, por ejemplo +593 99 000 0000.',
)
