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

# 1. ALL pages with any impressions in last 3 months
print('=' * 60)
print('TODAS LAS PAGINAS CON IMPRESIONES (jun-ago 2026)')
print('=' * 60)
try:
    data = query(token, {
        'startDate': '2026-06-01', 'endDate': '2026-08-27',
        'dimensions': ['page'], 'rowLimit': 200
    })
    rows = sorted(data.get('rows', []), key=lambda x: x['impressions'], reverse=True)
    print(f'\nTotal paginas con impresiones: {len(rows)}\n')
    for i, r in enumerate(rows):
        page = r['keys'][0].replace('https://dolarexpress.cl', '').replace('http://dolarexpress.cl', '').replace('http://www.dolarexpress.cl', '[www]').replace('https://www.dolarexpress.cl', '[www]') or '/'
        print(f'{i+1:3d}. {page}')
        print(f'     Clicks: {r["clicks"]:4d} | Imp: {r["impressions"]:6d} | Pos: {r["position"]:5.1f}')
except Exception as e:
    print(f'Error: {e}')

# 2. Pages with clicks
print('\n' + '=' * 60)
print('PAGINAS QUE GENERAN CLICKS (jun-ago 2026)')
print('=' * 60)
try:
    data = query(token, {
        'startDate': '2026-06-01', 'endDate': '2026-08-27',
        'dimensions': ['page'], 'rowLimit': 200
    })
    rows = [r for r in data.get('rows', []) if r['clicks'] > 0]
    rows.sort(key=lambda x: x['clicks'], reverse=True)
    print(f'\nTotal paginas con clicks: {len(rows)}\n')
    for i, r in enumerate(rows):
        page = r['keys'][0].replace('https://dolarexpress.cl', '').replace('http://dolarexpress.cl', '').replace('http://www.dolarexpress.cl', '[www]').replace('https://www.dolarexpress.cl', '[www]') or '/'
        print(f'{i+1}. {page}')
        print(f'   Clicks: {r["clicks"]} | Imp: {r["impressions"]} | CTR: {r["ctr"]*100:.1f}% | Pos: {r["position"]:.1f}')
except Exception as e:
    print(f'Error: {e}')

# 3. Compare first half June vs last half August (before vs after cleanup)
print('\n' + '=' * 60)
print('ANTES vs DESPUES: 1-15 junio vs 13-27 agosto')
print('=' * 60)
try:
    before = query(token, {'startDate': '2026-06-01', 'endDate': '2026-06-15', 'dimensions': [], 'rowLimit': 1})
    after = query(token, {'startDate': '2026-08-13', 'endDate': '2026-08-27', 'dimensions': [], 'rowLimit': 1})
    b = (before.get('rows') or [{'clicks':0,'impressions':0,'ctr':0,'position':0}])[0]
    a = (after.get('rows') or [{'clicks':0,'impressions':0,'ctr':0,'position':0}])[0]
    print(f'\n1-15 Junio:    {b["clicks"]} clicks | {b["impressions"]} imp | Pos {b["position"]:.1f}')
    print(f'13-27 Agosto:  {a["clicks"]} clicks | {a["impressions"]} imp | Pos {a["position"]:.1f}')
    if b['impressions'] > 0:
        print(f'Cambio imp:    {((a["impressions"]/b["impressions"]-1)*100):+.1f}%')
    if b['clicks'] > 0:
        print(f'Cambio clicks: {((a["clicks"]/b["clicks"]-1)*100):+.1f}%')
except Exception as e:
    print(f'Error: {e}')
