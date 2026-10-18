from django.apps import AppConfig


class InicioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inicio'
    label = 'inicio'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Inicio'
