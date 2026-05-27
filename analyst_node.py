"""
agents/analyst_node.py — Nodo B: Análisis IA de Primeros Principios
Llama a Gemini 1.5 Flash para encontrar el "secreto" del nicho y las brechas de autoridad.
Incluye detección de nicho legal para evitar alucinaciones downstream.
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deepseek_client import generate_content
from state import PSEOState
from validator_node import detect_niche, get_legal_framework


def analyst_node(state: PSEOState) -> PSEOState:
    """
    Nodo B: Aplica Filtro de Primeros Principios a la data extraída.
    Identifica el secreto de nicho, jerarquía semántica y brechas.
    Incluye contexto legal para guiar el análisis.
    """
    print(f"\n[Nodo B — Analista] Analizando {state['target_url']}...")

    if not state.get("scrape_success") or not state.get("clean_text"):
        state["errors"].append("Analista: no hay datos del scraper para analizar")
        return state

    meta = state.get("meta_tags", {})
    headings = state.get("heading_structure", {})
    keywords = state.get("keyword_analysis", {})
    transactional = state.get("transactional_patterns", {})
    niche_ctx = state.get("niche_context", "")

    # Detectar nicho temprano para guiar el análisis
    try:
        niche = detect_niche(state)
        framework = get_legal_framework(niche)
        state["detected_niche"] = niche
        state["legal_framework"] = framework
        print(f"  Nicho detectado: {niche}")
    except Exception as e:
        print(f"  [FAIL] Error detectando nicho: {e}")
        import traceback
        traceback.print_exc()
        niche = "generic"
        framework = get_legal_framework(niche)
        state["detected_niche"] = niche
        state["legal_framework"] = framework

    prompt = _build_analysis_prompt(
        url=state["target_url"],
        client_domain=state["client_domain"],
        meta=meta,
        headings=headings,
        keywords=keywords,
        transactional=transactional,
        clean_text=(state.get("clean_text") or "")[:6000],
        niche_context=niche_ctx,
        niche=niche,
        framework=framework
    )

    # Retry con backoff para manejar errores de API
    import time as _time
    max_retries = 3
    raw_output = None
    for retry in range(max_retries):
        try:
            raw_output = generate_content(prompt)
            break
        except Exception as e:
            if retry < max_retries - 1:
                wait = 10 * (retry + 1)
                print(f"  [RETRY] Error de API, esperando {wait}s (intento {retry+1}/{max_retries})...")
                _time.sleep(wait)
            else:
                raise e
    
    if raw_output is None:
        raise Exception("No se pudo obtener respuesta de DeepSeek después de reintentos")
    
    print(f"  [OK] Analisis recibido: {len(raw_output)} chars")

    try:
        parsed = _parse_analysis(raw_output)
        state["niche_secret"] = parsed.get("niche_secret", "")
        state["semantic_gaps"] = parsed.get("semantic_gaps", [])
        state["target_keywords"] = parsed.get("target_keywords", [])
        state["current_node"] = "analyst_done"

        print(f"  [OK] Keywords objetivo identificadas: {len(state['target_keywords'])}")
        print(f"  [OK] Brechas detectadas: {len(state['semantic_gaps'])}")

    except Exception as e:
        state["errors"].append(f"Analista API error: {str(e)}")
        print(f"  [FAIL] Error en analisis IA: {e}")

    return state


def _build_legal_context(niche: str, framework: dict) -> str:
    """Construye el contexto legal para guiar el análisis."""
    if niche == "tag":
        return f"""
CONTEXTO LEGAL DETECTADO: El nicho es Deuda TAG (Tránsito).
- Marco legal correcto: DFL 1 de 2007 (Ley de Tránsito), Ley 18.290
- NO mezclar con: Código del Trabajo, AFP, cotizaciones previsionales, Ley 17.322
- Tribunal competente: Juzgado de Policía Local (general) / Juzgado de Letras en lo Civil (demanda ejecutiva)
- Plazo de prescripción: 2 años
"""
    elif niche == "fintech":
        return f"""
