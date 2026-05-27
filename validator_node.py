"""
validator_node.py — Nodo E: Validación de Consistencia Legal y Semántica
Se ejecuta DESPUÉS del Escritor y ANTES del Publicador.
Detecta:
  1. Contradicciones de plazos (ej: "2 años" vs "3 años")
  2. Contradicciones de tribunales (ej: "Policía Local" vs "Letras en lo Civil")
  3. Mezcla de dominios legales (ej: "AFP" + "TAG" en misma página)
  4. Alucinaciones legales (leyes que no corresponden al nicho)
"""

import re
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import PSEOState

# ── GLOSARIO LEGAL FORZADO (Ground Truth) ─────────────────────────────────────
# Este diccionario define los hechos legales VERDADEROS para cada nicho.
# Se inyecta en los prompts y se usa como referencia en validación.
LEGAL_FRAMEWORKS = {
    "tag": {
        "nombre": "Deuda TAG (Tránsito)",
        "leyes_aplicables": [
            "Decreto con Fuerza de Ley N°1 de 2007 (Ley de Tránsito)",
            "Ley N°18.290 (Ley de Tránsito)"
        ],
        "leyes_prohibidas": [
            "Código del Trabajo",
            "Ley 17.322",
            "AFP",
            "cotizaciones previsionales",
            "despido",
            "Art. 162 Código del Trabajo",
            "Art. 58 Código del Trabajo",
            "Art. 19 Ley 17.322"
        ],
        "tribunal_correcto": "Juzgado de Policía Local",
        "tribunal_ejecutivo": "Juzgado de Letras en lo Civil (solo para demanda ejecutiva, no para el ciudadano común)",
        "plazo_prescripcion": "2 años (Art. 24 DFL 1 de 2007)",
        "plazo_alternativo_prohibido": "3 años",
        "temas_prohibidos": ["AFP", "cotizaciones", "previsional", "despido", "indemnización", "finiquito"]
    },
    "fintech": {
        "nombre": "Servicios Financieros / Fintech",
        "leyes_aplicables": [
            "Ley N°21.521 (Ley Fintech)",
            "Ley N°19.496 (Protección al Consumidor)",
            "Ley N°20.555 (SERNAC Financiero)"
        ],
        "leyes_prohibidas": [],
        "tribunal_correcto": "No aplica (servicio financiero privado)",
        "plazo_prescripcion": "5 años para acciones cambiarias (Código de Comercio)",
        "temas_prohibidos": []
    }
}

# Palabras clave para detectar automáticamente el nicho
NICHE_KEYWORDS = {
    "tag": ["tag", "deuda tag", "multa tag", "partes tag", "prescripción tag", "tacógrafo"],
    "fintech": ["cupo", "dólar", "fintech", "transferencia", "pesos", "divisa", "remesa"]
}


def detect_niche(state: PSEOState) -> str:
    """Detecta automáticamente el nicho basado en keywords y contexto."""
    niche_ctx = (state.get("niche_context") or "").lower()
    niche_secret = (state.get("niche_secret") or "").lower()
    keywords = " ".join(state.get("target_keywords", []) or []).lower()
    clean_text = (state.get("clean_text", "") or "").lower()[:3000]
    
    combined = f"{niche_ctx} {niche_secret} {keywords} {clean_text}"
    
    # Detectar TAG
    for kw in NICHE_KEYWORDS["tag"]:
        if kw in combined:
            return "tag"
    
    # Detectar fintech
    for kw in NICHE_KEYWORDS["fintech"]:
        if kw in combined:
            return "fintech"
    
    return "generic"


def get_legal_framework(niche: str) -> dict:
    """Retorna el framework legal para el nicho detectado."""
    return LEGAL_FRAMEWORKS.get(niche, {
        "nombre": "Genérico",
        "leyes_aplicables": [],
        "leyes_prohibidas": [],
        "tribunal_correcto": "",
        "plazo_prescripcion": "",
        "temas_prohibidos": []
    })


