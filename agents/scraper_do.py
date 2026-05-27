"""
agents/scraper_do.py - Nodo 1: OSINT / Google Dorking sobre el Diario Oficial
Estrategia:
  Usa DuckDuckGo para buscar: site:diariooficial.interior.gob.cl "RUT"
  Separa resultados en URLs HTML (se visitan con Playwright) y PDFs (se registran).
  Extrae texto bruto de cada pagina HTML visitada.
  Incluye delays y reintentos para evitar rate-limiting de DuckDuckGo.
  No usa BeautifulSoup ni limpieza - el LLM downstream estructura los datos.
"""

import asyncio
import re
import time
from ddgs import DDGS
from playwright.async_api import async_playwright


def formatear_ruts(rut_original: str) -> list:
    """Genera variantes del RUT para maximizar resultados."""
    solo_numeros = re.sub(r"[^0-9Kk]", "", rut_original)
    if len(solo_numeros) <= 1:
        return [rut_original]
    
    cuerpo = solo_numeros[:-1]
    dv = solo_numeros[-1]
    
    variantes = set()
    variantes.add(rut_original.strip())
    variantes.add(f"{cuerpo}-{dv}")
    cuerpo_formateado = ""
    for i, ch in enumerate(reversed(cuerpo)):
        if i > 0 and i % 3 == 0:
            cuerpo_formateado = "." + cuerpo_formateado
        cuerpo_formateado = ch + cuerpo_formateado
    variantes.add(f"{cuerpo_formateado}-{dv}")
    
    return list(variantes)


def buscar_en_duckduckgo(query: str, max_resultados: int = 20, intento: int = 1) -> list:
    """
    Busca en DuckDuckGo con reintentos y backoff.
    Retorna lista de URLs.
    """
    urls = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_resultados):
                url = r.get("href", "")
                if url and "diariooficial.interior.gob.cl" in url:
                    urls.append(url)
    except Exception as e:
        error_str = str(e)
        if "No results found" in error_str and intento <= 3:
            espera = intento * 3  # 3, 6, 9 segundos
            print(f"  [!] Rate limit (intento {intento}/3). Esperando {espera}s...")
            time.sleep(espera)
            return buscar_en_duckduckgo(query, max_resultados, intento + 1)
        print(f"  [!] Error en busqueda DuckDuckGo: {e}")
    return urls


def clasificar_urls(urls: list) -> tuple:
    """Separa URLs en HTML (para visitar) y PDF (para registrar)."""
    htmls = []
    pdfs = []
    for url in urls:
        url_lower = url.lower()
        if url_lower.endswith(".pdf"):
            pdfs.append(url)
        else:
            htmls.append(url)
    return htmls, pdfs


async def extraer_texto_url(page, url: str) -> str:
    """Navega a una URL HTML y extrae el texto visible del body."""
    try:
        await page.goto(url, timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)
        texto = await page.inner_text("body")
        return texto
    except Exception as e:
        print(f"  [!] Error al visitar {url}: {e}")
        return ""


