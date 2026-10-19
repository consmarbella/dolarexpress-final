# CHANGELOG_SEO — dolarexpress.cl (2026-09-24)

Repo: consmarbella/dolarexpress-final. Deploy: Vercel (build = `node generate-sitemap.js && node copy-html-files.js`, output `dist/`).
Canónica elegida: **https://www.dolarexpress.cl/**

## Fase 1 — Diagnóstico en vivo
- Build local OK: sitemap 25 URLs, 31 archivos → dist. El HTML live de `/vender-cupo-dolar` y `/` coincide con `dist/` (mismo title/h1/meta). **No hay overwrite de SPA**: el deploy sirve el HTML estático tal cual. La app React+Vite (`App.tsx`, `src/`, `pages/`) es código muerto en producción.
- **Sin Turnstile/Cloudflare**: 0 matches en `public/`, header live `Server: Vercel`, sin headers `cf-*`, HTML directo 200. La brecha móvil (12.85) vs escritorio (41.47) NO es bot-challenge.
- Lenguaje: titles/H1 producto-enfocados, 1 sola frase genérica ("cambio de divisas" en `cuanto-pagan-por-cupo-dolar.html:115`). Rankings a "casa de cambio" vienen de las columnas comparativas ("Casa de Cambio Online/Presencial") + URLs legacy.
- **Bug crítico hallado**: title corrupto en vivo en `que-es-cupo-en-dolares` ("Qu2009 es el Cupo en D243lares..."). Verificado en `public/`, `dist/` y live.

## Fase 2 — Canonicalización (https://www)
- Canonical tags: las 25 páginas ya apuntaban a `https://www` (verificado por grep). Sin cambios.
- Hallazgo: `https://dolarexpress.cl/` devolvía **200** (la regla `/:path*` no matchea root) → homepage duplicada (explica GSC pos 59.82 vs 5.66 vs 71). Fix: redirect 301 explícito `/` + host `dolarexpress.cl` → `https://www.dolarexpress.cl/` (primera regla en `vercel.json`).
- `http://` → 308 automático de Vercel (verificado live en ambas variantes).
- Verificación post-deploy: `curl.exe` a las 4 variantes (http/https × www/no-www) — pendiente resultado abajo.
- MANUAL: en dashboard Vercel → Settings → Domains → set `www.dolarexpress.cl` como Primary; en GSC → declarar propiedad de dominio preferida y pedir reindexación del home canónico.

## Fase 3 — Consolidación vercel.json (68 → 142 redirects, 0 rewrites)
- `public/` no tiene páginas de ciudad: las familias `cupo-en-dolares-en-*` y `avance-cupo-en-dolares-en-*` son legacy 404. Cruzadas 220 URLs indexadas conocidas vs redirects: 46 huérfanas (menos canónicas vivas).
- Primera tanda: `/cupo-en-dolares-:path*` → `/que-es-cupo-en-dolares`; wildcards por marca (`banco-chile/itau/ripley/lider/easy/jumbo/hites/paris/la-polar/abc-din/bbva`) → su pilar; 20 exactas temáticas (ej `/estoy-en-dicom-y-tengo-cupo-cmr` → `/vender-cupo-dolar-sin-dicom`, `/tengo-cupo-en-ripley-y-necesito-efectivo` → `/vender-cupo-ripley-rapido`, `/urgente-cupo-paris-hoy` → `/como-vender-cupo-dolar-rapido`, `/guia/evitar-estafas-cupo-dolar` → `/guia/vender-cupo-dolares`).
- Verificación post-deploy: spot-checks de redirects + `/avance-cupo-dolares` → 200 (loop eliminado).
- Creadas `/privacidad` y `/terminos` (institucionales que pedía el brief); sitemap final: 27 URLs.
- **Bug crítico hallado y fixeado**: `/avance-:path*` matcheaba `/avance-cupo-dolares` → **loop 301 a sí misma en vivo** (verificado con curl: `301 -> misma URL`). Reemplazada por 7 reglas específicas (`avance-cupo-en-dolares-*`, `avance-efectivo[-*]`, `avance-la-polar/lider/ripley/tarjeta-*`). Re-chequeo programático: 0 hijacks sobre las 25 canónicas.
- Segunda tanda desde backups archivados: wildcards `/urgente/`, `/ciudades/`, `/cambio-`, `/cambiar-`; exactas de alto valor (`/compro-cupo-dolar`, `/comprar-cupo-dolar`, `/que-es-cupo-dolar`, `/cupo-en-dolares`, `/es-legal-vender-cupo-dolar`, `/mejor-tasa-cupo-dolar` → landing comisión, `/vender-cupo-dolar-online/-transferencia`, `/vender-cupo-internacional`, `/girar-*`, `/convertir-cupo-dolar-pesos`, `/necesito-plata-tengo-cupo-*`, `/superavance-*`, 8 subpáginas `/guia/*` legacy → `/guia/vender-cupo-dolares`).

