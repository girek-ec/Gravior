"""Carga los contenidos de ejemplo del Bloque C (Productos e Infraestructura).

    python manage.py seed_bloque_c                 # crea lo que falta, no toca lo existente
    python manage.py seed_bloque_c --fill-blanks   # además completa campos vacíos

Textos genéricos basados en la maqueta, sin precios, cifras, capacidades,
certificaciones ni claims técnicos (sección 25). Las instalaciones no incluyen
capacidad exacta ni ubicaciones sensibles. Ver docs/CONTENIDO_EJEMPLO.md.
"""

from apps.core.seeding import SeedCommand, sample_pdf
from apps.infraestructura.models import Facility, FacilityCategory, FacilityGallery
from apps.productos.models import Product, ProductCategory, ProductDocument, ProductFeature

SAMPLE_DOCUMENT_TITLE = 'Documento de ejemplo – reemplazar'
PRODUCT_IMAGE_SIZE = (960, 640)
FACILITY_IMAGE_SIZE = (800, 635)
GALLERY_IMAGE_SIZE = (1040, 700)

PRODUCT_CATEGORIES = [
    {'name': 'Genética', 'order': 1,
     'description': 'Genética orientada a productividad y uniformidad, integrada con manejo, ambiente y sanidad.'},
    {'name': 'Bioseguridad', 'order': 2,
     'description': 'Enfoque preventivo en calidad y bioseguridad para proteger la continuidad de la operación.'},
    {'name': 'Soporte técnico', 'order': 3,
     'description': 'Acompañamiento técnico aplicado a campo y soporte especializado para fortalecer resultados.'},
]

PRODUCTS = [
    {
        'category': 'Genética', 'name': 'Línea genética', 'brand': 'Marca por confirmar', 'reference': 'EJ-01',
        'summary': 'Potencial productivo',
        'description': ('Solución genética orientada a expresar el potencial productivo de cada operación, '
                        'acompañada de recomendaciones de manejo y seguimiento técnico.'),
        'application': 'Operaciones avícolas que buscan uniformidad y eficiencia bajo un manejo adecuado.',
        'benefits': 'Selección genética, uniformidad de los lotes y acompañamiento técnico durante el ciclo productivo.',
        'inquiry_button_text': 'Solicitar información', 'is_featured': False, 'order': 1,
        'seo_title': 'Línea genética | GRAVIOR',
        'seo_description': 'Solución genética de GRAVIOR con acompañamiento técnico para una producción eficiente.',
        'image': 'gravior/home/solution-genetics.jpg',
        'features': [
            ('Selección genética', 'Genética orientada a productividad y uniformidad.'),
            ('Uniformidad y desempeño', 'Lotes consistentes que facilitan el manejo y la planificación.'),
            ('Eficiencia productiva', 'Enfoque en el aprovechamiento de recursos y en resultados sostenibles.'),
            ('Manejo según programa', 'Recomendaciones de manejo acordes con cada etapa productiva.'),
            ('Soporte según necesidad', 'Acompañamiento técnico ajustado a la realidad de cada operación.'),
        ],
    },
    {
        'category': 'Bioseguridad', 'name': 'Control sanitario', 'brand': 'GRAVIOR', 'reference': 'EJ-02',
        'summary': 'Prevención y seguridad',
        'description': ('Acompañamiento para revisar y fortalecer las prácticas de bioseguridad de la operación, '
                        'con foco en prevención, control y seguimiento.'),
        'application': 'Granjas y operaciones avícolas que buscan fortalecer sus prácticas preventivas.',
        'benefits': 'Protocolos ordenados, prevención de riesgos y seguimiento de las medidas implementadas.',
        'inquiry_button_text': 'Solicitar información', 'is_featured': True, 'order': 2,
        'seo_title': 'Control sanitario | GRAVIOR',
        'seo_description': 'Acompañamiento de GRAVIOR en bioseguridad: prevención, control y buenas prácticas.',
        'image': 'gravior/home/solution-biosecurity.jpg',
        'features': [
            ('Protocolos de bioseguridad', 'Criterios de acceso, circulación y control dentro de la operación.'),
            ('Prevención de riesgos', 'Identificación de puntos críticos y oportunidades de mejora.'),
            ('Buenas prácticas sanitarias', 'Rutinas de limpieza y desinfección más ordenadas y consistentes.'),
            ('Control de procesos', 'Seguimiento de las medidas aplicadas en campo.'),
            ('Seguimiento técnico', 'Ajustes propuestos según las condiciones observadas.'),
        ],
    },
    {
        'category': 'Soporte técnico', 'name': 'Asesoría técnica', 'brand': 'GRAVIOR', 'reference': 'EJ-03',
        'summary': 'Acompañamiento integral',
        'description': ('Soporte técnico desde el diagnóstico hasta el seguimiento de resultados, con '
                        'recomendaciones aplicadas a la realidad productiva de cada cliente.'),
        'application': 'Productores y empresas avícolas que necesitan respaldo técnico en cada etapa.',
        'benefits': 'Diagnóstico productivo, recomendaciones de manejo y seguimiento de resultados.',
        'inquiry_button_text': 'Hablar con un asesor', 'is_featured': True, 'order': 3,
        'seo_title': 'Asesoría técnica | GRAVIOR',
        'seo_description': 'Asesoría técnica de GRAVIOR para acompañar cada etapa de la producción avícola.',
        'image': 'gravior/home/solution-technical.jpg',
        'features': [
            ('Diagnóstico productivo', 'Conocemos las necesidades y objetivos de cada operación.'),
            ('Recomendaciones de manejo', 'Propuestas técnicas acordes con la realidad productiva.'),
            ('Seguimiento de resultados', 'Revisión de avances y oportunidades de ajuste.'),
            ('Capacitación técnica', 'Espacios para fortalecer criterios de trabajo del equipo de campo.'),
            ('Asistencia especializada', 'Respaldo técnico ante las necesidades de cada etapa.'),
        ],
    },
]

