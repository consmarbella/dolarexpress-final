from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json, urllib.request, urllib.parse, time
from datetime import datetime, timedelta

creds = service_account.Credentials.from_service_account_file(
    'scripts/gsc-service-account.json',
    scopes=['https://www.googleapis.com/auth/webmasters', 'https://www.googleapis.com/auth/webmasters.readonly']
)
creds.refresh(Request())

site = 'sc-domain:dolarexpress.cl'
encoded = urllib.parse.quote(site, safe='')

def gsc_request(endpoint, params=None, method='GET', body=None):
    base = 'https://www.googleapis.com/webmasters/v3'
    url = base + endpoint
    if params:
        url += '?' + urllib.parse.urlencode(params)
    headers = {'Authorization': 'Bearer ' + creds.token}
    if body:
        headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())

# 1. Full traffic data last 6 months
print("=" * 70)
print("1. TRAFFIC DATA (last 6 months)")
print("=" * 70)

body = {
    "startDate": "2026-03-01",
    "endDate": "2026-09-08",
    "dimensions": ["date"],
    "rowLimit": 200
}
data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
for row in data.get('rows', []):
    d = row['keys'][0]
    clicks = row['clicks']
    imp = row['impressions']
    ctr = row['ctr']
    pos = row['position']
    print(f"  {d}: {clicks} clicks | {imp} imp | CTR {ctr:.2%} | pos {pos:.1f}")

# 2. Pages by clicks (top pages)
print("\n" + "=" * 70)
print("2. TOP PAGES BY CLICKS")
print("=" * 70)

body = {
    "startDate": "2026-03-01",
    "endDate": "2026-09-08",
    "dimensions": ["page"],
    "rowLimit": 30,
    "orderDescending": True
}
data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
for row in data.get('rows', []):
    page = row['keys'][0]
    clicks = row['clicks']
    imp = row['impressions']
    ctr = row['ctr']
    pos = row['position']
    print(f"  {clicks:>3} clicks | pos {pos:>5.1f} | CTR {ctr:>5.1%} | {page}")

# 3. Queries (what people search)
print("\n" + "=" * 70)
print("3. TOP QUERIES")
print("=" * 70)

body = {
    "startDate": "2026-03-01",
    "endDate": "2026-09-08",
    "dimensions": ["query"],
    "rowLimit": 30,
    "orderDescending": True
}
data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
for row in data.get('rows', []):
    q = row['keys'][0]
    clicks = row['clicks']
    imp = row['impressions']
    ctr = row['ctr']
    pos = row['position']
    print(f"  {clicks:>3} clicks | pos {pos:>5.1f} | CTR {ctr:>5.1%} | {q}")

# 4. Pages with impressions but low clicks (CTR problem?)
print("\n" + "=" * 70)
print("4. HIGH IMPRESSIONS / LOW CTR (CTR issue?)")
print("=" * 70)

body = {
    "startDate": "2026-06-01",
    "endDate": "2026-09-08",
    "dimensions": ["page", "query"],
    "rowLimit": 50,
    "filters": [{"dimension": "impressions", "operator": "greaterThan", "expression": "50"}],
    "orderDescending": True
}
data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
rows = data.get('rows', [])
# Sort by impressions desc
rows.sort(key=lambda x: x['impressions'], reverse=True)
for row in rows[:20]:
    page = row['keys'][0].replace('https://www.dolarexpress.cl', '')
    q = row['keys'][1]
    clicks = row['clicks']
    imp = row['impressions']
    ctr = row['ctr']
    pos = row['position']
    print(f"  {imp:>5} imp | {clicks:>2} clicks | CTR {ctr:>5.1%} | pos {pos:>5.1f} | '{q}' -> {page}")

# 5. Device comparison
print("\n" + "=" * 70)
print("5. DEVICE BREAKDOWN (last 30 days)")
print("=" * 70)

body = {
    "startDate": "2026-08-09",
    "endDate": "2026-09-08",
    "dimensions": ["device"],
    "rowLimit": 10
}
data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
for row in data.get('rows', []):
    print(f"  {row['keys'][0]:>10}: {row['clicks']} clicks | {row['impressions']} imp | pos {row['position']:.1f}")

# 6. Country breakdown
print("\n" + "=" * 70)
print("6. COUNTRY (last 30 days)")
print("=" * 70)

body = {
    "startDate": "2026-08-09",
    "endDate": "2026-09-08",
    "dimensions": ["country"],
    "rowLimit": 10
}
data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
for row in data.get('rows', []):
    print(f"  {row['keys'][0]:>10}: {row['clicks']} clicks | {row['impressions']} imp | pos {row['position']:.1f}")

# 7. Search Appearance
print("\n" + "=" * 70)
print("7. SEARCH APPEARANCE (last 30 days)")
print("=" * 70)

body = {
    "startDate": "2026-08-09",
    "endDate": "2026-09-08",
    "dimensions": ["searchAppearance"],
    "rowLimit": 10
}
data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
for row in data.get('rows', []):
    print(f"  {row['keys'][0]}: {row['clicks']} clicks | {row['impressions']} imp")

# 8. Compare this month vs same month last year or previous months
print("\n" + "=" * 70)
print("8. MONTH-OVER-MONTH COMPARISON")
print("=" * 70)

months = [
    ("2026-03-01", "2026-03-31", "Marzo 2026"),
    ("2026-04-01", "2026-04-30", "Abril 2026"),
    ("2026-05-01", "2026-05-31", "Mayo 2026"),
    ("2026-06-01", "2026-06-30", "Junio 2026"),
    ("2026-07-01", "2026-07-31", "Julio 2026"),
    ("2026-08-01", "2026-08-31", "Agosto 2026"),
    ("2026-09-01", "2026-09-08", "Sept 2026 (parcial)"),
]
for start, end, label in months:
    body = {
        "startDate": start,
        "endDate": end,
        "rowLimit": 1
    }
    data = gsc_request(f'/sites/{encoded}/searchAnalytics/query', body=body, method='POST')
    rows = data.get('rows', [])
    if rows:
        r = rows[0]
        print(f"  {label:>25}: {r['clicks']:>3} clicks | {r['impressions']:>5} imp | CTR {r['ctr']:.2%} | pos {r['position']:.1f}")
    else:
        print(f"  {label:>25}: no data")
