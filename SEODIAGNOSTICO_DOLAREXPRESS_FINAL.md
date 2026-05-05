# 🔴 DIAGNÓSTICO SEO COMPLETO - DolarExpress.cl
## Fecha: 2026-05-05

---

## 1. RESUMEN EJECUTIVO

**Estado: CRÍTICO** - El sitio tiene múltiples problemas graves que están destruyendo su presencia en Google.

| Métrica | Valor Actual | Estado |
|---------|-------------|--------|
| Páginas en sitemap | ~200+ | ⚠️ |
| Páginas indexadas | ~372 | 🔴 |
| Páginas NO indexadas | 1,296 | 🔴 |
| Tasa de indexación | 22% | 🔴 |
| Errores 404 | 41 | 🔴 |
| Páginas con redirección | 761 | 🔴 |
| Páginas descubiertas sin indexar | 134 | ⚠️ |
| Build Vercel más reciente | **FALLIDO** | 🔴 |

---

## 2. PROBLEMA #1 (CRÍTICO): BUILD FALLANDO EN VERCEL

### El problema
El último deploy en Vercel (commit `454669d`) **falló** con este error:

```
Could not resolve "../components/Logo" from "pages/Home.tsx"
```

### Consecuencia
- El sitio está sirviendo una **versión cacheada antigua** desde Vercel
- Cualquier cambio que hayas hecho al código **no está en producción**
- Las correcciones SEO previas (si las hiciste) no se han desplegado

### Archivos involucrados en GitHub:
- `pages/Home.tsx` - intenta importar `../components/Logo`
- `components/Logo.tsx` - EXISTE en el repo
- `vite.config.ts` - define alias `@` apuntando a la raíz `.`

### ¿Por qué falla?
La importación `../components/Logo` desde `pages/Home.tsx` debería resolverse a `./components/Logo` (raíz del proyecto). Pero el alias `@` en `vite.config.ts` apunta a `path.resolve(__dirname, '.')` que es la raíz. Si `pages/Home.tsx` usa `import Logo from '../components/Logo'`, la ruta relativa desde `pages/` subiendo un nivel (`..`) sería la raíz, y luego `/components/Logo`. Esto DEBERÍA funcionar.

**Posible causa real**: Durante el build de Vite, el plugin de React podría estar buscando `components/Logo.tsx` sin extensión y fallando. O hay un problema de case-sensitivity (Windows vs Linux en Vercel).

---

## 3. PROBLEMA #2 (CRÍTICO): TODAS LAS PÁGINAS INTERNAS DAN 404

### Evidencia
- `https://www.dolarexpress.cl/venta-usd` → **404 NOT_FOUND (Vercel)**
- `https://www.dolarexpress.cl/venta-usd.html` → **404 NOT_FOUND (Vercel)**
- `https://www.dolarexpress.cl/recursos` → Probablemente 404 también

### Causa raíz
El archivo `_redirects` en el repo está **vacío** (solo tiene comentarios):

```
# Redirecciones correctas para dolarexpress.cl
# Solo redirecciones 301 necesarias
# NO agregues más redirecciones
```

**Falta la regla SPA para Vite/React:**

```
/*    /index.html   200
```

Sin esta regla, Vercel solo sirve el `index.html` en la raíz `/`. Cualquier otra ruta (como `/venta-usd`, `/cupo-dolar-banco-chile`, etc.) devuelve 404 porque no existe un archivo HTML correspondiente en `dist/`.

### Consecuencia catastrófica
- **Todas las ~200+ URLs del sitemap apuntan a páginas que devuelven 404**
- Googlebot encuentra 404 en cada página que intenta rastrear
- Esto explica los 1,296 "sin indexar" y los 41 errores 404 en GSC
- El sitio efectivamente **solo tiene 1 página funcional** (la home)

---

## 4. PROBLEMA #3 (GRAVE): 761 PÁGINAS CON REDIRECCIÓN

