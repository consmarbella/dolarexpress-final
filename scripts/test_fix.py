"""Test encoding fix on one file."""
import re

DOUBLE_ENCODED = {
    'Ã³': 'ó', 'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã±': 'ñ',
    'Ã¼': 'ü', 'Ã‰': 'É', 'Â¿': '¿', 'Â¡': '¡', 'Â°': '°',
    'Ãº': 'ú',
}
DOUBLE_A_PATTERN = re.compile(r'Ã([\x80-\xbf])')

def fix_a(match):
    try:
        return (match.group(0).encode('latin-1')).decode('utf-8')
    except:
        return match.group(0)

path = r'C:\Users\matte\OneDrive\Escritorio\legalhelser\reborn\dolarexpress-final\public\avance-cupo-dolares.html'
with open(path, 'rb') as f:
    data = f.read()
if data[:3] == b'\xef\xbb\xbf':
    data = data[3:]
text = data.decode('utf-8')

print('BEFORE:')
print('  Has double-encoded Ã:', 'Ã³' in text or 'Ã¡' in text)

for old, new in DOUBLE_ENCODED.items():
    text = text.replace(old, new)
text = DOUBLE_A_PATTERN.sub(fix_a, text)

print('AFTER:')
print('  Has double-encoded Ã:', 'Ã³' in text or 'Ã¡' in text)
print('  Has ó:', 'ó' in text)
print('  Has á:', 'á' in text)

m = re.search(r'<title>(.*?)</title>', text)
print('  Title:', m.group(1) if m else 'NOT FOUND')

m2 = re.search(r'meta name="description" content="(.*?)"', text)
print('  Desc:', m2.group(1)[:100] if m2 else 'NOT FOUND')

remaining = set(re.findall(r'Ã.', text))
print('  Remaining Ã:', remaining)

# Show a sample with accents
idx = text.find('dolares')
if idx > 0:
    print('  Sample:', text[idx:idx+30])
