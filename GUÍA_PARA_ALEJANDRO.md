# GUÍA PARA ALEJANDRO — rellenar las 6 páginas tarjeta (Commit 2)

Las 6 páginas están creadas con `meta robots noindex`, fuera del sitemap y fuera de headers index.
**No reciben tráfico hasta que completes este proceso.** Los placeholders están marcados como
`<!-- ALEJANDRO: ... -->` dentro de cada HTML y detallados en `CONTENIDO_A_RELLENAR.json`.

## Páginas (todas en `public/`)
- vender-cupo-dolar-tarjeta-abc.html
- vender-cupo-dolar-tarjeta-paris.html
- vender-cupo-dolar-tarjeta-hites.html
- vender-cupo-dolar-tarjeta-visa.html
- vender-cupo-dolar-tarjeta-mastercard.html
- vender-cupo-dolar-tarjeta-amex.html

## Qué rellenar por página (datos REALES de tu operación, nada inventado)
1. **MONTO_MÁXIMO + ejemplo calculado**: máximo USD visto + neto en pesos hoy (USD × tipo de cambio × 0.85).
2. **REQUISITO_3 / PASO_3**: solo si esa tarjeta tiene algo propio; si no, **elimina la línea** (mejor menos que relleno).
3. **CASO_1 y CASO_2**: iniciales + comuna + monto USD + minutos de depósito + quote textual del cliente. Deben ser casos reales (publicidad engañosa = Ley 19.496 + penalización Google).
4. Revisa que cada página quede con redacción distinta a sus hermanas (no copies el mismo texto 6 veces).

## Flip a index (cuando las 6 estén rellenas)
1. Quita `<meta name="robots" content="noindex">` de cada archivo.
2. Agrega las 6 URLs a `generate-sitemap.js` (priority 0.7, monthly).
3. Agrega los 6 slugs a las 2 reglas header index de `vercel.json` (la limpia y la `\.html`).
4. `npm run build` → commit → push → pedir indexación en GSC.
5. A los 30 días: la que tenga 0 impresiones se evalúa (consolidar con 301 o reforzar).
