"""
COMPREHENSIVE SEO FIX — dolarexpress.cl
Fixes ALL issues from audit in one pass.
"""
import os
import re
import json

PUB_DIR = os.path.join(os.path.dirname(__file__), "..", "public")
SITE = "https://www.dolarexpress.cl"

# ============================================================
# 1. MOJIBAKE REPLACEMENTS (broken UTF-8 artifacts)
# ============================================================
MOJIBAKE = {
    '\u201c': '"',   # left double quote
    '\u201d': '"',   # right double quote
    '\u2018': "'",   # left single quote
    '\u2019': "'",   # right single quote
    '\u2013': '–',   # en-dash
    '\u2014': '—',   # em-dash
    '\u2022': '•',   # bullet
    '\u2026': '…',   # ellipsis
    '\u2192': '→',   # right arrow
    '\u2030': '‰',   # per-mille
    '\u2039': '‹',   # single left-pointing angle
    '\u203A': '›',   # single right-pointing angle
}

# These are the actual broken byte sequences that appear as mojibake
# When UTF-8 bytes for — (E2 80 94) are read as Windows-1252: â€"
MOJIBAKE_BYTES = {
    'â€"': '—',   # em-dash
    'â€™': "'",    # right single quote
    'â€œ': '"',    # left double quote
    'â€': '"',     # right double quote  
    'â€¢': '•',    # bullet
    'â†': '→',     # arrow (partial match)
    'â˜…': '★',    # star
    'â€º': '›',    # right angle quote
    'â€˜': "'",    # left single quote
    'â‚¬': '€',    # euro
}

# ============================================================
# 2. dead links to fix
# ============================================================
DEAD_LINKS = {
    '/cupo-dolar-online.html': '/',           # page doesn't exist -> homepage
    '/simulador-dolar.html': '/comisiones',    # page doesn't exist -> comisiones
}

# ============================================================
# 3. Main processing
# ============================================================

def fix_mojibake(text):
    """Fix all mojibake / encoding artifacts."""
    for broken, correct in MOJIBAKE_BYTES.items():
        text = text.replace(broken, correct)
    for broken, correct in MOJIBAKE.items():
        text = text.replace(broken, correct)
    return text


def fix_dead_links(text):
    """Replace dead internal links."""
    for dead, replacement in DEAD_LINKS.items():
        text = text.replace(f'href="{dead}"', f'href="{replacement}"')
        text = text.replace(f"href='{dead}'", f"href='{replacement}'")
    return text


def fix_lang(text):
    """Standardize lang attribute to es-CL."""
    text = re.sub(r'<html\s+lang="es"', '<html lang="es-CL"', text)
    return text


def fix_canonical_conflicts(text, filename):
    """Fix canonical/redirect conflicts."""
    if filename == 'vender-cupo-international.html':
        # This page 301s to /cupo-internacional-a-pesos
        text = text.replace(
            f'href="{SITE}/vender-cupo-internacional"',
            f'href="{SITE}/cupo-internacional-a-pesos"'
        )
        text = text.replace(
            f'content="{SITE}/vender-cupo-internacional"',
            f'content="{SITE}/cupo-internacional-a-pesos"'
        )
    return text


def remove_duplicate_faq_schema(text, filename, is_preguntas, is_guia):
    """Remove FAQPage schema from all pages except preguntas-frecuentes and guia."""
    if is_preguntas or is_guia:
        return text  # Keep FAQ on these pages
    
    # Remove FAQPage JSON-LD blocks
    # Pattern: {"@type":"FAQPage",...}
    text = re.sub(
        r',\s*\{\s*"@type"\s*:\s*"FAQPage"[^}]*"mainEntity"\s*:\s*\[.*?\]\s*\}',
        '',
        text,
        flags=re.DOTALL
    )
    # Also handle case where FAQPage is the only item
    text = re.sub(
        r'\{\s*"@type"\s*:\s*"FAQPage"[^}]*"mainEntity"\s*:\s*\[.*?\]\s*\},?\s*',
        '',
        text,
        flags=re.DOTALL
    )
    # Clean up empty @graph arrays
    text = re.sub(r'"@graph"\s*:\s*\[\s*,', '"@graph": [', text)
    text = re.sub(r',\s*\]', ']', text)
    return text


def fix_twitter_title(text):
    """Fix wrong twitter:title on index.html."""
    text = text.replace(
        '<meta name="twitter:title" content="Index | DolarExpress">',
        '<meta name="twitter:title" content="Vender Cupo en D\u00f3lares a Pesos | DolarExpress">'
    )
    return text


def fix_og_image_consistency(text):
    """Standardize og:image to og-image.png (not .svg, not .jpg)."""
    text = text.replace('og-image.svg', 'og-image.png')
    text = text.replace('og-image.jpg', 'og-image.png')
    return text


def fix_voseo_to_tuteo(text):
    """Convert Argentine voseo to Chilean tuteo."""
    replacements = {
        '¿Necesitás': '¿Necesitas',
        '¿Tenés': '¿Tienes',
        '¿Querés': '¿Quieres',
        '¿Sos': '¿Eres',
        '¿Podés': '¿Puedes',
        '¿Vos': '¿Tú',
        'Cotizá': 'Cotiza',
        'Enviános': 'Envíanos',
        'Envianos': 'Envíanos',
        'Contactános': 'Contáctanos',
        'Comprámelo': 'Cómpralo',
        'Recibís': 'Recibes',
        'Tenés': 'Tienes',
        'Podés': 'Puedes',
        'Querés': 'Quieres',
        'Sos': 'Eres',
        'Mandános': 'Mándanos',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def fix_api_catalog(text):
    """Fix stale URL references in api-catalog."""
    text = text.replace('/vender-cupo-internacional', '/cupo-internacional-a-pesos')
    return text


def process_file(filepath, filename):
    """Process a single HTML file — apply all fixes."""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # Remove BOM
    if data[:3] == b'\xef\xbb\xbf':
        data = data[3:]
    
    text = data.decode('utf-8')
    original = text
    
    # Apply all fixes
    text = fix_mojibake(text)
    text = fix_dead_links(text)
    text = fix_lang(text)
    text = fix_canonical_conflicts(text, filename)
    text = fix_twitter_title(text)
    text = fix_og_image_consistency(text)
    text = fix_voseo_to_tuteo(text)
    
    is_preguntas = filename == 'preguntas-frecuentes.html'
    is_guia = 'guia/' in filepath.replace('\\', '/')
    text = remove_duplicate_faq_schema(text, filename, is_preguntas, is_guia)
    
    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    return False


def main():
    fixed_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(PUB_DIR):
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, PUB_DIR)
            total_count += 1
            
            if process_file(fpath, fname):
                print(f"FIXED: {rel}")
                fixed_count += 1
            else:
                print(f"OK:    {rel}")
    
    # Fix api-catalog
    api_catalog = os.path.join(PUB_DIR, '.well-known', 'api-catalog')
    if os.path.exists(api_catalog):
        with open(api_catalog, 'rb') as f:
            data = f.read()
        text = data.decode('utf-8')
        fixed = fix_api_catalog(text)
        if fixed != text:
            with open(api_catalog, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print("FIXED: .well-known/api-catalog")
    
    print(f"\n{fixed_count}/{total_count} files fixed")


if __name__ == "__main__":
    main()
