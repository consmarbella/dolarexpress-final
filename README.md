# RaguAbogados.cl v2.0 — Documentos Legales con IA

## Descripción
Plataforma de IA legal chilena que permite a usuarios crear **cualquier documento legal** (no solo plantillas fijas) mediante una conversación guiada de 3 fases:

1. **Diagnóstico**: El usuario describe su problema. La IA clasifica el documento y propone precio.
2. **Planificación**: La IA genera automáticamente un plan de entrevista con los campos necesarios para ESE documento específico.
3. **Entrevista estricta**: El backend controla campo por campo. La IA solo valida respuestas. Cero improvisación.

## Stack
- **Next.js 14** (App Router) + TypeScript + Tailwind CSS
- **Supabase** (Auth + PostgreSQL + Storage)
- **Stripe** (pagos Chile)
- **Anthropic Claude** (Sonnet 4 para diagnóstico/planificación/generación, Haiku para extracción)
- **Vercel** (deploy)

## Estructura de archivos
```
raguabogados-v2/
├── app/
│   ├── api/
│   │   ├── chat/route.ts          # State machine principal (3 fases)
│   │   ├── diagnose/route.ts      # Crear nuevo documento
│   │   ├── download/route.ts      # Descargar documento post-pago
│   │   ├── stripe/
│   │   │   ├── checkout/route.ts  # Crear sesión de pago
│   │   │   └── webhook/route.ts   # Webhook de Stripe
│   │   └── vision/route.ts        # OCR con Claude Vision
│   ├── chat/page.tsx              # Pantalla de chat + preview
│   ├── page.tsx                   # Landing con selector de documentos
│   ├── layout.tsx                 # Root layout con fuentes
│   └── globals.css                # Tailwind + fuentes
├── components/
│   ├── chat-panel.tsx             # Panel de chat con progreso
│   ├── doc-type-selector.tsx      # Grid de tipos de documento
│   ├── document-preview.tsx       # Preview con paywall blur
│   ├── image-uploader.tsx         # Dropzone para OCR
│   └── progress-bar.tsx           # Barra de progreso de entrevista
├── lib/
│   ├── types.ts                   # Tipos TypeScript
│   ├── supabase.ts                # Cliente Supabase (admin + browser)
│   ├── llm.ts                     # Wrapper de llamadas a Claude
│   ├── prompts.ts                 # Todos los prompts del sistema
│   └── validation.ts              # Pre-validación anti-desvío + validación de tipos
├── schema.sql                     # Schema de Supabase con RLS
├── middleware.ts                  # Auth de Supabase en rutas
├── next.config.js                 # Config de Next.js
├── tailwind.config.ts             # Config de Tailwind + colores
├── tsconfig.json                  # Paths (@/*)
├── package.json                   # Dependencias
└── .env.example                   # Variables de entorno
```

## Setup paso a paso

### 1. Crear proyecto Next.js
```bash
npx create-next-app@14 raguabogados-v2 --typescript --tailwind --eslint --app --src-dir=false
```

### 2. Instalar dependencias
```bash
cd raguabogados-v2
npm install @supabase/supabase-js @supabase/ssr stripe
npm install -D @types/node
```

