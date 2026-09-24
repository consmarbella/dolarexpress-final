#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

# Configuracion de las 24 nuevas paginas
new_pages = [
    # Vender
    "vender-cupo-cmr-hoy",
    "vender-cupo-ripley-rapido",
    "vender-cupo-lider-santiago",
    "vender-cupo-paris-efectivo",
    "vender-cupo-hites-ahora",
    "vender-cupo-abcdin-urgente",
    "vender-cupo-jumbo-online",
    "vender-cupo-easy-mismo-dia",
    # Liquidar
    "liquidar-cupo-cmr-efectivo",
    "liquidar-cupo-ripley-rapido",
    "liquidar-cupo-lider-hoy",
    "liquidar-cupo-paris-pesos",
    "liquidar-cupo-hites-transferencia",
    "liquidar-cupo-abcdin-online",
    "liquidar-cupo-tarjeta-retail",
    "liquidar-cupo-casa-comercial",
    # Urgencia
    "necesito-plata-tengo-cupo-cmr",
    "necesito-plata-tengo-cupo-ripley",
    "urgente-cupo-lider-efectivo",
    "urgente-cupo-paris-hoy",
    "efectivo-rapido-cupo-cmr",
    "efectivo-rapido-cupo-ripley",
    "convertir-cupo-cmr-pesos-hoy",
    "convertir-cupo-ripley-efectivo-rapido"
]

def update_sitemap():
    sitemap_path = "C:\\Users\\matte\\dolarexpress-final\\public\\sitemap.xml"

    # Leer el sitemap actual
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generar nuevas URLs
    new_urls = ""
    for page in new_pages:
        new_urls += f"""
  <url>
    <loc>https://dolarexpress.cl/{page}/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""

    # Reemplazar el comentario de total URLs
    total_before = int(content.split('<!-- Total de URLs: ')[1].split(' -->')[0])
    total_after = total_before + len(new_pages)

    content = content.replace(
        f'<!-- Total de URLs: {total_before} -->',
        f'<!-- Total de URLs: {total_after} -->'
    )

    # Actualizar fecha
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = content.replace(
        f'<!-- Generado automaticamente: ',
        f'<!-- Generado automaticamente: {now} -->'
    )
    # Hay que hacer esto de otra forma porque ya lo reemplacé
    lines = content.split('\n')
    lines[1] = f'<!-- Generado automaticamente: {now} -->'
    content = '\n'.join(lines)

    # Insertar antes de </urlset>
    content = content.replace('</urlset>', f'{new_urls}\n\n</urlset>')

    # Guardar
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[SUCCESS] Sitemap actualizado con {len(new_pages)} nuevas URLs")
    print(f"[INFO] Total de URLs ahora: {total_after}")

if __name__ == "__main__":
    update_sitemap()
