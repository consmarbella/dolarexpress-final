#!/usr/bin/env python3
"""
run_seo_overhaul.py - SEO Overhaul completo para DolarExpress
Ejecuta 5 tareas en orden: Backup, Fix vercel.json, Fix WhatsApp buttons,
Fix canonical URLs, Interlinking semantico.

Uso: python run_seo_overhaul.py
Ejecutar desde la raiz del repositorio (dolarexpress-final/)
"""

import os
import re
import json
import shutil
import glob
from datetime import datetime
from pathlib import Path

# --- CONFIGURACION -----------------------------------------------------------
BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_DIR = BASE_DIR / "public"
REPORTS_DIR = BASE_DIR / "reports"
EXCLUDED_FILES = {"index.html", "venta-usd.html", "terminos.html", "privacidad.html"}
EXCLUDED_DIRS = {"widget", "directorio-general"}
WHATSAPP_NUMBER = "56967658939"
WHATSAPP_TEXT = "Hola%2C%20tengo%20cupo%20en%20d%C3%B3lares%20y%20quiero%20cotizar"
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUMBER}?text={WHATSAPP_TEXT}"
DOMAIN = "https://www.dolarexpress.cl"

# Colores CSS del diseno
CSS_SEMANTIC_LINKS = """
.semantic-links { background: #f5f5f5; padding: 2rem 1rem; margin-top: 2rem; border-radius: 8px; }
.semantic-links h3 { color: #1a1a2e; font-size: 1.25rem; margin-bottom: 1rem; }
.semantic-links ul { list-style: none; padding: 0; }
.semantic-links li { margin-bottom: 0.5rem; }
.semantic-links a { color: #00b159; text-decoration: none; font-weight: 500; }
.semantic-links a:hover { color: #007a3d; text-decoration: underline; }
"""

# Bancos conocidos
BANCOS = [
    "banco-chile", "bancoestado", "bci", "santander", "scotiabank",
    "itau", "bice", "security", "banco-estado", "bancochile",
    "falabella", "cencosud", "american-express", "amex"
]

# Retails conocidos
RETAILS = ["cmr", "ripley", "paris", "lider", "hites", "abcdin", "jumbo", "easy", "la-polar", "johnson"]

# Ciudades conocidas
CIUDADES = [
    "santiago", "valparaiso", "vina-del-mar", "concepcion", "antofagasta",
    "la-serena", "iquique", "temuco", "rancagua", "puerto-montt",
    "arica", "calama", "copiapo", "chillan", "osorno", "punta-arenas",
    "las-condes", "providencia"
]

# Montos conocidos
MONTOS = [200, 500, 1000, 2000, 3000, 5000, 7000]

# Intenciones informativas
INTENCION_INFO = ["que-es", "como-funciona", "es-legal", "confiable", "conviene", "riesgos", "requisitos"]

# Intenciones transaccionales
INTENCION_TRANS = ["vender", "liquidar", "convertir", "necesito-plata", "cambiar", "cambio", "compra", "compro", "comprar"]

# Marcas de tarjetas
TARJETAS = ["visa", "mastercard", "amex", "american-express"]

# Tipos de tarjeta
TIPOS_TARJETA = ["gold", "platinum", "black", "signature"]


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def get_all_html_files():
    """Retorna lista de archivos .html en /public/ (no recursivo)"""
    files = []
    for f in PUBLIC_DIR.glob("*.html"):
        if f.name not in EXCLUDED_FILES:
            files.append(f)
    return sorted(files)


def slug_from_filename(filename):
    """Convierte nombre de archivo a slug URL"""
    return filename.replace(".html", "")


def url_for(filename):
    """Genera URL absoluta para un archivo"""
    slug = slug_from_filename(filename)
    return f"{DOMAIN}/{slug}/"