### Posibles causas
1. El dominio `dolarexpress.cl` redirige a `www.dolarexpress.cl` (configurado en Vercel) - esto es normal
2. Google descubrió páginas vía sitemap que no existen → Vercel responde con redirect a 404 (soft 404) o redirects en cadena
3. Posibles redirecciones mal configuradas entre versiones `http://` y `https://`

---

## 5. PROBLEMA #4: SITEMAP LLENO DE URLs INEXISTENTES

### El sitemap.xml lista ~200+ URLs como:
- `/venta-usd`
- `/cupo-dolar-banco-chile`
- `/avance-efectivo-tarjeta-cmr`
- etc.

Pero **ninguna de estas páginas existe** porque el sitio es una SPA (Single Page Application) y no tiene server-side rendering ni archivos HTML individuales.

### Esto es un problema porque:
- Google recibe el sitemap, intenta rastrear las URLs, encuentra 404/redirects
- GSC muestra los errores como "Página con redirección" o "No encontrado"
- La confianza del sitio con Google se deteriora

---

## 6. PLAN DE ACCIÓN PARA ARREGLARLO

### PRIORIDAD 1: Arreglar el build (HOY)

**Opción A - La más segura (crear archivos HTML estáticos):**
1. Generar archivos HTML individuales para cada ruta en `/public/` o usar `copy-html-files.js`
2. Cada HTML debe ser un entry point de Vite independiente o una copia del index.html
3. Agregar la regla SPA al `_redirects`

**Opción B - Arreglar la importación:**
1. Cambiar `import Logo from '../components/Logo'` → `import Logo from '@/components/Logo'` en `pages/Home.tsx`
2. Verificar que la build pase
3. Agregar `/*  /index.html  200` al `_redirects`

### PRIORIDAD 2: SPA Fallback (HOY)

Agregar al archivo `_redirects`:
```
/*    /index.html   200
```

### PRIORIDAD 3: Revisar sitemap (ESTA SEMANA)

Eliminar del sitemap las URLs que no correspondan a páginas reales o generar un sitemap que refleje la estructura real del sitio SPA.

### PRIORIDAD 4: Configurar metadata correctamente

- El `google-site-verification` tiene placeholder `REEMPLAZAR_CON_CODIGO_GSC`
- Verificar que el código de GSC sea el correcto

---

## 7. VERIFICACIÓN DE DOMINIOS EN VERCEL

| Dominio | Estado | Verificación |
|---------|--------|-------------|
| dolarexpress.cl | ✅ | Redirige a www.dolarexpress.cl |
| www.dolarexpress.cl | ✅ | Dominio principal |
| dolarexpress-final.vercel.app | ✅ | URL de Vercel |

✅ Los dominios están bien configurados.

---

## 8. RECOMENDACIONES ADICIONALES

1. **Quitar el placeholder de GSC**: `REEMPLAZAR_CON_CODIGO_GSC`
2. **Completar el schema de Organization**: El teléfono y WhatsApp tienen placeholders
3. **Asegurar que las imágenes OG existan**: `/og-image.png` y `/logo.png`
4. **Considerar pasar de SPA a SSG/SSR** (Next.js) para tener mejor SEO si el sitio tiene 200+ páginas de contenido
5. **Limpiar el repositorio**: Hay ~20 scripts de Python/Bash que sugieren intentos previos de arreglar SEO

---

## 9. ORDEN DE PRIORIDAD

| Orden | Acción | Impacto |
|-------|--------|---------|
| 🔴 1 | Arreglar `pages/Home.tsx` para que compile | Desbloquea deploys |
| 🔴 2 | Agregar SPA fallback en `_redirects` | Arregla 200+ páginas 404 |
| 🟡 3 | Verificar que build pase y hacer deploy | Cambios llegan a producción |
| 🟡 4 | Solicitar re-indexación en GSC | Google vuelve a rastrear |
| 🟢 5 | Limpiar sitemap | URLs correctas |
| 🟢 6 | Completar metadatos faltantes | Mejor presencia |

---

*Diagnóstico generado analizando: repositorio GitHub, build logs de Vercel, HTML en vivo, sitemap, navegación del sitio, y datos de Google Search Console.*