"""
URLs del sitio GRAVIOR (solo español, sin prefijo de idioma).

Cada app declara sus rutas completas en su propio urls.py.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.inicio.urls')),
    path('', include('apps.empresa.urls')),
    path('', include('apps.genetica.urls')),
    path('', include('apps.calidad.urls')),
    path('', include('apps.productos.urls')),
    path('', include('apps.infraestructura.urls')),
    path('', include('apps.equipo.urls')),
    path('', include('apps.aliados.urls')),
    path('', include('apps.actualidad.urls')),
    path('', include('apps.contacto.urls')),
]

if settings.DEBUG:
    # runserver ya sirve static/ en DEBUG; media/ se agrega aquí.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
