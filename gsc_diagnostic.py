#!/usr/bin/env python3
"""
GSC Diagnostic Tool for dolarexpress.cl
Uses service account to pull coverage issues and identify specific URLs.
"""
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

SITES = [
    "sc-domain:dolarexpress.cl",
    "https://dolarexpress.cl/",
]
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SERVICE_ACCOUNT_FILE = "c:/Users/matte/Downloads/gen-lang-client-0162130358-33f2b2373523.json"

print(":: Autenticando con service account...")
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("searchconsole", "v1", credentials=credentials)
print("[OK] Autenticado\n")

# 1. List sites to verify access
print(":: Verificando acceso a propiedades...")
sites = service.sites().list().execute()
all_sites = []
for site in sites.get("siteEntry", []):
    url = site.get("siteUrl", "")
    perm = site.get("permissionLevel", "unknown")
    all_sites.append(url)
    print(f"   {url} -> {perm}")

found_site = None
for candidate in SITES:
    if candidate in all_sites:
        found_site = candidate
        print(f"\n   --> Usando propiedad: {found_site}")
        break

if not found_site:
    print(f"\n[WARN] Service account no tiene acceso a dolarexpress.cl")
    print("Intentando inspeccion directa de URLs (puede que el site list falle pero inspection funcione)...\n")
    # Try inspection anyway with the URL-based format
    found_site = "https://dolarexpress.cl/"

url_inspection = service.urlInspection()
sitemaps = service.sitemaps()

# Query sitemaps
print(":: SITEMAPS:")
for sm_site in SITES:
    try:
        sm_list = sitemaps.list(siteUrl=sm_site).execute()
        for sm in sm_list.get("sitemap", []):
            path = sm.get("path", "")
            last_sub = sm.get("lastSubmitted", "N/A")
            warns = sm.get("warnings", 0)
            errs = sm.get("errors", 0)
            print(f"   {path}")
            print(f"      Submitted: {last_sub}, Warnings: {warns}, Errors: {errs}")
        break
    except Exception as e:
        err_msg = str(e)
        if "403" in err_msg or "permission" in err_msg.lower() or "forbidden" in err_msg.lower():
            continue
        print(f"   [{sm_site}] Error: {e}")
        break

print()

# 3. Inspect sample URLs
sample_urls = [
    "https://dolarexpress.cl/",
    "https://dolarexpress.cl/venta-usd",
    "https://dolarexpress.cl/contacto",
    "https://dolarexpress.cl/cupo-dolar-a-pesos",
    "https://dolarexpress.cl/cupo-dolar-banco-chile.html",
]

print(":: INSPECCION DE URLs DE MUESTRA:")
any_success = False
for url in sample_urls:
    for sm_site in SITES:
        try:
            result = url_inspection.index().inspect(
                body={"inspectionUrl": url, "siteUrl": sm_site}
            ).execute()
            inspection = result.get("inspectionResult", {})
            idx = inspection.get("indexStatusResult", {})
            verdict = idx.get("verdict", "UNKNOWN")
            coverage = idx.get("coverageState", "?")
            last_crawl = idx.get("lastCrawlTime", "N/A")
            crawling = idx.get("crawledAs", "?")

            redirect_url = idx.get("redirectingUrl", None)
            page_fetch = idx.get("pageFetchState", "?")

            print(f"\n   {url}")
            print(f"      Verdict: {verdict}, Coverage: {coverage}, CrawledAs: {crawling}")
            print(f"      LastCrawl: {last_crawl}, FetchState: {page_fetch}")
            if redirect_url:
                print(f"      [WARN] REDIRECTS TO: {redirect_url}")

            robot = idx.get("roboting", False)
            if robot:
                print(f"      [WARN] BLOCKED BY ROBOTS.TXT")
            any_success = True
            break
        except Exception as e:
            err_msg = str(e)
            if "403" in err_msg or "permission" in err_msg.lower() or "forbidden" in err_msg.lower():
                continue
            print(f"\n   {url}")
            print(f"      [ERROR] {e}")
            break
    else:
        print(f"\n   {url}")
        print(f"      [ERROR] No access for any site format")

if any_success:
    print("\n[OK] Diagnostico completado.")
else:
    print("\n[FAIL] No se pudo acceder a GSC. Se requiere agregar la service account manualmente.")