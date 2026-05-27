#!/usr/bin/env python3
"""Audit all HTML pages for SEO issues."""
import os, re, sys

html_dir = 'public'
pages = sorted([f for f in os.listdir(html_dir) if f.endswith('.html')])
total = len(pages)

www_canonical = []
no_canonical = []
ok_canonical = []
www_interlinking = []
noindex_pages = []
canonical_trailing_slash = []  # ends with /
canonical_html_ext = []  # ends with .html

for page in pages:
    path = os.path.join(html_dir, page)
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        continue

    # Canonical check
    canon_match = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content)
    if not canon_match:
        # Try with single quotes in diff order
        canon_match = re.search(r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', content)
    
    if not canon_match:
        no_canonical.append(page)
    else:
        canon_url = canon_match.group(1)
        if 'www.dolarexpress.cl' in canon_url:
            www_canonical.append((page, canon_url))
        elif canon_url.endswith('/'):
            canonical_trailing_slash.append((page, canon_url))
        elif canon_url.endswith('.html'):
            canonical_html_ext.append((page, canon_url))
        else:
            ok_canonical.append(page)

    # Check for www in all links
    www_links = re.findall(r'href=["\']https?://www\.dolarexpress\.cl[^"\']*["\']', content)
    if www_links:
        www_interlinking.append(page)

    # Noindex check
    if re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', content):
        noindex_pages.append(page)

# Output
lines = []
lines.append(f"TOTAL HTML PAGES: {total}")
lines.append("")
lines.append("=== PROBLEMA #1: CANONICAL CON www ===")
lines.append(f"Pages with www canonical: {len(www_canonical)}")
for p, url in www_canonical[:5]:
    lines.append(f"  {p} -> {url}")
if len(www_canonical) > 5:
    lines.append(f"  ... and {len(www_canonical) - 5} more")
lines.append("")
lines.append("=== CANONICAL: sin canonical ===")
lines.append(f"Pages without any canonical: {len(no_canonical)}")
for p in no_canonical[:5]:
    lines.append(f"  {p}")
lines.append("")
lines.append("=== CANONICAL: trailing slashes ===")
lines.append(f"Pages with / canonical: {len(canonical_trailing_slash)}")
lines.append("")
lines.append("=== CANONICAL: .html extension ===")
lines.append(f"Pages with .html canonical: {len(canonical_html_ext)}")
lines.append("")
lines.append("=== CANONICAL: OK ===")
lines.append(f"Pages OK: {len(ok_canonical)}")
lines.append("")
lines.append("=== PROBLEMA #2: INTERLINKING CON www ===")
lines.append(f"Pages with www links: {len(www_interlinking)}")
lines.append("")
lines.append("=== PROBLEMA #3: NOINDEX ===")
lines.append(f"Pages with noindex: {len(noindex_pages)}")
for p in noindex_pages:
    lines.append(f"  {p}")
lines.append("")
lines.append("=== RESUMEN DE IMPACTO GSC ===")
lines.append(f"")
lines.append(f"El Excel muestra estos problemas en GSC:")
lines.append(f"  - Paginas con redireccion: 761 (por www -> sin www)")
lines.append(f"  - Paginas alternativas con canonica adecuada: 327 (por www canonical)")
lines.append(f"  - No encontrado 404: 41")
lines.append(f"  - Excluida por noindex: 1")
lines.append(f"  - Sin indexar (descubiertas): 134")
lines.append(f"")
lines.append(f"CAUSA RAIZ: Cientos de paginas HTML tienen:")
lines.append(f"  1. canonical apuntando a www.dolarexpress.cl")
lines.append(f"  2. Links internos a www.dolarexpress.cl")
lines.append(f"  3. El dominio principal es dolarexpress.cl (sin www)")
lines.append(f"  4. Esto hace que Google vea redirecciones masivas y duplicados")

output = '\n'.join(lines)
print(output)
with open('SEO_AUDIT_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(output)
print("\n[OK] Report saved to SEO_AUDIT_REPORT.txt")