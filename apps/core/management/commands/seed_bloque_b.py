"""Carga los contenidos de ejemplo del Bloque B (Empresa, Genética, Calidad y bioseguridad).

    python manage.py seed_bloque_b                 # crea lo que falta, no toca lo existente
    python manage.py seed_bloque_b --fill-blanks   # además completa campos vacíos

Textos genéricos basados en el brief y la maqueta, sin cifras, certificaciones,
resultados productivos, nombres ni claims técnicos (sección 25). Cobb aparece
solo como referente genético, sin logo ni datos técnicos hasta contar con
material autorizado. Ver docs/CONTENIDO_EJEMPLO.md.
"""

from apps.calidad.models import QualityArea, QualityPage, QualityStep
from apps.core.seeding import SeedCommand, sample_pdf
from apps.empresa.models import AboutPage, CorporateValue
from apps.genetica.models import GeneticDocument, GeneticFeature, GeneticLine

ABOUT_PAGE = {
    'page_title': 'Nosotros',
    'intro': 'Impulsamos el desarrollo avícola con conocimiento y respaldo técnico',
    'company_description': (
        'GRAVIOR es una empresa del sector avícola dedicada a la producción y comercialización de genética '
        'avícola de alto valor. Trabajamos bajo criterios de calidad, bioseguridad, eficiencia productiva y '
        'compromiso con nuestros clientes.'
    ),
    'purpose': (
        'Ser un aliado estratégico para nuestros clientes y aportar al crecimiento y fortalecimiento de la '
        'avicultura en Ecuador.'
    ),
    'mission': (
        'Acompañar a productores y empresas avícolas con genética, conocimiento técnico y servicio cercano, '
        'para que cada operación avance hacia una producción más eficiente, segura y consistente.'
    ),
    'vision': (
        'Consolidarnos como una marca avícola sólida, confiable, moderna y técnicamente respaldada, con '
        'visión de futuro y capacidad de crecer junto a nuestros clientes.'
    ),
    'value_proposition': 'Conectamos genética, manejo y acompañamiento técnico',
    'client_commitment': (
        'Nuestro enfoque parte del análisis de cada operación para proponer soluciones alineadas con '
        'productividad, sanidad, manejo, bienestar y mejora continua.'
    ),
    'seo_title': 'Nosotros | GRAVIOR',
    'seo_description': (
        'Conoce GRAVIOR, una empresa avícola orientada a soluciones integrales en genética, calidad, '
        'bioseguridad y acompañamiento técnico.'
    ),
    'images': {
        'main_image': 'gravior/home/about-main.jpg',
        'secondary_image': 'gravior/home/field-main.jpg',
    },
}

CORPORATE_VALUES = [
    {'name': 'Genética avícola', 'icon_class': 'bi bi-heart-fill', 'order': 1,
     'description': 'Seleccionamos soluciones genéticas orientadas a expresar potencial productivo con manejo adecuado.',
     'images': {'image': 'gravior/home/solution-genetics.jpg'}},
    {'name': 'Calidad y bioseguridad', 'icon_class': 'bi bi-shield-fill-check', 'order': 2,
     'description': 'Promovemos protocolos y buenas prácticas que ayudan a reducir riesgos y fortalecer la seguridad sanitaria.',
     'images': {'image': 'gravior/home/solution-biosecurity.jpg'}},
    {'name': 'Asesoría técnica', 'icon_class': 'bi bi-people-fill', 'order': 3,
     'description': 'Acompañamos al productor con análisis, seguimiento y recomendaciones aplicadas a su realidad productiva.',
     'images': {'image': 'gravior/home/solution-technical.jpg'}},
    {'name': 'Manejo y producción', 'icon_class': 'bi bi-clipboard-check', 'order': 4,
     'description': 'Integramos criterios de manejo, ambiente y eficiencia para apoyar una producción consistente.',
     'images': {'image': 'gravior/home/field-main.jpg'}},
    {'name': 'Instalaciones', 'icon_class': 'bi bi-gear-fill', 'order': 5,
     'description': 'Valoramos infraestructura funcional, tecnificada y alineada con las exigencias de la avicultura moderna.',
     'images': {'image': 'gravior/home/solution-facilities.jpg'}},
    {'name': 'Sostenibilidad', 'icon_class': 'bi bi-hand-thumbs-up-fill', 'order': 6,
     'description': 'Impulsamos eficiencia, bienestar y mejora continua como parte de una visión responsable de producción.',
     'images': {'image': 'gravior/home/solution-sustainability.jpg'}},
]

