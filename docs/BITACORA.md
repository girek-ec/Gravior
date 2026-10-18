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

> Estado de estos pendientes al cerrar el Bloque A: la etiqueta "Servicios",
> el popup, los datos fijos del header/footer y la validación de archivos
> quedaron resueltos. El error JS quedó acotado (ver Bloque A).

---

## Bloque A · Configuración e Inicio (18/10/2026)

### Modelos y ubicación

| Modelo | App (grupo admin) | Motivo |
| --- | --- | --- |
| SiteConfiguration (singleton) | `core` (Configuración) | Datos globales de header, footer, contacto, WhatsApp y SEO |
| CorporateEmail | `core` (Configuración) | Correos reutilizados en footer y contacto |
| SocialNetwork | `core` (Configuración) | Redes del sitio completo |
| CallToAction | `core` (Configuración) | CTAs reutilizables en cualquier página, por identificador |
| HeroSlide | `inicio` (Inicio) | Slider principal del Home |
| Differential | `inicio` (Inicio) | Diferenciales del Home y Nosotros |
| Statistic | `inicio` (Inicio) | Indicadores del Home y Nosotros |
| ProcessStep | `inicio` (Inicio) | Proceso de trabajo del Home |

Campos exactamente los del documento (secciones 6 y 7). Añadidos por la
convención de la sección 5: `created_at` / `updated_at` en todos
(`core.models.TimeStampedModel`).

### Decisiones
- **Statistic.value es entero** (`PositiveIntegerField`): el contador de
  Crafto (`vertical-counter`) anima dígito a dígito y no admite decimales.
  Prefijo y sufijo se muestran junto al contador.
- **Singleton**: `SiteConfiguration.clean()` impide una segunda instancia;
  en el admin no se puede crear otra ni borrar la existente y el listado
  redirige al formulario.
- **Admin ordenado** como la sección 4 con `core.admin_site.GraviorAdminSite`
  (reemplaza a `django.contrib.admin` en `INSTALLED_APPS`).
- **Validación de archivos** (`core/validators.py`): JPG/PNG/WEBP (favicon
  PNG/ICO) y peso máximo por campo (logos 1 MB, slides 5 MB, etc.). Las
  ayudas del admin indican medidas recomendadas.
- **Enlaces administrables** validados: `/ruta/`, `#ancla`, `https://`,
  `mailto:`, `tel:`.
- **Context processor** `core.context_processors.site`: `site_config`,
  `corporate_emails`, `social_networks`, `whatsapp_url` (solo si
  `whatsapp_enabled`), `ctas` (CTA activos por `code`), `logo_url`,
  `logo_white_url` y `favicon_url` (con respaldo a las imágenes de la
  maqueta si no hay configuración). No se ejecuta en `/admin/`.
- **CTA por identificador**: `header_contact` (botón del header),
  `home_process` (sección de proceso), `about_contact` (Nosotros). Si se
  desactiva o borra, el bloque correspondiente no se muestra.
- **Slider**: un loop sobre el slide 1 de la maqueta. Las diferencias de
  atributos de los slides 2 y 3 (`data-responsive`, `border-radius`, `fb`)
  se conservan con `forloop.first`. `highlight_text` = etiqueta oscura,
  `eyebrow` = texto junto a ella, fondo grande = `company_name`. El botón 2
  abre `video_url` en popup si existe; si no, enlaza a
  `secondary_button_url`. `thumbnail` es el fondo de "Siguiente" (respaldo:
  imagen de escritorio).
- **Imagen móvil**: la demo reemplazaba el fondo de cada slide en ≤ 778 px
  por un placeholder (`gym-and-fitness.css`). El Home sobrescribe esa regla
  con `mobile_image` o, si falta, `desktop_image`.
- **Diferenciales**: Home (lista con flecha) y Nosotros (acordeón) según
  `show_home` / `show_about`. Muestra `image` si existe, si no `icon_class`.
  La flecha enlaza a Nosotros (el modelo no tiene campo de enlace).
- **Estados vacíos**: slider (y su JS), diferenciales, indicadores y proceso
  se omiten sin datos; el botón de WhatsApp solo aparece con número y
  activado; header/footer no fallan sin configuración.
- **WhatsApp**: botón flotante abajo a la izquierda (a la derecha y más
  pequeño en móvil para no tapar el slider; a la derecha en escritorio
  chocaría con la barra "Subir" del tema).
