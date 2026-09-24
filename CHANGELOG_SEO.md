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

## Fase 3 — Consolidación vercel.json (68 → 110 redirects, 0 rewrites)
- `public/` no tiene páginas de ciudad: las familias `cupo-en-dolares-en-*` y `avance-cupo-en-dolares-en-*` son legacy 404. Cruzadas 220 URLs indexadas conocidas vs redirects: 46 huérfanas (menos canónicas vivas).
- Nuevos 301: `/cupo-en-dolares-:path*` → `/que-es-cupo-en-dolares`; wildcards por marca (`banco-chile/itau/ripley/lider/easy/jumbo/hites/paris/la-polar/abc-din/bbva`) → su pilar; 20 exactas temáticas (ej `/estoy-en-dicom-y-tengo-cupo-cmr` → `/vender-cupo-dolar-sin-dicom`, `/tengo-cupo-en-ripley-y-necesito-efectivo` → `/vender-cupo-ripley-rapido`, `/urgente-cupo-paris-hoy` → `/como-vender-cupo-dolar-rapido`, `/guia/evitar-estafas-cupo-dolar` → `/guia/vender-cupo-dolares`).
- **Bug crítico hallado y fixeado**: `/avance-:path*` matcheaba `/avance-cupo-dolares` → **loop 301 a sí misma en vivo** (verificado con curl: `301 -> misma URL`). Reemplazada por 7 reglas específicas (`avance-cupo-en-dolares-*`, `avance-efectivo[-*]`, `avance-la-polar/lider/ripley/tarjeta-*`). Re-chequeo programático: 0 hijacks sobre las 25 canónicas.
- Verificación post-deploy: spot-checks de 4 redirects + `/avance-cupo-dolares` → 200.

## Fase 4 — Keywords en contenido
- Fix title corrupto `que-es-cupo-en-dolares.html:1` → "Qué es el Cupo en Dólares y Cómo Funciona | Guía Chile 2026" (cubre "cupo en dolares chile" 77 imp/trim).
- `cuanto-pagan-por-cupo-dolar.html:115`: "operaciones de cambio de divisas" → "operaciones con cupo en dólares de tarjeta de crédito".
- 2 FAQs nuevas en `vender-cupo-dolar.html` (visible + JSON-LD sincronizados): "¿Buscás alguien que compre cupo en dólares en Chile?" (cubre "compro cupo dolar" 68 imp) y "¿El cambio de cupo en dólares a pesos es lo mismo que venderlo?" (cubre "cambio cupo dolar" 71 imp).
- Sin stuffing: 2 inserciones léxicas + 1 frase reescrita.

## Fase 5 — Sitemap, robots, limpieza
- `sitemap.xml` regenerado: exactamente las 25 canónicas `https://www`, cero legacy (verificado por listado).
- `robots.txt`: `Allow: /`, sitemap correcto, sin bloqueos relevantes.
- Limpieza: ~40 scripts `fix-*`/`gen-*`/`add-*`/`check-*`, 5 carpetas `backup_*`, 18 HTML sueltos en raíz, zip/csv sueltos → movidos a `/archive/` (nota en `archive/README.md`). Se conservaron `generate-sitemap.js`, `copy-html-files.js`, `scripts/` (gsc_audit en uso). App React y dirs `legalhelp-*`/`temp-repo` NO tocados (revisar aparte).

## Pendiente MANUAL (sin acceso a consolas)
1. Vercel → Primary domain = `www.dolarexpress.cl`.
2. GSC → Removals: patrones `cupo-en-dolares-en-*`, `avance-cupo-en-dolares-en-*`, `vender-cupo-dolar-[banco]-[ciudad]`; luego "Solicitar indexación" de las 25 del sitemap.
3. GSC → declarar preferencia de dominio www (donde aplique).
4. GBP → renombrar a "DolarExpress" y responder reseñas.
5. Re-revisar en 7 días: impresiones, "excluida por noindex" (debe subir), 404 (debe bajar).