GENETIC_LINES = [
    {
        'name': 'Genética Cobb',
        'brand_name': 'Cobb',
        'summary': 'Genética, manejo y conocimiento para expresar el potencial productivo',
        'description': (
            'Cobb es un referente genético importante para GRAVIOR. Integramos esta genética con manejo, '
            'nutrición, ambiente, bioseguridad y acompañamiento técnico para favorecer resultados '
            'consistentes en cada etapa productiva.'
        ),
        'application': 'Genética y manejo para transformar el potencial genético en resultados productivos.',
        'is_featured': True,
        'order': 1,
        'seo_title': 'Genética Cobb | GRAVIOR',
        'seo_description': 'Genética Cobb con el acompañamiento técnico de GRAVIOR para una producción avícola eficiente.',
        'images': {'main_image': ('gravior/home/solution-genetics.jpg', (578, 691)),
                   'secondary_image': ('gravior/home/hero-02.jpg', (600, 672))},
        'features': [
            ('Potencial genético', 'Selección orientada a productividad, uniformidad y eficiencia bajo un manejo adecuado.',
             'bi bi-diagram-3-fill'),
            ('Uniformidad', 'Consistencia de los lotes para facilitar el manejo, la planificación y el desempeño productivo.',
             'bi bi-patch-check-fill'),
            ('Eficiencia', 'Enfoque en el aprovechamiento de recursos y en resultados productivos sostenibles.',
             'bi bi-graph-up-arrow'),
            ('Robustez', 'Características que favorecen la adaptación, la vitalidad y la estabilidad productiva en campo.',
             'bi bi-shield-fill-check'),
            ('Bienestar', 'Manejo responsable orientado a la salud, el comportamiento adecuado y el desempeño de las aves.',
             'bi bi-heart-fill'),
            ('Acompañamiento técnico', 'Soporte especializado para integrar genética, nutrición, ambiente, sanidad y bioseguridad.',
             'bi bi-people-fill'),
        ],
    },
    {
        'name': 'Línea genética de ejemplo',
        'brand_name': 'Marca por confirmar',
        'summary': 'Una línea preparada para presentar nuevas soluciones genéticas con información autorizada',
        'description': (
            'Espacio para una nueva línea genética. Su descripción, imágenes y documentos se publicarán con la '
            'información oficial aprobada por GRAVIOR y, cuando corresponda, por la marca genética.'
        ),
        'application': 'Operaciones avícolas que buscan desempeño, adaptación y acompañamiento técnico continuo.',
        'is_featured': False,
        'order': 2,
        'seo_title': 'Línea genética | GRAVIOR',
        'seo_description': 'Líneas genéticas de GRAVIOR con acompañamiento técnico en cada etapa productiva.',
        'images': {'main_image': ('gravior/home/solution-technical.jpg', (578, 691)),
                   'secondary_image': ('gravior/home/hero-01.jpg', (600, 672))},
        'features': [
            ('Desempeño', 'Orientación a resultados productivos consistentes bajo un manejo adecuado.', 'bi bi-graph-up-arrow'),
            ('Adaptación', 'Atención a las condiciones de cada operación y de su entorno productivo.', 'bi bi-gear-fill'),
            ('Respaldo técnico', 'Seguimiento y recomendaciones del equipo técnico de GRAVIOR.', 'bi bi-people-fill'),
        ],
    },
]

QUALITY_PAGE = {
    'page_title': 'Calidad y bioseguridad',
    'intro': 'Acompañamiento para fortalecer cada etapa productiva',
    'description': 'Soluciones pensadas para la realidad de cada operación.',
    'quality_commitment': (
        'Trabajamos con criterios de consistencia, precisión y operación profesional, revisando cada proceso '
        'junto al productor.'
    ),
    'biosecurity_approach': (
        'Entendemos la bioseguridad como prevención, control y responsabilidad: un conjunto de prácticas que '
        'protege la continuidad y la estabilidad de la operación avícola.'
    ),
    'cta_text': 'Conversemos sobre las necesidades de tu operación avícola.',
    'cta_url': '/contacto/',
    'seo_title': 'Calidad y bioseguridad | GRAVIOR',
    'seo_description': (
        'Conoce el enfoque de GRAVIOR en bioseguridad, manejo, ambiente, alimentación, bienestar, '
        'productividad y acompañamiento técnico para operaciones avícolas.'
    ),
    'images': {'main_image': 'gravior/home/solution-biosecurity.jpg'},
}

