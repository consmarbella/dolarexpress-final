import json

with open('scripts/gsc-service-account.json', 'rb') as f:
    raw = f.read()

# Find private_key field
idx = raw.find(b'"private_key"')
segment = raw[idx:idx+100]
print('Raw around private_key:', segment)

# Check if \n is literal
has_literal_backslash_n = b'\\\\n' in raw
print('Has literal backslash-n:', has_literal_backslash_n)

# Check the key itself
sa = json.loads(raw)
pk = sa['private_key']
print('Key length:', len(pk))
print('Newlines in key:', pk.count('\n'))

# Try to fix: replace literal \n with actual newlines if needed
if '\\n' in pk and pk.count('\n') < 5:
    print('FIXING: replacing literal \\n with actual newlines')
    pk = pk.replace('\\n', '\n')
    sa['private_key'] = pk
    with open('scripts/gsc-service-account.json', 'w') as f:
        json.dump(sa, f, indent=2)
    print('Fixed!')
else:
    print('Key looks OK, newlines are real')

# Test with cryptography
try:
    from cryptography.hazmat.primitives import serialization
    key_data = pk.encode() if isinstance(pk, str) else pk
    private_key = serialization.load_pem_private_key(key_data, password=None)
    print('PEM loaded OK:', type(private_key))
except Exception as e:
    print('PEM load error:', e)
