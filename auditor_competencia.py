import requests
import sys
from bs4 import BeautifulSoup

def extraer_competencia(url):
    # Validar que la URL sea correcta
    if not url.startswith("http"):
        url = "https://" + url

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        print(f"\n[*] Analizando objetivo: {url}")
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Limpieza de ruido visual
        for s in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            s.decompose()
        
        texto_limpio = soup.get_text(separator=' ', strip=True)
        
        # Nombre de archivo dinámico basado en el dominio
        nombre_archivo = "analisis_target.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(f"REPORTE DE EXTRACCIÓN - ORIGEN: {url}\n")
            f.write("="*50 + "\n")
            f.write(texto_limpio)
            
        print(f"[+] ÉXITO: Datos guardados en '{nombre_archivo}'")
        print("[*] Instrucción: Copia el contenido de ese archivo a tu LLM preferida.")

    except Exception as e:
        print(f"[!] ERROR al acceder a {url}: {e}")

if __name__ == "__main__":
    # Si pasas la URL por comando: python auditor_competencia.py google.com
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # Si no, te la pide al ejecutar
        target = input("Ingresa el dominio o URL a analizar: ")
    
    extraer_competencia(target)