#!/usr/bin/env python3
"""Generate sitemap.xml from all HTML files in /public/"""
import os
from datetime import datetime

PUBLIC = 'public'
BASE_URL = 'https://dolarexpress.cl'
TODAY = datetime.now().strftime('%Y-%m-%d')

# Priority mapping by slug prefix
PRIORITY_MAP = {
    'index': 1.0,
    'venta-usd': 0.9,
    'directorio': 0.8,
    'contacto': 0.7,
    'privacidad': 0.3,
    'terminos': 0.3,
    'prestamo': 0.7,
    'cupo': 0.7,
    'avance': 0.6,
    'credito': 0.6,
    'vender': 0.6,
    'cambiar': 0.6,
    'convertir': 0.5,
    'liquidar': 0.5,
    'pasar': 0.5,
    'transferir': 0.5,
    '404': 0.0,
}

def get_priority(slug):
    for prefix, priority in PRIORITY_MAP.items():
        if slug.startswith(prefix):
            return priority
    return 0.5

# Get all HTML files
html_files = sorted([f for f in os.listdir(PUBLIC) if f.endswith('.html') and f != '404.html'])

# Build sitemap
urls = []
urls.append({
    'loc': BASE_URL + '/',
    'priority': 1.0,
    'changefreq': 'weekly',
})

for html_file in html_files:
    slug = html_file.replace('.html', '')
    loc = BASE_URL + '/' + slug
    priority = get_priority(slug)
    changefreq = 'monthly' if priority >= 0.6 else 'weekly' if priority >= 0.3 else 'yearly'
    urls.append({
        'loc': loc,
        'priority': priority,
        'changefreq': changefreq,
    })

# Generate XML
xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in urls:
    xml += f'''  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']:.1f}</priority>
  </url>
'''

xml += '</urlset>'

with open(f'{PUBLIC}/sitemap.xml', 'w') as f:
    f.write(xml)

print(f'✅ Sitemap generado: {len(urls)} URLs')
print(f'   Total HTML en /public/: {len(html_files)}')
