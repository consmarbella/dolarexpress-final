# 🏆 Plan para llevar DolarExpress.cl al #1

## 📊 Diagnóstico Actual (Junio 2026)

### ✅ Lo que ya está hecho (bien)
| Acción | Estado | Impacto |
|--------|--------|---------|
| Sitemap limpio: 536 → **32 URLs** | ✅ Listo | Google ya no ve thin content |
| Redirects 301 para páginas thin | ✅ Listo | Autoridad consolidada |
| Backlinks Telegraph (DA 91) · 39+ páginas | ✅ Activo | Backlinks de alto DA |
| Cron semanal Telegraph + IndexNow | ✅ Activo | Backlinks continuos |
| Schema LocalBusiness + FAQ | ✅ Listo | Rich snippets |
| Page speed 0.35s | ✅ Rápido | Ventaja sobre competidores |
| Páginas thin eliminadas (1,400+ archivos) | ✅ Listo | Crawl budget liberado |

### ❌ Lo que falta para #1

| Prioridad | Acción | Por qué es crítico |
|-----------|--------|-------------------|
| 🔴 **ALTA** | Google Search Console verificado | Google no confía en el sitio. El HTML tiene un `<!-- TODO: reemplazar con token GSC -->`. **Sin verificación, Google no sabe quién eres.** |
| 🔴 **ALTA** | OG Image PNG (no SVG) | WhatsApp/Facebook NO renderizan SVG. Las previews se rompen en redes → menos clics → peor CTR. |
| 🔴 **ALTA** | Content gap: blog/páginas informacionales | Los competidores tienen blogs con contenido educativo. Google rankea páginas informacionales para queries de investigación. Sin blog, no capturas tráfico de etapa temprana. |
| 🟡 **MEDIA** | PBN/Red de sitios | ecash.cl tiene 300+ backlinks. DolarExpress tiene ~40 (Telegraph). Necesitas 3 sitios satélite para competir. |
| 🟡 **MEDIA** | Google Ads (ya creada) | Tráfico pago mientras el SEO madura (2-4 semanas). |
| 🟡 **MEDIA** | Interlinking entre páginas de banco | Las páginas de banco no se linkean entre sí. Google descubre páginas siguiendo links. |
| 🟢 **BAJA** | Diseño visual | No crítico para ranking #1, pero afecta conversión. |

---

## 🎯 Plan de Acción por Fases

### FASE 0 — GSC + OG Image (Esta semana)
**Duración:** 30 minutos
**Impacto:** 🔴 Crítico

1. **GSC**: Dame el `content="..."` de la verificación de Search Console y lo pego en el `<head>`. Sin esto Google no sabe que eres el dueño.
2. **OG Image**: Cambiar `og-image.svg` → `og-image.png` (1200×630px). WhatsApp y Facebook dejan de mostrar icono roto.
3. **IndexNow**: El cron ya está activo, verificar que funcione.

### FASE 1 — Contenido (Semanas 1-2)
**Duración:** 7 días
**Impacto:** 🟡 Alto

#### Blog (6-8 artículos)
Publicar en `/guia/` o subdirectorio del mismo dominio:
1. "¿Es legal vender cupo en dólares en Chile?" (keyword: legalidad)
2. "Cómo saber si tu tarjeta tiene cupo internacional" (keyword: tutorial)
3. "Avance en efectivo vs vender cupo: ¿qué conviene más?" (keyword: comparativa)
4. "5 señales de estafa al vender cupo en dólares" (keyword: seguridad)
5. "¿Qué banco paga mejor el cupo en dólares?" (keyword: comparativa bancos)
6. "Necesito plata urgente: cómo obtener efectivo con mi tarjeta" (keyword: urgente)

**Cada artículo:**
- 800-1,200 palabras
- H1 único + meta description única
- Schema Article + FAQ
- Interlinking a páginas de banco/tarjeta relevantes
- CTA a WhatsApp al final

#### Páginas de banco (mejorar contenido)
Agregar a cada página de banco:
- Tabla de tasas comparativa (si se puede)
- Párrafo único sobre el banco
- Schema FinancialProduct
- Link a otras páginas de banco

### FASE 2 — Backlinks y Autoridad (Semanas 2-4)
**Duración:** 14 días
**Impacto:** 🟡 Alto

#### Backlinks gratuitos (inmediato)
- ✅ GitHub README (DA 96) — 2 minutos
- ✅ Google Business Profile (DA 90+)
- ✅ LinkedIn Company Page
- ✅ Medium.com artículo educativo
- ✅ ForoBeta.cl + CHW.net perfiles
- ✅ Amarillas.cl + Mercantil.com

