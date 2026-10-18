# GRAVIOR · Sitio web corporativo

Backend Django del sitio corporativo de GRAVIOR. La maqueta visual se basa en
la plantilla Crafto HTML5: la plantilla controla el diseño y Django controla el
contenido (ver el documento de arquitectura del proyecto).

- Python 3.10+ · Django 5.2 LTS
- Solo español (`LANGUAGE_CODE='es'`, `TIME_ZONE='America/Guayaquil'`)

## Puesta en marcha (Windows / PowerShell)

```powershell
git clone <url-del-repo> Gravior
cd Gravior
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` y define una `SECRET_KEY` propia:

```powershell
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

Luego:

```powershell
python manage.py migrate
python manage.py seed_bloque_a   # contenidos de ejemplo del Bloque A (no pisa lo editado)
python manage.py seed_bloque_b   # contenidos de ejemplo del Bloque B
python manage.py createsuperuser
python manage.py runserver
```

- Sitio: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

En Linux/macOS la activación es `source venv/bin/activate` y la copia
`cp .env.example .env`.

## Contenidos de ejemplo

Los comandos `seed_bloque_*` cargan textos e imágenes de ejemplo para que
ninguna sección quede en blanco. Sin opciones solo crean lo que falta; con
`--fill-blanks` además completan los campos vacíos de registros existentes,
sin sobrescribir nunca lo que ya tiene contenido. La lista de lo que debe
reemplazarse antes de publicar está en `docs/CONTENIDO_EJEMPLO.md`.

## Tests

```powershell
python manage.py test
```

## Estructura

Todas las apps están dentro de `apps/` (paquete Python). Cada una conserva su
*label* original (`core`, `inicio`, …), por lo que las tablas y las migraciones
no cambian de nombre.

| App | Contenido |
| --- | --- |
| `apps/core` | Configuración general, correos, redes, CTAs y utilidades compartidas |
| `apps/inicio` | Slider, diferenciales, indicadores y proceso de la página de inicio |
| `apps/empresa` | Quiénes somos y valores corporativos |
| `apps/genetica` | Líneas genéticas, características y documentos |
| `apps/calidad` | Calidad y bioseguridad |
| `apps/productos` | Catálogo informativo (sin tienda) |
| `apps/infraestructura` | Instalaciones y galería |
| `apps/equipo` | Equipo técnico |
| `apps/aliados` | Aliados estratégicos |
| `apps/actualidad` | Noticias y artículos |
| `apps/contacto` | Motivos de consulta y mensajes recibidos |

- `templates/base.html`: layout Crafto con bloques `title`, `meta_description`,
  `extra_css`, `extra_head`, `nav`, `content`, `footer`, `after_footer` y `extra_js`.
- `templates/includes/`: header y footer.
- `templates/gravior/`: maqueta adaptada de cada página (la usan las vistas).
- `templates/crafto/`: HTML originales de la demo, solo como referencia.
- `static/crafto/`: assets de Crafto (css, js, images, fonts, revolution, demos).
- `media/`: archivos subidos desde el admin (no se versiona).

## Documentación

`docs/` contiene la bitácora de desarrollo (`BITACORA.md`), la lista de
contenido de ejemplo a reemplazar (`CONTENIDO_EJEMPLO.md`), el documento
maestro de arquitectura (fuente principal de
modelos, admin y plan por bloques) y el brief del cliente.

## Correo

En desarrollo los correos se imprimen en consola. Para producción, en `.env`:
`EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` y los datos
`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
`EMAIL_USE_TLS`/`EMAIL_USE_SSL` y `DEFAULT_FROM_EMAIL`.
