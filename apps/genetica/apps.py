from django.apps import AppConfig


class GeneticaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.genetica'
    label = 'genetica'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Genética'