QUALITY_AREAS = [
    ('Bioseguridad', 'line-icon-Car-Wheel', 'gravior/home/solution-biosecurity.jpg',
     'Prevención, control y responsabilidad para proteger la continuidad y la estabilidad de cada operación avícola.'),
    ('Manejo', 'line-icon-Gear-2', 'gravior/home/field-main.jpg',
     'Criterios de manejo durante el ciclo productivo para favorecer uniformidad, confort y buen comportamiento del lote.'),
    ('Ambiente', 'line-icon-Sand-watch', 'gravior/home/solution-facilities.jpg',
     'Revisión de temperatura, ventilación, iluminación y cama como parte de un entorno productivo estable.'),
    ('Alimentación', 'line-icon-Gear-2', 'gravior/home/hero-03.jpg',
     'Seguimiento del acceso a alimento y agua y del consumo para orientar decisiones oportunas de manejo.'),
    ('Bienestar', 'line-icon-Sand-watch', 'gravior/home/solution-sustainability.jpg',
     'Observación y buenas prácticas para valorar las condiciones de confort y manejo de las aves.'),
    ('Productividad', 'line-icon-Car-Wheel', 'gravior/home/solution-genetics.jpg',
     'Lectura clara de indicadores de desempeño para planificar y priorizar las mejoras de la operación.'),
    ('Soporte', 'line-icon-Gear-2', 'gravior/home/solution-technical.jpg',
     'Acompañamiento técnico desde el diagnóstico hasta el seguimiento de las recomendaciones acordadas.'),
]

# Etapas tomadas de la maqueta de Calidad y bioseguridad.
QUALITY_STEPS = {
    'Bioseguridad': [
        ('Evaluación de riesgos',
         'Revisamos puntos críticos, flujos de ingreso y condiciones generales para identificar oportunidades de fortalecimiento en bioseguridad.'),
        ('Protocolos de ingreso',
         'Organizamos criterios de acceso, circulación y control orientados a reducir riesgos dentro de la operación avícola.'),
        ('Limpieza y desinfección',
         'Acompañamos la revisión de rutinas de limpieza y desinfección para favorecer procesos más ordenados y consistentes.'),
        ('Seguimiento de medidas',
         'Damos seguimiento a las medidas implementadas y proponemos ajustes según las condiciones observadas en campo.'),
    ],
    'Manejo': [
        ('Recepción y arranque',
         'Acompañamos la preparación y el arranque del lote con atención a condiciones de recepción, confort y adaptación.'),
        ('Densidad y distribución',
         'Revisamos distribución, espacio disponible y condiciones de manejo para favorecer uniformidad y comportamiento adecuado.'),
        ('Consumo y uniformidad',
         'Observamos consumo, peso y uniformidad como referencias para orientar decisiones de manejo durante el ciclo productivo.'),
        ('Rutinas de campo',
         'Apoyamos la organización de rutinas de observación y registro para mantener criterios de trabajo claros y repetibles.'),
    ],
    'Ambiente': [
        ('Temperatura y confort',
         'Revisamos condiciones térmicas y comportamiento de las aves como parte del manejo del ambiente productivo.'),
        ('Ventilación',
         'Evaluamos criterios de ventilación y circulación de aire de acuerdo con la etapa y condiciones de la operación.'),
        ('Iluminación',
         'Acompañamos la revisión de iluminación y programación como elementos que influyen en el comportamiento y manejo del lote.'),
        ('Cama y humedad',
         'Observamos condiciones de cama y humedad para apoyar un entorno productivo más estable y manejable.'),
    ],
    'Alimentación': [
        ('Disponibilidad de alimento',
         'Revisamos disponibilidad, distribución y acceso al alimento como parte del seguimiento diario del lote.'),
        ('Agua de bebida',
         'Acompañamos la revisión del acceso al agua y del funcionamiento general de los sistemas de suministro.'),
        ('Consumo',
         'Analizamos tendencias de consumo para identificar variaciones y apoyar decisiones oportunas de manejo.'),
        ('Eficiencia alimentaria',
         'Integramos datos de consumo y desempeño para orientar una gestión más eficiente de los recursos.'),
    ],
    'Bienestar': [
        ('Observación del comportamiento',
         'Utilizamos la observación del comportamiento como una referencia práctica para valorar condiciones de confort y manejo.'),
        ('Acceso a recursos',
         'Revisamos que las aves dispongan de acceso adecuado a agua, alimento, espacio y condiciones ambientales.'),
        ('Manejo responsable',
         'Promovemos prácticas de manejo cuidadosas y consistentes durante las diferentes etapas del ciclo productivo.'),
        ('Seguimiento de condiciones',
         'Damos seguimiento a las condiciones observadas para apoyar ajustes que favorezcan bienestar y desempeño.'),
    ],
    'Productividad': [
        ('Indicadores clave',
         'Organizamos indicadores de desempeño para disponer de una lectura clara de la evolución del lote.'),
        ('Uniformidad',
         'Revisamos la uniformidad como referencia para el manejo, la planificación y la toma de decisiones productivas.'),
        ('Eficiencia',
         'Relacionamos desempeño y uso de recursos para identificar oportunidades de mejora dentro de la operación.'),
        ('Análisis de resultados',
         'Interpretamos resultados junto al productor para definir prioridades y próximos pasos de mejora.'),
    ],
    'Soporte': [
        ('Diagnóstico inicial',
         'Conocemos la realidad de la operación, sus objetivos y necesidades antes de proponer acciones técnicas.'),
        ('Plan de trabajo',
         'Definimos prioridades y acciones de acompañamiento de acuerdo con las condiciones observadas.'),
        ('Acompañamiento en campo',
         'Realizamos seguimiento técnico orientado a fortalecer la aplicación práctica de las recomendaciones acordadas.'),
        ('Mejora continua',
         'Revisamos avances y oportunidades de ajuste para sostener un proceso de mejora continua.'),
    ],
}