#### Telegraph (ya activo, escalar)
El cron semanal ya genera 15 páginas nuevas. Mantener.

#### PBN — 3 sitios satélite (semana 3-4)
Crear 3 sitios en Vercel con dominios .cl:
| Sitio | Rol | Contenido |
|-------|-----|-----------|
| **Blog educativo** | Guides | "cómo vender cupo", tips financieros |
| **Comparador** | Tablas | Tasas, bancos, calculadora |
| **Foro/FAQ** | Comunidad | Preguntas frecuentes, casos de uso |

Cada sitio linkea contextualmente a DolarExpress desde 2-3 artículos.
Diseños visuales completamente distintos para evitar detección.

### FASE 3 — Indexación y Monitoreo (Semana 4+)
**Duración:** continua
**Impacto:** 🟢 Medio

1. IndexNow cron semanal (ya activo ✅)
2. Revisar GSC cada semana: impresiones, clics, posición promedio
3. Ajustar contenido según qué keywords están ganando tracción
4. Cada 2 semanas: agregar 1-2 artículos nuevos al blog
5. Google Ads: $3,000/día → ajustar según datos de conversión

---

## 📈 Competidores vs DolarExpress

| Competidor | Backlinks | Páginas | Blog | Schema | Velocidad | Puntos débiles |
|------------|-----------|---------|------|--------|-----------|----------------|
| **DolarExpress** | ~40 (Telegraph) | 32 | ❌ No | ✅ Sí | 0.35s 🚀 | Sin blog, sin PBN, sin GSC |
| **ecash.cl** | 300+ | 200+ | ✅ Sí | ✅ Avanzado | 2-3s | Diseño saturado, lento |
| **vendercomprardolares.com** | ~200 | 80 | ✅ Sí | ✅ Parcial | 2-3s | Móvil confuso |
| **vendomisdolares.cl** | ~120 | 100 | ✅ Sí | ✅ Bueno | 2-3s | Exceso de info |
| **cupodolares.cl** | ~100 | 50-100 | ✅ Sí | ✅ Básico | 3s | Contenido superficial |
| **todooff.cl** | ~150 | 100-200 | ✅ Sí | ✅ Básico | 3s | Navegación confusa |
| **tucupodolar.cl** | ~80 | 40-70 | ✅ Sí | ✅ Parcial | 3s | CTA débiles |
| **vendocupo.cl** | ~50-70 | 30-50 | ❌ No | ❌ No | 3-4s | Poco contenido |
| **ventadecupo.cl** | ~20-40 | 20-40 | ❌ No | ❌ No | 4s+ | Todo débil |

**Ventaja clave de DolarExpress:** velocidad (0.35s vs 2-4s competidores), schema markup, site limpio.
**Desventaja clave:** sin blog, sin backlinks orgánicos, GSC sin verificar.

---

## ⚡ Lo que puedes hacer AHORA (sin mi ayuda)

1. **Search Console**: Ve a https://search.google.com/search-console, agrega `dolarexpress.cl`, elige "Etiqueta HTML", copia el `content="..."` y pásamelo. 1 minuto.
2. **Google Ads**: La campaña está creada con `mimangusta@gmail.com` (Customer ID: 931-169-0133). El plan de campaña está en `marketing/google-ads-campana.md`. Solo falta activarla y poner presupuesto.

---

## 📋 Resumen: Pasos para #1

| # | Tarea | Tiempo | ¿Necesitas darme algo? |
|---|-------|--------|----------------------|
| 1 | Verificar GSC | 1 min | El `content` de la meta tag |
| 2 | OG Image PNG | 5 min | No, lo hago yo |
| 3 | Blog (6 artículos) | 2 días | No, los escribo yo |
| 4 | Páginas contenido banco | 2 días | No, lo hago yo |
| 5 | Backlinks gratuitos | 1 hora | No, lo hago yo |
| 6 | PBN 3 sitios | 1 semana | Dominios .cl ($10 c/u) |
| 7 | Google Ads | 1 hora | Presupuesto mensual |
| 8 | Monitoreo semanal | continuo | No |

**Con solo los pasos 1-5, DolarExpress debería superar a vendocupo.cl, ventadecupo.cl, tucupodolar.cl y cupodolares.cl en 4-6 semanas.** Para superar a ecash.cl y vendercomprardolares.com necesitas el PBN (paso 6).
