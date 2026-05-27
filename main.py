"""
main.py — Punto de entrada del pipeline pSEO con LangGraph + Gemini 1.5 Flash

Uso:
    python main.py --url https://atlascash.cl --client dolarexpress.cl
    python main.py --batch clientes_ejemplo.csv --workers 3
    python main.py --url https://competidor.cl --client agnt.cl --context "fintech cupo dólar"
"""

import argparse
import csv
import json
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Cargar .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Validar dependencias
try:
    from langgraph.graph import StateGraph
except ImportError:
    print("ERROR: LangGraph no instalado. Ejecuta: pip install -r requirements.txt")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai no instalado. Ejecuta: pip install openai")
    sys.exit(1)

# Validar API key antes de arrancar
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("\n[ERROR] DEEPSEEK_API_KEY no configurada.")
    print("Opciones:")
    print("  1. Crea un archivo .env en esta carpeta con:  DEEPSEEK_API_KEY=sk-...")
    print("  2. Windows PowerShell:  $env:DEEPSEEK_API_KEY = 'sk-...'")
    print("  3. Mac/Linux:           export DEEPSEEK_API_KEY='sk-...'")
    sys.exit(1)

from graph import run_pseo_pipeline


def run_single(target_url: str, client_domain: str, niche_context: str = "") -> dict:
    try:
        final_state = run_pseo_pipeline(target_url, client_domain, niche_context)
        return {
            "success": final_state.get("publish_success", False),
            "url": target_url,
            "client": client_domain,
            "pages_generated": final_state.get("pages_generated", 0),
            "keywords_found": len(final_state.get("target_keywords", [])),
            "errors": final_state.get("errors", [])
        }
    except Exception as e:
        return {
            "success": False,
            "url": target_url,
            "client": client_domain,
            "pages_generated": 0,
            "keywords_found": 0,
            "errors": [str(e)]
        }


def run_batch_from_csv(csv_path: str, max_workers: int = 2) -> list:
    jobs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            jobs.append({
                "target_url": row.get("target_url", "").strip(),
                "client_domain": row.get("client_domain", "").strip(),
                "niche_context": row.get("niche_context", "").strip()
            })

    print(f"\n[Batch Mode] {len(jobs)} clientes | {max_workers} en paralelo")

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_single, j["target_url"], j["client_domain"], j["niche_context"]): j
            for j in jobs if j["target_url"] and j["client_domain"]
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "[OK]" if result["success"] else "[FAIL]"
            print(f"  {status} {result['client']} — {result['pages_generated']} páginas")

    return results


def print_summary(results: list) -> None:
    total = len(results)
    success = sum(1 for r in results if r["success"])
    total_pages = sum(r["pages_generated"] for r in results)

    print(f"\n{'='*60}")
    print(f"  RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"  Clientes procesados: {total}")
    print(f"  Exitosos:            {success}/{total}")
    print(f"  Total páginas:       {total_pages}")
    print(f"{'='*60}")

    summary_path = Path("output/batch_summary.json")
    summary_path.parent.mkdir(exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  Resumen guardado: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description='pSEO Pipeline — Gemini 1.5 Flash + LangGraph',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py --url https://atlascash.cl --client dolarexpress.cl
  python main.py --url https://competidor.cl --client agnt.cl --context "fintech cupo dolar Chile"
  python main.py --batch clientes_ejemplo.csv --workers 3
        """
    )

    parser.add_argument('--url', help='URL del competidor a analizar')
    parser.add_argument('--client', help='Tu dominio (ej: dolarexpress.cl)')
    parser.add_argument('--context', default='', help='Contexto del nicho (opcional)')
    parser.add_argument('--batch', help='CSV con múltiples clientes')
    parser.add_argument('--workers', type=int, default=2, help='Paralelismo batch (default: 2)')

    args = parser.parse_args()

    print(f"[OK] DeepSeek API configurada - modelo: deepseek-chat")

    if args.batch:
        if not Path(args.batch).exists():
            print(f"ERROR: No se encuentra {args.batch}")
            sys.exit(1)
        results = run_batch_from_csv(args.batch, max_workers=args.workers)
        print_summary(results)

    elif args.url and args.client:
        result = run_single(args.url, args.client, args.context)
        if result["success"]:
            print(f"\n[OK] Completado: {result['pages_generated']} paginas en /output")
        else:
            print(f"\n[FAIL] Fallo: {result['errors']}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
