"""Verify all fixes applied correctly."""
import os, re

pub = r'C:\Users\matte\OneDrive\Escritorio\legalhelser\reborn\dolarexpress-final\public'
issues = []

for root, dirs, files in os.walk(pub):
    for f in files:
        if not f.endswith('.html'):
            continue
        fpath = os.path.join(root, f)
        rel = os.path.relpath(fpath, pub)
        with open(fpath, 'rb') as fh:
            data = fh.read()
        if data[:3] == b'\xef\xbb\xbf':
            data = data[3:]
        text = data.decode('utf-8')
        
        if re.search(r'â€|â†|â˜', text):
            issues.append(f'{rel}: mojibake')
        if '/cupo-dolar-online' in text or '/simulador-dolar' in text:
            issues.append(f'{rel}: dead link')
        if re.search(r'lang="es"', text) and 'lang="es-CL"' not in text:
            issues.append(f'{rel}: lang=es')
        if 'og-image.svg' in text:
            issues.append(f'{rel}: og-image.svg')
        if re.search(r'Necesitás|Cotizá|Enviános|Tenés|Podés|Querés', text):
            issues.append(f'{rel}: voseo')
        if 'twitter:title" content="Index' in text:
            issues.append(f'{rel}: wrong twitter:title')

# Check api-catalog
api = os.path.join(pub, '.well-known', 'api-catalog')
if os.path.exists(api):
    with open(api) as f:
        if '/vender-cupo-internacional' in f.read():
            issues.append('api-catalog: stale URL')

# Check exposed files deleted
for f in ['generar-sitemap.bat', 'BingSiteAuth.xml', 'e36d247015d03788f92ccf1139b25fe6.txt']:
    if os.path.exists(os.path.join(pub, f)):
        issues.append(f'{f}: not deleted')

if issues:
    print('REMAINING ISSUES:')
    for i in issues:
        print(f'  {i}')
else:
    print('ALL CHECKS PASSED - 0 issues remaining')
