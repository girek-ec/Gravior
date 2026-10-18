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
    path('', include('inicio.urls')),
    path('', include('empresa.urls')),
    path('', include('genetica.urls')),
    path('', include('calidad.urls')),
    path('', include('productos.urls')),
    path('', include('infraestructura.urls')),
    path('', include('equipo.urls')),
    path('', include('aliados.urls')),
    path('', include('actualidad.urls')),
    path('', include('contacto.urls')),
]

if settings.DEBUG:
    # runserver ya sirve static/ en DEBUG; media/ se agrega aquí.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
