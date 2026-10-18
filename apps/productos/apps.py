from django.apps import AppConfig


class ProductosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.productos'
    label = 'productos'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Productos'
