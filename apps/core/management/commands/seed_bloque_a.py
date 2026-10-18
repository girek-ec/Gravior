"""Carga los contenidos de ejemplo del Bloque A (Configuración e Inicio).

    python manage.py seed_bloque_a                 # crea lo que falta, no toca lo existente
    python manage.py seed_bloque_a --fill-blanks   # además completa campos vacíos

Los textos salen de la maqueta y del brief (docs/). Los datos que solo puede
entregar el cliente usan valores de ejemplo evidentes. No se cargan
indicadores (Statistic): solo se publican cifras oficiales aprobadas.
Ver docs/CONTENIDO_EJEMPLO.md.
"""

from apps.core.models import CallToAction, CorporateEmail, SiteConfiguration, SocialNetwork
from apps.core.seeding import SeedCommand
from apps.inicio.models import Differential, HeroSlide, ProcessStep

EXAMPLE_PHONE = '+593 00 000 0000'

SITE_CONFIGURATION = {
    'company_name': 'GRAVIOR',
    'legal_name': 'Razón social por confirmar',
    'short_description': (
        'Gravior es una empresa del sector avícola dedicada a la producción y comercialización de '
        'genética avícola de alto valor, orientada a atender las necesidades de productores y '
        'empresas de la industria avícola.'
    ),
    'phone': EXAMPLE_PHONE,
    'whatsapp_number': EXAMPLE_PHONE,
    'whatsapp_message': 'Hola, quisiera recibir información sobre GRAVIOR.',
    'whatsapp_enabled': True,
    'main_email': 'info@example.com',
    'address': 'Dirección por definir',
    'city': 'Ciudad por definir',
    'province': 'Provincia por definir',
    'country': 'Ecuador',
    'business_hours': 'Lunes a viernes: horario por definir',
    'google_maps_url': 'https://maps.example.com/gravior',
    'copyright_text': 'Copyright 2026',
    'default_seo_title': 'GRAVIOR | Soluciones avícolas integrales',
    'default_seo_description': (
        'GRAVIOR impulsa el desarrollo de la avicultura con soluciones integrales en genética, '
        'calidad, bioseguridad y acompañamiento técnico.'
    ),
    # Relleno de la maqueta: el cliente debe reemplazarlo por su identidad oficial.
    'images': {
        'logo': 'demo-gym-and-fitness-logo-black.png',
        'logo_white': 'demo-gym-and-fitness-logo-white.png',
        'favicon': 'favicon.png',
    },
}

CORPORATE_EMAILS = [
    {'label': 'Información', 'email': 'info@example.com', 'email_type': CorporateEmail.EmailType.INFO, 'order': 1},
    {'label': 'Comercial', 'email': 'comercial@example.com', 'email_type': CorporateEmail.EmailType.COMMERCIAL, 'order': 2},
    {'label': 'Ventas', 'email': 'ventas@example.com', 'email_type': CorporateEmail.EmailType.SALES, 'order': 3},
    {'label': 'Administración', 'email': 'administracion@example.com', 'email_type': CorporateEmail.EmailType.ADMIN, 'order': 4},
]

SOCIAL_NETWORKS = [
    {'name': 'Facebook', 'icon_class': 'fa-brands fa-facebook-f', 'url': 'https://www.facebook.com/example', 'order': 1},
    {'name': 'Instagram', 'icon_class': 'fa-brands fa-instagram', 'url': 'https://www.instagram.com/example', 'order': 2},
    {'name': 'LinkedIn', 'icon_class': 'fa-brands fa-linkedin-in', 'url': 'https://www.linkedin.com/company/example', 'order': 3},
]

CALLS_TO_ACTION = [
    {'code': 'header_contact', 'title': 'Contacto',
     'text': 'Conversemos sobre las necesidades de tu operación avícola.',
     'button_text': 'Contáctanos', 'button_url': '/contacto/'},
    {'code': 'home_process', 'title': 'Trabajamos junto a cada productor',
     'text': 'Te acompañamos desde el diagnóstico hasta el seguimiento de resultados.',
     'button_text': 'Contactar asesor', 'button_url': '/contacto/'},
    {'code': 'about_contact', 'title': 'Hablar con un asesor',
     'text': 'Nuestro equipo comercial y técnico está disponible para orientarte.',
     'button_text': 'Contactar asesor', 'button_url': '/contacto/'},
]

