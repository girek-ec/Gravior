# Contenido de ejemplo a reemplazar antes de publicar

Todo lo listado aquí lo cargan los comandos `seed_bloque_a` y `seed_bloque_b`
para que ninguna sección quede en blanco. **No es información oficial**: debe
reemplazarse desde el Django Admin con contenido aprobado por GRAVIOR (sección
19 del documento de arquitectura).

Leyenda: **[Cliente]** dato que solo puede entregar GRAVIOR (hoy con valores de
ejemplo evidentes) · **[Validar]** texto redactado desde el brief o la maqueta
que GRAVIOR debe aprobar o reescribir · **[Imagen]** imagen de relleno de la
maqueta.

Para cargar los ejemplos:

```bash
python manage.py seed_bloque_a
python manage.py seed_bloque_b
# Completar solo campos vacíos de registros existentes (nunca sobrescribe):
python manage.py seed_bloque_a --fill-blanks
python manage.py seed_bloque_b --fill-blanks
```

---

## Bloque A · Configuración e Inicio

### Configuración general (SiteConfiguration)
| Campo | Valor de ejemplo | Tipo |
| --- | --- | --- |
| Logo principal / logo para fondos oscuros | Logos "WORKOUT" de la demo Crafto | [Imagen] [Cliente] |
| Favicon | Favicon de Crafto | [Imagen] [Cliente] |
| Isotipo | (vacío) | [Cliente] |
| Razón social | Razón social por confirmar | [Cliente] |
| Descripción corporativa breve | Texto del brief | [Validar] |
| Teléfono / número de WhatsApp | +593 00 000 0000 | [Cliente] |
| Mensaje inicial de WhatsApp | Hola, quisiera recibir información sobre GRAVIOR. | [Validar] |
| Botón de WhatsApp | **Activado con número de ejemplo**: corregir o desactivar antes de publicar | [Cliente] |
| Correo general | info@example.com | [Cliente] |
| Dirección / ciudad / provincia | Dirección por definir / Ciudad por definir / Provincia por definir | [Cliente] |
| País | Ecuador | [Validar] |
| Horario de atención | Lunes a viernes: horario por definir | [Cliente] |
| Enlace a Google Maps | https://maps.example.com/gravior | [Cliente] |
| Copyright | Copyright 2026 | [Validar] |
| Título y descripción SEO generales | Textos de la maqueta | [Validar] |

### Correos corporativos (CorporateEmail)
info@, comercial@, ventas@ y administracion@ **example.com** — [Cliente].

### Redes sociales (SocialNetwork)
Facebook, Instagram y LinkedIn con URLs `.../example` — [Cliente]. Desactivar
las que no existan.

### Llamados a la acción (CallToAction)
`header_contact`, `home_process`, `about_contact`: textos y botones redactados
para el sitio, enlazan a /contacto/ — [Validar].

### Slider principal (HeroSlide)
3 slides con textos de la maqueta, botones a páginas internas y fotos de
`static/crafto/images/gravior/home/` — [Validar] [Imagen]. Sin video.

### Diferenciales (Differential)
Genética, Calidad, Bioseguridad, Tecnología, Eficiencia y Confianza con los
mensajes de la sección 2.2 del documento — [Validar].

### Proceso de trabajo (ProcessStep)
Diagnóstico, Estrategia y Acompañamiento (textos de la maqueta) — [Validar].

### Indicadores (Statistic)
**No se cargan.** Solo cifras oficiales con fuente interna aprobada — [Cliente].

---

## Bloque B · Empresa, Genética, Calidad y bioseguridad

### Quiénes somos (AboutPage)
| Campo | Origen del ejemplo | Tipo |
| --- | --- | --- |
| Título de página, introducción | Maqueta | [Validar] |
| Descripción de la empresa | Brief | [Validar] |
| Propósito | Brief ("aliado estratégico… avicultura en Ecuador") | [Validar] |
| Misión | Redactada de forma genérica | [Cliente] |
| Visión | Redactada desde el posicionamiento del brief | [Cliente] |
| Propuesta de valor | Maqueta | [Validar] |
| Compromiso con clientes | Maqueta | [Validar] |
| Imagen principal / secundaria | Fotos de relleno de la maqueta | [Imagen] |
| Video corporativo | (vacío: se muestra el video de YouTube de la demo) | [Cliente] |
| SEO | Textos de la maqueta | [Validar] |

### Valores corporativos (CorporateValue)
6 pilares de "Lo que hacemos" de la maqueta (Genética avícola, Calidad y
bioseguridad, Asesoría técnica, Manejo y producción, Instalaciones,
Sostenibilidad) con fotos de relleno — [Validar] [Imagen].

### Líneas genéticas (GeneticLine, GeneticFeature, GeneticDocument)
- **Genética Cobb** (marca Cobb, destacada): texto genérico que presenta a
  Cobb como referente genético, **sin logo ni datos técnicos**. 6
  características de la maqueta. Requiere material e información
  **autorizados por Cobb** — [Cliente].
- **Línea genética de ejemplo** (marca "Marca por confirmar"): marcador para
  una segunda línea, 3 características genéricas — [Cliente]. Eliminar o
  reemplazar.
- Imágenes de relleno recortadas a 578 × 691 y 600 × 672 — [Imagen].
- Cada línea tiene un PDF **"Documento de ejemplo – reemplazar"** generado
  por el sistema — reemplazar por fichas, manuales o guías aprobadas para
  distribución — [Cliente].

### Calidad y bioseguridad (QualityPage, QualityArea, QualityStep)
- Página: título, introducción, descripción, compromiso de calidad, enfoque
  de bioseguridad, CTA y SEO redactados desde el brief y la maqueta —
  [Validar].
- 7 áreas (Bioseguridad, Manejo, Ambiente, Alimentación, Bienestar,
  Productividad, Soporte) con 4 etapas cada una, textos de la maqueta —
  [Validar]. Confirmar qué procesos pueden comunicarse públicamente
  (sección 25: no publicar protocolos internos).
- Imágenes de las áreas: relleno de la maqueta — [Imagen].

---

## Otros elementos de relleno fuera del admin
- Dos videos de YouTube de la demo Crafto (Home "Cómo trabajamos" y
  "Acompañamiento en campo"; Nosotros mientras no haya video corporativo).
- Franja de Instagram del footer con imágenes placeholder.
- Imágenes decorativas `placehold.co` de la maqueta en Nosotros, Genética y
  Calidad.
- Equipo, aliados, testimonios y noticias del Home: Bloques C–E y futuros.
