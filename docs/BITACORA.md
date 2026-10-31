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

---

## Ajustes del Bloque A (18/10/2026)

### Decisiones del cliente interno
- Los 2 videos de YouTube de la demo (Home: "Cómo trabajamos" y
  "Acompañamiento en campo") **se quedan** hasta tener videos propios.
  Pendiente: reemplazarlos.
- La franja de Instagram del footer se queda como está.
- Las franjas de frases en movimiento, los títulos de sección y las etiquetas
  de menú/footer quedan fijos como diseño.
- No se agrega campo de enlace a Differential ni CTA final al Home (lo pedirá
  diseño).

### Regla de textos de ejemplo
Todo texto editable debe venir con un ejemplo cargado (nada en blanco). En el
Bloque A se completaron razón social, ciudad, provincia, enlace de mapa de
ejemplo, textos de apoyo de los CTA e iconos de las etapas. Statistic sigue
sin cifras.

### `--fill-blanks`
Los comandos `seed_bloque_*` comparten `apps/core/seeding.py`:
- Sin opción: un modelo se carga solo si su tabla está vacía; nunca modifica
  registros existentes.
- `--fill-blanks`: además completa los campos **vacíos** (también imágenes)
  de los registros que coinciden por clave (email, name, code, title,
  number), sin sobrescribir contenido. Si el cliente cambió la clave, el
  registro no se toca.
- En la base local completó: configuración general (legal_name, city,
  province, google_maps_url), texto de los 3 CTA e icon_class de las 3
  etapas.

---

## Bloque B · Empresa, Genética, Calidad y bioseguridad (18/10/2026)

### Modelos y ubicación
| Modelo | App (grupo admin) |
| --- | --- |
| AboutPage (singleton), CorporateValue | `apps/empresa` (Empresa) |
| GeneticLine, GeneticFeature, GeneticDocument | `apps/genetica` (Genética) |
| QualityPage (singleton), QualityArea, QualityStep | `apps/calidad` (Calidad y bioseguridad) |

Campos del documento (secciones 8–10) + `created_at`/`updated_at`.

### Decisiones
- **Utilidades comunes**: `SingletonModel` y `SingletonAdminMixin` (usados
  también por SiteConfiguration), `unique_slug` y validadores de PDF
  (extensión, firma `%PDF-` y 10 MB).
- **Slugs** de GeneticLine y QualityArea: se autogeneran desde el nombre si
  están vacíos (sufijo -2, -3 si se repiten), son editables y no cambian si
  luego se edita el nombre.
- **on_delete (21.3)**: CASCADE en GeneticFeature y QualityStep (no existen
  sin su padre); **PROTECT en GeneticDocument**: una línea con documentos no
  se puede borrar por accidente; hay que retirar antes sus documentos.
- **Medios**: `media/about/`, `media/about/values/`, `media/genetics/`,
  `media/genetics/brands/`, `media/genetics/documents/`, `media/quality/`,
  `media/quality/areas/`.
- **PDF de ejemplo**: generado en código (`sample_pdf`, PDF 1.4 mínimo de una
  página) en lugar de reportlab, para no sumar una dependencia solo para un
  relleno. Validado con pypdf en modo estricto.
- **Imágenes de relleno** recortadas al centro con Pillow a las proporciones
  de la maqueta cuando hace falta (líneas genéticas).
- **SEO por página**: `SeoMixin` pasa `seo_title`/`seo_description`; base.html
  usa los de la configuración general si están vacíos. Genética usa el SEO
  general (no hay modelo de página para el listado).

### Mapeo a la maqueta
- **Nosotros**: cabecera (page_title, intro, main_image); "Nuestra visión"
  (secondary_image, value_proposition, vision, video: corporate_video_url o el
  de la maqueta); franja (purpose); "Lo que hacemos" = CorporateValue
  (imagen, icono, nombre, descripción); "¿Por qué GRAVIOR?" (client_commitment
  + diferenciales).
- **Genética**: una sección por línea activa (main_image, brand_name, name,
  description, documentos activos como descargas, application y brand_logo
  si existe) y su grilla de características activas (título de la grilla =
  summary; fondo = secondary_image).
