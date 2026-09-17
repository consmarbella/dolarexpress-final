import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    'scripts/gsc-service-account.json',
    scopes=['https://www.googleapis.com/auth/webmasters.readonly']
)
service = build('searchconsole', 'v1', credentials=creds)

SITE = 'sc-domain:dolarexpress.cl'

# Total summary
request = {
    'startDate': '2026-08-20',
    'endDate': '2026-09-16',
    'dataState': 'final'
}
print('=== TOTAL SUMMARY (last 28 days) ===')
try:
    response = service.searchanalytics().query(siteUrl=SITE, body=request).execute()
    if 'rows' in response:
        for row in response['rows']:
            print(f"  Clicks: {row.get('clicks',0)}")
            print(f"  Impressions: {row.get('impressions',0)}")
            print(f"  CTR: {row.get('ctr',0):.2%}")
            print(f"  Avg Position: {row.get('position',0):.1f}")
except Exception as e:
    print(f'Error: {e}')

# Pages
request2 = {
    'startDate': '2026-08-20',
    'endDate': '2026-09-16',
    'dimensions': ['page'],
    'rowLimit': 25,
    'dataState': 'final'
}
print('\n=== TOP PAGES ===')
try:
    response2 = service.searchanalytics().query(siteUrl=SITE, body=request2).execute()
    if 'rows' in response2:
        for row in response2['rows']:
            page = row['keys'][0].replace('https://www.dolarexpress.cl', '') or '/'
            print(f"  {page}: clicks={row.get('clicks',0)}, imp={row.get('impressions',0)}, pos={row.get('position',0):.1f}")
except Exception as e:
    print(f'Error: {e}')

# Device comparison
request3 = {
    'startDate': '2026-08-20',
    'endDate': '2026-09-16',
    'dimensions': ['device'],
    'dataState': 'final'
}
print('\n=== DEVICE BREAKDOWN ===')
try:
    response3 = service.searchanalytics().query(siteUrl=SITE, body=request3).execute()
    if 'rows' in response3:
        for row in response3['rows']:
            print(f"  {row['keys'][0]}: clicks={row.get('clicks',0)}, imp={row.get('impressions',0)}, pos={row.get('position',0):.1f}")
except Exception as e:
    print(f'Error: {e}')

# Trend: last 28 vs previous 28
print('\n=== TREND: Previous 28d vs Current 28d ===')
for label, start, end in [('Previous (Jul23-Aug19)', '2026-07-23', '2026-08-19'), ('Current (Aug20-Sep16)', '2026-08-20', '2026-09-16')]:
    req = {'startDate': start, 'endDate': end, 'dataState': 'final'}
    try:
        resp = service.searchanalytics().query(siteUrl=SITE, body=req).execute()
        if 'rows' in resp:
            for row in resp['rows']:
                print(f"  {label}: clicks={row.get('clicks',0)}, imp={row.get('impressions',0)}, pos={row.get('position',0):.1f}")
    except Exception as e:
        print(f'  {label}: Error {e}')

# Country
request4 = {
    'startDate': '2026-08-20',
    'endDate': '2026-09-16',
    'dimensions': ['country'],
    'dataState': 'final'
}
print('\n=== COUNTRY BREAKDOWN ===')
try:
    response4 = service.searchanalytics().query(siteUrl=SITE, body=request4).execute()
    if 'rows' in response4:
        for row in response4['rows']:
            print(f"  {row['keys'][0]}: clicks={row.get('clicks',0)}, imp={row.get('impressions',0)}, pos={row.get('position',0):.1f}")
except Exception as e:
    print(f'Error: {e}')
