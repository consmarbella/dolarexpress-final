"""
Submit 404 URLs for removal from Google index via GSC Indexing API.
Uses urlNotifications:publish to mark as GONE.
"""
import json
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import urllib.request

SA_FILE = os.path.join(os.path.dirname(__file__), "gsc-service-account.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]

# Pages deleted that are still in Google index
URLS_TO_REMOVE = [
    "https://www.dolarexpress.cl/avance-cupo-en-dolares-en-conchali",
    "https://www.dolarexpress.cl/avance-cupo-en-dolares-en-la-granja",
    "https://www.dolarexpress.cl/avance-cupo-en-dolares-en-quilpue",
    "https://www.dolarexpress.cl/avance-cupo-en-dolares-en-villa-alemana",
    "https://www.dolarexpress.cl/alternativa-avance-la-polar",
    "https://www.dolarexpress.cl/avance-dolares-tarjeta-credito",
    "https://www.dolarexpress.cl/avance-efectivo",
    "https://www.dolarexpress.cl/avance-efectivo-tarjeta-lider",
    "https://www.dolarexpress.cl/avance-efectivo-tarjeta-ripley",
    "https://www.dolarexpress.cl/avance-efectivo.html",
    "https://www.dolarexpress.cl/avance-la-polar-cuotas",
]

def get_token():
    creds = service_account.Credentials.from_service_account_file(
        SA_FILE, scopes=SCOPES
    )
    creds.refresh(Request())
    return creds.token

def submit_removal(url, token):
    """Submit URL for removal using Indexing API urlNotifications:publish"""
    body = json.dumps({
        "url": url,
        "type": "URL_DELETED"
    }).encode()

    req = urllib.request.Request(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "detail": e.read().decode()[:200]}

def main():
    token = get_token()
    print(f"Token OK")
    print(f"Submitting {len(URLS_TO_REMOVE)} URLs for removal...\n")

    for url in URLS_TO_REMOVE:
        r = submit_removal(url, token)
        if "error" in r:
            print(f"FAIL {url}")
            print(f"  Error: {r['error']} - {r.get('detail', '')}\n")
        else:
            print(f"OK   {url}")
            print(f"  Type: {r.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('type', '?')}\n")

if __name__ == "__main__":
    main()
