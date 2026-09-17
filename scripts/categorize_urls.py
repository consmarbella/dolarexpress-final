import json

with open('scripts/indexed_urls.json') as f:
    urls = json.load(f)

# Pages that actually exist now (19 pages)
live_pages = [
    'https://www.dolarexpress.cl/',
    'https://www.dolarexpress.cl/avance-cupo-dolares',
    'https://www.dolarexpress.cl/vender-cupo-dolar',
    'https://www.dolarexpress.cl/que-es-cupo-dolares',
    'https://www.dolarexpress.cl/cuanto-cupo-vender',
    'https://www.dolarexpress.cl/cupo-dolares-por-banco',
    'https://www.dolarexpress.cl/guia/vender-cupo-dolares',
    'https://www.dolarexpress.cl/preguntas-frecuentes',
    'https://www.dolarexpress.cl/vender-cupo-banco-chile',
    'https://www.dolarexpress.cl/vender-cupo-bci',
    'https://www.dolarexpress.cl/vender-cupo-santander',
    'https://www.dolarexpress.cl/vender-cupo-scotiabank',
    'https://www.dolarexpress.cl/vender-cupo-itau',
    'https://www.dolarexpress.cl/vender-cupo-cmr-falabella',
    'https://www.dolarexpress.cl/vender-cupo-ripley-rapido',
    'https://www.dolarexpress.cl/vender-cupo-lider-santiago',
    'https://www.dolarexpress.cl/testimonios',
    'https://www.dolarexpress.cl/nosotros',
    'https://www.dolarexpress.cl/contacto',
]

# URLs to REMOVE (dead pages still indexed)
to_remove = []
for url in urls:
    # Normalize
    normalized = url
    if normalized.endswith('/'):
        normalized = normalized[:-1]
    
    # Check if it's a live page
    is_live = False
    for live in live_pages:
        live_norm = live.rstrip('/')
        if normalized == live_norm or url == live:
            is_live = True
            break
    
    if not is_live:
        to_remove.append(url)

# Save removal list
with open('scripts/urls_to_remove.txt', 'w') as f:
    for url in sorted(to_remove):
        f.write(url + '\n')

print(f"TOTAL INDEXED: {len(urls)}")
print(f"LIVE PAGES: {len([u for u in urls if any(u.rstrip('/') == l.rstrip('/') for l in live_pages)])}")
print(f"TO REMOVE: {len(to_remove)}")
print()
print("=== URLs TO REMOVE FROM GOOGLE INDEX ===")
for url in sorted(to_remove):
    print(f"  {url}")
