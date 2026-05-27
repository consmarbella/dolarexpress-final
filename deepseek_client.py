"""
deepseek_client.py — Cliente DeepSeek centralizado
Usa API compatible con OpenAI. Todos los nodos importan desde aquí.
"""

import os
import sys
from openai import OpenAI


def get_model(model_name: str = "deepseek-chat"):
    """Retorna un cliente DeepSeek configurado. Falla con mensaje claro si falta la key."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("\n[ERROR] Variable de entorno DEEPSEEK_API_KEY no configurada.")
        print("Ejecuta en tu terminal ANTES de correr el pipeline:")
        print("  Windows PowerShell:  $env:DEEPSEEK_API_KEY = 'sk-...'")
        print("  O crea un archivo .env con:  DEEPSEEK_API_KEY=sk-...")
        sys.exit(1)
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    return client, model_name


def generate_content(prompt: str, model_name: str = "deepseek-chat", temperature: float = 0.7) -> str:
    """Genera contenido usando DeepSeek. Wrapper simple."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("\n[ERROR] Variable de entorno DEEPSEEK_API_KEY no configurada.")
        sys.exit(1)
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=4096
    )
    
    return response.choices[0].message.content