FACILITY_CATEGORIES = [
    {'name': 'Galpones', 'order': 1},
    {'name': 'Tecnología', 'order': 2},
    {'name': 'Bioseguridad', 'order': 3},
    {'name': 'Operación', 'order': 4},
]

# (categoría, título, resumen, imagen principal, imágenes de galería)
FACILITIES = [
    ('Galpones', 'Galpones tecnificados', 'Espacios productivos organizados para un manejo ordenado del lote.',
     'gravior/home/hero-01.jpg', ['gravior/home/hero-03.jpg', 'gravior/home/solution-facilities.jpg']),
    ('Tecnología', 'Sistemas de ventilación', 'Criterios de ventilación y circulación de aire según cada etapa.',
     'gravior/home/solution-facilities.jpg', ['gravior/home/hero-01.jpg', 'gravior/home/hero-02.jpg']),
    ('Tecnología', 'Control ambiental', 'Atención a temperatura, humedad y confort dentro del galpón.',
     'gravior/home/hero-02.jpg', ['gravior/home/solution-sustainability.jpg', 'gravior/home/hero-03.jpg']),
    ('Bioseguridad', 'Áreas de bioseguridad', 'Espacios y flujos pensados para la prevención y el control sanitario.',
     'gravior/home/solution-biosecurity.jpg', ['gravior/home/about-main.jpg', 'gravior/home/field-main.jpg']),
    ('Operación', 'Equipamiento productivo', 'Equipos de trabajo que apoyan una operación ordenada y eficiente.',
     'gravior/home/hero-03.jpg', ['gravior/home/hero-01.jpg', 'gravior/home/solution-facilities.jpg']),
    ('Tecnología', 'Sistemas de alimentación', 'Distribución y acceso al alimento como parte del manejo diario.',
     'gravior/home/solution-sustainability.jpg', ['gravior/home/hero-02.jpg', 'gravior/home/hero-03.jpg']),
    ('Operación', 'Incubación y manejo inicial', 'Atención a la recepción y al arranque de cada lote.',
     'gravior/home/solution-genetics.jpg', ['gravior/home/hero-02.jpg', 'gravior/home/solution-genetics.jpg']),
    ('Tecnología', 'Monitoreo técnico', 'Registro y observación de indicadores para orientar decisiones de manejo.',
     'gravior/home/solution-technical.jpg', ['gravior/home/field-main.jpg', 'gravior/home/about-main.jpg']),
    ('Galpones', 'Distribución y flujo operativo', 'Organización de espacios y circulación dentro de la operación.',
     'gravior/home/field-main.jpg', ['gravior/home/hero-01.jpg', 'gravior/home/solution-biosecurity.jpg']),
    ('Bioseguridad', 'Higiene y desinfección', 'Rutinas de limpieza y desinfección como parte de la prevención.',
     'gravior/home/about-main.jpg', ['gravior/home/solution-biosecurity.jpg', 'gravior/home/field-main.jpg']),
    ('Operación', 'Bienestar y manejo', 'Prácticas de manejo cuidadosas durante el ciclo productivo.',
     'gravior/home/hero-02.jpg', ['gravior/home/solution-sustainability.jpg', 'gravior/home/hero-01.jpg']),
    ('Galpones', 'Infraestructura para producción', 'Infraestructura funcional alineada con la avicultura moderna.',
     'gravior/home/solution-facilities.jpg', ['gravior/home/hero-03.jpg', 'gravior/home/solution-technical.jpg']),
]