def validator_node(state: PSEOState) -> PSEOState:
    """
    Nodo E: Valida la consistencia legal y semántica de las páginas generadas.
    Se ejecuta después del Writer y antes del Publisher.
    """
    print(f"\n[Nodo E — Validador] Verificando consistencia legal...")
    
    variations = state.get("page_variations", [])
    if not variations:
        state["errors"].append("Validador: no hay páginas para validar")
        return state
    
    # Detectar nicho automáticamente
    niche = detect_niche(state)
    framework = get_legal_framework(niche)
    print(f"  Nicho detectado: {niche} ({framework['nombre']})")
    
    issues = []
    pages_clean = []
    pages_rejected = 0
    
    for i, page in enumerate(variations):
        html = page.get("html_content", "")
        keyword = page.get("keyword", "")
        slug = page.get("slug", "")
        page_issues = []
        
        # ── Verificación 1: Leyes prohibidas ────────────────────────────────
        for ley in framework.get("leyes_prohibidas", []):
            if ley.lower() in html.lower():
                page_issues.append(f"Contiene referencia prohibida: '{ley}'")
        
        # ── Verificación 2: Temas prohibidos ────────────────────────────────
        for tema in framework.get("temas_prohibidos", []):
            if tema.lower() in html.lower():
                page_issues.append(f"Contiene tema prohibido: '{tema}'")
        
        # ── Verificación 3: Tribunal incorrecto ─────────────────────────────
        if niche == "tag":
            # Si menciona "Letras en lo Civil" sin aclarar el contexto ejecutivo
            if "letras en lo civil" in html.lower() and "demanda ejecutiva" not in html.lower():
                page_issues.append("Menciona 'Juzgado de Letras en lo Civil' sin aclarar que es solo para demanda ejecutiva")
            # Si NO menciona "Policía Local" cuando debería
            if "policía local" not in html.lower() and "juzgado" in html.lower():
                page_issues.append("Menciona tribunales pero no especifica 'Juzgado de Policía Local'")
        
        # ── Verificación 4: Plazos contradictorios ──────────────────────────
        if niche == "tag":
            plazos_encontrados = set()
            for match in re.finditer(r'(\d+)\s*años?', html.lower()):
                plazos_encontrados.add(match.group(1))
            if len(plazos_encontrados) > 1:
                page_issues.append(f"Plazos contradictorios detectados: {', '.join(sorted(plazos_encontrados))} años")
            elif "3" in plazos_encontrados:
                page_issues.append("Menciona plazo de 3 años (debería ser 2 años para TAG)")
        
        # ── Verificación 5: Alucinaciones de leyes ──────────────────────────
        leyes_chilenas_conocidas = [
            "código del trabajo", "ley 17.322", "ley 18.290", "ley 19.496",
            "ley 20.555", "ley 21.521", "dfl 1", "ley de tránsito",
            "código de comercio", "código civil", "ley 19.300"
        ]
        leyes_mencionadas = []
        for ley in leyes_chilenas_conocidas:
            if ley in html.lower():
                leyes_mencionadas.append(ley)
        
        # Verificar que las leyes mencionadas estén en las permitidas
        leyes_permitidas = [l.lower() for l in framework.get("leyes_aplicables", [])]
        for ley_mencionada in leyes_mencionadas:
            if leyes_permitidas and not any(perm in ley_mencionada for perm in leyes_permitidas):
                # Solo marcar si hay leyes permitidas definidas y esta no está
                if framework["leyes_aplicables"]:
                    page_issues.append(f"Ley posiblemente incorrecta para el nicho: '{ley_mencionada}'")
        
        # ── Reportar issues de esta página ──────────────────────────────────
        if page_issues:
            print(f"  [!] [{slug}] {len(page_issues)} issue(s):")
            for issue in page_issues:
                print(f"      - {issue}")
            issues.append({
                "slug": slug,
                "keyword": keyword,
                "issues": page_issues
            })
            pages_rejected += 1
        else:
            pages_clean.append(page)
    
    # ── Verificación entre páginas (consistencia global) ────────────────────
    global_issues = _check_global_consistency(variations, niche, framework)
    issues.extend(global_issues)
    
    # ── Resultado final ─────────────────────────────────────────────────────
    if issues:
        print(f"\n  [!] {len(issues)} issue(s) de validación encontrados")
        print(f"  [!] {pages_rejected} página(s) con problemas")
        
        # Si hay páginas limpias, publicar solo esas
        if pages_clean:
            state["page_variations"] = pages_clean
            state["pages_generated"] = len(pages_clean)
            print(f"  → Publicando solo {len(pages_clean)} página(s) válida(s)")
        else:
            print(f"  → 0 páginas válidas. No se publicará nada.")
            state["errors"].append("Validador: todas las páginas fueron rechazadas por inconsistencias")
    else:
        print(f"  [OK] Todas las páginas pasaron la validación ({len(variations)} páginas)")
    
    # Guardar issues en el state para trazabilidad
    state["validation_issues"] = issues
    state["current_node"] = "validator_done"
    
    return state


def _check_global_consistency(variations: list, niche: str, framework: dict) -> list:
    """Verifica consistencia entre todas las páginas generadas."""
    global_issues = []
    
    if not variations:
        return global_issues
    
    # Verificar que todas las páginas mencionen el mismo tribunal
    if niche == "tag":
        tribunales_mencionados = set()
        for page in variations:
            html = page.get("html_content", "").lower()
            if "policía local" in html:
                tribunales_mencionados.add("policia_local")
            if "letras en lo civil" in html:
                tribunales_mencionados.add("letras_civil")
        
        if len(tribunales_mencionados) > 1:
            global_issues.append({
                "slug": "__global__",
                "keyword": "CONSISTENCIA GLOBAL",
                "issues": [f"Tribunales inconsistentes entre páginas: {', '.join(tribunales_mencionados)}"]
            })
    
    # Verificar plazos globales
    if niche == "tag":
        todos_plazos = set()
        for page in variations:
            html = page.get("html_content", "").lower()
            for match in re.finditer(r'(\d+)\s*años?', html):
                todos_plazos.add(match.group(1))
        if len(todos_plazos) > 1:
            global_issues.append({
                "slug": "__global__",
                "keyword": "CONSISTENCIA GLOBAL",
                "issues": [f"Plazos de prescripción inconsistentes entre páginas: {', '.join(sorted(todos_plazos))} años"]
            })
    
    return global_issues