## Fase 4 — Keywords en contenido
- Fix title corrupto `que-es-cupo-en-dolares.html:1` → "Qué es el Cupo en Dólares y Cómo Funciona | Guía Chile 2026" (cubre "cupo en dolares chile" 77 imp/trim).
- `cuanto-pagan-por-cupo-dolar.html:115`: "operaciones de cambio de divisas" → "operaciones con cupo en dólares de tarjeta de crédito".
- 2 FAQs nuevas en `vender-cupo-dolar.html` (visible + JSON-LD sincronizados): "¿Buscás alguien que compre cupo en dólares en Chile?" (cubre "compro cupo dolar" 68 imp) y "¿El cambio de cupo en dólares a pesos es lo mismo que venderlo?" (cubre "cambio cupo dolar" 71 imp).
- Sin stuffing: 2 inserciones léxicas + 1 frase reescrita.

## Fase 5 — Sitemap, robots, limpieza
- `sitemap.xml` regenerado: 27 URLs (`https://www`): 25 canónicas + `/privacidad` + `/terminos`, cero legacy (verificado por listado).
- `robots.txt`: `Allow: /`, sitemap correcto, sin bloqueos relevantes.
- Limpieza: ~40 scripts `fix-*`/`gen-*`/`add-*`/`check-*`, 5 carpetas `backup_*`, 18 HTML sueltos en raíz, zip/csv sueltos → movidos a `/archive/` (nota en `archive/README.md`). Se conservaron `generate-sitemap.js`, `copy-html-files.js`, `scripts/` (gsc_audit en uso). App React y dirs `legalhelp-*`/`temp-repo` NO tocados (revisar aparte).

## Fase 6 — Hub-and-spoke en variantes del negocio (2026-09-24)
- Pilar `/vender-cupo-dolar` no enlazaba a ninguna variante: sección bancos/retail convertida a links (8 variantes + hub). Homepage nav+footer → pilar con anchor "vender cupo (en dólares)" (el pilar estaba huérfano de la página más fuerte).
- Hub `/cupo-dolares-por-banco`: cada ficha ahora enlaza a su variante (5 bancos + CMR + Ripley).
- `tabla-comparativa` 443 → ~900 palabras: metodología con caso USD 1.000, links a 10 variantes/pilares, 3 FAQs.

## Fase 7 — 6 páginas tarjeta-variantes con placeholders (2026-10-04, commit d37ac01b)
- Creadas `vender-cupo-dolar-tarjeta-{abc,paris,hites,visa,mastercard,amex}.html` con `meta robots noindex`, canonical sin slash, FAQ schema+visible, links a pilar/hub/tabla, 7 placeholders `ALEJANDRO` c/u. Fuera del sitemap (sigue 27).
- `CONTENIDO_A_RELLENAR.json` + `GUÍA_PARA_ALEJANDRO.md` en raíz (no se despliegan: el copy solo lee `public/`).
- `vercel.json` 144→146 redirects: +`/sacar-plata-:path*`, +`/cuanto-presta-:path*` → pilar; +trailing-slash exactas `cuanto-presta-tarjeta-paris/`, `sacar-plata-tarjeta-lider/`. Eliminados hijacks `/privacidad`→`/`, `/terminos`→`/` (ahora son páginas reales, 200 live).
- Verificado live: 6×200 con noindex, slash-URLs→301, privacidad/terminos 200, avance 200, 0 hijacks.
- Commit 2 (Alejandro): rellenar datos reales → quitar noindex → sitemap+headers → push → GSC.

## Fase 8 — Higiene técnica (plan de Claude, 2026-10-19, rama seo-fixes-oct-2026)
Correcciones de código existente. Sin páginas nuevas. Un commit por tarea. Sin push hasta aprobación.

