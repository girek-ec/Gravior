from django.apps import AppConfig


class AliadosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.aliados'
    label = 'aliados'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Aliados'
