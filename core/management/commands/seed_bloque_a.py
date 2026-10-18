"""Carga los contenidos por defecto del Bloque A (Configuración e Inicio).

Idempotente y conservador: un modelo solo se carga si su tabla está vacía, y
los llamados a la acción se crean por identificador si no existen. Nunca
modifica registros existentes, así que no pisa lo que el cliente ya editó.

Los textos salen de la maqueta y del brief (docs/). Los datos que solo puede
entregar el cliente se cargan con valores de ejemplo evidentes.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import CallToAction, CorporateEmail, SiteConfiguration, SocialNetwork
from inicio.models import Differential, HeroSlide, ProcessStep

STATIC_IMAGES = Path(settings.BASE_DIR) / 'static' / 'crafto' / 'images'

EXAMPLE_PHONE = '+593 00 000 0000'

SITE_CONFIGURATION = {
    'company_name': 'GRAVIOR',
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
    'country': 'Ecuador',
    'business_hours': 'Lunes a viernes: horario por definir',
    'copyright_text': 'Copyright 2026',
    'default_seo_title': 'GRAVIOR | Soluciones avícolas integrales',
    'default_seo_description': (
        'GRAVIOR impulsa el desarrollo de la avicultura con soluciones integrales en genética, '
        'calidad, bioseguridad y acompañamiento técnico.'
    ),
}
# Imágenes de relleno de la maqueta; el cliente debe reemplazarlas por el logo oficial.
SITE_IMAGES = {
    'logo': 'demo-gym-and-fitness-logo-black.png',
    'logo_white': 'demo-gym-and-fitness-logo-white.png',
    'favicon': 'favicon.png',
}

CORPORATE_EMAILS = [
    ('Información', 'info@example.com', CorporateEmail.EmailType.INFO),
    ('Comercial', 'comercial@example.com', CorporateEmail.EmailType.COMMERCIAL),
    ('Ventas', 'ventas@example.com', CorporateEmail.EmailType.SALES),
    ('Administración', 'administracion@example.com', CorporateEmail.EmailType.ADMIN),
]

SOCIAL_NETWORKS = [
    ('Facebook', 'fa-brands fa-facebook-f', 'https://www.facebook.com/example'),
    ('Instagram', 'fa-brands fa-instagram', 'https://www.instagram.com/example'),
    ('LinkedIn', 'fa-brands fa-linkedin-in', 'https://www.linkedin.com/company/example'),
]

CALLS_TO_ACTION = [
    {'code': 'header_contact', 'title': 'Contacto', 'button_text': 'Contáctanos', 'button_url': '/contacto/'},
    {'code': 'home_process', 'title': 'Trabajamos junto a cada productor',
     'button_text': 'Contactar asesor', 'button_url': '/contacto/'},
    {'code': 'about_contact', 'title': 'Hablar con un asesor',
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
        'images': ('gravior/home/hero-01.jpg', 'gravior/home/hero-thumb-01.jpg'),
    },
    {
        'highlight_text': 'TECNOLOGÍA', 'eyebrow': 'Genética de alto desempeño',
        'title': 'Soluciones que nacen de la genética',
        'description': 'Integramos conocimiento, calidad y manejo para fortalecer el desempeño '
                       'productivo de cada operación avícola.',
        'primary_button_text': 'Conoce más', 'primary_button_url': '/genetica/',
        'secondary_button_text': 'Hablar con un asesor', 'secondary_button_url': '/contacto/',
        'images': ('gravior/home/hero-02.jpg', 'gravior/home/hero-thumb-02.jpg'),
    },
    {
        'highlight_text': 'CONFIANZA', 'eyebrow': 'Acompañamiento especializado',
        'title': 'Conocimiento para producir mejor',
        'description': 'Trabajamos junto al productor con soluciones enfocadas en bioseguridad, '
                       'eficiencia, bienestar y resultados consistentes.',
        'primary_button_text': 'Conoce más', 'primary_button_url': '/calidad-bioseguridad/',
        'secondary_button_text': 'Hablar con un asesor', 'secondary_button_url': '/contacto/',
        'images': ('gravior/home/hero-03.jpg', 'gravior/home/hero-thumb-03.jpg'),
    },
]

# Mensajes de la sección 2.2 del documento de arquitectura (lectura del brief).
DIFFERENTIALS = [
    ('Genética', 'Genética avícola de alto valor, con desempeño y respaldo técnico.', 'bi bi-heart-fill'),
    ('Calidad', 'Consistencia, precisión y criterios de operación profesional.', 'bi bi-patch-check-fill'),
    ('Bioseguridad', 'Prevención, control y responsabilidad en los procesos.', 'bi bi-shield-fill-check'),
    ('Tecnología', 'Una empresa moderna y tecnificada, con visión de futuro.', 'bi bi-cpu'),
    ('Eficiencia', 'Orientación a la productividad, los resultados y la generación de valor.',
     'bi bi-graph-up-arrow'),
    ('Confianza', 'Cumplimiento, solidez y relaciones comerciales de largo plazo.', 'bi bi-hand-thumbs-up-fill'),
]

PROCESS_STEPS = [
    ('01', 'Diagnóstico', 'Conocemos las necesidades, condiciones y objetivos de cada operación.'),
    ('02', 'Estrategia', 'Definimos soluciones técnicas acordes con la realidad productiva.'),
    ('03', 'Acompañamiento', 'Damos seguimiento para fortalecer procesos y resultados de manera continua.'),
]


def attach_image(instance, field_name, relative_path):
    """Copia una imagen de static/crafto/images/ al campo (y por lo tanto a media/)."""
    source = STATIC_IMAGES / relative_path
    with source.open('rb') as fh:
        getattr(instance, field_name).save(source.name, File(fh), save=False)


class Command(BaseCommand):
    help = 'Carga los contenidos por defecto del Bloque A sin modificar registros existentes.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.seed_site_configuration()
        self.seed_collection(CorporateEmail, 'correos corporativos', [
            CorporateEmail(label=label, email=email, email_type=kind, order=i)
            for i, (label, email, kind) in enumerate(CORPORATE_EMAILS, start=1)
        ])
        self.seed_collection(SocialNetwork, 'redes sociales', [
            SocialNetwork(name=name, icon_class=icon, url=url, order=i)
            for i, (name, icon, url) in enumerate(SOCIAL_NETWORKS, start=1)
        ])
        self.seed_calls_to_action()
        self.seed_hero_slides()
        self.seed_collection(Differential, 'diferenciales', [
            Differential(title=title, description=text, icon_class=icon, order=i)
            for i, (title, text, icon) in enumerate(DIFFERENTIALS, start=1)
        ])
        self.seed_collection(ProcessStep, 'etapas del proceso', [
            ProcessStep(number=number, title=title, description=text, order=i)
            for i, (number, title, text) in enumerate(PROCESS_STEPS, start=1)
        ])
        self.stdout.write('Indicadores: no se cargan cifras (solo se publican cifras oficiales aprobadas).')
        self.stdout.write(self.style.SUCCESS('Bloque A listo.'))

    def report(self, label, created):
        if created:
            self.stdout.write(self.style.SUCCESS(f'{label}: {created} creado(s).'))
        else:
            self.stdout.write(f'{label}: ya tiene datos, no se modifica.')

    def seed_site_configuration(self):
        if SiteConfiguration.objects.exists():
            return self.report('Configuración general', 0)
        config = SiteConfiguration(**SITE_CONFIGURATION)
        for field, filename in SITE_IMAGES.items():
            attach_image(config, field, filename)
        config.save()
        self.report('Configuración general', 1)

    def seed_collection(self, model, label, objects):
        if model.objects.exists():
            return self.report(label.capitalize(), 0)
        model.objects.bulk_create(objects)
        self.report(label.capitalize(), len(objects))

    def seed_calls_to_action(self):
        created = 0
        for data in CALLS_TO_ACTION:
            _, was_created = CallToAction.objects.get_or_create(code=data['code'], defaults=data)
            created += was_created
        if created:
            self.report('Llamados a la acción', created)
        else:
            self.stdout.write('Llamados a la acción: todos los identificadores ya existen, no se modifican.')

    def seed_hero_slides(self):
        if HeroSlide.objects.exists():
            return self.report('Slider principal', 0)
        for i, data in enumerate(HERO_SLIDES, start=1):
            data = dict(data)
            desktop, thumbnail = data.pop('images')
            slide = HeroSlide(order=i, **data)
            attach_image(slide, 'desktop_image', desktop)
            attach_image(slide, 'thumbnail', thumbnail)
            slide.save()
        self.report('Slider principal', len(HERO_SLIDES))
