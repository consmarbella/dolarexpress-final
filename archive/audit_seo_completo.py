#!/usr/bin/env python3
"""
AUDITORÍA SEO COMPLETA - DolarExpress
Analiza 300+ páginas HTML para:
- Interlinking (qué enlaza a dónde)
- Meta tags (title, description, canonical)
- Estructura (URLs, rutas)
- Problemas comunes de SEO
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import csv

class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self.canonical = None
        self.h1 = None
        self.links = []
        self.images = []
        self.meta_robots = None
        self.open_graph = {}
        self.structured_data = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "title":
            pass  # Will handle in data
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            property_attr = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")

            if name == "description":
                self.description = content
            elif name == "robots":
                self.meta_robots = content
            elif property_attr and property_attr.startswith("og:"):
                self.open_graph[property_attr] = content

        elif tag == "link":
            rel = attrs_dict.get("rel", "").lower()
            if rel == "canonical":
                self.canonical = attrs_dict.get("href", "")

        elif tag == "h1":
            pass  # Will handle in data

        elif tag == "a":
            href = attrs_dict.get("href", "")
            text = attrs_dict.get("title", "")
            if href:
                self.links.append({"url": href, "text": text})

        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            if src:
                self.images.append({"src": src, "alt": alt})

        elif tag == "script":
            if attrs_dict.get("type") == "application/ld+json":
                pass  # Will handle in data

    def handle_data(self, data):
        if self.getpos()[0] == 1:  # Si estamos en title
            if not self.title:
                self.title = data.strip()

def extract_json_ld(html_content):
    """Extrae structured data (JSON-LD) del HTML"""
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    data = []
    for match in matches:
        try:
            data.append(json.loads(match))
        except:
            pass
    return data

def parse_html(file_path, base_url="https://dolarexpress.cl"):
    """Parsea un archivo HTML y extrae datos SEO"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
    except:
        return None

    parser = SEOParser()
    try:
        parser.feed(html_content)
    except:
        pass

    # Extraer título del tag <title>
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if title_match:
        parser.title = title_match.group(1).strip()

    # Extraer H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        parser.h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

    # Extraer JSON-LD
    parser.structured_data = extract_json_ld(html_content)

    return {
        "file": str(file_path),
        "title": parser.title,
        "description": parser.description,
        "canonical": parser.canonical,
        "h1": parser.h1,
        "meta_robots": parser.meta_robots,
        "links": parser.links,
        "images": parser.images,
        "open_graph": parser.open_graph,
        "structured_data": bool(parser.structured_data),
        "html_size": len(html_content)
    }

def get_url_from_path(file_path):
    """Convierte ruta de archivo a URL"""
    relative = str(file_path).replace("\\", "/")

    # Si está en public/, quitar ese prefijo
    if "/public/" in relative:
        relative = relative.split("/public/")[1]

    # Archivo sin extensión
    if relative.endswith(".html"):
        relative = relative[:-5]

    # Rutas especiales
    if relative == "index":
        return "https://dolarexpress.cl/"

    return f"https://dolarexpress.cl/{relative}/"