- **Calidad y bioseguridad**: cabecera y descripción (QualityPage),
  contadores calculados (áreas publicadas y etapas máximas por área),
  pestañas = QualityArea, acordeón = QualityStep (número, título,
  descripción; recuadro con imagen y nombre del área), franja final =
  cta_text/cta_url.
- **Home**: "Sobre GRAVIOR" (intro, company_description, main_image);
  pestañas de soluciones = líneas destacadas + áreas de calidad (máx. 5),
  con una estructura común lista para sumar productos en el Bloque C;
  "Conocimiento aplicado" = primeras 3 áreas (nombre, descripción, icono).

### Datos de ejemplo
`python manage.py seed_bloque_b` (y `--fill-blanks`). Detalle de lo cargado y
de lo que debe reemplazarse en `docs/CONTENIDO_EJEMPLO.md`. En la base local
se recargaron una vez las 2 líneas de ejemplo para aplicar el recorte de
imágenes (eran datos de ejemplo recién creados).

### Verificación
`check` sin issues · `makemigrations --check` sin cambios · `migrate` al día ·
34 tests OK · 11 URLs públicas + admin en 200 con datos y con tablas vacías ·
PDF servido como `application/pdf` · Nosotros, Genética, Calidad y Home
revisados en navegador a 1366 px y 375 px (pestañas de Calidad cambian
correctamente) · sin errores de consola en esta revisión.

### Pendientes
- Campos sin lugar en la maqueta actual (editables y con ejemplo, pero no
  visibles): AboutPage.mission, QualityPage.quality_commitment y
  QualityPage.biosecurity_approach. Requieren un bloque aprobado por diseño.
