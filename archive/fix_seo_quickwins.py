#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Quick Wins - DolarExpress
Corrige canonical mismatches, agrega og:image, Twitter Cards,
Google Search Console, y meta descriptions faltantes en todas las paginas HTML.
"""

import os
import re
import glob
import sys

# Forzar UTF-8 para prints
sys.stdout.reconfigure(encoding='utf-8')

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
INDEX_HTML = os.path.join(os.path.dirname(__file__), "index.html")

# Estadisticas
stats = {
    "canonical_fixed": 0,
    "og_image_added": 0,
    "twitter_card_added": 0,
    "gsc_added": 0,
    "meta_desc_fixed": 0,
    "files_processed": 0,
}

def fix_canonical_mismatch(content, filepath):
    """Corrige canonical URLs con ./ en la ruta"""
    pattern = r'(<link\s+rel="canonical"\s+href="https://dolarexpress\.cl/)\./'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1', content)
        stats["canonical_fixed"] += 1
        print(f"  [+] Canonical fixed: {os.path.basename(filepath)}")
    return content

def add_og_image(content, filepath):
    """Agrega og:image si no existe"""
    if 'og:image' not in content:
        og_tags = re.findall(r'<meta\s+property="og:[^"]*"[^>]*/>', content)
        if og_tags:
            last_og = og_tags[-1]
            og_image_block = '\n    <meta property="og:image" content="https://dolarexpress.cl/og-image.png" />\n    <meta property="og:image:width" content="1200" />\n    <meta property="og:image:height" content="630" />'
            content = content.replace(last_og, last_og + og_image_block)
            stats["og_image_added"] += 1
            print(f"  [+] og:image added: {os.path.basename(filepath)}")
    return content

def add_twitter_card(content, filepath):
    """Agrega Twitter Card tags si no existen"""
    if 'twitter:card' not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'og:image:height' in line:
                twitter_block = '    <!-- Twitter Card -->\n    <meta name="twitter:card" content="summary_large_image" />\n    <meta name="twitter:title" content="REEMPLAZAR_CON_TITULO" />\n    <meta name="twitter:description" content="REEMPLAZAR_CON_DESCRIPCION" />\n    <meta name="twitter:image" content="https://dolarexpress.cl/og-image.png" />'
                lines.insert(i + 1, twitter_block)
                content = '\n'.join(lines)
                stats["twitter_card_added"] += 1
                print(f"  [+] Twitter Card added: {os.path.basename(filepath)}")
                break
    return content

def add_gsc_verification(content, filepath):
    """Agrega Google Search Console verification si no existe"""
    if 'google-site-verification' not in content:
        if 'msvalidate.01' in content:
            gsc_tag = '    <meta name="google-site-verification" content="REEMPLAZAR_CON_CODIGO_GSC" />'
            content = content.replace(
                '<meta name="msvalidate.01"',
                gsc_tag + '\n    <meta name="msvalidate.01"'
            )
            stats["gsc_added"] += 1
            print(f"  [+] GSC added: {os.path.basename(filepath)}")
    return content

def fix_missing_meta_description(content, filepath):
    """Agrega meta description si falta"""
    if 'name="description"' not in content:
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            title = title_match.group(1)
            desc = f"{title}. Servicio rapido y seguro de compra de cupo en dolares en Chile. Transferencia inmediata."
            if len(desc) > 160:
                desc = desc[:157] + "..."
            meta_desc = f'    <meta name="description" content="{desc}" />'
            content = content.replace('<meta charset="UTF-8" />', '<meta charset="UTF-8" />\n' + meta_desc)
            stats["meta_desc_fixed"] += 1
            print(f"  [+] Meta description added: {os.path.basename(filepath)}")
    return content

def process_file(filepath):
    """Procesa un archivo HTML con todas las correcciones"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Aplicar correcciones
        content = fix_canonical_mismatch(content, filepath)
        content = add_og_image(content, filepath)
        content = add_twitter_card(content, filepath)
        content = add_gsc_verification(content, filepath)
        content = fix_missing_meta_description(content, filepath)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            stats["files_processed"] += 1
        else:
            print(f"  [i] No changes: {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"  [!] Error processing {filepath}: {e}")

def main():
    print("=" * 60)
    print("SEO QUICK WINS - DolarExpress")
    print("=" * 60)
    
    # Procesar index.html
    print("\n[1] Processing index.html...")
    process_file(INDEX_HTML)
    
    # Procesar todos los HTML en public/
    print("\n[2] Processing public/*.html...")
    html_files = glob.glob(os.path.join(PUBLIC_DIR, "*.html"))
    print(f"    Found {len(html_files)} HTML files")
    
    for filepath in sorted(html_files):
        process_file(filepath)
    
    # Resumen
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Files processed:     {stats['files_processed']}")
    print(f"  Canonical fixed:     {stats['canonical_fixed']}")
    print(f"  og:image added:      {stats['og_image_added']}")
    print(f"  Twitter Card added:  {stats['twitter_card_added']}")
    print(f"  GSC added:           {stats['gsc_added']}")
    print(f"  Meta desc fixed:     {stats['meta_desc_fixed']}")
    print("\nDone!")

if __name__ == "__main__":
    main()
