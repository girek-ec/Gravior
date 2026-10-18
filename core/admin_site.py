from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig

# Orden de grupos y modelos según la sección 4 del documento de arquitectura.
APP_ORDER = [
    'core', 'inicio', 'empresa', 'genetica', 'calidad', 'productos',
    'infraestructura', 'equipo', 'aliados', 'actualidad', 'contacto', 'auth',
]
MODEL_ORDER = {
    'core': ['SiteConfiguration', 'CorporateEmail', 'SocialNetwork', 'CallToAction'],
    'inicio': ['HeroSlide', 'Differential', 'Statistic', 'ProcessStep'],
}


class GraviorAdminSite(AdminSite):
    site_header = 'Administración del sitio web'
    site_title = 'Administración del sitio web'
    index_title = 'Contenido del sitio'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        def app_key(app):
            label = app['app_label']
            return APP_ORDER.index(label) if label in APP_ORDER else len(APP_ORDER)

        for app in app_list:
            order = MODEL_ORDER.get(app['app_label'])
            if order:
                app['models'].sort(
                    key=lambda m: order.index(m['object_name']) if m['object_name'] in order else len(order))
        return sorted(app_list, key=app_key)


class GraviorAdminConfig(AdminConfig):
    """Reemplaza a django.contrib.admin en INSTALLED_APPS para usar GraviorAdminSite."""

    default_site = 'core.admin_site.GraviorAdminSite'
