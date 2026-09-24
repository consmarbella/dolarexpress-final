#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agrega interlinking SEO a todas las paginas HTML estaticas en public/
Basado en palabras clave compartidas entre nombres de archivo.
"""
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent / "public"

# Recolectar todas las paginas HTML
pages = []
for path in sorted(ROOT.rglob("*.html")):
    rel = path.relative_to(ROOT)
    name = path.stem
    url = f"https://dolarexpress.cl/{name}"
    pages.append({"path": str(path), "url": url, "name": name})

print(f"Total paginas encontradas: {len(pages)}")

def get_related(current_name, all_pages, max_links=6):
    """Encuentra paginas relacionadas por palabras clave compartidas"""
    words = set(re.split(r'[-_]', current_name.lower()))
    scored = []
    for p in all_pages:
        if p["name"] == current_name:
            continue
        other_words = set(re.split(r'[-_]', p["name"].lower()))
        score = len(words & other_words)
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored[:max_links]]

def make_title(name):
    """Convierte slug a titulo legible"""
    return name.replace("-", " ").replace("_", " ").title()

# Agregar interlinking a cada pagina
modified = 0
for page in pages:
    with open(page["path"], "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Saltar si ya tiene seccion de interlinking
    if 'id="interlinking-seo"' in content:
        continue

    related = get_related(page["name"], pages)
    if not related:
        continue

    links_html = "\n".join([
        f'          <a href="{r["url"]}" class="text-[#C8A045] hover:underline text-sm">{make_title(r["name"])}</a>'
        for r in related
    ])

    interlinking_block = f"""
<!-- Interlinking SEO -->
<div id="interlinking-seo" class="mt-12 pt-8 border-t border-gray-300">
  <p class="font-bold text-lg mb-4 text-[#1a1a1a]">Articulos Relacionados</p>
  <nav class="flex flex-wrap gap-x-6 gap-y-2">
{links_html}
  </nav>
</div>
"""

    # Insertar antes del </body>
    if "</body>" in content:
        content = content.replace("</body>", interlinking_block + "\n</body>")
        with open(page["path"], "w", encoding="utf-8") as f:
            f.write(content)
        modified += 1
        print(f"  [+] Interlinking added: {page['name']}.html")

print(f"\nPaginas modificadas con interlinking: {modified}")
print("Listo!")
