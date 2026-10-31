"""Carga los contenidos de ejemplo del Bloque D (Equipo y Aliados).

    python manage.py seed_bloque_d                 # crea lo que falta, no toca lo existente
    python manage.py seed_bloque_d --fill-blanks   # además completa campos vacíos

Reglas (sección 25): no se inventan nombres, cargos, correos, teléfonos ni
perfiles reales. Los integrantes usan nombres claramente genéricos y su correo,
teléfono y LinkedIn quedan vacíos (no se muestran). Los aliados son genéricos,
sin logos reales ni marcas de terceros; Cobb no se carga hasta tener su logo
autorizado. Ver docs/CONTENIDO_EJEMPLO.md.
"""

from apps.aliados.models import Partner
from apps.core.models import CallToAction
from apps.core.seeding import SeedCommand, placeholder_logo
from apps.equipo.models import TeamMember

PHOTO_SIZE = (600, 832)
PARTNER_IMAGE_SIZE = (300, 300)
TEAM_PHOTOS = ['gravior/home/team-01.jpg', 'gravior/home/team-02.jpg', 'gravior/home/team-03.jpg']

SPECIALTIES = ['Genética avícola', 'Calidad y bioseguridad', 'Asesoría técnica', 'Producción avícola',
               'Manejo y bienestar', 'Soporte en campo']

TEAM_MEMBERS = [
    {
        'name': f'Nombre del integrante {i}',
        'position': 'Cargo del integrante',
        'specialty': specialty,
        'short_bio': 'Perfil profesional pendiente de incorporar con información oficial del equipo GRAVIOR.',
        'biography': ('Biografía pendiente. Se publicará solo con la información y la autorización de la '
                      'persona integrante del equipo.'),
        'is_featured': i <= 3,
        'order': i,
        'images': {'photo': (TEAM_PHOTOS[(i - 1) % len(TEAM_PHOTOS)], PHOTO_SIZE)},
    }
    for i, specialty in enumerate(SPECIALTIES, start=1)
]

# (tipo de relación, reseña, imagen para el carrusel) — textos genéricos de la maqueta.
PARTNERS = [
    ('Genética', 'Trabajamos con aliados especializados para acercar soluciones genéticas y conocimiento técnico '
                 'al productor.', 'gravior/home/solution-genetics.jpg'),
    ('Soporte técnico', 'La actualización técnica y el intercambio de experiencia fortalecen la toma de decisiones '
                        'en cada operación.', 'gravior/home/solution-technical.jpg'),
    ('Tecnología', 'Integramos herramientas, procesos y criterios técnicos orientados a una producción moderna y '
                   'eficiente.', 'gravior/home/solution-facilities.jpg'),
    ('Bioseguridad', 'La colaboración especializada permite fortalecer protocolos, prevención y buenas prácticas '
                     'en toda la cadena.', 'gravior/home/solution-biosecurity.jpg'),
    ('Producción', 'Impulsamos soluciones que conectan genética, manejo, ambiente y seguimiento técnico.',
     'gravior/home/solution-sustainability.jpg'),
    ('Relación comercial', 'Construimos vínculos profesionales basados en confianza, acompañamiento y objetivos '
                           'compartidos con el sector avícola.', 'gravior/home/field-main.jpg'),
    ('Distribución', 'Aliados comerciales que acercan las soluciones de GRAVIOR a más productores.',
     'gravior/home/hero-01.jpg'),
]

PARTNER_ROWS = [
    {
        'name': f'Aliado de ejemplo {i}',
        'alliance_type': alliance_type,
        'description': description,
        'website': 'https://www.example.com',
        'is_featured': i <= 4,
        'order': i,
        'files': {'logo': placeholder_logo(f'ALIADO {i:02d}')},
        'images': {'image': (image, PARTNER_IMAGE_SIZE)},
    }
    for i, (alliance_type, description, image) in enumerate(PARTNERS, start=1)
]

CALLS_TO_ACTION = [
    {'code': 'team_contact', 'title': 'Contactar al equipo',
     'text': 'Nuestro equipo técnico está disponible para orientarte.',
     'button_text': 'Contactar al equipo', 'button_url': '/contacto/'},
]


class Command(SeedCommand):
    help = 'Carga los contenidos de ejemplo del Bloque D. Con --fill-blanks completa campos vacíos.'

    def seed(self):
        self.seed_collection(TeamMember, 'Miembros del equipo', 'name', TEAM_MEMBERS)
        self.seed_collection(Partner, 'Aliados estratégicos', 'name', PARTNER_ROWS)
        self.seed_calls_to_action()
        self.stdout.write('Cobb: no se carga como aliado hasta contar con su logo y material autorizados.')
        self.stdout.write(self.style.SUCCESS('Bloque D listo.'))

    def seed_calls_to_action(self):
        for row in CALLS_TO_ACTION:
            instance = CallToAction.objects.filter(code=row['code']).first()
            if instance is None:
                self.build(CallToAction, row).save()
                self.report(f'Llamado a la acción «{row["code"]}»', 1)
            elif self.fill_blanks:
                self.fill(instance, row, f'Llamados a la acción «{row["code"]}»')
