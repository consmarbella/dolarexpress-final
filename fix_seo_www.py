#!/usr/bin/env python3
"""
Fix all SEO issues at once:
1. Replace www.dolarexpress.cl -> dolarexpress.cl in ALL HTML files
2. Fix canonical URLs to match actual .html URLs (not trailing slash)
3. Remove noindex from recursos.html
4. Regenerate sitemap.xml pointing to correct canonical URLs
"""
import os, re, glob
from datetime import date

public_dir = "public"

# Collect all HTML files
all_files = []
for root, dirs, files in os.walk(public_dir):
    for f in files:
        if f.endswith('.html'):
            all_files.append(os.path.join(root, f))

print(f"Processing {len(all_files)} HTML files...")
count_www_replacements = 0
count_canonical_fixed = 0
count_interlinking_pages = 0

for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    filename = os.path.basename(filepath)
    
    # 1. Replace ALL www.dolarexpress.cl -> dolarexpress.cl
    www_count = content.count('www.dolarexpress.cl')
    if www_count > 0:
        content = content.replace('www.dolarexpress.cl', 'dolarexpress.cl')
        count_www_replacements += www_count
        count_interlinking_pages += 1
    
    # 2. Fix canonical: remove www, remove trailing slash, ensure .html matches file
    def fix_canonical_url(full_url):
        """Fix a canonical URL to match actual file."""
        url = full_url
        # Remove www
        url = url.replace('www.dolarexpress.cl', 'dolarexpress.cl')
        # Remove trailing slash
        url = url.rstrip('/')
        # Extract last part
        parts = url.split('/')
        last = parts[-1]
        # If it doesn't end in .html, add it (match the actual HTML file naming)
        if not last.endswith('.html') and last != 'dolarexpress.cl':
            url = url + '.html'
        return url
    
    # Pattern 1: rel="canonical" href="..."
    pattern1 = r'(<link\s+rel=["\']canonical["\']\s+href=["\'])([^"\']+)(["\'])'
    def repl1(m):
        global count_canonical_fixed
        count_canonical_fixed += 1
        return m.group(1) + fix_canonical_url(m.group(2)) + m.group(3)
    content = re.sub(pattern1, repl1, content)
    
    # Pattern 2: href="..." rel="canonical"
    pattern2 = r'(<link\s+href=["\'])([^"\']+)(["\']\s+rel=["\']canonical["\'])'
    def repl2(m):
        global count_canonical_fixed
        count_canonical_fixed += 1
        return m.group(1) + fix_canonical_url(m.group(2)) + m.group(3)
    content = re.sub(pattern2, repl2, content)
    
    # 3. Replace noindex with index in meta robots tags
    if 'noindex' in content.lower():
        # Pattern: name="robots" content="noindex, follow" or similar
        content = re.sub(
            r'(<meta\s+name=["\']robots["\']\s+content=["\'])noindex([^"\']*["\'])',
            r'\1index\2',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'(<meta\s+content=["\'])noindex([^"\']*["\']\s+name=["\']robots["\'])',
            r'\1index\2',
            content,
            flags=re.IGNORECASE
        )
    
    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"\nReplacements summary:")
print(f"  - www.dolarexpress.cl -> dolarexpress.cl: {count_www_replacements} occurrences in {count_interlinking_pages} pages")
print(f"  - Canonical URLs fixed: {count_canonical_fixed}")

# 4. Regenerate sitemap.xml
print("\nRegenerating sitemap.xml...")
today = date.today().isoformat()

all_pages = []
for root, dirs, files in os.walk(public_dir):
    for f in files:
        if f.endswith('.html') and f != 'recursos.html':
            rel_dir = os.path.relpath(root, public_dir)
            if rel_dir == '.':
                all_pages.append(f)
            else:
                all_pages.append(f"{rel_dir}/{f}")

high_priority = ["index.html", "venta-usd.html", "contacto.html", "cupo-dolar-a-pesos.html"]

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for page in sorted(set(all_pages)):
    if page == "index.html":
        url_path = ""
    else:
        url_path = page
    
    prio = "1.0" if page in high_priority else ("0.9" if page.split('/')[-1] in high_priority else "0.7")
    freq = "weekly" if prio in ("1.0", "0.9") else "monthly"
    
    lines.append(f"  <url>")
    lines.append(f"    <loc>https://dolarexpress.cl/{url_path}</loc>")
    lines.append(f"    <lastmod>{today}</lastmod>")
    lines.append(f"    <changefreq>{freq}</changefreq>")
    lines.append(f"    <priority>{prio}</priority>")
    lines.append(f"  </url>")

lines.append('</urlset>')

with open(os.path.join(public_dir, "sitemap.xml"), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

sm_count = len([l for l in lines if '<loc>' in l])
print(f"  - Sitemap regenerated: {sm_count} URLs")
print(f"\n[DONE] All SEO fixes applied!")