HERO_SLIDES = [
    {
        'highlight_text': 'GRAVIOR', 'eyebrow': 'Genética · calidad · bioseguridad',
        'title': 'Impulsamos el futuro avícola',
        'description': 'Soluciones integrales para una avicultura eficiente, segura y sostenible, '
                       'con acompañamiento técnico en cada etapa.',
        'primary_button_text': 'Conoce más', 'primary_button_url': '/nosotros/',
        'secondary_button_text': 'Hablar con un asesor', 'secondary_button_url': '/contacto/',
        'order': 1,
        'images': {'desktop_image': 'gravior/home/hero-01.jpg', 'thumbnail': 'gravior/home/hero-thumb-01.jpg'},
    },
    {
        'highlight_text': 'TECNOLOGÍA', 'eyebrow': 'Genética de alto desempeño',
        'title': 'Soluciones que nacen de la genética',
        'description': 'Integramos conocimiento, calidad y manejo para fortalecer el desempeño '
                       'productivo de cada operación avícola.',
        'primary_button_text': 'Conoce más', 'primary_button_url': '/genetica/',
        'secondary_button_text': 'Hablar con un asesor', 'secondary_button_url': '/contacto/',
        'order': 2,
        'images': {'desktop_image': 'gravior/home/hero-02.jpg', 'thumbnail': 'gravior/home/hero-thumb-02.jpg'},
    },
    {
        'highlight_text': 'CONFIANZA', 'eyebrow': 'Acompañamiento especializado',
        'title': 'Conocimiento para producir mejor',
        'description': 'Trabajamos junto al productor con soluciones enfocadas en bioseguridad, '
                       'eficiencia, bienestar y resultados consistentes.',
        'primary_button_text': 'Conoce más', 'primary_button_url': '/calidad-bioseguridad/',
        'secondary_button_text': 'Hablar con un asesor', 'secondary_button_url': '/contacto/',
        'order': 3,
        'images': {'desktop_image': 'gravior/home/hero-03.jpg', 'thumbnail': 'gravior/home/hero-thumb-03.jpg'},
    },
]

# Mensajes de la sección 2.2 del documento de arquitectura (lectura del brief).
DIFFERENTIALS = [
    {'title': 'Genética', 'description': 'Genética avícola de alto valor, con desempeño y respaldo técnico.',
     'icon_class': 'bi bi-heart-fill', 'order': 1},
    {'title': 'Calidad', 'description': 'Consistencia, precisión y criterios de operación profesional.',
     'icon_class': 'bi bi-patch-check-fill', 'order': 2},
    {'title': 'Bioseguridad', 'description': 'Prevención, control y responsabilidad en los procesos.',
     'icon_class': 'bi bi-shield-fill-check', 'order': 3},
    {'title': 'Tecnología', 'description': 'Una empresa moderna y tecnificada, con visión de futuro.',
     'icon_class': 'bi bi-cpu', 'order': 4},
    {'title': 'Eficiencia', 'description': 'Orientación a la productividad, los resultados y la generación de valor.',
     'icon_class': 'bi bi-graph-up-arrow', 'order': 5},
    {'title': 'Confianza', 'description': 'Cumplimiento, solidez y relaciones comerciales de largo plazo.',
     'icon_class': 'bi bi-hand-thumbs-up-fill', 'order': 6},
]

PROCESS_STEPS = [
    {'number': '01', 'title': 'Diagnóstico', 'icon_class': 'bi bi-clipboard-check', 'order': 1,
     'description': 'Conocemos las necesidades, condiciones y objetivos de cada operación.'},
    {'number': '02', 'title': 'Estrategia', 'icon_class': 'bi bi-diagram-3-fill', 'order': 2,
     'description': 'Definimos soluciones técnicas acordes con la realidad productiva.'},
    {'number': '03', 'title': 'Acompañamiento', 'icon_class': 'bi bi-people-fill', 'order': 3,
     'description': 'Damos seguimiento para fortalecer procesos y resultados de manera continua.'},
]


class Command(SeedCommand):
    help = 'Carga los contenidos de ejemplo del Bloque A. Con --fill-blanks completa campos vacíos.'

    def seed(self):
        self.seed_singleton(SiteConfiguration, SITE_CONFIGURATION, 'Configuración general')
        self.seed_collection(CorporateEmail, 'Correos corporativos', 'email', CORPORATE_EMAILS)
        self.seed_collection(SocialNetwork, 'Redes sociales', 'name', SOCIAL_NETWORKS)
        self.seed_calls_to_action()
        self.seed_collection(HeroSlide, 'Slider principal', 'title', HERO_SLIDES)
        self.seed_collection(Differential, 'Diferenciales', 'title', DIFFERENTIALS)
        self.seed_collection(ProcessStep, 'Etapas del proceso', 'number', PROCESS_STEPS)
        self.stdout.write('Indicadores: no se cargan cifras (solo se publican cifras oficiales aprobadas).')
        self.stdout.write(self.style.SUCCESS('Bloque A listo.'))

    def seed_calls_to_action(self):
        """Los CTA se crean por identificador: la plantilla depende de cada código."""
        created = 0
        for row in CALLS_TO_ACTION:
            instance = CallToAction.objects.filter(code=row['code']).first()
            if instance is None:
                self.build(CallToAction, row).save()
                created += 1
            elif self.fill_blanks:
                self.fill(instance, row, f'Llamados a la acción «{row["code"]}»')
        if created:
            self.report('Llamados a la acción', created)
        else:
            self.stdout.write('Llamados a la acción: todos los identificadores ya existen.')
