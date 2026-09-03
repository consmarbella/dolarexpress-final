#!/usr/bin/env python3
import re
from pathlib import Path

files_to_fix = [
    "public/avance-efectivo-sin-avance-habilitado.html",
    "public/como-sacar-plata-si-no-tengo-avance.html", 
    "public/como-usar-el-cupo-de-mi-tarjeta-sin-avance.html",
    "public/tarjeta-sin-avance-habilitado-chile.html"
]

descriptions = [
    "Saca efectivo de tu tarjeta de tienda sin avance. Comision 15%, 15-30 min. Proceso garantizado, sin rechazos. DolarExpress Chile.",
    "Como sacar plata si no tengo avance en mi tarjeta retail. Metodo seguro y rápido. Comisión fija 15%, proceso en minutos.",
    "Usa tu cupo de tarjeta sin tener avance habilitado. DolarExpress permite convertir cualquier cupo a efectivo en 15-30 minutos.",
    "Tarjeta sin avance habilitado en Chile: Soluciones para sacar efectivo de tu cupo. Comisión 15%, proceso garantizado DolarExpress."
]

for filepath, desc in zip(files_to_fix, descriptions):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(
        r'name="description" content="[^"]*"',
        f'name="description" content="{desc}"',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Fixed: {Path(filepath).name}")