SAMPLE_DOCUMENT_TITLE = 'Documento de ejemplo – reemplazar'


def sample_document(line_name):
    return ('documento-de-ejemplo.pdf', sample_pdf(SAMPLE_DOCUMENT_TITLE, [
        f'Línea: {line_name}',
        'Este archivo es un relleno temporal del sitio web de GRAVIOR.',
        'Reemplázalo desde el administrador por documentación oficial aprobada.',
    ]))


class Command(SeedCommand):
    help = 'Carga los contenidos de ejemplo del Bloque B. Con --fill-blanks completa campos vacíos.'

    def seed(self):
        self.seed_singleton(AboutPage, ABOUT_PAGE, 'Quiénes somos')
        self.seed_collection(CorporateValue, 'Valores corporativos', 'name', CORPORATE_VALUES)
        self.seed_genetics()
        self.seed_singleton(QualityPage, QUALITY_PAGE, 'Página de calidad y bioseguridad')
        self.seed_quality()
        self.stdout.write(self.style.SUCCESS('Bloque B listo.'))

    def seed_genetics(self):
        rows = [{k: v for k, v in line.items() if k != 'features'} for line in GENETIC_LINES]
        lines = self.seed_collection(GeneticLine, 'Líneas genéticas', 'name', rows)
        for data in GENETIC_LINES:
            line = lines.get(data['name'])
            if line is None:
                continue
            self.seed_collection(GeneticFeature, f'Características de «{line.name}»', 'title', [
                {'title': title, 'description': text, 'icon_class': icon, 'order': i}
                for i, (title, text, icon) in enumerate(data['features'], start=1)
            ], genetic_line=line)
            self.seed_collection(GeneticDocument, f'Documentos de «{line.name}»', 'title', [{
                'title': SAMPLE_DOCUMENT_TITLE,
                'document_type': GeneticDocument.DocumentType.DATASHEET,
                'order': 1,
                'files': {'file': sample_document(line.name)},
            }], genetic_line=line)

    def seed_quality(self):
        rows = [{'name': name, 'icon_class': icon, 'description': text, 'order': i, 'images': {'image': image}}
                for i, (name, icon, image, text) in enumerate(QUALITY_AREAS, start=1)]
        areas = self.seed_collection(QualityArea, 'Áreas de calidad', 'name', rows)
        for name, steps in QUALITY_STEPS.items():
            area = areas.get(name)
            if area is None:
                continue
            self.seed_collection(QualityStep, f'Etapas de «{area.name}»', 'title', [
                {'number': f'{i:02d}', 'title': title, 'description': text, 'order': i}
                for i, (title, text) in enumerate(steps, start=1)
            ], quality_area=area)
