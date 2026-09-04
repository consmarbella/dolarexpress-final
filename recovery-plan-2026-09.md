# DolarExpress.cl — Plan de Recovery de Penalización Doorway (Septiembre 2026)

**Contexto:** Google penalizó el sitio por doorway pages. La auditoría confirmó que 5 páginas de banco (`/banco-chile`, `/banco-estado`, `/bci`, `/santander`, `/scotiabank`) tienen contenido **100% idéntico** — solo cambia el nombre del banco. Esto se extiende probablemente a `/bbva`, `/itau`, `/cmr`, `/ripley`, `/cencosud`, `/lider`, `/la-polar`, `/paris`, `/hites`, `/abcdin`, `/jumbo`, `/easy`, `/internacional`.

**Total affected:** ~15 páginas (97% del sitemap son near-duplicates)

---

## 🔍 Diagnóstico Técnico

### Estructura actual del sitio
```
/public/
  ├─ index.html           ← Home (única, good content)
  ├─ vender-cupo-dolar.html
  ├─ cupo-internacional-a-pesos.html
  ├─ avance-cupo-dolares.html
  ├─ cupo-dolares-por-banco.html      ← Contenido profundo (good)
  ├─ que-es-cupo-en-dolares.html      ← Contenido profundo (good)
  ├─ cuanto-pagan-por-cupo-dolar.html ← Contenido profundo (good)
  ├─ banco-{banco}.html × 8           ← DOORWAY: identical content
  ├─ {retail}.html × 7                ← DOORWAY: identical content  
  ├─ internacional.html               ← DOORWAY: identical content
  ├─ contacto.html                    ← Única
  ├─ comisiones.html                  ← Única
  ├─ preguntas-frecuentes.html        ← Única
  ├─ directorio-general.html          ← Única (hub)
  ├─ nosotros.html                    ← Única
  ├─ seguridad.html                   ← Única
  ├─ testimonios.html                 ← Única
  ├─ privacidad.html                  ← Única
  ├─ terminos.html                    ← Única
  └─ venta-cupo-dolares.html
```

---

## 📈 Estrategia de Recovery

### Fase 1: Sitemap Cleanup (inmediato — 1h)
**Eliminar del sitemap + 301 redirect a hub:**

Páginas doorway a **redirigir 301 → `/cupo-dolares-por-banco`**:
- `/banco-chile` → `/cupo-dolares-por-banco`
- `/banco-estado` → `/cupo-dolares-por-banco`
- `/bci` → `/cupo-dolares-por-banco`
- `/santander` → `/cupo-dolares-por-banco`
- `/scotiabank` → `/cupo-dolares-por-banco`
- `/bbva` → `/cupo-dolares-por-banco`
- `/itau` → `/cupo-dolares-por-banco`
- `/cmr` → `/cupo-dolares-por-banco`
- `/ripley` → `/cupo-dolares-por-banco`
- `/cencosud` → `/cupo-dolares-por-banco`
- `/lider` → `/cupo-dolares-por-banco`
- `/la-polar` → `/cupo-dolares-por-banco`
- `/paris` → `/cupo-dolares-por-banco`
- `/hites` → `/cupo-dolares-por-banco`
- `/abcdin` → `/cupo-dolares-por-banco`
- `/jumbo` → `/cupo-dolares-por-banco`
- `/easy` → `/cupo-dolares-por-banco`
- `/internacional` → `/cupo-dolares-por-banco`
- `/venta-cupo-dolares` → `/vender-cupo-dolar` (duplicate)
- `/vender-cupo-internacional` → `/` (duplicate, redirect exists)
- `/vender-cupo-tarjeta-credito` → `/vender-cupo-dolar` (duplicate)

