from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    label = 'core'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Configuración'