### 3. Configurar Supabase
1. Crear proyecto en [supabase.com](https://supabase.com)
2. Ir a SQL Editor → New query
3. Pegar el contenido de `schema.sql`
4. Ejecutar
5. Copiar URL y anon key a `.env.local`
6. En Settings → API → Service Role Key → copiar a `.env.local`

### 4. Configurar Stripe
1. Crear cuenta en [stripe.com](https://stripe.com)
2. Obtener Secret Key y Publishable Key
3. Configurar webhook endpoint: `https://tusitio.com/api/stripe/webhook`
4. Seleccionar evento: `checkout.session.completed`
5. Copiar Webhook Secret a `.env.local`

### 5. Configurar Anthropic
1. Obtener API key en [console.anthropic.com](https://console.anthropic.com)
2. Agregar a `.env.local`

### 6. Variables de entorno
Copiar `.env.example` a `.env.local` y llenar todos los valores.

### 7. Deploy en Vercel
```bash
npm run build
# O conectar repo GitHub a Vercel
```

## Arquitectura de 3 Fases (anti-desvío)

### Fase 1: Diagnóstico (Abierto)
- Modelo: **Claude Sonnet 4**
- El usuario describe su problema en lenguaje natural.
- La IA clasifica el documento, propone título, resumen y precio.
- Máximo 3 mensajes. Luego se fuerza transición a Planificación.

### Fase 2: Planificación (Automático)
- Modelo: **Claude Sonnet 4**
- Basado en el diagnóstico, genera un JSON con los campos necesarios.
- Ejemplo para "desalojo": `demandante_nombre`, `demandado_nombre`, `direccion_propiedad`, `canon_mensual`, etc.
- Una vez generado el plan, se convierte en inmutable.

### Fase 3: Entrevista (Estricta)
- Modelo: **Claude Haiku** (barato y obediente)
- El backend itera el plan campo por campo.
- El LLM recibe SOLO: campo actual + respuesta del usuario.
- El LLM responde SOLO con JSON: `{"valid": true/false, "value": "..."}`
- Si el usuario se desvía, pregunta o pide consejo → `valid: false` → se repite la pregunta.

## Guardrails implementados

| Problema | Solución |
|----------|----------|
| Pregunta cosas irrelevantes | El plan JSON define exactamente qué campos existen. No se pueden inventar. |
| Da consejos legales | Prompt de Fase 3: "Eres extractor de datos. No eres abogado." |
| Usuario se desvía | Pre-validación detecta preguntas, consejos, evasión. Se ignora y se repite la pregunta. |
| Temas no cubiertos | Lista negra: penal, constitucional, familia compleja. Rechazo inmediato. |
| Conversación infinita | Máximo 3 mensajes en diagnóstico. Máximo 2 reintentos por campo. |

## Modelos recomendados

| Fase | Modelo | Por qué |
|------|--------|---------|
| Diagnóstico | Claude Sonnet 4 | Razonamiento legal y comprensión de contexto chileno |
| Planificación | Claude Sonnet 4 | Conocimiento de qué campos son legales para cada documento |
| Extracción | Claude Haiku | Solo validación JSON. Barato ($0.25/M tokens vs $3/M) y obediente. |
| Generación | Claude Sonnet 4 | Calidad de redacción legal formal |
| OCR/Vision | Claude Sonnet 4 | Extrae texto de fotos de documentos |

## Precios de documentos

| Tipo | Precio |
|------|--------|
| Prescripción TAG | $20.000 |
| Finiquito Laboral | $10.000 |
| Carta de Reclamo | $10.000 |
| Poder Simple | $10.000 |
| Escrito Libre / Demanda / Contrato | $15.000 - $30.000 (dinámico según complejidad) |

## Flujo de pago
1. Usuario completa entrevista → Documento se genera en preview.
2. Preview muestra 1/3 del documento. El resto está difuminado (blur + gradiente).
3. Botón "Pagar y descargar" → Stripe Checkout.
4. Webhook confirma pago → Status cambia a PAID.
5. Usuario puede descargar HTML/DOCX/PDF completo.

## Notas para el desarrollador

### No modificar estos archivos sin entender la state machine:
- `app/api/chat/route.ts` — El corazón del sistema. Las 3 fases están aquí.
- `lib/prompts.ts` — Los prompts controlan el comportamiento de la IA.
- `lib/validation.ts` — Los guardrails anti-desvío.

### Para agregar un nuevo tipo de documento:
No necesitas modificar código. El sistema es dinámico:
1. El usuario describe su caso.
2. La IA diagnostica y planifica automáticamente.
3. Se generan los campos necesarios.

### Para agregar plantillas rápidas (como TAG, Finiquito):
En `app/api/diagnose/route.ts`, puedes pasar `templateKey` para saltar diagnóstico y cargar un plan fijo predefinido (no implementado en v2.0, pero la arquitectura lo soporta).

## Licencia
Privado. Todos los derechos reservados.
