from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    'scripts/gsc-service-account.json',
    scopes=['https://www.googleapis.com/auth/webmasters']
)
service = build('searchconsole', 'v1', credentials=creds)

sites = service.sites().list().execute()
print('=== ALL SITES ===')
for s in sites.get('siteEntry', []):
    print(f"  {s['siteUrl']}  perm={s.get('permissionLevel','?')}")

# Try inspecting a URL on the www property
print('\n=== URL INSPECTION (www) ===')
try:
    result = service.urlInspection().index().inspect(
        body={
            "inspectionUrl": "https://www.dolarexpress.cl/",
            "siteUrl": "https://www.dolarexpress.cl/"
        }
    ).execute()
    verdict = result.get('inspectionResult', {}).get('indexStatusResult', {})
    print(f"  Coverage: {verdict.get('coverageState', '?')}")
    print(f"  Crawled as: {verdict.get('crawledAs', '?')}")
    print(f"  Indexing state: {verdict.get('indexingState', '?')}")
    print(f"  Page fetch: {verdict.get('pageFetch', '?')}")
    print(f"  Robots txt state: {verdict.get('robotsTxtState', '?')}")
    print(f"  Verdict: {verdict.get('verdict', '?')}")
    refs = verdict.get('referringUrls', [])
    if refs:
        print(f"  Referring URLs: {refs[:3]}")
except Exception as e:
    print(f"  Error: {e}")

# Check sitemaps on sc-domain property
print('\n=== SITEMAPS (sc-domain) ===')
try:
    sitemaps = service.sitemaps().list(siteUrl='sc-domain:dolarexpress.cl').execute()
    for sm in sitemaps.get('sitemapDefault', []):
        print(f"  {sm.get('path','?')} pathSubmitted={sm.get('isPending','?')} lastSubmitted={sm.get('lastSubmitted','?')}")
except Exception as e:
    print(f"  Error: {e}")

# Check sitemaps on www property
print('\n=== SITEMAPS (www) ===')
try:
    sitemaps = service.sitemaps().list(siteUrl='https://www.dolarexpress.cl/').execute()
    for sm in sitemaps.get('sitemapDefault', []):
        print(f"  {sm.get('path','?')} pathSubmitted={sm.get('isPending','?')} lastSubmitted={sm.get('lastSubmitted','?')}")
    if not sitemaps.get('sitemapDefault'):
        print("  (no sitemaps)")
except Exception as e:
    print(f"  Error: {e}")