- La insignia del recuadro "Enfoque" de las pestañas del Home ("Alto
  desempeño", etc.) se omitió: no hay campo en el modelo y era un claim fijo.
- En la franja de propósito de Nosotros se perdió el subrayado de las
  últimas palabras (el texto ahora es un solo campo).
- Videos de YouTube de la demo, franja de Instagram e imágenes
  `placehold.co` decorativas siguen pendientes de material propio.
- Error JS intermitente del carrusel de testimonios: no apareció en esta
  revisión; sigue anotado.

---

## Actualización de seguridad y de versiones (28 oct 2026)

### Versiones
| Componente | Antes | Después | Motivo |
| --- | --- | --- | --- |
| Python (venv) | 3.10.11 | **3.13.15** | Python 3.10 sin soporte desde el 1 oct 2026; Pillow 13 exige ≥ 3.11 y Django 6.x ≥ 3.12 |
| pip | 23.0.1 | **26.2.2** | CVE-2026-6357 (corregido en 26.1) |
| Django | 5.2.18 | **6.1.2** | Parches de seguridad de 6.1.2 (CVE-2026-77050, -84429, -87890, -87975 y la corrección de CVE-2026-15830) y alinear la versión con el resto del equipo. 5.2.18 ya traía los mismos parches, pero el equipo trabaja en 6.1 |
| Pillow | 12.3.0 | **13.0.0** | 38 correcciones de seguridad (2 críticas, entre ellas el desbordamiento del decodificador JPEG); 12.x no recibe esos parches |
| python-dotenv | 1.2.4 | 1.2.4 | Sin cambios |
| asgiref / sqlparse / tzdata (transitivas) | 3.12.1 / 0.6.0 / 2026.5 | 3.13.0 / 0.6.0 / 2026.6 | Las instala Django |
| Brotli / brotlicffi | no instalados | no instalados | CVE-2026-111497 no aplica |
| litellm | no instalado | no instalado | La versión maliciosa 1.107.0 no está presente |

`requirements.txt` pasa de versiones fijas a mínimos: `Django>=6.1.2,<6.2`,
`Pillow>=13.0.0`, `python-dotenv>=1.2.4` (sin congelar transitivas).

### Entorno
- El venv anterior quedó como `venv_py310_old/` (ignorado con `venv_*/`).
- Nuevo venv: `py -3.13 -m venv venv` + `pip install -r requirements.txt`.

### Revisión de Django 6.0 y 6.1 contra el código
Se revisaron los cambios incompatibles, eliminaciones y obsolescencias de
ambas versiones frente a settings, URLs, apps, admin, validadores, context
processor, comandos, tests y templates.
- **Correo (único cambio necesario)**: Django 6.1 declara obsoletos los
  ajustes `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
  `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `EMAIL_USE_SSL` y `EMAIL_TIMEOUT`
  (8 `RemovedInDjango2028Warning`). `settings.py` ahora arma `MAILERS`
  (`default`) desde las mismas variables del `.env`; las opciones SMTP solo
  se pasan al backend SMTP. Probado: envío por consola y construcción del
  backend SMTP con host/puerto/TLS desde variables (sin envío real).
- Sin impacto: `DEFAULT_AUTO_FIELD` ya era `BigAutoField`; no se usan
  `list_select_related=True`, `select_related()` sin argumentos,
  `values_list(flat=True)` sin campo, `get_connection`/`fail_silently`,
  `format_html` sin argumentos, `save()` con posicionales, búsquedas
  `{{ a..b }}` ni la clase CSS `wide` del admin; los `.first()` no dependen
  de `order_by()` vacío; SQLite 3.50.4 (mínimo 3.37).
- Migraciones: `makemigrations --check` sin cambios y `migrate --plan` sin
  operaciones (ni del proyecto ni de las apps de Django). Se respaldó
  `db.sqlite3` fuera del repo antes de verificar; no hubo que migrar.

### Verificación
- `python -Wa manage.py check`: sin issues ni advertencias.
- `python -Wa manage.py test`: 35 tests OK, sin DeprecationWarning (incluye
  un test nuevo de subida y vista previa de imagen en el admin con Pillow 13
  y rechazo de un archivo falso).
- Servidor con el venv nuevo: 11 páginas públicas + `/admin/login/` en 200
  con datos y con las tablas de los bloques vacías (sobre una copia de la
  base, luego restaurada); media y static servidos.
- `seed_bloque_a` y `seed_bloque_b` (con `--fill-blanks`) funcionan; también
  en los tests sobre base y media temporales.
- Datos intactos: superusuario `admin` y todos los registros de los seeds.
- Navegador: Home y login del admin correctos. Sigue apareciendo de forma
  intermitente el error JS del carrusel de testimonios (`main.js:2720`), sin
  relación con esta actualización.

### Pendiente para cada desarrollador
Recrear su venv con Python ≥ 3.12 (recomendado 3.13) e instalar
`requirements.txt`; en PyCharm, seleccionar `venv\Scripts\python.exe` como
intérprete.

---

## Bloque C · Productos e Infraestructura (29 oct 2026)

### Sincronización previa
`lucho` ya está integrada en `main` en GitHub (PR #1, `d016d4e`); ese merge
no agrega contenido. No había cambios nuevos del equipo. `lucho` lleva 4
commits locales sin subir (actualización a Python 3.13 / Django 6.1).

### Modelos y ubicación
| Modelo | App (grupo admin) |
| --- | --- |
| ProductCategory, Product, ProductFeature, ProductDocument | `apps/productos` (Productos) |
| FacilityCategory, Facility, FacilityGallery | `apps/infraestructura` (Infraestructura) |

Campos de las secciones 11 y 12 + `created_at`/`updated_at`. Catálogo
informativo: sin precio, carrito, stock ni pago.

### Decisiones
- **on_delete (21.3)**: PROTECT de Product → ProductCategory y Facility →
  FacilityCategory (no se borra una categoría con elementos, ejemplo literal
  del documento) y de ProductDocument → Product (documentación publicada);
  CASCADE en ProductFeature y FacilityGallery (dependen del padre).
- **Slugs**: `SlugFromNameMixin` (core.models) para categorías, productos e
  instalaciones; autogenerados si están vacíos, editables y estables.
  Listos para futuras páginas de detalle (hoy hay anclas `#<slug>`).
- **Medios**: `media/products/`, `media/products/documents/`,
  `media/facilities/`, `media/facilities/gallery/`.
- **Botón de consulta**: template tag `inquiry_url` → WhatsApp con el mensaje
  configurado + nombre del producto (`SiteConfiguration.whatsapp_link`) si
  WhatsApp está activo; si no, `/contacto/`. Se oculta si el producto no tiene
  `inquiry_button_text`.
- **Filtro de productos**: en el servidor (`/productos/?categoria=<slug>`),
  con botones de Crafto. No se usó `.portfolio-filter` porque el JS del tema
  cancela la navegación de esos enlaces. Una categoría inexistente muestra
  todo.
- **Instalaciones**: filtro isotope de Crafto por categoría (`.cat-<slug>`) y
  lightbox de Crafto: la foto principal y la galería activa comparten
  `data-group`. Para que el tema los agrupe, el enlace pasó a estar dentro de
  `.portfolio-box` (el CSS solo usa selectores descendientes, el diseño no
  cambia). El título del lightbox incluye la ubicación pública si existe.
- **Home**: pestañas de soluciones = líneas destacadas + productos destacados
  (enfoque = categoría, enlace al catálogo filtrado) + áreas de calidad,
  máximo 5.
- **Nombres de producto cortos**: la tarjeta muestra el nombre en tamaño
  grande y la maqueta asume una o dos palabras; se acortó el ejemplo y el
  admin lo indica.

### Mapeo a la maqueta
- **Productos**: cabecera (fondo = imagen del primer producto); "Una propuesta
  integral" = descripciones de categorías en dos columnas; tarjeta = badge de
  categoría, `<sub>` referencia (o número), nombre, resumen, características
  activas (descripción como tooltip), botón de consulta, documentos activos y
  franja derecha con la imagen principal; "Destacado" = `is_featured`.
- **Instalaciones**: filtro + grilla con imagen principal y título.

### Datos de ejemplo
`python manage.py seed_bloque_c` (y `--fill-blanks`). Detalle en
`docs/CONTENIDO_EJEMPLO.md`.

### Verificación
`check -Wa` sin issues ni advertencias · `makemigrations --check` sin cambios ·
50 tests OK · 11 URLs públicas + admin en 200 con datos y con tablas vacías ·
navegador a 1366 px y 375 px: productos (filtro, WhatsApp por producto,
documentos), instalaciones (3 columnas, filtro: Galpones muestra 3 de 12,
lightbox con 3 fotos y ubicación) y pestaña de producto en el Home. El error
JS del carrusel de testimonios no apareció en estas cargas.

### Pendientes
- Campos sin lugar en la maqueta actual: Product.description, application,
  benefits y brand; Facility.description y video_url (no hay página de
  detalle). Quedan cargados y editables.
- En móvil, la franja decorativa derecha de las tarjetas de producto se
  superpone ~35 px al texto (rasgo de la maqueta; revisar en frontend).
- Subtítulo de Instalaciones con texto de la demo: "Instalaciones - Three
  column layout".
- El contador del lightbox ("1 of 3") viene en inglés desde el plugin del
  tema.

---

## Pendientes para diseño (actualizado 31 oct 2026)

Lista consolidada de lo acordado para resolver en diseño/frontend. Ninguno
bloquea el backend; el contenido ya es editable desde el admin.

| # | Tema | Detalle | Origen |
| --- | --- | --- | --- |
| 1 | CTA final del Home | El documento prevé un llamado a la acción final en el inicio, pero la maqueta no tiene ese bloque. Lo pedirá diseño. | Bloque A |
| 2 | Campos editables sin lugar en la maqueta | `AboutPage.mission`, `QualityPage.quality_commitment`, `QualityPage.biosecurity_approach`; `Product.description`, `application`, `benefits`, `brand`; `Facility.description`, `video_url`. Están cargados y editables; en el admin, los de Product y Facility dicen "Aún no se muestra en la web". No habrá página de detalle por ahora. | Bloques B y C |
| 3 | Franja decorativa de las tarjetas de producto en móvil | La franja de imagen de la derecha (`w-65px`, posición absoluta) se superpone ~35 px al texto a 375 px. | Bloque C |
| 4 | Menú lateral largo | "Calidad y bioseguridad" ocupa dos líneas muy juntas en el menú lateral de escritorio. | Bloque A |
| 5 | Subrayado perdido en Nosotros | La franja de propósito mostraba las últimas palabras subrayadas; ahora el texto es un solo campo (`AboutPage.purpose`). | Bloque B |
| 6 | Nombres de producto largos | El nombre se muestra en tamaño grande en la tarjeta; nombres de más de dos palabras o palabras largas se parten o tocan la franja. El admin recomienda nombres cortos. | Bloque C |
| 7 | Sección de aliados en el Home | El documento prevé aliados destacados en el inicio (`Partner.is_featured`), pero la maqueta del Home no tiene ese bloque. El campo ya existe. | Bloque D |
| 8 | Carrusel de Aliados en móvil | En móvil el carrusel aparece desplazado: la maqueta incluye diapositivas espaciadoras `d-none d-lg-block` que Swiper sigue contando. | Bloque D |
| 9 | Estrellas en tarjetas de equipo y aliados | La maqueta muestra 5 estrellas junto a integrantes y aliados; pueden leerse como calificaciones o testimonios. Se mantienen como diseño (siempre 5, sin variar por registro). | Bloque D |

Resueltos en esta revisión (ya no están pendientes):
- Subtítulo de demo "Instalaciones - Three column layout" → texto fijo en
  español.
- Contador del lightbox en inglés → traducido por configuración de Magnific
  Popup en `base.html` ("1 de 3"), sin editar archivos del tema.


---

## Bloque D · Equipo y Aliados (31 oct 2026)

### Ajustes previos del Bloque C
- `help_text` "Aún no se muestra en la web" en Product (descripción,
  aplicación, beneficios, marca) y Facility (descripción, video).
- Lightbox en español por configuración de Magnific Popup en `base.html`.
- Subtítulo de Instalaciones en español.
- Sección "Pendientes para diseño" consolidada.

### Modelos y ubicación
| Modelo | App (grupo admin) |
| --- | --- |
| TeamMember | `apps/equipo` (Equipo) |
| Partner | `apps/aliados` (Aliados) |

Campos de la sección 13 + `created_at`/`updated_at`. Cada modelo en su app
para que el admin muestre los grupos "Equipo" y "Aliados" de la sección 4.

### Decisiones
- **Datos personales**: correo, teléfono y LinkedIn son opcionales, con
  aviso en el admin; el template los muestra solo si tienen contenido
  (`includes/member_social.html`). El seed nunca los completa, tampoco con
  `--fill-blanks`.
- **Nombres genéricos**: "Nombre del integrante N", "Cargo del integrante",
  "Aliado de ejemplo N". Sin personas, marcas ni logos reales.
- **Cobb** no se carga como aliado (el logo es obligatorio y no hay material
  autorizado).
- **Logos de relleno**: `placeholder_logo()` genera PNG con el diseño de los
  SVG de la maqueta, porque `ImageField` (Pillow) no acepta SVG.
- **Equipo**: el primer integrante (por orden) ocupa la tarjeta destacada; el
  resto, la grilla; la tarjeta "+" usa el CTA `team_contact`.
- **Aliados**: grilla de logos (enlace solo si hay sitio web) y carrusel con
  los aliados que tienen reseña; la cabecera usa la imagen de un aliado si
  existe.
- **Home**: pestañas del equipo con los integrantes destacados; la maqueta no
  tiene sección de aliados (queda en "Pendientes para diseño").
- Medios: `media/team/`, `media/partners/`, `media/partners/images/`.

### Datos de ejemplo
`python manage.py seed_bloque_d` (y `--fill-blanks`). Detalle en
`docs/CONTENIDO_EJEMPLO.md`.

### Verificación
`check -Wa` sin issues · `makemigrations --check` sin cambios · 61 tests OK ·
11 URLs públicas + admin en 200 · navegador a 1366 px y 375 px: equipo
(tarjeta destacada, grilla, tarjeta de contacto), aliados (logos, carrusel
autoplay) y equipo destacado del Home; sin errores de consola. El error JS
del carrusel de testimonios no apareció en estas cargas.
