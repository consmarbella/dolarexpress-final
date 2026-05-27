"""
agents/writer_node.py — Nodo C: Generación de Páginas pSEO
Genera variaciones de landing pages optimizadas en batch con Gemini 1.5 Flash.
Incluye restricciones de dominio legal para evitar alucinaciones.
"""

import re
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deepseek_client import generate_content
from state import PSEOState
from validator_node import detect_niche, get_legal_framework

PAGES_PER_BATCH = 10


def writer_node(state: PSEOState) -> PSEOState:
    """
    Nodo C: Genera variaciones de páginas pSEO basadas en el análisis.
    Crea template HTML + N variaciones con keywords/slugs únicos.
    Inyecta restricciones de dominio legal para evitar alucinaciones.
    """
    print(f"\n[Nodo C — Escritor] Generando páginas pSEO para {state['client_domain']}...")

    # Detectar nicho y framework legal
    niche = detect_niche(state)
    framework = get_legal_framework(niche)
    state["detected_niche"] = niche
    state["legal_framework"] = framework
    print(f"  Nicho detectado: {niche} — aplicando restricciones legales")

    keywords = state.get("target_keywords", [])
    if not keywords:
        state["errors"].append("Escritor: sin keywords objetivo del analista")
        return state

    batch_keywords = keywords[:PAGES_PER_BATCH]

    try:
        template = _generate_template(state, niche, framework)
        state["page_template"] = template
        print(f"  [OK] Template base generado ({len(template)} chars)")

        variations = _generate_variations(state, batch_keywords, template, niche, framework)
        state["page_variations"] = variations
        state["pages_generated"] = len(variations)
        state["current_node"] = "writer_done"

        print(f"  [OK] {len(variations)} páginas generadas")

    except Exception as e:
        state["errors"].append(f"Escritor error: {str(e)}")
        print(f"  [FAIL] Error en generación: {e}")

    return state


def _build_legal_restrictions(niche: str, framework: dict) -> str:
    """Construye el bloque de restricciones legales para inyectar en prompts."""
    if niche == "tag":
        return f"""
=== RESTRICCIONES LEGALES ESTRICTAS (NO VIOLAR) ===
Tema: Deuda TAG (Tránsito)

LEYES CORRECTAS (SOLO estas):
- Decreto con Fuerza de Ley N°1 de 2007 (Ley de Tránsito)
- Ley N°18.290 (Ley de Tránsito)

LEYES PROHIBIDAS (NO MENCIONAR BAJO NINGÚN CONCEPTO):
- Código del Trabajo (PROHIBIDO)
- Ley 17.322 (PROHIBIDO)
- AFP (PROHIBIDO)
- Cotizaciones previsionales (PROHIBIDO)
- Art. 162 Código del Trabajo (PROHIBIDO)
- Art. 58 Código del Trabajo (PROHIBIDO)
- Despido o indemnización laboral (PROHIBIDO)

TRIBUNAL CORRECTO:
- Juzgado de Policía Local (para la mayoría de los casos)
- Juzgado de Letras en lo Civil (solo si es demanda ejecutiva avanzada, aclarar contexto)

PLAZO DE PRESCRIPCIÓN:
- 2 años (Art. 24 DFL 1 de 2007) — NUNCA digas 3 años

TEMAS PROHIBIDOS:
- AFP, cotizaciones, previsional, despido, indemnización, finiquito

REGLAS DE ORO:
1. NO mezcles leyes laborales con TAG. Son dominios legales distintos.
2. Si mencionas un tribunal, sé consistente en toda la página.
3. El plazo de prescripción del TAG es 2 años, no 3.
4. NO uses frases como "Código del Trabajo" en una página sobre TAG.
"""
    elif niche == "fintech":
        return f"""
=== RESTRICCIONES LEGALES ===
Tema: Servicios Financieros / Fintech

LEYES APLICABLES:
- Ley N°21.521 (Ley Fintech)
- Ley N°19.496 (Protección al Consumidor)
- Ley N°20.555 (SERNAC Financiero)

PLAZO DE PRESCRIPCIÓN:
- 5 años para acciones cambiarias (Código de Comercio)

REGLAS DE ORO:
1. No mezcles con leyes laborales o de tránsito.
2. Mantén el foco en servicios financieros.
"""
    return ""