def extract_page_name(filename):
    """Extrae nombre descriptivo de pagina desde filename"""
    name = filename.replace(".html", "").replace("-", " ").title()
    # Reemplazos comunes
    replacements = {
        "Cupo Dolar": "Cupo Dolar",
        "Banco Chile": "Banco de Chile",
        "Bancoestado": "BancoEstado",
        "Bci": "BCI",
        "Itau": "Itau",
        "Cmr": "CMR",
        "Usd": "USD",
        "Clp": "CLP",
        "Ame x": "Amex",
        "Vina Del Mar": "Vina del Mar",
        "La Serena": "La Serena",
        "La Polar": "La Polar",
        "Puerto Montt": "Puerto Montt",
        "Punta Arenas": "Punta Arenas",
        "Las Condes": "Las Condes",
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    return name


def classify_page(filename):
    """
    Clasifica una pagina segun su contenido semantico.
    Retorna dict con categorias detectadas.
    """
    slug = slug_from_filename(filename)
    slug_lower = slug.lower()
    result = {
        "bancos": [],
        "retails": [],
        "ciudades": [],
        "monto": None,
        "es_info": False,
        "es_transaccional": False,
        "es_tarjeta": False,
        "tipo_tarjeta": None,
        "slug": slug,
        "filename": filename,
    }

    for banco in BANCOS:
        if banco in slug_lower:
            result["bancos"].append(banco)

    for retail in RETAILS:
        if retail in slug_lower:
            result["retails"].append(retail)

    for ciudad in CIUDADES:
        if ciudad in slug_lower:
            result["ciudades"].append(ciudad)

    for monto in MONTOS:
        if str(monto) in slug_lower:
            result["monto"] = monto

    for info in INTENCION_INFO:
        if info in slug_lower:
            result["es_info"] = True

    for trans in INTENCION_TRANS:
        if trans in slug_lower:
            result["es_transaccional"] = True

    for tarjeta in TARJETAS:
        if tarjeta in slug_lower:
            result["es_tarjeta"] = True

    for tipo in TIPOS_TARJETA:
        if tipo in slug_lower:
            result["tipo_tarjeta"] = tipo

    return result


def find_related_pages(page_class, all_pages_classes):
    """
    Encuentra paginas relacionadas segun la clasificacion semantica.
    Retorna lista de (filename, anchor_text) para interlinking.
    """
    related = []
    slug = page_class["slug"]
    candidates = [p for p in all_pages_classes if p["slug"] != slug]

    # 1. Si tiene banco -> enlazar a pagina madre del banco, ciudades, transaccional
    if page_class["bancos"]:
        for banco in page_class["bancos"]:
            madre_slug = f"cupo-dolar-{banco}"
            for c in candidates:
                if c["slug"] == madre_slug:
                    related.append((c["filename"], f"Todo sobre el cupo dolar {banco.replace('-', ' ').title()}"))
                    break

            # Ciudades del mismo banco (maximo 2)
            ciudad_count = 0
            for c in candidates:
                if ciudad_count >= 2:
                    break
                if banco in c["slug"] and c["ciudades"] and c["slug"] not in [r[0].replace(".html", "") for r in related]:
                    ciudad = c["ciudades"][0].replace("-", " ").title()
                    related.append((c["filename"], f"Cupo dolar {banco.replace('-', ' ').title()} en {ciudad}"))
                    ciudad_count += 1

            # Intencion transaccional del mismo banco
            for c in candidates:
                if banco in c["slug"] and c["es_transaccional"]:
                    related.append((c["filename"], f"Vende tu cupo {banco.replace('-', ' ').title()} y recibe efectivo hoy"))
                    break

    # 2. Si tiene retail -> enlazar a pagina madre, variantes, comparativa
    if page_class["retails"]:
        for retail in page_class["retails"]:
            madre_slug = f"cupo-dolar-{retail}"
            for c in candidates:
                if c["slug"] == madre_slug:
                    related.append((c["filename"], f"Guia completa del cupo dolar {retail.upper()}"))
                    break

            # Variantes (cuanto-presta, sin-avance)
            for c in candidates:
                if retail in c["slug"] and ("cuanto-presta" in c["slug"] or "sin-avance" in c["slug"] or "plata-rapido" in c["slug"]):
                    if len(related) < 6:
                        related.append((c["filename"], f"Cuanto te presta {retail.upper()}? Descubrelo aqui"))

    # 3. Si tiene ciudad -> enlazar a pagina regional y otros bancos en esa ciudad
    if page_class["ciudades"]:
        for ciudad in page_class["ciudades"]:
            regional_slug = "cupo-dolar-regiones-chile"
            for c in candidates:
                if c["slug"] == regional_slug:
                    related.append((c["filename"], f"Servicio de cupo dolar disponible en todas las regiones de Chile"))
                    break

            # Otros bancos en la misma ciudad
            for c in candidates:
                if ciudad in c["slug"] and c["bancos"] and c["slug"] != slug:
                    banco_nombre = c["bancos"][0].replace("-", " ").title()
                    ciudad_nombre = ciudad.replace("-", " ").title()
                    related.append((c["filename"], f"Cupo dolar {banco_nombre} tambien disponible en {ciudad_nombre}"))

    # 4. Si tiene monto -> enlazar a montos adyacentes y monto minimo
    if page_class["monto"]:
        monto = page_class["monto"]
        montos_adyacentes = [m for m in MONTOS if abs(m - monto) <= 1000 and m != monto]
        for m in montos_adyacentes[:2]:
            m_slug = f"cupo-dolar-{m}-usd"
            for c in candidates:
                if c["slug"] == m_slug:
                    related.append((c["filename"], f"Convierte ${m} USD a pesos chilenos con nosotros"))
                    break

        # Monto minimo
        for c in candidates:
            if c["slug"] == "cupo-dolar-monto-minimo":
                related.append((c["filename"], "Cual es el monto minimo para operar? Descubrelo"))
                break

    # 5. Si es informativa -> enlazar a transaccionales y venta-usd
    if page_class["es_info"]:
        for c in candidates:
            if c["es_transaccional"]:
                related.append((c["filename"], "Convierte tu cupo en efectivo hoy mismo - cotiza sin compromiso"))
                break
        # venta-usd
        related.append(("venta-usd.html", "Cotiza ahora tu cupo dolar por WhatsApp y recibe tu dinero en minutos"))

    # 6. Si es transaccional -> enlazar a informativas y venta-usd
    if page_class["es_transaccional"]:
        for c in candidates:
            if c["es_info"]:
                related.append((c["filename"], "Resuelve todas tus dudas sobre el cupo dolar antes de operar"))
                break
        if not any("venta-usd" in r[0] for r in related):
            related.append(("venta-usd.html", "Cotiza tu cupo dolar ahora - proceso 100% online y rapido"))

    # 7. Si tiene tarjeta (visa, mastercard) -> enlazar a pagina madre
    if page_class["es_tarjeta"]:
        for c in candidates:
            if c["slug"] == f"cupo-dolar-{page_class['slug'].split('-')[0]}":
                related.append((c["filename"], f"Informacion completa sobre cupo dolar {page_class['slug'].split('-')[0].title()}"))

    # 8. Si tiene tipo de tarjeta (gold, platinum, etc.)
    if page_class["tipo_tarjeta"]:
        tipo = page_class["tipo_tarjeta"]
        for c in candidates:
            if c["slug"] == f"cupo-dolar-{tipo}":
                related.append((c["filename"], f"Beneficios del cupo dolar tarjeta {tipo.title()}"))

    # Fallback: si no hay suficientes relacionados, agregar genericos
    if len(related) < 4:
        fallbacks = [
            ("cupo-dolar-como-funciona.html", "Como funciona el cupo dolar? Te explicamos paso a paso"),
            ("cupo-dolar-requisitos.html", "Requisitos para vender tu cupo dolar - enterate aqui"),
            ("cupo-dolar-confiable.html", "Es confiable vender el cupo dolar? Respondemos tus dudas"),
            ("cupo-dolar-rapido.html", "Cupo dolar rapido: recibe tu dinero en 15 minutos"),
        ]
        for fb_slug, fb_text in fallbacks:
            if len(related) >= 6:
                break
            fb_filename = fb_slug
            if not any(fb_filename in r[0] for r in related):
                related.append((fb_filename, fb_text))

    # Limitar a maximo 6, minimo 4
    related = related[:6]

    # Generar anchor texts variados si hay duplicados
    seen_texts = set()
    unique_related = []
    for filename, text in related:
        if text not in seen_texts:
            seen_texts.add(text)
            unique_related.append((filename, text))
        else:
            # Generar variante
            variants = [
                f"Mas informacion sobre {extract_page_name(filename)}",
                f"Conoce mas sobre {extract_page_name(filename)}",
                f"Tambien te puede interesar: {extract_page_name(filename)}",
            ]
            for v in variants:
                if v not in seen_texts:
                    seen_texts.add(v)
                    unique_related.append((filename, v))
                    break

    return unique_related[:6]


# ==============================================================================
# TAREA 1: Backup y preparacion
# ==============================================================================
def tarea1_backup():
    log("=" * 60)
    log("TAREA 1: Backup y preparacion")
    log("=" * 60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BASE_DIR / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Copiar todo /public/
    shutil.copytree(PUBLIC_DIR, backup_dir / "public", dirs_exist_ok=True)
    log(f"[OK] Backup creado en: {backup_dir}/")

    # Crear reports/
    REPORTS_DIR.mkdir(exist_ok=True)
    log(f"[OK] Directorio reports/ listo")

    return backup_dir


# ==============================================================================
# TAREA 2: Fix vercel.json
# ==============================================================================
def tarea2_fix_vercel():
    log("=" * 60)
    log("TAREA 2: Fix vercel.json")
    log("=" * 60)

    vercel_path = BASE_DIR / "vercel.json"
    if not vercel_path.exists():
        log("[ERR] vercel.json no encontrado")
        return

    with open(vercel_path, "r", encoding="utf-8") as f:
        original = f.read()

    log(f"[INFO] vercel.json actual: {original.strip()}")

    # Generar lista de rutas .html existentes
    html_files = get_all_html_files()
    html_routes = []
    for f in html_files:
        slug = slug_from_filename(f.name)
        html_routes.append({
            "source": f"/{slug}",
            "destination": f"/{slug}.html"
        })

    # Nuevo vercel.json
    new_config = {
        "buildCommand": "vite build && node copy-html-files.js",
        "outputDirectory": "dist",
        "rewrites": [
            # Redirigir /page.html -> /page/ (301)
            {"source": "/(.*)\\.html", "destination": "/$1/", "permanent": True},
            # Rutas especificas para archivos .html existentes
            *html_routes,
            # Fallback solo para rutas que no existen como archivos estaticos
            {"source": "/(.*)", "destination": "/index.html"}
        ]
    }

    with open(vercel_path, "w", encoding="utf-8") as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)

    log(f"[OK] vercel.json actualizado con {len(html_routes)} rutas .html explicitas")
    log(f"[INFO] Nuevo contenido:")
    log(json.dumps(new_config, indent=2, ensure_ascii=False))


# ==============================================================================
# TAREA 3: Fix botones WhatsApp
# ==============================================================================
def tarea3_fix_whatsapp():
    log("=" * 60)
    log("TAREA 3: Fix botones WhatsApp")
    log("=" * 60)

    files = get_all_html_files()
    report = {
        "total_archivos": len(files),
        "archivos_modificados": [],
        "enlaces_reemplazados": 0,
        "errores": []
    }

    # Patrones de enlaces a venta-usd en contexto de boton CTA
    cta_patterns = [
        r'(<a\s[^>]*class="[^"]*(?:btn|cta|whatsapp|ws|header)[^"]*"[^>]*href="https?://[^"]*venta-usd[^"]*"[^>]*>)',
        r'(<a\s[^>]*href="https?://[^"]*venta-usd[^"]*"[^>]*class="[^"]*(?:btn|cta|whatsapp|ws|header)[^"]*"[^>]*>)',
        r'(<a\s[^>]*href="/venta-usd[^"]*"[^>]*class="[^"]*(?:btn|cta|whatsapp|ws|header)[^"]*"[^>]*>)',
        r'(<a\s[^>]*class="[^"]*(?:btn|cta|whatsapp|ws|header)[^"]*"[^>]*href="/venta-usd[^"]*"[^>]*>)',
        r'(<a\s[^>]*href="venta-usd\.html[^"]*"[^>]*class="[^"]*(?:btn|cta|whatsapp|ws|header)[^"]*"[^>]*>)',
        r'(<a\s[^>]*class="[^"]*(?:btn|cta|whatsapp|ws|header)[^"]*"[^>]*href="venta-usd\.html[^"]*"[^>]*>)',
    ]

    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content
            changes = 0

            # Reemplazar enlaces CTA que apuntan a venta-usd
            for pattern in cta_patterns:
                def replace_cta(match, ch=changes):
                    nonlocal changes
                    full_tag = match.group(1)
                    # Reemplazar el href manteniendo todo lo demas
                    new_tag = re.sub(
                        r'href="[^"]*venta-usd[^"]*"',
                        f'href="{WHATSAPP_URL}"',
                        full_tag
                    )
                    if new_tag != full_tag:
                        changes += 1
                    return new_tag

                content, count = re.subn(pattern, replace_cta, content)
                changes += count

            # Tambien buscar enlaces directos a venta-usd en secciones hero, cta-final, header
            section_patterns = [
                (r'(<section class="hero">.*?)</section>', re.DOTALL),
                (r'(<section class="cta-final">.*?)</section>', re.DOTALL),
                (r'(<header>.*?)</header>', re.DOTALL),
            ]

            for section_pat, flags in section_patterns:
                def replace_section_links(match, ch=changes):
                    section_content = match.group(1)
                    new_section = re.sub(
                        r'href="[^"]*venta-usd[^"]*"',
                        f'href="{WHATSAPP_URL}"',
                        section_content
                    )
                    if new_section != section_content:
                        nonlocal changes
                        changes += 1
                    return new_section

                content = re.sub(section_pat, replace_section_links, content, flags=flags)

            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                report["archivos_modificados"].append(filepath.name)
                report["enlaces_reemplazados"] += changes
                log(f"  [OK] {filepath.name}: {changes} enlace(s) reemplazado(s)")

        except Exception as e:
            report["errores"].append({"archivo": filepath.name, "error": str(e)})
            log(f"  [ERR] Error en {filepath.name}: {e}")

    # Guardar reporte
    report_path = REPORTS_DIR / "report_whatsapp_fix.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    log(f"\n[INFO] Reporte WhatsApp guardado en: {report_path}")
    log(f"   Archivos modificados: {len(report['archivos_modificados'])}")
    log(f"   Enlaces reemplazados: {report['enlaces_reemplazados']}")
    if report["errores"]:
        log(f"   Errores: {len(report['errores'])}")

    return report


# ==============================================================================
# TAREA 4: Fix canonical URLs
# ==============================================================================
def tarea4_fix_canonical():
    log("=" * 60)
    log("TAREA 4: Fix canonical URLs")
    log("=" * 60)

    files = get_all_html_files()
    # Tambien incluir index.html y venta-usd.html para canonicos
    all_files = list(files)
    for extra in ["index.html", "venta-usd.html"]:
        extra_path = PUBLIC_DIR / extra
        if extra_path.exists():
            all_files.append(extra_path)

    report = {
        "total_archivos": len(all_files),
        "canonical_fix_index": 0,
        "canonical_fix_html": 0,
        "ogurl_fix_index": 0,
        "ogurl_fix_html": 0,
        "archivos_modificados": [],
        "errores": []
    }

    for filepath in all_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content
            filename = filepath.name

            # 1. Fix <link rel="canonical" href=".../index/"> -> .../
            content, count_index = re.subn(
                r'(<link\s+rel="canonical"\s+href="[^"]*/)index/(")',
                r'\1\2',
                content
            )
            report["canonical_fix_index"] += count_index

            # 2. Fix <link rel="canonical" href=".../.html"> -> .../
            content, count_html = re.subn(
                r'(<link\s+rel="canonical"\s+href="[^"]*)\.html(")',
                r'\1/\2',
                content
            )
            report["canonical_fix_html"] += count_html

            # 3. Fix <meta property="og:url" content=".../index/"> -> .../
            content, count_og_index = re.subn(
                r'(<meta\s+property="og:url"\s+content="[^"]*/)index/(")',
                r'\1\2',
                content
            )
            report["ogurl_fix_index"] += count_og_index

            # 4. Fix <meta property="og:url" content=".../.html"> -> .../
            content, count_og_html = re.subn(
                r'(<meta\s+property="og:url"\s+content="[^"]*)\.html(")',
                r'\1/\2',
                content
            )
            report["ogurl_fix_html"] += count_og_html

            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                report["archivos_modificados"].append(filename)
                total_fixes = count_index + count_html + count_og_index + count_og_html
                log(f"  [OK] {filename}: {total_fixes} fix(es) aplicado(s)")

        except Exception as e:
            report["errores"].append({"archivo": filepath.name, "error": str(e)})
            log(f"  [ERR] Error en {filepath.name}: {e}")

    # Guardar reporte
    report_path = REPORTS_DIR / "report_canonical_fix.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    log(f"\n[INFO] Reporte Canonical guardado en: {report_path}")
    log(f"   Archivos modificados: {len(report['archivos_modificados'])}")
    log(f"   Canonical /index/ -> /: {report['canonical_fix_index']}")
    log(f"   Canonical .html -> /: {report['canonical_fix_html']}")
    log(f"   OG:url /index/ -> /: {report['ogurl_fix_index']}")
    log(f"   OG:url .html -> /: {report['ogurl_fix_html']}")

    return report


# ==============================================================================
# TAREA 5: Interlinking semantico
# ==============================================================================
def tarea5_interlinking():
    log("=" * 60)
    log("TAREA 5: Interlinking semantico")
    log("=" * 60)

    files = get_all_html_files()
    # Clasificar todas las paginas
    all_pages_classes = [classify_page(f.name) for f in files]

    report = {
        "total_archivos": len(files),
        "archivos_modificados": [],
        "total_enlaces_agregados": 0,
        "errores": []
    }

    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content
            filename = filepath.name
            page_class = classify_page(filename)

            # Verificar si ya existe interlinking (idempotencia)
            if 'data-interlink="semantic"' in content:
                log(f"  [SKIP] {filename}: ya tiene interlinking, saltando")
                continue

            # Encontrar paginas relacionadas
            related = find_related_pages(page_class, all_pages_classes)

            if not related:
                log(f"  [SKIP] {filename}: no se encontraron paginas relacionadas")
                continue

            # Generar HTML de interlinking
            links_html = ""
            for rel_filename, anchor_text in related:
                rel_slug = slug_from_filename(rel_filename)
                rel_url = f"{DOMAIN}/{rel_slug}/"
                links_html += f'          <li><a href="{rel_url}" data-interlink="semantic">{anchor_text}</a></li>\n'

            interlinking_html = f"""
<nav aria-label="Enlaces relacionados" class="semantic-links">
  <h3>Tambien te puede interesar</h3>
  <ul>
{links_html}  </ul>
</nav>"""

            # Insertar antes del footer o al final del main
            if "</footer>" in content:
                insert_pos = content.rfind("</footer>")
                content = content[:insert_pos] + interlinking_html + "\n" + content[insert_pos:]
            elif "</body>" in content:
                insert_pos = content.rfind("</body>")
                content = content[:insert_pos] + interlinking_html + "\n" + content[insert_pos:]
            else:
                log(f"  [WARN] {filename}: no se encontro </footer> ni </body>, saltando")
                continue

            # Agregar CSS si no existe
            if ".semantic-links" not in content:
                # Insertar antes de </head>
                css_html = f"<style>{CSS_SEMANTIC_LINKS}</style>\n"
                content = content.replace("</head>", css_html + "</head>")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            report["archivos_modificados"].append(filename)
            report["total_enlaces_agregados"] += len(related)
            log(f"  [OK] {filename}: {len(related)} enlace(s) agregado(s)")

        except Exception as e:
            report["errores"].append({"archivo": filepath.name, "error": str(e)})
            log(f"  [ERR] Error en {filepath.name}: {e}")

    # Guardar reporte
    report_path = REPORTS_DIR / "report_interlinking.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    log(f"\n[INFO] Reporte Interlinking guardado en: {report_path}")
    log(f"   Archivos modificados: {len(report['archivos_modificados'])}")
    log(f"   Total enlaces agregados: {report['total_enlaces_agregados']}")

    return report


# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  DolarExpress SEO Overhaul")
    print(f"  Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")

    # Tarea 1
    backup_dir = tarea1_backup()
    print()

    # Tarea 2
    tarea2_fix_vercel()
    print()

    # Tarea 3
    tarea3_fix_whatsapp()
    print()

    # Tarea 4
    tarea4_fix_canonical()
    print()

    # Tarea 5
    tarea5_interlinking()
    print()

    print("=" * 60)
    print("  SEO Overhaul completado exitosamente")
    print(f"  Backup en: {backup_dir}/")
    print(f"  Reportes en: {REPORTS_DIR}/")
    print("=" * 60 + "\n")
