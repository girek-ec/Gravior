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
python manage.py createsuperuser
python manage.py runserver
```

- Sitio: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

En Linux/macOS la activación es `source venv/bin/activate` y la copia
`cp .env.example .env`.

## Tests

```powershell
python manage.py test
```

## Estructura

| App | Contenido |
| --- | --- |
| `core` | Configuración general, correos, redes, CTAs y bloques de Inicio |
| `empresa` | Quiénes somos y valores corporativos |
| `genetica` | Líneas genéticas, características y documentos |
| `calidad` | Calidad y bioseguridad |
| `productos` | Catálogo informativo (sin tienda) |
| `infraestructura` | Instalaciones y galería |
| `equipo` | Equipo técnico y aliados |
| `actualidad` | Noticias y artículos |
| `contacto` | Motivos de consulta y mensajes recibidos |

- `templates/`: `base.html` y un template por sección.
- `static/`: assets de Crafto (css, js, images, fonts).
- `media/`: archivos subidos desde el admin (no se versiona).

## Correo

En desarrollo los correos se imprimen en consola. Para producción, en `.env`:
`EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` y los datos
`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
`EMAIL_USE_TLS`/`EMAIL_USE_SSL` y `DEFAULT_FROM_EMAIL`.