def _generate_template(state: PSEOState, niche: str = "generic", framework: dict = None) -> str:
    niche_secret = state.get("niche_secret", "")
    client_domain = state["client_domain"]
    gaps = state.get("semantic_gaps", [])
    legal_restrictions = _build_legal_restrictions(niche, framework or {})

    prompt = f"""Eres un experto en diseño de landing pages de conversión para el mercado chileno.

Cliente: {client_domain}
Secreto de nicho identificado: {niche_secret}
Brechas a atacar: {', '.join(gaps[:3])}
{legal_restrictions}

Crea un template HTML completo para páginas pSEO con estas características:
- Diseño profesional y moderno
- Variables de reemplazo literales: {{KEYWORD}}, {{SLUG}}, {{H1_TITLE}}, {{META_DESCRIPTION}}, {{CTA_TEXT}}, {{BENEFIT_1}}, {{BENEFIT_2}}, {{BENEFIT_3}}
- CTA principal con WhatsApp: https://wa.me/56XXXXXXXXX
- Schema.org FinancialService (si aplica) o LegalService (si es TAG)
- Mobile-first responsive
- Sin dependencias externas (CSS inline)

Devuelve SOLO el HTML completo, sin explicaciones ni backticks."""

    return generate_content(prompt)


def _generate_variations(state: PSEOState, keywords: list, template: str, niche: str = "generic", framework: dict = None) -> list:
    client_domain = state["client_domain"]
    niche_secret = state.get("niche_secret", "")
    legal_restrictions = _build_legal_restrictions(niche, framework or {})
    variations = []

    prompt = f"""Eres un experto en SEO programático y copywriting para el mercado chileno.

Cliente: {client_domain}
Contexto del nicho: {niche_secret}
{legal_restrictions}

Para cada keyword de la lista, genera los campos para una landing page pSEO.
Devuelve un array JSON con exactamente este formato (sin markdown, sin backticks):

[
  {{
    "keyword": "la keyword exacta",
    "slug": "slug-url-amigable",
    "h1_title": "Título H1 optimizado con la keyword (máx 60 chars)",
    "meta_description": "Meta description persuasiva con keyword y CTA (máx 155 chars)",
    "cta_text": "Texto del botón CTA específico para esta keyword",
    "benefit_1": "Beneficio 1 relevante para esta keyword",
    "benefit_2": "Beneficio 2 relevante para esta keyword",
    "benefit_3": "Beneficio 3 relevante para esta keyword"
  }}
]

Keywords a procesar:
{json.dumps(keywords, ensure_ascii=False, indent=2)}

Devuelve SOLO el JSON array. Sin markdown, sin backticks, sin explicaciones."""

    try:
        raw = generate_content(prompt).strip()
        if "```" in raw:
            parts = raw.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("["):
                    raw = part
                    break

        page_data_list = json.loads(raw.strip())

        for page_data in page_data_list:
            html = template
            for key, placeholder in [
                ("keyword", "{KEYWORD}"),
                ("slug", "{SLUG}"),
                ("h1_title", "{H1_TITLE}"),
                ("meta_description", "{META_DESCRIPTION}"),
                ("cta_text", "{CTA_TEXT}"),
                ("benefit_1", "{BENEFIT_1}"),
                ("benefit_2", "{BENEFIT_2}"),
                ("benefit_3", "{BENEFIT_3}"),
            ]:
                html = html.replace(placeholder, page_data.get(key, ""))

            variations.append({
                "slug": page_data.get("slug", ""),
                "keyword": page_data.get("keyword", ""),
                "meta_title": page_data.get("h1_title", ""),
                "meta_description": page_data.get("meta_description", ""),
                "html_content": html,
                "filename": f"{page_data.get('slug', 'page')}.html"
            })

    except Exception as e:
        print(f"  [FAIL] Error generando variaciones: {e}")
        for kw in keywords:
            slug = re.sub(r'[^a-z0-9]+', '-', kw.lower()).strip('-')
            variations.append({
                "slug": slug,
                "keyword": kw,
                "meta_title": f"{kw} — {client_domain}",
                "meta_description": f"Servicio de {kw} en {client_domain}. Consulta sin costo.",
                "html_content": template.replace("{KEYWORD}", kw).replace("{SLUG}", slug),
                "filename": f"{slug}.html"
            })

    return variations
