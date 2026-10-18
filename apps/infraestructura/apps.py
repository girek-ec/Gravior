from django.apps import AppConfig


class InfraestructuraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.infraestructura'
    label = 'infraestructura'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Infraestructura'
