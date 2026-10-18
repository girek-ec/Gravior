"""Utilidades para los comandos seed_bloque_*.

Reglas comunes:
- Sin opciones, un modelo solo se carga si su tabla está vacía y nunca se
  modifica un registro existente.
- Con --fill-blanks, además se completan los campos VACÍOS de los registros
  existentes que coinciden con un registro de ejemplo (por su clave), sin
  sobrescribir jamás un campo que ya tenga contenido.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.fields.files import FieldFile

STATIC_IMAGES = Path(settings.BASE_DIR) / 'static' / 'crafto' / 'images'


def attach_file(instance, field_name, source):
    """Guarda `source` (Path) en el campo de archivo, copiándolo a media/."""
    with Path(source).open('rb') as fh:
        getattr(instance, field_name).save(Path(source).name, File(fh), save=False)


def attach_image(instance, field_name, relative_path):
    attach_file(instance, field_name, STATIC_IMAGES / relative_path)


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