CONTEXTO LEGAL DETECTADO: El nicho es Servicios Financieros / Fintech.
- Marco legal: Ley 21.521 (Ley Fintech), Ley 19.496 (Protección al Consumidor), Ley 20.555 (SERNAC Financiero)
- No mezclar con leyes laborales o de tránsito.
"""
    return ""


def _build_analysis_prompt(url, client_domain, meta, headings, keywords, transactional, clean_text, niche_context, niche="generic", framework=None) -> str:
    legal_context = _build_legal_context(niche, framework or {})
    
    return f"""Eres un experto en SEO programático y análisis competitivo para mercados chilenos.

CONTEXTO: Estoy construyendo pSEO para {client_domain}.
Extracción realizada con Python (Requests + BeautifulSoup) — datos crudos, sin bias de herramientas comerciales.
{f"Contexto adicional: {niche_context}" if niche_context else ""}
{legal_context}

=== DATA EXTRAÍDA DE: {url} ===

META TAGS:
- Title: {meta.get('title', 'N/D')}
- Description: {meta.get('description', 'N/D')}
- Canonical: {meta.get('canonical', 'N/D')}
- Schema: {', '.join(meta.get('schema_types', [])) or 'ninguno'}

JERARQUÍA SEMÁNTICA:
H1: {' | '.join(headings.get('h1', ['sin H1']))}
H2: {' | '.join(headings.get('h2', [])[:6])}
H3: {' | '.join(headings.get('h3', [])[:6])}

TOP KEYWORDS:
Unigramas: {', '.join([f"{k}({v})" for k,v in list(keywords.get('unigrams', {}).items())[:20]])}
Bigramas: {', '.join([f"{k}({v})" for k,v in list(keywords.get('bigrams', {}).items())[:10]])}
Trigramas: {', '.join([f"{k}({v})" for k,v in list(keywords.get('trigrams', {}).items())[:8]])}

PATRONES TRANSACCIONALES:
CTAs: {', '.join(transactional.get('cta_phrases', []))}
Bancos: {', '.join(transactional.get('bank_mentions', []))}
Servicios: {', '.join(transactional.get('service_patterns', []))}
Urgencia: {', '.join(transactional.get('urgency_triggers', []))}

TEXTO LIMPIO (primeros 6000 chars):
{clean_text}

=== INSTRUCCIÓN ===
Responde EXACTAMENTE en este formato JSON (sin markdown, sin backticks, sin explicaciones):

{{
  "niche_secret": "descripción en 2-3 oraciones del secreto de nicho que usa este sitio",
  "semantic_gaps": [
    "gap 1: tema que tocan superficialmente",
    "gap 2: tema que tocan superficialmente",
    "gap 3: tema que tocan superficialmente",
    "gap 4: tema que tocan superficialmente",
    "gap 5: tema que tocan superficialmente"
  ],
  "target_keywords": [
    "keyword long-tail 1",
    "keyword long-tail 2",
    "keyword long-tail 3",
    "keyword long-tail 4",
    "keyword long-tail 5",
    "keyword long-tail 6",
    "keyword long-tail 7",
    "keyword long-tail 8",
    "keyword long-tail 9",
    "keyword long-tail 10",
    "keyword long-tail 11",
    "keyword long-tail 12",
    "keyword long-tail 13",
    "keyword long-tail 14",
    "keyword long-tail 15"
  ],
  "authority_strategy": "estrategia concreta en 2-3 oraciones para superar este sitio"
}}"""


def _parse_analysis(raw: str) -> dict:
    """Parsea la respuesta JSON de Gemini, tolerante a markdown y errores."""
    try:
        clean = raw.strip()
        # Gemini a veces devuelve ```json ... ```
        if "```" in clean:
            parts = clean.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:]
                part = part.strip()
                if part.startswith("{"):
                    return json.loads(part)
        return json.loads(clean)
    except json.JSONDecodeError:
        return {
            "niche_secret": raw[:500],
            "semantic_gaps": [],
            "target_keywords": [],
            "authority_strategy": ""
        }
