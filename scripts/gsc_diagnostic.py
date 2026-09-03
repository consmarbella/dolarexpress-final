import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import urllib.request
import urllib.parse

SA_FILE = 'scripts/gsc-service-account.json'

def get_token():
    with open(SA_FILE) as f:
        sa = json.load(f)
    creds = service_account.Credentials.from_service_account_info(
        sa, scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    creds.refresh(Request())
    return creds.token

def api_get(token, url):
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def api_post(token, url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

token = get_token()
print('Token OK\n')

# 1. List all properties this service account can access
print('=== PROPIEDADES ACCESIBLES ===\n')
try:
    sites = api_get(token, 'https://searchconsole.googleapis.com/webmasters/v3/sites')
    for s in sites.get('siteEntry', []):
        print(f'  {s["siteUrl"]}  (tipo: {s.get("permissionLevel", "?")})')
    if not sites.get('siteEntry'):
        print('  NINGUNA - la service account no tiene acceso a ninguna propiedad')
except Exception as e:
    print(f'  Error listando: {e}')

print()

# 2. Try different siteUrl formats
print('=== PRUEBA DE FORMATOS siteUrl ===\n')
formats = [
    'https://dolarexpress.cl',
    'https://dolarexpress.cl/',
    'http://dolarexpress.cl',
    'http://dolarexpress.cl/',
    'sc-domain:dolarexpress.cl',
    'https://www.dolarexpress.cl',
    'https://www.dolarexpress.cl/',
]
for fmt in formats:
    try:
        data = api_post(token,
            f'https://searchconsole.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(fmt, safe="")}/searchAnalytics/query',
            {'startDate': '2026-08-20', 'endDate': '2026-08-27', 'dimensions': [], 'rowLimit': 1}
        )
        row = (data.get('rows') or [None])[0]
        if row:
            print(f'  OK  {fmt}  -> clicks={row["clicks"]} imp={row["impressions"]} pos={row["position"]:.1f}')
        else:
            print(f'  OK  {fmt}  -> sin datos (pero sin error)')
    except urllib.error.HTTPError as e:
        print(f'  {e.code}  {fmt}  -> {e.reason}')
    except Exception as e:
        print(f'  ERR {fmt}  -> {e}')
