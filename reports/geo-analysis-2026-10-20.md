# GEO-ANALYSIS.md — dolarexpress.cl (2026-10-20)

## GEO Readiness Score: 74/100

Después de aplicar fixes de hoy (antes ~58).

## Desglose

| Criterio | Peso | Puntaje | Nota |
|---|---|---|---|
| Citability (pasajes 134–167 palabras, datos concretos) | 25% | 17/25 | FAQ con cifras ($748.000, 15%, USD 300) en todas las páginas; faltan definiciones "X es..." en primeros 60 palabras de algunos pilares |
| Legibilidad estructural (H1→H2→H3, FAQ, tablas) | 20% | 18/20 | Excepcional: FAQPage+Cómo+tablas+listas en 22 páginas |
| Contenido multi-modal | 15% | 8/15 | Calculadora interactiva (home) suma; sin video ni infografías |
| Autoridad y señal de marca | 20% | 13/20 | Fechas de actualización visibles ✓, FinancialService con address ✓ y teléfono ✓; falta sameAs (no hay redes sociales reales) |
| Accesibilidad técnica (SSR, crawlers IA) | 20% | 18/20 | HTML estático server-side (AIs leen todo sin JS) ✓; crawlers IA permitidos ✓; llms.txt ahora correcto ✓ |

## Estado de crawlers de IA (robots.txt) — SIN CAMBIOS NECESARIOS
- Permitidos: GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended ✓
- Bloqueados (entrenamiento): CCBot, Bytespider, meta-externalagent ✓
- Sitemap declarado ✓

## llms.txt — CORREGIDO HOY
- Antes: 9 URLs que llevaban a 404 (banco-estado, bci, bbva, cencosud...) + contradicción "Sin comisiones" vs comisión 15% real → riesgo alto de respuesta alucinada/inconsistente
- Ahora: 34 URLs reales, bloque "Hechos clave" ($748.000 ejemplo, 15%, USD 300, tel +56 9 6765 8939, Vitacura 7181) + llms-full.txt enlazado

## SSR — verificada
Sitio 100% HTML estático servido por Vercel: los crawlers que no ejecutan JS (GPTBot, ClaudeBot, PerplexityBot) leen el contenido completo, incl. FAQ, tablas y tickers con valor por defecto $880.

## Menciones de marca (para medir offline)
Sin presencia en Wikipedia/Reddit/YouTube/LinkedIn. Palanca #1 de citabilidad en ChatGPT (Wikipedia 47.9% de citas) — ver acciones de alto impacto.

## Schema (estado)
- FinancialService (@graph, home): teléfono, areaServed, priceRange, openingHours, contactPoint + **address (NUEVO hoy: Av. Vitacura 7181, Las Condes)**
- HowTo, FAQPage, DefinedTermSet, BreadcrumbList en páginas clave ✓
- Falta: sameAs (requiere perfiles reales), Organization sibling

## Top 5 cambios de mayor impacto
1. ✅ **HECHO** — llms.txt reescrito (era la fuga mayor: AIs seguían enlaces 404 y contradictorios)
2. ✅ **HECHO** — Address del FinancialService (entidad verificable en mapa/GBP)
3. **PENDIENTE SEMANAL** — creación de pasajes definición-al-principio en pilares ("El cupo en dólares es..."): /vender-cupo-dolar y /que-es-cupo-en-dolares ya lo tienen; extender a 6 tarjetas retail
4. **PENDIENTE usuario** — crear perfiles reales (Google Business Profile ya debería existir, LinkedIn empresa, YouTube 1 video testimonial) y retorcer sameAs — ChatGPT cita Wikipedia/LinkedIn/YouTube 3x más que backlinks
5. **PENDIENTE backlinks-como-marca** — conseguir menciones en comunidades ( forum.r/d Chile: r/chile, r/finanzas) respondiendo consultas de cupo en dólares con link natural; Perplexity la cita de Reddit (46.7%)

## Próximos pasos medibles (2 semanas en GSC)
- Consultas con "tarjeta" y "banco" (AAO): deben subir impresiones
- Monitor con DataForSEO LLM mentions mensual: keyword "vender cupo en dólares" en chat_gpt+google