**Sitemap resultante (18 URLs quality):**
1. `/`
2. `/vender-cupo-dolar`
3. `/cupo-internacional-a-pesos`
4. `/avance-cupo-dolares`
5. `/cupo-dolares-por-banco`
6. `/que-es-cupo-en-dolares`
7. `/cuanto-pagan-por-cupo-dolar`
8. `/guia/vender-cupo-dolares`
9. `/directorio-general`
10. `/contacto`
11. `/comisiones`
12. `/preguntas-frecuentes`
13. `/nosotros`
14. `/seguridad`
15. `/testimonios`
16. `/privacidad`
17. `/terminos`
18. `/venta-cupo-dolares`

### Fase 2: Vercel redirects (15 min)
```json
// vercel.json — agregar antes de "handle: filesystem"
{ "src": "^/(banco-chile|banco-estado|bci|santander|scotiabank|bbva|itau|cmr|ripley|cencosud|lider|la-polar|paris|hites|abcdin|jumbo|easy|internacional)/?$",
  "dest": "/cupo-dolares-por-banco", "status": 301 },
{ "src": "^/venta-cupo-dolares/?$", "dest": "/vender-cupo-dolar", "status": 301 },
{ "src": "^/vender-cupo-tarjeta-credito/?$", "dest": "/vender-cupo-dolar", "status": 301 },
```

### Fase 3: Enriquecer páginas hub (3-4h)
La página `/cupo-dolares-por-banco` ya tiene contenido profundo. Hay que **añadir más contenido único** para cada banco (mínimo 500 palabras de contenido único por hub):
- `/cupo-dolares-por-banco` → ya tiene FAQ + tabla de bancos. OK.
- `/vender-cupo-dolar` → ya tiene calculator + FAQ. OK.
- `/que-es-cupo-en-dolares` → ya tiene comparativa + FAQ. OK.
- `/cuanto-pagan-por-cupo-dolar` → revisar contenido.

### Fase 4: GSC & recuperación (post-deploy)
1. **Enviar sitemap actualizado** a GSC (Index → Sitemaps → `sitemap.xml`)
2. **Request Indexing** de las 18 URLs quality (GSC → URL Inspection)
3. **Borrar URLs doorway** de GSC (Index → Coverage → excluir)
4. **Esperar 4-12 semanas** para recovery completo

### Fase 5: Fortalecer señales
- **Telegraph backlinks** (cron activo — ya está)
- **IndexNow** (cron activo — ya está)
- **Bing URL Submission** (configurar)
- **Revisar GSC Performance** — mapear queries que perdieron tráfico → asegurar cobertura en páginas hub

---

## ⚡ Timeline de Recovery

| Semana | Acción | Esperado |
|--------|--------|----------|
| **Semana 0 (hoy)** | Sitemap cleanup + 301 redirects + deploy | Inmediato |
| **Semana 1** | GSC sitemap submit + URL inspection (18 URLs) | Indexación normal en 3-7 días |
| **Semana 2** | Monitor coverage report — 0 errores esperado | Confirmar redirects trabajando |
| **Semana 4-8** | Google re-indexa → recovery algoritmo | Tráfico empieza a recuperar |
| **Semana 12** | Full recovery esperado | Tráfico baseline restaurado |

---

## 🚨 Riesgo: Over-consolidation

**No** hacer redirect de TODO a `/` — eso confunde a Google. Mejor mantener páginas hub específicas:
- 1 hub para bancos: `/cupo-dolares-por-banco`
- 1 hub para retail: `/vender-cupo-dolar` (con mención a CMR, Ripley, etc.)
- 1 hub para preguntas: `/preguntas-frecuentes`

---

## 📋 Checklist de Acción (pending user approval)

- [ ] **Aprobar** sitemap cleanup (18 URLs, 20 redirects)
- [ ] **Aprobar** modificación de `vercel.json` con redirects
- [ ] **Aprobar** generación de sitemap dinámico con 18 URLs
- [ ] **Aprobar** eliminación de HTML doorway files de `public/`
- [ ] **Aprobar** deploy (1 click)
- [ ] **Aprobar** GSC submission

> **Estado actual:** Token GSC verificado ✅ | og-image.png fixed ✅ | deploy listo 🚀

¿**Dale** a todo? (NUNCA editar sin aprobación explícita del usuario)
