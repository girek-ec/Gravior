from django.apps import AppConfig


class ContactoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacto'
    label = 'contacto'  # se conserva el label original: migraciones, tablas y django_migrations no cambian
    verbose_name = 'Contacto'
