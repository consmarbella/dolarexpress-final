"""
graph.py — Motor de Orquestación LangGraph
El cerebro del pipeline pSEO. Define nodos, edges y lógica de retry.

Flujo:
  START → Scraper → [retry si falla] → Analista → Escritor → Validador → Publicador → END
"""

from langgraph.graph import StateGraph, END
from state import PSEOState, initial_state
from scraper_node import scraper_node
from analyst_node import analyst_node
from writer_node import writer_node
from publisher_node import publisher_node
from validator_node import validator_node


# ── FUNCIONES DE ROUTING (edges condicionales) ─────────────────────────────────

def route_after_scraper(state: PSEOState) -> str:
    """
    Si el scraper falló y no superó el máximo de intentos → vuelve al scraper.
    Si falló y agotó intentos → termina con error.
    Si tuvo éxito → continúa al analista.
    """
    if state["scrape_success"]:
        return "analyst"
    elif state["scrape_attempts"] < 3:
        print(f"  → Reintentando scraper (intento {state['scrape_attempts'] + 1}/3)...")
        return "scraper"  # Retry automático
    else:
        print("  → Máximo de reintentos alcanzado. Terminando pipeline.")
        return "end_with_error"


def route_after_analyst(state: PSEOState) -> str:
    """Si el análisis produjo keywords → generar páginas. Si no → terminar."""
    if state.get("target_keywords") and len(state["target_keywords"]) > 0:
        return "writer"
    else:
        print("  → Sin keywords identificadas. Revisá el niche_context.")
        return "end_with_error"


def route_after_writer(state: PSEOState) -> str:
    """Si hay páginas generadas → pasar al validador. Si no → terminar."""
    if state.get("page_variations") and len(state["page_variations"]) > 0:
        return "validator"
    else:
        return "end_with_error"


def route_after_validator(state: PSEOState) -> str:
    """
    Si hay páginas válidas después de la validación → publicar.
    Si todas fueron rechazadas → terminar con error.
    """
    if state.get("page_variations") and len(state["page_variations"]) > 0:
        print(f"  → {len(state['page_variations'])} página(s) válidas → Publicando")
        return "publisher"
    else:
        print("  → 0 páginas válidas después de validación. Terminando.")
        return "end_with_error"


def end_with_error_node(state: PSEOState) -> PSEOState:
    """Nodo terminal de error — registra el estado final."""
    state["completed"] = True
    print(f"\n[!] Pipeline terminado con errores:")
    for err in state.get("errors", []):
        print(f"    - {err}")
    return state


def end_success_node(state: PSEOState) -> PSEOState:
    """Nodo terminal de éxito — imprime resumen."""
    state["completed"] = True
    print(f"\n{'='*60}")
    print(f"  ✓ PIPELINE COMPLETADO")
    print(f"{'='*60}")
    print(f"  URL analizada:    {state['target_url']}")
    print(f"  Cliente:          {state['client_domain']}")
    print(f"  Nicho detectado:  {state.get('detected_niche', 'N/D')}")
    print(f"  Páginas creadas:  {state.get('pages_generated', 0)}")
    print(f"  Issues validación:{len(state.get('validation_issues', []))}")
    print(f"  Secreto de nicho: {state.get('niche_secret', '')[:80]}...")
    print(f"  Keywords:         {len(state.get('target_keywords', []))}")
    print(f"  Errores:          {len(state.get('errors', []))}")
    print(f"{'='*60}")
    return state


# ── CONSTRUCCIÓN DEL GRAFO ─────────────────────────────────────────────────────

def build_pseo_graph() -> StateGraph:
    """Construye y compila el grafo del pipeline pSEO."""
    
    graph = StateGraph(PSEOState)

    # Registrar nodos
    graph.add_node("scraper", scraper_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)
    graph.add_node("validator", validator_node)
    graph.add_node("publisher", publisher_node)
    graph.add_node("end_success", end_success_node)
    graph.add_node("end_with_error", end_with_error_node)

    # Punto de entrada
    graph.set_entry_point("scraper")

    # Edges condicionales (la lógica de routing)
    graph.add_conditional_edges(
        "scraper",
        route_after_scraper,
        {
            "scraper": "scraper",        # Retry
            "analyst": "analyst",        # Continuar
            "end_with_error": "end_with_error"  # Fallo total
        }
    )

    graph.add_conditional_edges(
        "analyst",
        route_after_analyst,
        {
            "writer": "writer",
            "end_with_error": "end_with_error"
        }
    )

    graph.add_conditional_edges(
        "writer",
        route_after_writer,
        {
            "validator": "validator",
            "end_with_error": "end_with_error"
        }
    )

    graph.add_conditional_edges(
        "validator",
        route_after_validator,
        {
            "publisher": "publisher",
            "end_with_error": "end_with_error"
        }
    )

    # Edge final (siempre termina bien si publisher completa)
    graph.add_edge("publisher", "end_success")
    graph.add_edge("end_success", END)
    graph.add_edge("end_with_error", END)

    return graph.compile()


# ── FUNCIÓN DE EJECUCIÓN ÚNICA ─────────────────────────────────────────────────

def run_pseo_pipeline(target_url: str, client_domain: str, niche_context: str = "") -> PSEOState:
    """
    Ejecuta el pipeline pSEO completo para una URL.
    
    Args:
        target_url: URL del competidor a analizar
        client_domain: Tu dominio (ej: dolarexpress.cl)
        niche_context: Contexto adicional (ej: "fintech cupo dólar Chile")
    
    Returns:
        PSEOState con todos los resultados
    """
    graph = build_pseo_graph()
    state = initial_state(target_url, client_domain, niche_context)

    print(f"\n{'='*60}")
    print(f"  PSEO PIPELINE — LangGraph")
    print(f"{'='*60}")
    print(f"  Target:  {target_url}")
    print(f"  Cliente: {client_domain}")

    final_state = graph.invoke(state)
    return final_state