def audit_seo():
    """Ejecuta auditoría completa"""

    print("🔍 INICIANDO AUDITORÍA SEO...\n")

    # Encontrar todos los archivos HTML
    html_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"📄 Encontrados {len(html_files)} archivos HTML\n")

    # Parsear cada archivo
    pages_data = {}
    errors = []

    for i, html_file in enumerate(html_files, 1):
        if i % 50 == 0:
            print(f"  Procesando: {i}/{len(html_files)}...")

        data = parse_html(html_file)
        if data:
            url = get_url_from_path(html_file)
            pages_data[url] = data
        else:
            errors.append(html_file)

    print(f"\n✅ Parseados: {len(pages_data)} páginas")
    print(f"❌ Errores: {len(errors)}\n")

    # ANÁLISIS
    print("="*70)
    print("📊 ANÁLISIS DE INTERLINKING")
    print("="*70 + "\n")

    # Contar enlaces internos vs externos
    total_links = 0
    internal_links = defaultdict(set)
    external_links = set()
    broken_links = []

    for url, page_data in pages_data.items():
        for link in page_data["links"]:
            href = link["url"]
            total_links += 1

            # Filtrar enlaces válidos
            if href.startswith("#") or href.startswith("javascript:") or not href:
                continue

            # Determinar si es interno o externo
            if "dolarexpress" in href.lower() or href.startswith("/"):
                # Es enlace interno
                # Normalizar
                if href.startswith("http"):
                    normalized = href.rstrip("/")
                else:
                    normalized = urljoin(url, href).rstrip("/")

                internal_links[url].add(normalized)
            else:
                external_links.add(href)

    print(f"Total de Enlaces: {total_links}")
    print(f"Enlaces Internos: {sum(len(v) for v in internal_links.values())}")
    print(f"Enlaces Externos: {len(external_links)}")

    # Páginas huérfanas (sin enlaces que las apunten)
    print("\n" + "="*70)
    print("🚨 PÁGINAS SIN INTERLINKING (HUÉRFANAS)")
    print("="*70 + "\n")

    all_linked_pages = set()
    for links in internal_links.values():
        all_linked_pages.update(links)

    orphaned = []
    for url in pages_data.keys():
        if url not in all_linked_pages:
            orphaned.append(url)

    print(f"Páginas Huérfanas: {len(orphaned)}")
    if orphaned and len(orphaned) <= 20:
        for page in orphaned[:20]:
            print(f"  - {page}")
        if len(orphaned) > 20:
            print(f"  ... y {len(orphaned) - 20} más")

    # Meta Tags
    print("\n" + "="*70)
    print("🏷️  ANÁLISIS DE META TAGS")
    print("="*70 + "\n")

    missing_title = 0
    missing_description = 0
    missing_h1 = 0
    missing_canonical = 0

    for url, page_data in pages_data.items():
        if not page_data["title"]:
            missing_title += 1
        if not page_data["description"]:
            missing_description += 1
        if not page_data["h1"]:
            missing_h1 += 1
        if not page_data["canonical"]:
            missing_canonical += 1

    total = len(pages_data)
    print(f"Meta Title faltante: {missing_title}/{total} ({missing_title*100/total:.1f}%)")
    print(f"Meta Description faltante: {missing_description}/{total} ({missing_description*100/total:.1f}%)")
    print(f"H1 faltante: {missing_h1}/{total} ({missing_h1*100/total:.1f}%)")
    print(f"Canonical faltante: {missing_canonical}/{total} ({missing_canonical*100/total:.1f}%)")

    # URLs
    print("\n" + "="*70)
    print("🔗 ANÁLISIS DE URLs")
    print("="*70 + "\n")

    urls_with_issues = []
    for url, page_data in pages_data.items():
        # Verificar si canonical coincide con URL
        if page_data["canonical"]:
            if page_data["canonical"].rstrip("/") != url.rstrip("/"):
                urls_with_issues.append({
                    "url": url,
                    "canonical": page_data["canonical"],
                    "issue": "Canonical no coincide con URL"
                })

    print(f"URLs con Canonical incorrecto: {len(urls_with_issues)}")
    if urls_with_issues and len(urls_with_issues) <= 10:
        for issue in urls_with_issues[:10]:
            print(f"  - {issue['url']}")
            print(f"    Canonical: {issue['canonical']}\n")

    # GENERAR REPORTES CSV
    print("\n" + "="*70)
    print("💾 GENERANDO REPORTES")
    print("="*70 + "\n")

    # Reporte 1: Resumen de páginas
    with open("seo_audit_pages.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Title", "Description", "H1", "Canonical", "Total_Links", "Links_In", "Issues"])

        for url, page_data in pages_data.items():
            links_in = len([v for v in internal_links.values() if url in v])
            issues = []

            if not page_data["title"]:
                issues.append("No title")
            if not page_data["description"]:
                issues.append("No description")
            if not page_data["h1"]:
                issues.append("No h1")
            if not page_data["canonical"]:
                issues.append("No canonical")
            if page_data["canonical"] and page_data["canonical"].rstrip("/") != url.rstrip("/"):
                issues.append("Canonical mismatch")
            if links_in == 0:
                issues.append("Orphaned")

            writer.writerow([
                url,
                page_data["title"][:50] if page_data["title"] else "",
                page_data["description"][:50] if page_data["description"] else "",
                page_data["h1"][:50] if page_data["h1"] else "",
                page_data["canonical"] if page_data["canonical"] else "",
                len(page_data["links"]),
                links_in,
                "; ".join(issues)
            ])

    # Reporte 2: Interlinking
    with open("seo_audit_interlinking.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["From_URL", "To_URL"])

        for from_url, to_urls in internal_links.items():
            for to_url in to_urls:
                writer.writerow([from_url, to_url])

    # Reporte 3: Páginas Huérfanas
    with open("seo_audit_orphaned.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Orphaned_URL", "Title", "Description"])

        for url in orphaned:
            if url in pages_data:
                writer.writerow([
                    url,
                    pages_data[url]["title"][:50] if pages_data[url]["title"] else "",
                    pages_data[url]["description"][:50] if pages_data[url]["description"] else ""
                ])

    print("✅ seo_audit_pages.csv - Resumen de todas las páginas")
    print("✅ seo_audit_interlinking.csv - Estructura de enlaces internos")
    print("✅ seo_audit_orphaned.csv - Páginas sin enlaces entrantes")

    # RESUMEN EJECUTIVO
    print("\n" + "="*70)
    print("📋 RESUMEN EJECUTIVO")
    print("="*70 + "\n")

    score = 100

    if missing_title > 0:
        print(f"❌ {missing_title} páginas sin meta title (CRÍTICO)")
        score -= 20
    if missing_description > 0:
        print(f"⚠️  {missing_description} páginas sin meta description")
        score -= 10
    if missing_h1 > 0:
        print(f"⚠️  {missing_h1} páginas sin H1")
        score -= 10
    if len(orphaned) > 0:
        print(f"❌ {len(orphaned)} páginas huérfanas sin interlinking (CRÍTICO)")
        score -= 20
    if len(urls_with_issues) > 0:
        print(f"⚠️  {len(urls_with_issues)} URLs con canonical incorrecto")
        score -= 10

    if score >= 80:
        print(f"\n✅ SCORE SEO: {score}/100 - BUENO")
    elif score >= 60:
        print(f"\n⚠️  SCORE SEO: {score}/100 - REQUIERE MEJORAS")
    else:
        print(f"\n❌ SCORE SEO: {score}/100 - CRÍTICO")

    print("\n" + "="*70)
    print("Próximos pasos:")
    print("1. Revisar seo_audit_pages.csv para identificar páginas problemáticas")
    print("2. Usar seo_audit_orphaned.csv para crear enlaces internos a esas páginas")
    print("3. Revisar seo_audit_interlinking.csv para optimizar estrategia de links")
    print("="*70 + "\n")

if __name__ == "__main__":
    audit_seo()
