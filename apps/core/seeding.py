"""Utilidades para los comandos seed_bloque_*.

Reglas comunes:
- Sin opciones, un modelo solo se carga si su tabla está vacía y nunca se
  modifica un registro existente.
- Con --fill-blanks, además se completan los campos VACÍOS de los registros
  existentes que coinciden con un registro de ejemplo (por su clave), sin
  sobrescribir jamás un campo que ya tenga contenido.
"""

from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.fields.files import FieldFile
from PIL import Image, ImageOps

STATIC_IMAGES = Path(settings.BASE_DIR) / 'static' / 'crafto' / 'images'


def attach_file(instance, field_name, source):
    """Guarda `source` en el campo de archivo (copia a media/).

    `source` puede ser una ruta (Path/str) o una tupla (nombre, bytes) para archivos generados.
    """
    if isinstance(source, tuple):
        name, content = source
        getattr(instance, field_name).save(name, ContentFile(content), save=False)
        return
    with Path(source).open('rb') as fh:
        getattr(instance, field_name).save(Path(source).name, File(fh), save=False)


def sample_pdf(title, lines=()):
    """PDF mínimo de una página (Helvetica, texto en Latin-1), sin dependencias externas."""
    def escape(text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    commands = ['BT', '/F1 22 Tf', '72 760 Td', f'({escape(title)}) Tj', '/F1 12 Tf']
    for line in lines:
        commands += ['0 -24 Td', f'({escape(line)}) Tj']
    commands.append('ET')
    stream = '\n'.join(commands).encode('cp1252', 'replace')
    objects = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R '
        b'/Resources << /Font << /F1 5 0 R >> >> >>',
        b'<< /Length %d >>\nstream\n' % len(stream) + stream + b'\nendstream',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
    ]
    pdf = bytearray(b'%PDF-1.4\n')
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += b'%d 0 obj\n' % number + body + b'\nendobj\n'
    xref = len(pdf)
    pdf += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objects) + 1)
    pdf += b''.join(b'%010d 00000 n \n' % offset for offset in offsets)
    pdf += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objects) + 1, xref)
    return bytes(pdf)


def attach_image(instance, field_name, spec):
    """Copia una imagen de static/crafto/images/.

    `spec` es la ruta relativa o (ruta, (ancho, alto)) para recortarla al centro con esas medidas,
    de modo que el relleno respete las proporciones que espera la plantilla.
    """
    if isinstance(spec, tuple):
        relative_path, size = spec
        source = STATIC_IMAGES / relative_path
        with Image.open(source) as image:
            fitted = ImageOps.fit(image.convert('RGB'), size)
            buffer = BytesIO()
            fitted.save(buffer, 'JPEG', quality=85)
        name = f'{source.stem}-{size[0]}x{size[1]}.jpg'
        getattr(instance, field_name).save(name, ContentFile(buffer.getvalue()), save=False)
        return
    attach_file(instance, field_name, STATIC_IMAGES / spec)


def is_blank(value):
    return value is None or value == '' or (isinstance(value, FieldFile) and not value)


class SeedCommand(BaseCommand):
    """Base de los comandos de datos de ejemplo."""

    def add_arguments(self, parser):
        parser.add_argument(
            '--fill-blanks', action='store_true',
            help='Completa solo los campos vacíos de registros existentes (nunca sobrescribe contenido).')

    def handle(self, *args, **options):
        self.fill_blanks = options['fill_blanks']
        self.filled = []
        with transaction.atomic():
            self.seed()
        if self.fill_blanks:
            if self.filled:
                self.stdout.write(self.style.SUCCESS('Campos completados:'))
                for line in self.filled:
                    self.stdout.write(f'  - {line}')
            else:
                self.stdout.write('No había campos vacíos que completar.')

    def seed(self):
        raise NotImplementedError

    # -- reportes -----------------------------------------------------------
    def report(self, label, created):
        if created:
            self.stdout.write(self.style.SUCCESS(f'{label}: {created} creado(s).'))
        else:
            self.stdout.write(f'{label}: ya tiene datos, no se crean registros.')

    # -- creación y relleno -------------------------------------------------
    def build(self, model, row, **extra):
        """Crea (sin guardar) una instancia a partir de un registro de ejemplo."""
        data = {k: v for k, v in row.items() if k not in ('images', 'files')}
        instance = model(**data, **extra)
        for field, path in row.get('images', {}).items():
            attach_image(instance, field, path)
        for field, path in row.get('files', {}).items():
            attach_file(instance, field, path)
        return instance

    def fill(self, instance, row, label):
        """Completa los campos vacíos de `instance` con los valores de `row`."""
        changed = []
        for field, value in row.items():
            if field in ('images', 'files'):
                continue
            if is_blank(getattr(instance, field)) and not is_blank(value):
                setattr(instance, field, value)
                changed.append(field)
        for key in ('images', 'files'):
            for field, path in row.get(key, {}).items():
                if is_blank(getattr(instance, field)):
                    (attach_image if key == 'images' else attach_file)(instance, field, path)
                    changed.append(field)
        if changed:
            instance.save()
            self.filled.append(f'{label}: {", ".join(changed)}')
        return instance

    def seed_singleton(self, model, row, label):
        instance = model.objects.first()
        if instance is None:
            instance = self.build(model, row)
            instance.save()
            self.report(label, 1)
        else:
            self.report(label, 0)
            if self.fill_blanks:
                self.fill(instance, row, label)
        return instance

    def seed_collection(self, model, label, key, rows, **extra):
        """Carga `rows` si la tabla está vacía; con --fill-blanks completa los existentes por `key`.

        `extra` son valores fijos (por ejemplo la FK al padre) que también acotan la búsqueda.
        Devuelve un dict {clave: instancia} de los registros cargados o encontrados.
        """
        queryset = model.objects.filter(**extra)
        found = {}
        if not queryset.exists():
            for row in rows:
                instance = self.build(model, row, **extra)
                instance.save()
                found[row[key]] = instance
            self.report(label, len(rows))
            return found
        self.report(label, 0)
        for row in rows:
            instance = queryset.filter(**{key: row[key]}).first()
            if instance is None:
                continue
            found[row[key]] = instance
            if self.fill_blanks:
                self.fill(instance, row, f'{label} «{row[key]}»')
        return found