_Ejecutado el 2026-10-19 en la rama `seo-fixes-oct-2026`. Los bloques T2–T5 y T8 se editaron en conjunto por proximidad; se registran aquí por tarea. Commits separados en el historial._

### T2 — JSON-LD roto (4 páginas) ✅
- Los bloques `FAQPage` de `vender-cupo-{banco-chile,bci,santander,scotiabank}.html` terminaban cerrando solo `mainEntity`+FAQPage (`...]}`), faltando `]}` (cierre de `@graph` + raíz). Schema inválido → Google descartaba el rich result.
- Fix: añadido `]}` al final de los 4 bloques. Validado con `JSON.parse` post-edit: los 4 parsean. Resto del sitio: 27 bloques ya válidos, 0 rotos.

### T3 — Bloque CITIES + links internos rotos ✅
- `index.html`: eliminada sección CITIES completa (16 tarjetas de ciudad, todas apuntando a rutas con 301 → pilar). Sin crear páginas de ciudad.
- 8 hrefs rotos corregidos: `banco-chile`→`/vender-cupo-santander` y `banco-estado`→`/vender-cupo-dolar`; `bci`→`/vender-cupo-banco-chile`; `santander` y `scotiabank` `/vender-cupo-dolares`→`/vender-cupo-dolar`; `scotiabank` `/vender-cupo-banco-state`→`/vender-cupo-banco-chile`; `santander` `/comprar-dolares`→`/vender-cupo-dolar`; `scotiabank` `/vender-cupo-bice`→`/tabla-comparativa`. Verificado: 0 hrefs a rutas con redirect literal.

### T4 — Canonical .html ✅
- `vercel.json`: +2 redirects al final — `/index.html`→`/`, `/(.*)\.html`→`/$1` (301). Sin destino .html previo, sin loops. Solo matchea `.html` (svg/png/xml/txt siguen sirviéndose estáticos). Validado `ConvertFrom-Json`.
- 8 hrefs `.html` internos → rutas limpias (nosotros, preguntas-frecuentes, testimonios). Verificado: 0 restantes.

### T5 — 404 `/avance-abc-visa` ✅
- Redirect 301 → `/vender-cupo-dolar` (pilar indexado; evita el pilar de tarjeta en noindex).

### T8 — og:url vs canonical ✅
- `og:url` de nosotros, preguntas-frecuentes y testimonios sin trailing slash (igual a canonical). Verificado: og == canonical en las 3.

### T6 — lastmod real del sitemap
- `generate-sitemap.js`: lastmod por URL = fecha del último commit git del HTML fuente (`git log -1 --format=%cI`), fallback a hoy si no hay historial. Antes: misma fecha de build para todas.

### T7 — og:image rasterizada
- Generado `public/og-image.png` 1200×630 desde el SVG existente (one-shot con `npx sharp-cli`; sin dependencia nueva en package.json, sin cambio de build).
- 15 tags `og:image` → `.png`.
- `copy-html-files.js`: añadido `.png` a la lista de copia a `dist/`.

### T8 — og:url vs canonical
- `og:url` de nosotros, preguntas-frecuentes y testimonios sin trailing slash (igual a canonical).

### T1 — Páginas órfanas enlazadas
- 5 enlaces añadidos al footer de las 26 páginas del sitemap: `/que-es-cupo-en-dolares`, `/cuanto-pagan-por-cupo-dolar`, `/guia/vender-cupo-dolares`, `/nosotros`, `/terminos`.

### T9 — Token GitHub hardcodeado
- `push-to-github.ts`: token `github_pat_…` (línea 8) reemplazado por `process.env.GITHUB_TOKEN` + throw si falta. ACCIÓN PENDIENTE DEL USUARIO: revocar el PAT comprometido en GitHub (Settings → Developer settings → Personal access tokens).

## Pendiente MANUAL (sin acceso a consolas)
1. Vercel → Primary domain = `www.dolarexpress.cl`.
2. GSC → Removals: patrones `cupo-en-dolares-en-*`, `avance-cupo-en-dolares-en-*`, `vender-cupo-dolar-[banco]-[ciudad]`, `urgente/*`, `ciudades/*`, `montos/*`, `comparativa/*`; luego "Solicitar indexación" de las 27 del sitemap.
3. GSC → declarar preferencia de dominio www (donde aplique).
4. GBP → renombrar a "DolarExpress" y responder reseñas.
5. Re-revisar en 7 días: impresiones, "excluida por noindex" (debe subir), 404 (debe bajar).
