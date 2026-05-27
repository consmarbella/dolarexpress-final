"""
utils/gemini_client.py — Cliente Gemini centralizado
Un solo lugar para configurar la API. Todos los nodos importan desde aquí.
"""

import os
import sys
import google.generativeai as genai


def get_model(model_name: str = "gemini-2.0-flash"):
    """Retorna un modelo Gemini configurado. Falla con mensaje claro si falta la key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n[ERROR] Variable de entorno GEMINI_API_KEY no configurada.")
        print("Ejecuta en tu terminal ANTES de correr el pipeline:")
        print("  Windows PowerShell:  $env:GEMINI_API_KEY = 'AIzaSy...'")
        print("  Mac/Linux:           export GEMINI_API_KEY='AIzaSy...'")
        print("  O crea un archivo .env con:  GEMINI_API_KEY=AIzaSy...")
        sys.exit(1)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)