async def node_diario_oficial(state: dict) -> dict:
    """
    Nodo de LangGraph: Busca menciones del RUT en el DO usando Google Dorking
    via DuckDuckGo, visita cada resultado HTML y extrae el texto bruto.
    """
    rut_objetivo = state.get("rut_objetivo")
    if not rut_objetivo:
        return {"errores": "RUT objetivo no proporcionado"}

    print(f"[+] Buscando RUT {rut_objetivo} en Diario Oficial via DuckDuckGo...")

    # -- 1. Generar variantes del RUT y buscar ------------------------------
    variantes_rut = formatear_ruts(rut_objetivo)
    print(f"  Variantes de RUT a buscar: {variantes_rut}")

    todas_las_urls = set()
    for i, variante in enumerate(variantes_rut):
        if i > 0:
            # Delay entre consultas para evitar rate-limiting
            print("  Esperando 2s entre consultas...")
            time.sleep(2)
        
        query = f'site:diariooficial.interior.gob.cl "{variante}"'
        print(f"  Buscando: {query}")
        urls = buscar_en_duckduckgo(query, max_resultados=20)
        print(f"    -> {len(urls)} resultados encontrados")
        for u in urls:
            todas_las_urls.add(u)

    if not todas_las_urls:
        print("[-] No se encontraron resultados en el DO para este RUT")
        return {
            "text_bruto_do": "",
            "enlaces_pdfs_do": [],
            "urls_encontradas_do": []
        }

    # -- 2. Separar HTMLs de PDFs -------------------------------------------
    urls_html, urls_pdf = clasificar_urls(sorted(todas_las_urls))
    print(f"\n[+] Total URLs unicas: {len(todas_las_urls)}")
    print(f"    HTMLs para visitar: {len(urls_html)}")
    print(f"    PDFs (solo registro): {len(urls_pdf)}")

    for u in urls_html:
        print(f"    HTML: {u}")
    for u in urls_pdf:
        print(f"    PDF:  {u}")

    # -- 3. Visitar cada URL HTML y extraer texto ---------------------------
    textos_por_url = {}
    todos_los_pdfs = set(urls_pdf)

    if urls_html:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = await context.new_page()

            for i, url in enumerate(urls_html):
                print(f"\n  [{i+1}/{len(urls_html)}] Visitando: {url}")
                texto = await extraer_texto_url(page, url)
                if texto:
                    textos_por_url[url] = texto
                    print(f"    -> {len(texto)} caracteres extraidos")
                    try:
                        pdfs = await page.eval_on_selector_all(
                            "a[href*='.pdf']",
                            "elements => elements.map(e => e.href)"
                        )
                        for pdf in pdfs:
                            todos_los_pdfs.add(pdf)
                    except Exception:
                        pass
                else:
                    print(f"    -> Sin texto extraido")

            await browser.close()
    else:
        print("\n  No hay URLs HTML para visitar.")

    # -- 4. Consolidar resultados -------------------------------------------
    texto_consolidado = ""
    for url, texto in textos_por_url.items():
        texto_consolidado += f"\n{'='*60}\n"
        texto_consolidado += f"FUENTE: {url}\n"
        texto_consolidado += f"{'='*60}\n"
        texto_consolidado += texto
        texto_consolidado += "\n"

    print(f"\n[+] Resumen final:")
    print(f"  URLs HTML visitadas: {len(urls_html)}")
    print(f"  URLs con texto extraido: {len(textos_por_url)}")
    print(f"  Texto total consolidado: {len(texto_consolidado)} caracteres")
    print(f"  PDFs encontrados (directos + desde HTML): {len(todos_los_pdfs)}")

    return {
        "text_bruto_do": texto_consolidado,
        "enlaces_pdfs_do": sorted(todos_los_pdfs),
        "urls_encontradas_do": sorted(todas_las_urls)
    }


# -- BLOQUE DE PRUEBA LOCAL ------------------------------------------------------
if __name__ == "__main__":
    import sys
    rut = sys.argv[1] if len(sys.argv) > 1 else "76.432.324-4"
    estado_prueba = {"rut_objetivo": rut}
    resultado = asyncio.run(node_diario_oficial(estado_prueba))
    
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    texto = resultado.get("text_bruto_do", "")
    print(f"Longitud del texto bruto: {len(texto)} caracteres")
    print(f"PDFs encontrados: {len(resultado.get('enlaces_pdfs_do', []))}")
    print(f"URLs encontradas: {len(resultado.get('urls_encontradas_do', []))}")
    
    if resultado.get("errores"):
        print(f"ERRORES: {resultado['errores']}")
    
    if texto:
        print("\n--- PRIMERAS 30 LINEAS ---")
        for i, linea in enumerate(texto.split("\n")[:30]):
            print(f"  {linea}")
