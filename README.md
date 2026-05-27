# pSEO Pipeline — LangGraph Stack
**Extracción → Análisis IA → Generación → Publicación**

## Estructura del proyecto

```
pseo_agent/
├── main.py                    ← Punto de entrada (ejecutar esto)
├── graph.py                   ← Motor LangGraph (nodos + edges + retry logic)
├── state.py                   ← Estado compartido entre nodos
├── requirements.txt
├── clientes_ejemplo.csv
├── agents/
│   ├── scraper_node.py        ← Nodo A: Extracción con retry automático
│   ├── analyst_node.py        ← Nodo B: Análisis IA (Primeros Principios)
│   ├── writer_node.py         ← Nodo C: Generación de páginas pSEO
│   └── publisher_node.py      ← Nodo D: Publicación local + Vercel/GitHub
└── output/                    ← Páginas HTML generadas (se crea automático)
```

## Setup en VS Code (5 minutos)

### 1. Instalar dependencias
```bash
cd pseo_agent
pip install -r requirements.txt
```

### 2. Configurar API Key
```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Mac/Linux
export ANTHROPIC_API_KEY="sk-ant-..."
```

O crea un archivo `.env` en la raíz:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Ejecutar

**URL única:**
```bash
python main.py --url https://atlascash.cl --client dolarexpress.cl --context "cupo dólar fintech Chile"
```

**Batch (múltiples competidores en paralelo):**
```bash
python main.py --batch clientes_ejemplo.csv --workers 3
```

## Flujo del grafo

```
START
  │
  ▼
[Nodo A: Scraper]
  │ ✓ éxito → [Nodo B: Analista]
  │ ✗ fallo → reintento (hasta 3x con headers distintos)
  │ ✗ fallo total → END con error
  │
  ▼
[Nodo B: Analista] (Claude IA)
  │ → Secreto de nicho
  │ → Keywords objetivo (15)
  │ → Brechas de autoridad
  │
  ▼
[Nodo C: Escritor] (Claude IA)
  │ → Template HTML base
  │ → 10 variaciones de página
  │
  ▼
[Nodo D: Publicador]
  │ → Guarda HTMLs en /output
  │ → Genera sitemap.xml
  │ → Genera reporte JSON
  │ → (opcional) Git push → Vercel auto-deploy
  │
  ▼
END ✓
```

## Variables de entorno opcionales

| Variable | Default | Descripción |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | requerida | Tu API key de Anthropic |
| `PSEO_AUTO_DEPLOY` | `false` | Si `true`, hace git push automático |

## Salida en /output

Después de ejecutar encontrarás:
- `{slug}.html` — Landing pages optimizadas listas para Vercel
- `index.html` — Índice de todas las páginas (no indexable)
- `sitemap.xml` — Sitemap para Google Search Console
- `reporte_pseo.json` — Data completa del análisis

## Deploy a Vercel

1. Mueve el contenido de `/output` a la raíz de tu repo en GitHub
2. Vercel detecta los cambios y hace deploy automático
3. Sube el `sitemap.xml` a Google Search Console

Con `PSEO_AUTO_DEPLOY=true` el paso 1 es automático.
