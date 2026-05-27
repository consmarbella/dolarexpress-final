"""
state.py — El "cerebro compartido" del grafo pSEO
Todos los nodos leen y escriben aquí. Es el único lugar de verdad.
"""

from typing import TypedDict, Optional, List, Dict, Any


class PSEOState(TypedDict):
    # ── INPUT ──────────────────────────────────────────────────────────────
    target_url: str                      # URL del competidor a analizar
    client_domain: str                   # Dominio del cliente (ej: dolarexpress.cl)
    niche_context: str                   # Contexto adicional (ej: "cupo dólar fintech")

    # ── SCRAPER (Nodo A) ───────────────────────────────────────────────────
    raw_html: Optional[str]              # HTML crudo descargado
    meta_tags: Optional[Dict]            # Title, description, OG, schema
    heading_structure: Optional[Dict]    # H1-H6 jerárquico
    clean_text: Optional[str]            # Texto sin ruido (señal pura)
    internal_links: Optional[List]       # Links internos con anchor text
    scrape_attempts: int                 # Contador para retry logic
    scrape_success: bool                 # Flag de éxito

    # ── ANALISTA (Nodo B) ──────────────────────────────────────────────────
    keyword_analysis: Optional[Dict]     # Unigramas, bigramas, trigramas
    transactional_patterns: Optional[Dict]  # CTAs, bancos, precios
    niche_secret: Optional[str]          # El "secreto" encontrado por IA
    semantic_gaps: Optional[List[str]]   # Brechas de autoridad detectadas
    target_keywords: Optional[List[str]] # Keywords objetivo para pSEO

    # ── ESCRITOR (Nodo C) ──────────────────────────────────────────────────
    page_template: Optional[str]         # Template HTML base generado
    page_variations: Optional[List[Dict]] # Lista de variaciones [{slug, title, content}]
    pages_generated: int                 # Contador de páginas creadas

    # ── PUBLICADOR (Nodo D) ────────────────────────────────────────────────
    pages_published: Optional[List[str]] # URLs publicadas exitosamente
    github_commit_sha: Optional[str]     # SHA del commit en GitHub/Vercel
    publish_success: bool

    # ── VALIDADOR (Nodo E) ─────────────────────────────────────────────────
    validation_issues: Optional[List[Dict]]  # Issues encontrados por el validador
    detected_niche: Optional[str]            # Nicho detectado (tag, fintech, generic)
    legal_framework: Optional[Dict]          # Framework legal aplicado

    # ── CONTROL DE FLUJO ───────────────────────────────────────────────────
    current_node: str                    # Nodo actual (para logging)
    errors: List[str]                    # Errores acumulados
    completed: bool                      # ¿Terminó el pipeline?


def initial_state(target_url: str, client_domain: str, niche_context: str = "") -> PSEOState:
    """Crea el estado inicial limpio para un nuevo análisis."""
    return PSEOState(
        target_url=target_url,
        client_domain=client_domain,
        niche_context=niche_context,
        raw_html=None,
        meta_tags=None,
        heading_structure=None,
        clean_text=None,
        internal_links=None,
        scrape_attempts=0,
        scrape_success=False,
        keyword_analysis=None,
        transactional_patterns=None,
        niche_secret=None,
        semantic_gaps=None,
        target_keywords=None,
        page_template=None,
        page_variations=None,
        pages_generated=0,
        pages_published=None,
        github_commit_sha=None,
        publish_success=False,
        validation_issues=None,
        detected_niche=None,
        legal_framework=None,
        current_node="start",
        errors=[],
        completed=False,
    )
