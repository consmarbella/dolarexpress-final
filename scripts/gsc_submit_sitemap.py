from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    'scripts/gsc-service-account.json',
    scopes=['https://www.googleapis.com/auth/webmasters']
)
service = build('searchconsole', 'v1', credentials=creds)

# Submit sitemap to sc-domain property
print("Submitting sitemap to sc-domain:dolarexpress.cl ...")
try:
    result = service.sitemaps().submit(
        siteUrl='sc-domain:dolarexpress.cl',
        feedpath='https://www.dolarexpress.cl/sitemap.xml'
    ).execute()
    print(f"  OK: {result}")
except Exception as e:
    print(f"  Error: {e}")

# Verify it's there
print("\nChecking sitemaps on sc-domain property...")
try:
    sitemaps = service.sitemaps().list(siteUrl='sc-domain:dolarexpress.cl').execute()
    items = sitemaps.get('sitemapDefault', [])
    if items:
        for sm in items:
            print(f"  {sm.get('path','?')} pending={sm.get('isPending','?')} submitted={sm.get('lastSubmitted','?')} errors={sm.get('errors','0')}")
    else:
        print("  (no sitemaps found)")
except Exception as e:
    print(f"  Error: {e}")
