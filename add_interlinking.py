import os
import re
from pathlib import Path

# Carpeta raíz del proyecto
ROOT = r"C:\Users\matte\dolarexpress-final"

# Recolectar todas las páginas HTML y sus URLs
pages = []
for path in Path(ROOT).rglob("*.html"):
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if parts[0] == "public":
        url = "https://dolarexpress.cl/" + "/".join(parts[1:]).replace(".html", "") + "/"
    else:
        name = parts[0].replace(".html", "")
        url = "https://dolarexpress.cl/" + name + "/" if name != "index" else "https://dolarexpress.cl/"
    pages.append({"path": str(path), "url": url, "name": path.stem})

print(f"Total páginas encontradas: {len(pages)}")

# Generar bloque de links relacionados
def get_related(current_name, all_pages, max_links=5):
    related = []
    words = set(re.split(r'[-_]', current_name))
    scored = []
    for p in all_pages:
        if p["name"] == current_name:
            continue
        other_words = set(re.split(r'[-_]', p["name"]))
        score = len(words & other_words)
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored[:max_links]]

def make_title(name):
    return name.replace("-", " ").replace("_", " ").title()

# Agregar interlinking a cada página
modified = 0
for page in pages:
    with open(page["path"], "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Saltar si ya tiene sección de interlinking
    if 'id="interlinking-seo"' in content:
        continue

    related = get_related(page["name"], pages)
    if not related:
        continue

    links_html = "\n".join([
        f'        <a href="{r["url"]}">{make_title(r["name"])}</a>'
        for r in related
    ])

    interlinking_block = f"""
<!-- Interlinking SEO -->
<div id="interlinking-seo" style="margin:2rem 0;padding:1rem;border-top:1px solid #eee;">
  <p><strong>Artículos relacionados:</strong></p>
  <nav>
{links_html}
  </nav>
</div>
"""

    # Insertar antes del </body>
    if "</body>" in content:
        content = content.replace("</body>", interlinking_block + "</body>")
        with open(page["path"], "w", encoding="utf-8") as f:
            f.write(content)
        modified += 1

print(f"Páginas modificadas con interlinking: {modified}")
print("Listo. Ahora corre: git add -A && git commit -m 'Add interlinking' && git push")
