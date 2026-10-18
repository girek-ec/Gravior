from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),

    # =========================================================
    # CRAFTO - Recursos originales
    # Se mantienen temporalmente para no modificar los HTML.
    # Solo para desarrollo.
    # =========================================================

    re_path(
        r'^(?P<path>(?:css|js|images|fonts|demos|revolution)/.*)$',
        serve,
        {
            'document_root': settings.BASE_DIR / 'static' / 'crafto'
        },
    ),

    # =========================================================
    # Aplicación
    # =========================================================

    path('', include('core.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )