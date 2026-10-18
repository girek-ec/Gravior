# Bitácora de desarrollo · Backend GRAVIOR

Registro de lo implementado, decisiones tomadas y pendientes por bloque.
Fuente principal de requisitos: `docs/GRAVIOR_Arquitectura_Contenidos_Modelos_Django.pdf`.

Flujo de trabajo: el backend se desarrolla en la rama `lucho`; `main` se
actualiza por merge cuando un bloque está aprobado.

---

## Paso 0 · Base del proyecto (18/10/2026)

### Estado encontrado
- Proyecto `gravior` recién creado (Django 5.2.18 en el venv, Python 3.10;
  el encabezado de `settings.py` decía Django 6.1.2, que exige Python ≥ 3.12).
- `.idea/` versionada, `requirements.txt` en UTF-16 con pip freeze completo.
- `SECRET_KEY` hardcodeado y bloque `MAILERS` inválido en `settings.py`.

### Implementado
- **Higiene:** `.gitignore` (venv, `__pycache__`, `db.sqlite3`, IDE, `media/`,
  `staticfiles/`, `.env`, `*.log`), `.idea` fuera del índice, `requirements.txt`
  con dependencias directas (Django 5.2 LTS, Pillow, python-dotenv).
- **Configuración:** variables desde `.env` (`.env.example` documentado);
  `LANGUAGE_CODE='es'`, `TIME_ZONE='America/Guayaquil'`, sin `i18n_patterns`;
  `STATICFILES_DIRS`, `STATIC_ROOT`, `MEDIA_URL`, `MEDIA_ROOT`; correo con
  backend de consola en desarrollo y variables SMTP listas.
- **Apps por dominio** (con `verbose_name` en español = grupo del admin):

  | App | Grupo admin | Modelos (bloque) |
  | --- | --- | --- |
  | `core` | Configuración | SiteConfiguration, CorporateEmail, SocialNetwork, CallToAction (A) |
  | `inicio` | Inicio | HeroSlide, Differential, Statistic, ProcessStep (A) |
  | `empresa` | Empresa | AboutPage, CorporateValue (B) |
  | `genetica` | Genética | GeneticLine, GeneticFeature, GeneticDocument (B) |
  | `calidad` | Calidad y bioseguridad | QualityPage, QualityArea, QualityStep (B) |
  | `productos` | Productos | ProductCategory, Product, ProductFeature, ProductDocument (C) |
  | `infraestructura` | Infraestructura | FacilityCategory, Facility, FacilityGallery (C) |
  | `equipo` | Equipo | TeamMember (D) |
  | `aliados` | Aliados | Partner (D) |
  | `actualidad` | Actualidad | PostCategory, Post (E) |
  | `contacto` | Contacto | ContactReason, ContactMessage (E) |

- **URLs** (sin prefijo de idioma; cada app declara sus rutas completas):

  | URL | Nombre | Template |
  | --- | --- | --- |
  | `/` | `inicio:index` | `gravior/index.html` |
  | `/nosotros/` | `empresa:index` | `gravior/nosotros.html` |
  | `/genetica/` · `/genetica/<slug>/` | `genetica:index` · `genetica:detail` | `gravior/genetica.html` · 404 hasta bloque B |
  | `/calidad-bioseguridad/` | `calidad:index` | `gravior/servicios.html` |
  | `/productos/` · `/productos/<slug>/` | `productos:index` · `productos:detail` | `gravior/productos.html` · 404 hasta bloque C |
  | `/instalaciones/` · `/instalaciones/<slug>/` | `infraestructura:index` · `infraestructura:detail` | `gravior/instalaciones.html` · 404 hasta bloque C |
  | `/equipo/` | `equipo:index` | `gravior/equipo.html` |
  | `/aliados/` | `aliados:index` | `gravior/aliados.html` |
  | `/actualidad/` · `/actualidad/<slug>/` | `actualidad:index` · `actualidad:detail` | `gravior/actualidad.html` · `gravior/actualidad-detalle.html` (maqueta) |
  | `/contacto/` | `contacto:index` | `gravior/contacto.html` |
  | `/admin/` | — | Django Admin |

- **Tests de humo** en `core/tests.py`: páginas 200, detalles pendientes 404,
  maqueta del detalle de actualidad 200 y login del admin.
- **docs/** con el documento de arquitectura, el brief y esta bitácora.

### Integración de la maqueta (merge de la Fase 04)
La Fase 04 (`0f92d9f`) ya traía las 11 páginas maquetadas y enlazadas
(`templates/gravior/`, `templates/includes/`, assets en `static/crafto/`) con
vistas en una sola app `core`. En el merge:
- Se mantuvo la configuración del paso 0 (sin `SECRET_KEY` hardcodeado ni
  `MAILERS`) y `db.sqlite3` dejó de versionarse.
- Cada página pasó a ser servida por la vista de su app.
- Los `{% url %}` de la maqueta usan los namespaces (`inicio:index`, etc.) y
  el menú activo se resuelve con `request.resolver_match.app_name`.
  No se modificó ningún otro contenido HTML de la maqueta.
- Se eliminaron los alias `demo-*.html` y la ruta que servía `css/`, `js/`,
  `images/` en la raíz (la maqueta usa `{% static 'crafto/...' %}`).
- `base.html` de la maqueta suma los bloques `extra_head`, `nav` y `footer`.

### Decisiones
- **Django 5.2 LTS** (compatible con el Python 3.10 del entorno).
- **Apps `inicio` y `aliados` separadas** de `core` y `equipo` para que el
  admin muestre los grupos de la sección 4 del documento.
- **Templates de la maqueta en `templates/gravior/`** (no se movieron a
  carpetas por app para no romper el trabajo de maquetación).
- **Detalles por slug reservados** con `core.views.PendingDetailView` (404)
  hasta que exista el modelo del bloque correspondiente.
- **`SECRET_KEY` antiguo** queda en el historial de git (decisión del
  responsable); ya no se usa.

### Verificación
`manage.py check` sin issues · `makemigrations` sin cambios · `migrate` al día ·
4 tests OK · 11 páginas 200 · 69 referencias `{% static %}` existen en disco ·
revisión visual en navegador.

### Pendientes observados (no corresponden al paso 0)
- Error JS de la maqueta en todas las páginas: `main.js` → `slideChange`
  (`Cannot read properties of undefined (reading 'querySelectorAll')`).
  Revisar en frontend.
- La etiqueta de menú sigue diciendo "Servicios"; el documento recomienda
  "Calidad y bioseguridad".
- Popup de la demo Crafto al abrir el inicio.
- Formulario de `contacto.html` sin `{% csrf_token %}` y formulario de
  `actualidad-detalle.html` apuntando a un `.php` de la demo (bloque E).
- Textos de negocio fijos en la maqueta (teléfono, correo, dirección "por
  definir", logos de la demo): se reemplazan desde el admin en el bloque A.
- Validación de extensiones/tamaño de archivos: se implementa en el bloque A
  con los primeros `ImageField`.