- Se eliminó el popup promocional de la demo y "Servicios" pasó a
  "Calidad y bioseguridad" en header y footer.

### Datos por defecto
```bash
python manage.py seed_bloque_a
```
Idempotente: cada modelo se carga solo si su tabla está vacía (los CTA, por
identificador) y nunca modifica registros existentes. Copia imágenes de
`static/crafto/images/` a `media/` como relleno.

Carga: configuración general (textos del brief/maqueta; teléfono y WhatsApp
`+593 00 000 0000`, correo `info@example.com`, dirección y horario "por
definir", país Ecuador, logos y favicon de la demo), 4 correos
`@example.com`, 3 redes de ejemplo, 3 CTA, 3 slides, 6 diferenciales
(mensajes de la sección 2.2), 3 etapas. **No carga indicadores.**

### Verificación
`check` sin issues · `makemigrations --check` sin cambios · `migrate` al
día · 16 tests OK (context processor, singleton, seed idempotente, admin,
secciones del Home) · 11 URLs públicas 200 con datos y con las tablas del
bloque vacías · Home y Nosotros revisados en navegador a 1366 px y 375 px
(menú lateral, slider, diferenciales, indicadores con datos temporales,
proceso, footer, WhatsApp, estado vacío).

### Error JS de la consola
`main.js:2720` (`slideChange` → `current_slide.querySelectorAll`). Viene del
carrusel de testimonios del Home (`.slider-one-slide`, sección "Experiencias
y confianza"), **no** del slider principal ni del header. Es intermitente
(aparece en algunas primeras cargas, cuando Swiper se inicializa con 0
slides) y no se reprodujo al recargar. No se tocó `main.js`. Posible
arreglo en frontend: comprobar `current_slide` antes de usarlo en ese
handler. En Calidad y Aliados no hay error (lo que se veía antes era el log
arrastrado del Home).

### Pendientes
- Contenido real del cliente para reemplazar los ejemplos (logo, teléfono,
  WhatsApp, correos, dirección, horario, redes, Google Maps). **Antes de
  publicar** desactivar o corregir el WhatsApp de ejemplo.
- Textos que siguen fijos en header, footer y Home: lista entregada para
  decisión (no se cambian sin aprobación).
- El documento prevé un "CTA final" en el Home, pero la maqueta no tiene ese
  bloque.
- "Calidad y bioseguridad" ocupa dos líneas muy juntas en el menú lateral de
  escritorio (revisar en diseño).
- Statistic.description no tiene lugar visible en el diseño de contadores
  (se usa como `title` del elemento). ProcessStep.icon_class tampoco se
  muestra (el diseño usa el número).
- Error JS intermitente del carrusel de testimonios (frontend).

---

## Reorganización · apps dentro de `apps/` (18/10/2026)

Para despejar la raíz del proyecto, las 11 apps se movieron con `git mv` a
`apps/<app>/` (se conserva el historial). Templates, static y media no se
movieron.

```
Gravior/
├── apps/            core, inicio, empresa, genetica, calidad, productos,
│                    infraestructura, equipo, aliados, actualidad, contacto
├── gravior/         settings.py, urls.py, wsgi.py, asgi.py
├── templates/  static/  docs/  media/ (no versionado)
└── manage.py  requirements.txt  README.md
```

- Cada `apps.py` usa `name = 'apps.<app>'` y **`label = '<app>'`**. El label
  es el que Django usa para nombrar tablas (`core_siteconfiguration`), en
  `django_migrations`, en los content types, los permisos y las rutas del
  admin (`admin:core_siteconfiguration_change`). Conservarlo evita recrear
  migraciones, renombrar tablas o perder datos y permisos.
- Se actualizaron `INSTALLED_APPS`, el admin personalizado
  (`apps.core.admin_site.GraviorAdminConfig`), el context processor, los
  `include()` de `gravior/urls.py`, los imports entre apps, el comando
  `seed_bloque_a`, los tests y los imports de `core.validators` dentro de
  las migraciones (solo el import; el esquema no cambia).
- Verificación: `check` sin issues, `makemigrations --check` sin cambios,
  `migrate` sin pendientes, 16 tests OK, 11 URLs públicas + admin en 200,
  mismos registros del Bloque A y superusuario intacto. Respaldo previo de
  `db.sqlite3` fuera del repo.
