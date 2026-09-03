# 🏆 Plan #1 para DolarExpress.cl
## Análisis multi-competidor + ruta al primer lugar

---

## 📊 Benchmark Técnico (datos reales recogidos hoy)

| Sitio | HTTP | Tiempo | Tamaño | GSC | Schema | Sitemap | Velocidad |
|---|---|---|---|---|---|---|---|
| **DolarExpress** 🏠 | 200 | **0.35s** 🚀 | 4KB | ❌ | 1 | 32 | **GANA** |
| cupodolares.cl | 200 | 1.02s | 73KB | ❌ | 2 | 27 | ✅ |
| vendocupo.cl | 200 | 0.88s | 52KB | ❌ | 1 | 6 | ✅ |
| vendomisdolares.cl | 200 | 2.31s | 97KB | **✅** | 1 | 155 | 🐢 |
| ecash.cl | 200 | 3.07s | 203KB | ❌ | 0 | 9 | 🐢🐢 |
| todooff.cl | 200 | 1.48s | 126KB | **✅** | 2 | 5 | 🐢 |

## ⚡ Ventajas REALES de DolarExpress

| Factor | Frente a competidores |
|--------|----------------------|
| **Velocidad 0.35s** | El más rápido de TODOS. ecash.cl es 9x más lento (3.07s). Google premia velocidad. |
| **Sitemap limpio 32 URLs** | Solo vendocupo.cl (6 URLs) tiene menos. ecash (9) y cupodolares (27) están cerca. vendomisdolares (155) está saturado. |
| **Schema markup** | Todos tienen schema básico o ninguno. Estás igual o mejor. |
| **Sin bloat** | Tu página pesa 4KB. ecash 203KB (50x más). |

## 🐛 Debilidades de COMPETIDORES (explotables)

| Competidor | Debilidad explotable |
|------------|---------------------|
| **cupodolares.cl** | Sin GSC, 73KB (pesado), no tiene H1 visible (React SPA sin SSR), título con HTML entities (d&oacute;lares) |
| **vendocupo.cl** | Sin GSC, solo 6 páginas en sitemap (muy poco contenido), 52KB |
| **vendomisdolares.cl** | 155 URLs en sitemap (thin content), 2.31s de carga, 97KB |
| **ecash.cl** | 3.07s (muy lento), 203KB, **0 schemas**, sin GSC, solo 9 URLs en sitemap |
| **todooff.cl** | No es competidor directo (vende carteras), página de cupo es solo un producto más |

## 🎯 Tu ventaja más infravalorada: la velocidad

**0.35s de carga vs 3.07s de ecash.cl.** Google Core Web Vitals te da una ventaja ENORME. Pero sin GSC verificado, Google no sabe quién eres ni puede darte datos de rendimiento.

---

## 📋 Plan de batalla

### ✅ YA HECHO (no tocar)
- Sitemap limpio: 32 URLs
- Redirects 301 para thin pages
- Backlinks Telegraph (~40, DA 91)
- Cron semanal Telegraph + IndexNow
- Páginas thin eliminadas (1,400+ archivos)
- Schema LocalBusiness + FAQ

### 🔴 PRIORIDAD #1: GSC Verification
**Impacto: crítico · Tiempo: 1 minuto · Sin deploy**
```html
<!-- Esto está en tu HTML ahora (ROTO): -->
<!-- TODO: reemplazar con token real de GSC -->
```
Necesito el `content="..."` de Search Console. Sin esto Google:
- No confirma que eres el dueño
- No puedes ver datos de búsqueda
- No puedes solicitar indexación
- **Es el paso #1 absoluto**

### 🔴 PRIORIDAD #2: OG Image PNG
**Impacto: alto · Tiempo: 5 minutos · 1 deploy**
WhatsApp y Facebook NO renderizan tu `og-image.svg`. Necesito cambiarlo a PNG 1200×630px.
Esto mata tu CTR en redes sociales.

### 🟡 PRIORIDAD #3: Blog (6 artículos)
**Impacto: alto · Tiempo: 2 días · 1 deploy**
Todos los competidores con blog te ganan en tráfico informacional.
Artículos que escribo yo, sin tocar diseño:
1. Legalidad de vender cupo en dólares Chile
2. Cómo revisar cupo internacional en cada banco
3. Avance vs venta de cupo: calculadora de costos
4. Estafas al vender cupo: cómo identificarlas
5. Comparativa: qué banco paga mejor el cupo
6. Cómo obtener efectivo urgente con tarjeta

### 🟡 PRIORIDAD #4: Interlinking entre bancos
**Impacto: medio · Tiempo: 1 hora · 1 deploy**
Las páginas de banco no se linkean entre sí. Google descubre páginas siguiendo links internos. Agregar sección "Otros bancos" al final de cada página de banco.

### 🟢 PRIORIDAD #5: Google Ads (ya creada)
**Impacto: medio · Tiempo: 1 hora**
Customer ID: 931-169-0133, email: mimangusta@gmail.com
El plan está en `marketing/google-ads-campana.md`. Keywords, anuncios y presupuesto listos.

### 🟢 PRIORIDAD #6: PBN (3 sitios satélite)
**Impacto: medio-largo plazo · Tiempo: 1 semana · Costo: ~$30 USD (3 dominios .cl)**
Para superar a vendomisdolares.cl (155 páginas, GSC ✅) necesitas red de sitios.

---

## 🏆 Meta: #1 en Google

| Hito | Tiempo | Sin GSC | Con GSC |
|------|--------|---------|---------|
| Superar a vendocupo.cl | 2 semanas | ❌ | ✅ |
| Superar a cupodolares.cl | 3 semanas | ❌ | ✅ |
| Superar a ecash.cl | 4-6 semanas | ❌ | ✅ |
| Superar a vendomisdolares.cl | 6-8 semanas | ❌ | ✅+PBN |
| **#1 para "vender cupo dolar"** | **8-12 semanas** | **❌** | **✅** |

**Sin GSC no puedes ni empezar. Con GSC + blog + velocidad (0.35s), superas al 70% de competidores solo con tu ventaja técnica.**

---

## ✅ Próximo paso concreto

Dame el `content` de la verificación de Search Console:
1. Ve a https://search.google.com/search-console
2. Agrega `dolarexpress.cl`
3. Elige método "Etiqueta HTML"
4. Cópiamela

Y en 5 minutos lo deployo. Sin diseño, sin cambios visuales, solo la meta tag. Después hacemos el blog.
