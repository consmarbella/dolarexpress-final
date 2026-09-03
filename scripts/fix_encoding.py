"""Fix double-encoded UTF-8 in HTML files."""
import os
import re

PUB_DIR = os.path.join(os.path.dirname(__file__), "..", "public")

# Double-encoded sequences: the literal Ã³ in the file should be ó, etc.
# These are UTF-8 bytes that were read as Latin-1, then re-encoded as UTF-8
DOUBLE_ENCODED = {
    'Ã³': 'ó', 'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã±': 'ñ',
    'Ã¼': 'ü', 'Ã‰': 'É', 'Ã\x81': 'Á',
    'Â¿': '¿', 'Â¡': '¡', 'Â°': '°',
    'Ãº': 'ú',
}

# Regex patterns for remaining double-encoded chars
# Ã + any char that's a Latin-1 second byte
DOUBLE_A_PATTERN = re.compile(r'Ã([\x80-\xbf])')
DOUBLE_B_PATTERN = re.compile(r'Â([\xb0-\xbf])')

def fix_double_encoding(text):
    """Fix double-encoded UTF-8 text."""
    # Apply known replacements
    for old, new in DOUBLE_ENCODED.items():
        text = text.replace(old, new)
    
    # Fix remaining Ã + byte patterns: ÃX -> decode as Latin-1 to get original UTF-8
    def fix_a(match):
        try:
            return (match.group(0).encode('latin-1')).decode('utf-8')
        except:
            return match.group(0)
    text = DOUBLE_A_PATTERN.sub(fix_a, text)
    
    # Fix Â + byte patterns
    def fix_b(match):
        try:
            return (match.group(0).encode('latin-1')).decode('utf-8')
        except:
            return match.group(0)
    text = DOUBLE_B_PATTERN.sub(fix_b, text)
    
    return text

def process_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # Remove BOM
    if data[:3] == b'\xef\xbb\xbf':
        data = data[3:]
    
    text = data.decode('utf-8')
    
    # Check if it needs fixing
    if not re.search(r'Ã[³¡°±²³µ¹º¼½¾\x80-\xbf]|Â[¿¡°\xb0-\xbf]', text):
        return False  # Already OK
    
    fixed = fix_double_encoding(text)
    
    # Verify fix worked
    still_broken = re.search(r'Ã[³¡°±²³µ¹º¼½¾\x80-\xbf]|Â[¿¡°\xb0-\xbf]', fixed)
    if still_broken:
        print(f"  WARNING: Still has broken chars after fix")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    
    return True

def main():
    for root, dirs, files in os.walk(PUB_DIR):
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, PUB_DIR)
            fixed = process_file(fpath)
            if fixed:
                print(f"FIXED: {rel}")
            else:
                print(f"OK:    {rel}")

if __name__ == "__main__":
    main()
