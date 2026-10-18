from django.apps import AppConfig


class EmpresaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.empresa'
    label = 'empresa'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Empresa'