GALLERY_CAPTIONS = ['Vista general', 'Detalle de la instalación']


def sample_document(product_name):
    return ('documento-de-ejemplo.pdf', sample_pdf(SAMPLE_DOCUMENT_TITLE, [
        f'Producto: {product_name}',
        'Este archivo es un relleno temporal del sitio web de GRAVIOR.',
        'Reemplázalo desde el administrador por documentación oficial aprobada.',
    ]))


class Command(SeedCommand):
    help = 'Carga los contenidos de ejemplo del Bloque C. Con --fill-blanks completa campos vacíos.'

    def seed(self):
        self.seed_products()
        self.seed_facilities()
        self.stdout.write(self.style.SUCCESS('Bloque C listo.'))

    def seed_products(self):
        categories = self.seed_collection(ProductCategory, 'Categorías de productos', 'name', PRODUCT_CATEGORIES)
        for data in PRODUCTS:
            category = categories.get(data['category'])
            if category is None:
                continue
            row = {k: v for k, v in data.items() if k not in ('category', 'image', 'features')}
            row['images'] = {'main_image': (data['image'], PRODUCT_IMAGE_SIZE)}
            # Los productos se cargan por categoría: si el cliente ya tiene productos en ella, no se crean.
            product = self.seed_collection(Product, f'Productos de «{category.name}»', 'name', [row],
                                           category=category).get(data['name'])
            if product is None:
                continue
            self.seed_collection(ProductFeature, f'Características de «{product.name}»', 'title', [
                {'title': title, 'description': text, 'order': i}
                for i, (title, text) in enumerate(data['features'], start=1)
            ], product=product)
            self.seed_collection(ProductDocument, f'Documentos de «{product.name}»', 'title', [{
                'title': SAMPLE_DOCUMENT_TITLE,
                'document_type': ProductDocument.DocumentType.DATASHEET,
                'order': 1,
                'files': {'file': sample_document(product.name)},
            }], product=product)

    def seed_facilities(self):
        categories = self.seed_collection(FacilityCategory, 'Categorías de instalaciones', 'name', FACILITY_CATEGORIES)
        rows_by_category = {}
        for i, (category_name, title, summary, image, gallery) in enumerate(FACILITIES, start=1):
            rows_by_category.setdefault(category_name, []).append({
                'title': title, 'summary': summary,
                'description': (f'{summary} Contenido de referencia: se reemplazará con la descripción y las '
                                'fotografías propias aprobadas por GRAVIOR.'),
                'public_location': 'Provincia por confirmar',
                'is_featured': i <= 3, 'order': i,
                'images': {'main_image': (image, FACILITY_IMAGE_SIZE)},
                'gallery': gallery,
            })
        for category_name, rows in rows_by_category.items():
            category = categories.get(category_name)
            if category is None:
                continue
            clean_rows = [{k: v for k, v in row.items() if k != 'gallery'} for row in rows]
            facilities = self.seed_collection(Facility, f'Instalaciones de «{category.name}»', 'title', clean_rows,
                                              category=category)
            for row in rows:
                facility = facilities.get(row['title'])
                if facility is None:
                    continue
                self.seed_collection(FacilityGallery, f'Galería de «{facility.title}»', 'caption', [
                    {'caption': caption, 'order': n, 'images': {'image': (path, GALLERY_IMAGE_SIZE)}}
                    for n, (caption, path) in enumerate(zip(GALLERY_CAPTIONS, row['gallery']), start=1)
                ], facility=facility)
