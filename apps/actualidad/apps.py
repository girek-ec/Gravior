from django.apps import AppConfig


class ActualidadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.actualidad'
    label = 'actualidad'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Actualidad'
