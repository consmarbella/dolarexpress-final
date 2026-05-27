"""
agents/publisher_node.py — Nodo D: Publicación de Páginas
Guarda los HTMLs localmente y opcionalmente hace push a GitHub (→ Vercel auto-deploy).
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from state import PSEOState

# Directorio de salida local
OUTPUT_DIR = Path("output")


def publisher_node(state: PSEOState) -> PSEOState:
    """
    Nodo D: Publica las páginas generadas.
    Modo 1 (default): Guarda localmente en /output
    Modo 2 (opcional): Commit + push a GitHub → Vercel auto-deploy
    """
    print(f"\n[Nodo D — Publicador] Publicando {state.get('pages_generated', 0)} páginas...")

    variations = state.get("page_variations", [])
    if not variations:
        state["errors"].append("Publicador: no hay páginas para publicar")
        return state

    OUTPUT_DIR.mkdir(exist_ok=True)
    published_files = []

    try:
        # ── Guardar cada página HTML ───────────────────────────────────────
        for page in variations:
            filename = page.get("filename", f"{page.get('slug', 'page')}.html")
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page["html_content"])

            published_files.append(str(filepath))
            print(f"  ✓ Guardado: {filepath}")

        # ── Generar index de páginas (para sitemap/navegación) ─────────────
        _generate_index(variations, state)
        _generate_sitemap(variations, state)
        _generate_report(state, published_files)

        state["pages_published"] = published_files
        state["publish_success"] = True
        state["current_node"] = "publisher_done"

        print(f"\n  ✓ {len(published_files)} páginas guardadas en /output")
        print(f"  ✓ Sitemap generado: output/sitemap.xml")
        print(f"  ✓ Reporte: output/reporte_pseo.json")

        # ── Opcional: Git push para Vercel auto-deploy ─────────────────────
        use_git = os.getenv("PSEO_AUTO_DEPLOY", "false").lower() == "true"
        if use_git:
            sha = _git_push(state)
            if sha:
                state["github_commit_sha"] = sha
                print(f"  ✓ Commit: {sha[:8]} → Vercel deploy en progreso")

    except Exception as e:
        state["errors"].append(f"Publicador error: {str(e)}")
        print(f"  ✗ Error: {e}")

    return state


def _generate_index(variations: list, state: PSEOState) -> None:
    """Genera página índice con todas las landing pages."""
    client_domain = state["client_domain"]
    links = "\n".join([
        f'  <li><a href="{p["slug"]}.html">{p["meta_title"]}</a> '
        f'<small>({p["keyword"]})</small></li>'
        for p in variations
    ])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex">
<title>Index pSEO — {client_domain}</title>
<style>body{{font-family:sans-serif;max-width:800px;margin:2rem auto;padding:1rem}}li{{margin:.5rem 0}}small{{color:#888}}</style>
</head>
<body>
<h1>Páginas pSEO generadas — {client_domain}</h1>
<p>Total: {len(variations)} páginas | Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<ul>
{links}
</ul>
</body>
</html>"""

    with open(OUTPUT_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(html)


def _generate_sitemap(variations: list, state: PSEOState) -> None:
    """Genera sitemap XML para las páginas generadas."""
    client_domain = state["client_domain"]
    if not client_domain.startswith("http"):
        base_url = f"https://{client_domain}"
    else:
        base_url = client_domain

    today = datetime.now().strftime('%Y-%m-%d')
    urls = "\n".join([
        f"""  <url>
    <loc>{base_url}/{p['slug']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
        for p in variations
    ])

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""

    with open(OUTPUT_DIR / "sitemap.xml", 'w', encoding='utf-8') as f:
        f.write(sitemap)


def _generate_report(state: PSEOState, published_files: list) -> None:
    """Genera reporte JSON del pipeline completo."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "target_url": state["target_url"],
        "client_domain": state["client_domain"],
        "pages_generated": state.get("pages_generated", 0),
        "niche_secret": state.get("niche_secret", ""),
        "semantic_gaps": state.get("semantic_gaps", []),
        "target_keywords": state.get("target_keywords", []),
        "published_files": published_files,
        "errors": state.get("errors", []),
        "meta_tags_found": state.get("meta_tags", {}),
        "keyword_top10": dict(list(state.get("keyword_analysis", {}).get("unigrams", {}).items())[:10])
    }

    with open(OUTPUT_DIR / "reporte_pseo.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def _git_push(state: PSEOState) -> str:
    """Hace commit y push de las páginas generadas (requiere repo git configurado)."""
    try:
        subprocess.run(["git", "add", "output/"], check=True, capture_output=True)
        msg = f"pSEO: {state.get('pages_generated', 0)} páginas para {state['client_domain']}"
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        subprocess.run(["git", "push"], check=True, capture_output=True)

        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Git error: {e}")
        return ""
