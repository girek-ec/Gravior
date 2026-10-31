"""Carga los contenidos de ejemplo del Bloque E (Actualidad y Contacto).

    python manage.py seed_bloque_e                 # crea lo que falta, no toca lo existente
    python manage.py seed_bloque_e --fill-blanks   # además completa campos vacíos

Publicaciones con textos técnicos generales, sin cifras, resultados,
certificaciones ni claims (sección 25). No se cargan mensajes de contacto:
solo llegan desde el formulario. Ver docs/CONTENIDO_EJEMPLO.md.
"""

from datetime import timedelta

from django.utils import timezone

from apps.actualidad.models import Post, PostCategory
from apps.contacto.models import ContactReason
from apps.core.seeding import SeedCommand

MAIN_IMAGE_SIZE = (1600, 920)
THUMBNAIL_SIZE = (600, 430)
AUTHOR = 'Equipo GRAVIOR'

POST_CATEGORIES = [
    {'name': 'Genética', 'order': 1},
    {'name': 'Bioseguridad', 'order': 2},
    {'name': 'Manejo', 'order': 3},
    {'name': 'Tecnología', 'order': 4},
]

POSTS = [
    ('Genética', 'Claves para expresar el potencial genético en producción avícola',
     'La genética es el punto de partida; el manejo, la nutrición y el ambiente permiten que ese potencial se exprese.',
     ['La genética define el punto de partida de cada lote, pero su potencial solo se expresa cuando se integra con un '
      'manejo adecuado, una nutrición acorde con cada etapa y un ambiente controlado.',
      'Por eso conviene revisar de forma conjunta las condiciones de recepción, la uniformidad del lote y los registros '
      'de seguimiento, en lugar de analizar cada factor por separado.',
      'El acompañamiento técnico ayuda a ordenar esa información y a priorizar los ajustes que tienen mayor impacto en '
      'la operación.'],
     'gravior/home/solution-genetics.jpg'),
    ('Bioseguridad', 'Bioseguridad: prevención como parte de la eficiencia productiva',
     'La bioseguridad es una herramienta preventiva que debe integrarse a la operación diaria.',
     ['La bioseguridad es una herramienta preventiva que debe integrarse a la operación diaria. Su eficacia depende de '
      'protocolos claros, disciplina operativa, control de accesos, limpieza, desinfección y seguimiento continuo.',
      'La prevención comienza con la identificación de puntos críticos y la definición de medidas prácticas que puedan '
      'cumplirse de forma consistente dentro de la operación.',
      'El control de accesos, la higiene del personal, la limpieza de equipos y la separación de áreas ayudan a reducir '
      'riesgos y a mantener procesos más estables.'],
     'gravior/home/solution-biosecurity.jpg'),
    ('Manejo', 'Ambiente y manejo para una producción consistente',
     'Temperatura, ventilación, iluminación y cama forman parte de un mismo sistema de manejo.',
     ['Temperatura, ventilación, iluminación y condiciones de cama forman parte de un mismo sistema: un cambio en uno de '
      'ellos suele afectar a los demás.',
      'La observación del comportamiento de las aves es una referencia práctica para detectar ajustes necesarios antes '
      'de que se reflejen en el desempeño del lote.',
      'Registrar las condiciones de forma ordenada facilita tomar decisiones oportunas y repetir las prácticas que '
      'funcionan.'],
     'gravior/home/hero-02.jpg'),
    ('Tecnología', 'Registro de datos para decisiones técnicas más claras',
     'Ordenar los registros de campo permite leer mejor la evolución de cada lote.',
     ['Los registros de campo son una herramienta de gestión: permiten comparar lotes, detectar variaciones y evaluar el '
      'efecto de los ajustes realizados.',
      'Definir qué datos registrar, con qué frecuencia y quién los revisa ayuda a que la información sea útil y '
      'consistente.',
      'Con datos ordenados, el análisis junto al equipo técnico se enfoca en las prioridades de mejora de la operación.'],
     'gravior/home/solution-technical.jpg'),
    ('Bioseguridad', 'Limpieza y desinfección: rutinas que sostienen la prevención',
     'Las rutinas de limpieza y desinfección son parte central de un programa preventivo.',
     ['Las rutinas de limpieza y desinfección son parte central de un programa preventivo y requieren una secuencia '
      'clara y responsables definidos.',
      'Revisar periódicamente su cumplimiento permite identificar oportunidades de mejora y mantener criterios '
      'homogéneos en toda la operación.'],
     'gravior/home/hero-03.jpg'),
    ('Manejo', 'Recepción y arranque del lote: primeros días, decisiones clave',
     'La preparación previa y la atención durante la recepción influyen en el desarrollo posterior del lote.',
     ['La preparación de las instalaciones antes de la llegada del lote y la atención durante la recepción influyen en '
      'su desarrollo posterior.',
      'Confort, acceso a agua y alimento, y una observación cercana durante los primeros días ayudan a detectar a tiempo '
      'cualquier ajuste necesario.'],
     'gravior/home/hero-01.jpg'),
]

CONTACT_REASONS = ['Genética', 'Productos', 'Calidad y bioseguridad', 'Asesoría técnica', 'Información general']


class Command(SeedCommand):
    help = 'Carga los contenidos de ejemplo del Bloque E. Con --fill-blanks completa campos vacíos.'

    def seed(self):
        categories = self.seed_collection(PostCategory, 'Categorías de actualidad', 'name', POST_CATEGORIES)
        now = timezone.now()
        rows_by_category = {}
        for i, (category, title, excerpt, paragraphs, image) in enumerate(POSTS):
            rows_by_category.setdefault(category, []).append({
                'title': title,
                'excerpt': excerpt,
                'content': '\n\n'.join(paragraphs),
                'author': AUTHOR,
                'published_at': now - timedelta(days=7 * (i + 1)),
                'is_published': True,
                'is_featured': i < 3,
                'seo_title': f'{title} | GRAVIOR'[:70],
                'seo_description': excerpt,
                'images': {'main_image': (image, MAIN_IMAGE_SIZE), 'thumbnail': (image, THUMBNAIL_SIZE)},
            })
        for category_name, rows in rows_by_category.items():
            category = categories.get(category_name)
            if category is not None:
                self.seed_collection(Post, f'Publicaciones de «{category.name}»', 'title', rows, category=category)
        self.seed_collection(ContactReason, 'Motivos de consulta', 'name', [
            {'name': name, 'order': i} for i, name in enumerate(CONTACT_REASONS, start=1)
        ])
        self.stdout.write('Mensajes de contacto: no se cargan (solo llegan desde el formulario).')
        self.stdout.write(self.style.SUCCESS('Bloque E listo.'))
