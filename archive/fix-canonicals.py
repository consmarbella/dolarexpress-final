"""
fix-canonicals.py
Recorre todos los .html de /public/ y corrige:
  1. Quita www  (https://www.dolarexpress.cl/... -> https://dolarexpress.cl/...)
  2. Quita trailing slash en canonical  (/slug/ -> /slug)
  3. Quita .html del canonical si existe  (/slug.html -> /slug)
No toca nada del diseno, solo la linea del <link rel="canonical">.
"""
import os, re, sys

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")

CANONICAL_RE = re.compile(
    r'(<link\s+rel="canonical"\s+href=")([^"]+)("\s*/?>)',
    re.IGNORECASE
)

def fix_canonical_url(url):
    url = url.replace("https://www.dolarexpress.cl", "https://dolarexpress.cl")
    url = url.replace("http://www.dolarexpress.cl", "https://dolarexpress.cl")
    url = url.replace("http://dolarexpress.cl", "https://dolarexpress.cl")
    url = re.sub(r'\.html$', '', url)
    if url != "https://dolarexpress.cl/":
        url = url.rstrip("/")
    return url

fixed = skipped = errors = 0

for root, dirs, files in os.walk(PUBLIC_DIR):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            match = CANONICAL_RE.search(content)
            if not match:
                skipped += 1
                continue
            original_url = match.group(2)
            fixed_url = fix_canonical_url(original_url)
            if original_url == fixed_url:
                skipped += 1
                continue
            new_content = CANONICAL_RE.sub(
                lambda m: m.group(1) + fix_canonical_url(m.group(2)) + m.group(3),
                content
            )
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            rel = os.path.relpath(fpath, PUBLIC_DIR)
            print(f"  FIXED  {rel}  {original_url} -> {fixed_url}")
            fixed += 1
        except Exception as e:
            print(f"  ERROR  {fpath}: {e}", file=sys.stderr)
            errors += 1

print(f"\n{'='*55}")
print(f"  Corregidos : {fixed}")
print(f"  Ya estaban bien : {skipped}")
print(f"  Errores    : {errors}")
print(f"{'='*55}")
