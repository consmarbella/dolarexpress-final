"""
agents/descargar_pdfs_do.py
Descarga todos los PDFs del Diario Oficial encontrados para un RUT.
Los guarda en: agents/pdfs_do/{RUT}/

Uso:
  python agents/descargar_pdfs_do.py 80172508          # Busca y descarga
  python agents/descargar_pdfs_do.py 80172508 --direct  # Solo descarga (usa URLs ya conocidas)
"""

import asyncio
import os
import sys
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.scraper_do import node_diario_oficial


# URLs conocidas para RUT 80172508 (cacheadas para --direct)
PDFS_CONOCIDOS_80172508 = [
    "https://www.diariooficial.interior.gob.cl/publicaciones/2017/05/10/41753/01/1212250.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2018/03/08/42002/01/1362487.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2018/05/24/42064/01/1401780.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2021/01/27/42865/01/1885842.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2022/11/28/43412/01/2223508.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2022/12/07/43420/01/2229408.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2023/03/08/43496/01/2282505.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2023/03/15/43502-B/01/2286986.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2023/06/02/43567/01/2323248.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/03/14/43801/01/2465917.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/04/08/43820/01/2475725.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/04/16/43827/01/2479734.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/04/27/43837/01/2484983.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/08/08/43920/01/2528080.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/08/08/43920/01/2528448.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/08/20/43929/01/2532815.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/10/09/43969/01/2553196.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/10/24/43982-B/01/2561825.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2024/12/06/44017/01/2580516.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/01/16/44050/01/2596006.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/01/16/44050/01/2596247.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/02/03/44065/01/2602506.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/02/13/44074/01/2608415.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/04/12/44124/01/2631205.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/05/23/44155/01/2647308.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/05/30/44161/01/2651280.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/06/25/44182/01/2662210.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/06/28/44185/01/2666088.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/17/44200/01/2668555.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/18/44201/01/2671968.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/24/44206/01/2674464.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/07/29/44210/01/2676741.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/08/14/44225/01/2683072.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/08/26/44234/01/2688492.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/08/28/44236/01/2691712.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/08/29/44237/01/2690926.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/08/29/44237/01/2692526.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/09/25/44258/01/2702453.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/11/04/44290/01/2720363.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/11/05/44291/01/2721285.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/11/06/44292/01/2719890.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/11/08/44294/01/2724901.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/11/14/44299/01/2727229.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2025/12/17/44326-B/01/2743431.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/01/26/44359/01/2755406.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/02/21/44382/01/2772573.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/03/03/44390/01/2772404.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/04/08/44419/01/2793142.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/04/08/44419/01/2794503.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/04/09/44420/01/2788270.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/04/22/44431/01/2796789.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/04/24/44433/01/2801433.pdf",
    "https://www.diariooficial.interior.gob.cl/publicaciones/2026/05/08/44444/01/2808701.pdf",
]


def descargar_pdf(url: str, ruta_destino: str) -> bool:
    """Descarga un PDF desde una URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        
        with open(ruta_destino, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"  [!] Error descargando {url}: {e}")
        return False


def nombre_archivo(url: str) -> str:
    """Extrae un nombre legible de la URL del PDF."""
    partes = url.split("/")
    if len(partes) >= 7:
        fecha = f"{partes[-6]}-{partes[-5]}-{partes[-4]}"
        return f"{fecha}_{partes[-1]}"
    return url.split("/")[-1]


async def main():
    rut = sys.argv[1] if len(sys.argv) > 1 else "80172508"
    modo_directo = "--direct" in sys.argv
    
    if modo_directo and rut == "80172508":
        print(f"[+] Usando URLs cacheadas para RUT {rut}")
        pdfs = PDFS_CONOCIDOS_80172508
    else:
        print(f"[+] Buscando PDFs para RUT {rut}...")
        resultado = await node_diario_oficial({"rut_objetivo": rut})
        pdfs = resultado.get("enlaces_pdfs_do", [])
    
    if not pdfs:
        print("[-] No se encontraron PDFs para descargar.")
        return
    
    # Crear carpeta de destino
    rut_limpio = rut.replace(".", "").replace("-", "")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(script_dir, "pdfs_do", rut_limpio)
    os.makedirs(carpeta, exist_ok=True)
    
    print(f"\n[+] Descargando {len(pdfs)} PDFs a: {carpeta}")
    print("=" * 60)
    
    exitosos = 0
    for i, url in enumerate(pdfs):
        nombre = nombre_archivo(url)
        ruta_pdf = os.path.join(carpeta, nombre)
        
        # Saltar si ya existe
        if os.path.exists(ruta_pdf):
            tamano = os.path.getsize(ruta_pdf)
            print(f"  [{i+1}/{len(pdfs)}] {nombre} -> YA EXISTE ({tamano/1024:.0f} KB)")
            exitosos += 1
            continue
        
        print(f"  [{i+1}/{len(pdfs)}] {nombre}")
        if descargar_pdf(url, ruta_pdf):
            exitosos += 1
            tamano = os.path.getsize(ruta_pdf)
            print(f"    -> OK ({tamano/1024:.0f} KB)")
        else:
            print(f"    -> FALLO")
    
    print(f"\n[+] Resumen: {exitosos}/{len(pdfs)} PDFs descargados en:")
    print(f"    {carpeta}")
    
    # Mostrar el ultimo (mas reciente)
    if exitosos > 0:
        ultimo = sorted(os.listdir(carpeta))[-1]
        print(f"\n[+] Ultimo PDF descargado: {ultimo}")
        print(f"    Abrelo con: start {os.path.join(carpeta, ultimo)}")


if __name__ == "__main__":
    asyncio.run(main())
