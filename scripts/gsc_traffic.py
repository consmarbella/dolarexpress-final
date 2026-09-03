import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import urllib.request
import urllib.parse
import time

SA_FILE = 'scripts/gsc-service-account.json'
SITE = 'sc-domain:dolarexpress.cl'

def get_token():
    with open(SA_FILE) as f:
        sa = json.load(f)
    creds = service_account.Credentials.from_service_account_info(
        sa, scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    creds.refresh(Request())
    return creds.token

def query(token, payload):
    url = f'https://searchconsole.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE, safe="")}/searchAnalytics/query'
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

token = get_token()
print('Token OK\n')

# 1. TRAFICO MENSUAL
print('=' * 60)
print('TRAFICO MENSUAL')
print('=' * 60)
months = [
    ('2026-06-01', '2026-06-30', 'Junio 2026'),
    ('2026-07-01', '2026-07-31', 'Julio 2026'),
    ('2026-08-01', '2026-08-27', 'Agosto 2026'),
]
for start, end, label in months:
    try:
        data = query(token, {'startDate': start, 'endDate': end, 'dimensions': [], 'rowLimit': 1})
        row = (data.get('rows') or [None])[0]
        if row:
            print(f'\n{label}:')
            print(f'  Clicks:      {row["clicks"]}')
            print(f'  Impressions: {row["impressions"]}')
            print(f'  CTR:         {row["ctr"]*100:.2f}%')
            print(f'  Posicion:    {row["position"]:.1f}')
        else:
            print(f'\n{label}: Sin datos')
    except Exception as e:
        print(f'\n{label}: Error - {e}')
    time.sleep(1)

# 2. COMPARACION JULIO vs AGOSTO
print('\n' + '=' * 60)
print('COMPARACION: JULIO vs AGOSTO')
print('=' * 60)
try:
    jul = query(token, {'startDate': '2026-07-01', 'endDate': '2026-07-31', 'dimensions': [], 'rowLimit': 1})
    ago = query(token, {'startDate': '2026-08-01', 'endDate': '2026-08-27', 'dimensions': [], 'rowLimit': 1})
    j = (jul.get('rows') or [{'clicks':0,'impressions':0,'ctr':0,'position':0}])[0]
    a = (ago.get('rows') or [{'clicks':0,'impressions':0,'ctr':0,'position':0}])[0]
    
    cd = a['clicks'] - j['clicks']
    cp = f'{(a["clicks"]/j["clicks"]-1)*100:+.1f}%' if j['clicks'] else 'N/A'
    id = a['impressions'] - j['impressions']
    ip = f'{(a["impressions"]/j["impressions"]-1)*100:+.1f}%' if j['impressions'] else 'N/A'
    pd = a['position'] - j['position']
    
    print(f'\nJulio (31 dias):    {j["clicks"]} clicks | {j["impressions"]} imp | CTR {j["ctr"]*100:.2f}% | Pos {j["position"]:.1f}')
    print(f'Agosto (27 dias):   {a["clicks"]} clicks | {a["impressions"]} imp | CTR {a["ctr"]*100:.2f}% | Pos {a["position"]:.1f}')
    print(f'\nClicks:      {cd:+d} ({cp})')
    print(f'Impresiones: {id:+d} ({ip})')
    print(f'Posicion:    {pd:+.1f} {"MEJOR" if pd < 0 else "PEOR" if pd > 0 else "="}')
except Exception as e:
    print(f'Error: {e}')

# 3. TOP 20 PAGINAS
print('\n' + '=' * 60)
print('TOP 20 PAGINAS POR CLICKS (ultimos 28 dias)')
print('=' * 60)
try:
    data = query(token, {
        'startDate': '2026-07-31', 'endDate': '2026-08-27',
        'dimensions': ['page'], 'rowLimit': 20
    })
    for i, r in enumerate(sorted(data.get('rows', []), key=lambda x: x['clicks'], reverse=True)):
        page = r['keys'][0].replace('https://dolarexpress.cl', '').replace('http://dolarexpress.cl', '') or '/'
        print(f'{i+1:2d}. {page}')
        print(f'     Clicks: {r["clicks"]:4d} | Imp: {r["impressions"]:6d} | CTR: {r["ctr"]*100:5.1f}% | Pos: {r["position"]:5.1f}')
except Exception as e:
    print(f'Error: {e}')

# 4. TOP 20 QUERIES
print('\n' + '=' * 60)
print('TOP 20 QUERIES POR IMPRESIONES (ultimos 28 dias)')
print('=' * 60)
try:
    data = query(token, {
        'startDate': '2026-07-31', 'endDate': '2026-08-27',
        'dimensions': ['query'], 'rowLimit': 20
    })
    for i, r in enumerate(sorted(data.get('rows', []), key=lambda x: x['impressions'], reverse=True)):
        print(f'{i+1:2d}. "{r["keys"][0]}"')
        print(f'     Clicks: {r["clicks"]:4d} | Imp: {r["impressions"]:6d} | CTR: {r["ctr"]*100:5.1f}% | Pos: {r["position"]:5.1f}')
except Exception as e:
    print(f'Error: {e}')

# 5. QUERIES QUE GENERAN CLICKS
print('\n' + '=' * 60)
print('TOP 15 QUERIES POR CLICKS (las que traen trafico real)')
print('=' * 60)
try:
    data = query(token, {
        'startDate': '2026-07-31', 'endDate': '2026-08-27',
        'dimensions': ['query'], 'rowLimit': 15
    })
    for i, r in enumerate(sorted(data.get('rows', []), key=lambda x: x['clicks'], reverse=True)):
        print(f'{i+1:2d}. "{r["keys"][0]}"')
        print(f'     Clicks: {r["clicks"]:4d} | Imp: {r["impressions"]:6d} | CTR: {r["ctr"]*100:5.1f}% | Pos: {r["position"]:5.1f}')
except Exception as e:
    print(f'Error: {e}')

# 6. EVOLUCION SEMANAL
print('\n' + '=' * 60)
print('EVOLUCION SEMANAL (jun-ago 2026)')
print('=' * 60)
try:
    data = query(token, {
        'startDate': '2026-06-01', 'endDate': '2026-08-27',
        'dimensions': ['date'], 'rowLimit': 100
    })
    rows = sorted(data.get('rows', []), key=lambda x: x['keys'][0])
    for r in rows:
        print(f'  {r["keys"][0]}  clicks={r["clicks"]:3d}  imp={r["impressions"]:5d}  pos={r["position"]:5.1f}')
except Exception as e:
    print(f'Error: {e}')
