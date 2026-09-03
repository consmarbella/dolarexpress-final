#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

# Definición de las 24 páginas nuevas
pages_config = {
    # Grupo 1: Vender cupo (8 páginas)
    "vender": [
        {
            "filename": "vender-cupo-cmr-hoy.html",
            "title": "Vender Cupo CMR Hoy | DolarExpress",
            "description": "Vende tu cupo de CMR Falabella a pesos hoy mismo. Cotización al instante y transferencia en 15 min. 100% online.",
            "h1": "Vender Cupo CMR <span>Hoy</span>",
            "action": "Vender cupo CMR",
            "card": "CMR Falabella",
            "intro": "¿Tienes cupo disponible en tu tarjeta CMR y necesitas venderlo hoy? DolarExpress te convierte ese cupo a pesos en menos de 15 minutos.",
            "slug": "vender-cupo-cmr-hoy"
        },
        {
            "filename": "vender-cupo-ripley-rapido.html",
            "title": "Vender Cupo Ripley Rápido | DolarExpress",
            "description": "Vende tu cupo Ripley de forma rápida y fácil. Proceso ágil, sin papeles, 100% online. Dinero en tu cuenta al instante.",
            "h1": "Vender Cupo Ripley <span>Rápido</span>",
            "action": "Vender cupo Ripley",
            "card": "Ripley",
            "intro": "¿Necesitas vender tu cupo Ripley de forma rápida? DolarExpress tiene el proceso más ágil: cotización al instante y dinero en tu cuenta.",
            "slug": "vender-cupo-ripley-rapido"
        },
        {
            "filename": "vender-cupo-lider-santiago.html",
            "title": "Vender Cupo Líder Santiago | DolarExpress",
            "description": "Vende tu cupo Líder en Santiago al mejor precio. Sin trámites, 100% online. Recibe el dinero en 15 minutos.",
            "h1": "Vender Cupo Líder <span>Santiago</span>",
            "action": "Vender cupo Líder",
            "card": "Líder",
            "intro": "Vende tu cupo Líder en Santiago sin salir de casa. DolarExpress te da la mejor cotización y transfiere al instante.",
            "slug": "vender-cupo-lider-santiago"
        },
        {
            "filename": "vender-cupo-paris-efectivo.html",
            "title": "Vender Cupo Paris por Efectivo | DolarExpress",
            "description": "Vende tu cupo Paris y recibe efectivo (transferencia) en 15 minutos. Cotización garantizada. 100% online.",
            "h1": "Vender Cupo Paris <span>por Efectivo</span>",
            "action": "Vender cupo Paris",
            "card": "Paris / Cencosud",
            "intro": "¿Quieres vender tu cupo Paris por efectivo? DolarExpress te hace la transferencia en menos de 15 minutos.",
            "slug": "vender-cupo-paris-efectivo"
        },
        {
            "filename": "vender-cupo-hites-ahora.html",
            "title": "Vender Cupo Hites Ahora | DolarExpress",
            "description": "Vende tu cupo Hites ahora mismo. Proceso instant, sin demoras, sin papeles. Dinero en tu cuenta en 15 min.",
            "h1": "Vender Cupo Hites <span>Ahora</span>",
            "action": "Vender cupo Hites",
            "card": "Hites",
            "intro": "Vende tu cupo Hites ahora mismo sin esperas. Cotización al instante y transferencia garantizada en 15 minutos.",
            "slug": "vender-cupo-hites-ahora"
        },
        {
            "filename": "vender-cupo-abcdin-urgente.html",
            "title": "Vender Cupo ABCDin Urgente | DolarExpress",
            "description": "Vende tu cupo ABCDin de forma urgente. Proceso express, dinero en 15 minutos. Cotiza hoy mismo.",
            "h1": "Vender Cupo ABCDin <span>Urgente</span>",
            "action": "Vender cupo ABCDin",
            "card": "ABCDin",
            "intro": "Necesitas vender tu cupo ABCDin urgentemente? DolarExpress tiene proceso express con transferencia en 15 minutos.",
            "slug": "vender-cupo-abcdin-urgente"
        },
        {
            "filename": "vender-cupo-jumbo-online.html",
            "title": "Vender Cupo Jumbo Online | DolarExpress",
            "description": "Vende tu cupo Jumbo 100% online sin ir a sucursales. Dinero en tu cuenta en 15 minutos. Cotiza ahora.",
            "h1": "Vender Cupo Jumbo <span>Online</span>",
            "action": "Vender cupo Jumbo",
            "card": "Jumbo",
            "intro": "Vende tu cupo Jumbo 100% online. Sin papeles, sin trámites, sin ir a ningún lado. Dinero en 15 minutos.",
            "slug": "vender-cupo-jumbo-online"
        },
        {
            "filename": "vender-cupo-easy-mismo-dia.html",
            "title": "Vender Cupo Easy Mismo Día | DolarExpress",
            "description": "Vende tu cupo Easy el mismo día. Proceso rápido, sin demoras. Dinero en tu cuenta garantizado.",
            "h1": "Vender Cupo Easy <span>Mismo Día</span>",
            "action": "Vender cupo Easy",
            "card": "Easy",
            "intro": "Vende tu cupo Easy el mismo día. DolarExpress te da el dinero en tu cuenta sin esperas ni trámites.",
            "slug": "vender-cupo-easy-mismo-dia"
        }
    ],
    # Grupo 2: Liquidar cupo (8 páginas)
    "liquidar": [
        {
            "filename": "liquidar-cupo-cmr-efectivo.html",
            "title": "Liquidar Cupo CMR por Efectivo | DolarExpress",
            "description": "Liquida tu cupo CMR y recibe efectivo en tu cuenta. Rápido, seguro, 100% online. Cotiza al instante.",
            "h1": "Liquidar Cupo CMR <span>por Efectivo</span>",
            "action": "Liquidar cupo CMR",
            "card": "CMR Falabella",
            "intro": "Liquida tu cupo CMR sin papeles. DolarExpress te convierte tu saldo en efectivo y lo transfiere en 15 minutos.",
            "slug": "liquidar-cupo-cmr-efectivo"
        },
        {
            "filename": "liquidar-cupo-ripley-rapido.html",
            "title": "Liquidar Cupo Ripley Rápido | DolarExpress",
            "description": "Liquida tu cupo Ripley de forma rápida. Sin trámites, 100% online. Dinero en 15 minutos.",
            "h1": "Liquidar Cupo Ripley <span>Rápido</span>",
            "action": "Liquidar cupo Ripley",
            "card": "Ripley",
            "intro": "Liquida tu cupo Ripley sin demoras. DolarExpress hace el proceso rápido y seguro, con dinero en tu cuenta al instante.",
            "slug": "liquidar-cupo-ripley-rapido"
        },
        {
            "filename": "liquidar-cupo-lider-hoy.html",
            "title": "Liquidar Cupo Líder Hoy | DolarExpress",
            "description": "Liquida tu cupo Líder hoy mismo. Sin trámites bancarios, 100% online. Recibe tu dinero en 15 min.",
            "h1": "Liquidar Cupo Líder <span>Hoy</span>",
            "action": "Liquidar cupo Líder",
            "card": "Líder",
            "intro": "Liquida tu cupo Líder hoy mismo sin ir a sucursales. DolarExpress te transfiere el dinero en 15 minutos.",
            "slug": "liquidar-cupo-lider-hoy"
        },
        {
            "filename": "liquidar-cupo-paris-pesos.html",
            "title": "Liquidar Cupo Paris a Pesos | DolarExpress",
            "description": "Liquida tu cupo Paris y convierte a pesos. Cotización garantizada. Dinero en tu cuenta en 15 minutos.",
            "h1": "Liquidar Cupo Paris <span>a Pesos</span>",
            "action": "Liquidar cupo Paris",
            "card": "Paris / Cencosud",
            "intro": "Liquida tu cupo Paris y recibe pesos en tu cuenta. DolarExpress hace la transferencia en 15 minutos.",
            "slug": "liquidar-cupo-paris-pesos"
        },
        {
            "filename": "liquidar-cupo-hites-transferencia.html",
            "title": "Liquidar Cupo Hites por Transferencia | DolarExpress",
            "description": "Liquida tu cupo Hites y recibe transferencia. Sin papeles, 100% online. Dinero al instante.",
            "h1": "Liquidar Cupo Hites <span>por Transferencia</span>",
            "action": "Liquidar cupo Hites",
            "card": "Hites",
            "intro": "Liquida tu cupo Hites por transferencia al instante. Sin papeles, sin trámites, 100% online.",
            "slug": "liquidar-cupo-hites-transferencia"
        },
        {
            "filename": "liquidar-cupo-abcdin-online.html",
            "title": "Liquidar Cupo ABCDin Online | DolarExpress",
            "description": "Liquida tu cupo ABCDin 100% online. Rápido y seguro. Dinero en tu cuenta en 15 minutos.",
            "h1": "Liquidar Cupo ABCDin <span>Online</span>",
            "action": "Liquidar cupo ABCDin",
            "card": "ABCDin",
            "intro": "Liquida tu cupo ABCDin 100% online sin ir a sucursales. DolarExpress te da el dinero en 15 minutos.",
            "slug": "liquidar-cupo-abcdin-online"
        },
        {
            "filename": "liquidar-cupo-tarjeta-retail.html",
            "title": "Liquidar Cupo Tarjeta Retail | DolarExpress",
            "description": "Liquida tu cupo de cualquier tarjeta retail. Sin trámites, 100% online. Dinero garantizado.",
            "h1": "Liquidar Cupo <span>Tarjeta Retail</span>",
            "action": "Liquidar cupo retail",
            "card": "Tarjeta Retail",
            "intro": "Liquida tu cupo de tarjeta retail sin papeles. DolarExpress te da el dinero en tu cuenta en 15 minutos.",
            "slug": "liquidar-cupo-tarjeta-retail"
        },
        {
            "filename": "liquidar-cupo-casa-comercial.html",
            "title": "Liquidar Cupo Casa Comercial | DolarExpress",
            "description": "Liquida tu cupo de casa comercial. Rápido, seguro, 100% online. Cotiza al instante.",
            "h1": "Liquidar Cupo <span>Casa Comercial</span>",
            "action": "Liquidar cupo casa comercial",
            "card": "Casa Comercial",
            "intro": "Liquida tu cupo de casa comercial sin ir a sucursales. DolarExpress te convierte a dinero en 15 minutos.",
            "slug": "liquidar-cupo-casa-comercial"
        }
    ],
    # Grupo 3: Urgencia/Pain points (8 páginas)
    "urgencia": [
        {
            "filename": "necesito-plata-tengo-cupo-cmr.html",
            "title": "Necesito Plata y Tengo Cupo CMR | DolarExpress",
            "description": "Necesitas plata y tienes cupo CMR? Convierte a dinero en 15 minutos. 100% online, sin papeles.",
            "h1": "Necesito Plata y Tengo Cupo <span>CMR</span>",
            "action": "Convertir cupo a plata",
            "card": "CMR Falabella",
            "intro": "¿Necesitas plata ahora y tienes cupo CMR disponible? DolarExpress te lo convierte a dinero en tu cuenta en 15 minutos.",
            "slug": "necesito-plata-tengo-cupo-cmr"
        },
        {
            "filename": "necesito-plata-tengo-cupo-ripley.html",
            "title": "Necesito Plata y Tengo Cupo Ripley | DolarExpress",
            "description": "Tienes cupo Ripley y necesitas plata? Recibe dinero en 15 minutos. Sin papeles, 100% online.",
            "h1": "Necesito Plata y Tengo Cupo <span>Ripley</span>",
            "action": "Convertir cupo Ripley",
            "card": "Ripley",
            "intro": "¿Necesitas plata urgente y tienes cupo Ripley? DolarExpress te lo convierte al instante, sin papeles.",
            "slug": "necesito-plata-tengo-cupo-ripley"
        },
        {
            "filename": "urgente-cupo-lider-efectivo.html",
            "title": "Urgente: Cupo Líder a Efectivo | DolarExpress",
            "description": "Necesitas urgente convertir tu cupo Líder a efectivo? Dinero en 15 minutos, 100% online.",
            "h1": "Urgente: Cupo Líder <span>a Efectivo</span>",
            "action": "Convertir urgente",
            "card": "Líder",
            "intro": "Situación urgente? Tienes cupo Líder? DolarExpress te lo convierte a dinero en 15 minutos, sin papeles.",
            "slug": "urgente-cupo-lider-efectivo"
        },
        {
            "filename": "urgente-cupo-paris-hoy.html",
            "title": "Urgente: Cupo Paris Hoy | DolarExpress",
            "description": "Cupo Paris y lo necesitas hoy? Dinero en tu cuenta en 15 minutos. Sin trámites.",
            "h1": "Urgente: Cupo Paris <span>Hoy</span>",
            "action": "Convertir cupo urgente",
            "card": "Paris / Cencosud",
            "intro": "¿Urgente? ¿Tienes cupo Paris? DolarExpress lo convierte a dinero en 15 minutos, hoy mismo.",
            "slug": "urgente-cupo-paris-hoy"
        },
        {
            "filename": "efectivo-rapido-cupo-cmr.html",
            "title": "Efectivo Rápido: Cupo CMR | DolarExpress",
            "description": "Necesitas efectivo rápido con tu cupo CMR? Dinero en 15 minutos. Cotiza al instante.",
            "h1": "Efectivo Rápido: Cupo <span>CMR</span>",
            "action": "Efectivo rápido CMR",
            "card": "CMR Falabella",
            "intro": "Necesitas efectivo rápido? Tienes cupo CMR? DolarExpress es la forma más rápida: dinero en 15 minutos.",
            "slug": "efectivo-rapido-cupo-cmr"
        },
        {
            "filename": "efectivo-rapido-cupo-ripley.html",
            "title": "Efectivo Rápido: Cupo Ripley | DolarExpress",
            "description": "Necesitas efectivo rápido del cupo Ripley? Dinero en 15 minutos. Sin papeles, 100% online.",
            "h1": "Efectivo Rápido: Cupo <span>Ripley</span>",
            "action": "Efectivo rápido Ripley",
            "card": "Ripley",
            "intro": "Necesitas efectivo rápido con tu cupo Ripley? DolarExpress te lo da en 15 minutos, sin salir de casa.",
            "slug": "efectivo-rapido-cupo-ripley"
        },
        {
            "filename": "convertir-cupo-cmr-pesos-hoy.html",
            "title": "Convertir Cupo CMR a Pesos Hoy | DolarExpress",
            "description": "Convierte tu cupo CMR a pesos hoy mismo. Dinero al instante, cotización garantizada.",
            "h1": "Convertir Cupo CMR <span>a Pesos Hoy</span>",
            "action": "Convertir cupo a pesos",
            "card": "CMR Falabella",
            "intro": "¿Quieres convertir tu cupo CMR a pesos hoy mismo? DolarExpress te lo hace en 15 minutos.",
            "slug": "convertir-cupo-cmr-pesos-hoy"
        },
        {
            "filename": "convertir-cupo-ripley-efectivo-rapido.html",
            "title": "Convertir Cupo Ripley a Efectivo Rápido | DolarExpress",
            "description": "Convierte tu cupo Ripley a efectivo de forma rápida. 15 minutos, 100% online.",
            "h1": "Convertir Cupo Ripley <span>a Efectivo Rápido</span>",
            "action": "Convertir cupo Ripley",
            "card": "Ripley",
            "intro": "Convierte tu cupo Ripley a efectivo de forma rápida. DolarExpress lo hace en 15 minutos, 100% online.",
            "slug": "convertir-cupo-ripley-efectivo-rapido"
        }
    ]
}

def read_template():
    """Lee el archivo template"""
    template_path = 'C:\\Users\\matte\\dolarexpress-final\\public\\cupo-dolar-banco-chile-santiago.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_page(template, config):
    """Genera una página personalizada basada en el template y la configuración"""
    html = template

    # Reemplazar título
    html = html.replace(
        '<title>Cupo Dólar Banco de Chile Santiago | DolarExpress</title>',
        f'<title>{config["title"]}</title>'
    )

    # Reemplazar meta description
    html = html.replace(
        'content="Convierte tu cupo en dólares de Banco de Chile en Santiago a pesos en 15 min. 100% online. Sin ir a oficinas. Cotiza ahora."',
        f'content="{config["description"]}"'
    )

    # Reemplazar canonical URL
    html = html.replace(
        'href="https://dolarexpress.cl/cupo-dolar-banco-chile-santiago/"',
        f'href="https://dolarexpress.cl/{config["slug"]}/"'
    )

    # Reemplazar og:url
    html = html.replace(
        'content="https://dolarexpress.cl/cupo-dolar-banco-chile-santiago.html"',
        f'content="https://dolarexpress.cl/{config["slug"]}/"'
    )

    # Reemplazar H1
    html = html.replace(
        '<h1>Cupo Dólar <span>Banco de Chile</span> en Santiago</h1>',
        f'<h1>{config["h1"]}</h1>'
    )

    # Reemplazar intro
    html = html.replace(
        '¿Tienes una tarjeta de Banco de Chile con cupo en dólares y estás en Santiago? DolarExpress te convierte ese cupo a pesos chilenos en menos de 15 minutos, sin salir de casa.',
        config["intro"]
    )

    # Reemplazar contenido principal
    old_content = '''<h2>Servicio de cupo dólar Banco de Chile en Santiago</h2>
<p>Atendemos a clientes de Banco de Chile en Santiago y toda la región de forma 100% online. El proceso se coordina por WhatsApp y la transferencia llega a cualquier cuenta bancaria en Chile.</p>

<h2>Requisitos para tu tarjeta Banco de Chile</h2>
<ul>
  <li>Tarjeta de crédito Banco de Chile con cupo internacional disponible (mínimo USD 200)</li>
  <li>Tarjeta habilitada para compras internacionales — actívala en Mi Banco de Chile si es necesario</li>
  <li>Cuenta bancaria en Chile a tu nombre</li>
  <li>Ser titular de la tarjeta</li>
</ul>

<h2>¿Por qué no necesitas ir a una sucursal en Santiago?</h2>
<p>La operación se realiza como una compra online en un sitio internacional. Tú coordinas con nosotros por WhatsApp, procesas el pago desde tu computador o celular, y recibes la transferencia en tu cuenta. Sin filas, sin papeles, sin horarios restrictivos.</p>'''

    new_content = f'''<h2>{config["action"].title()} {config["card"]}</h2>
<p>DolarExpress te ayuda a {config["action"].lower()} de forma rápida, segura y 100% online. El proceso se coordina por WhatsApp y la transferencia llega a cualquier cuenta bancaria en Chile en menos de 15 minutos.</p>

<h2>Requisitos para tu tarjeta {config["card"]}</h2>
<ul>
  <li>Tarjeta de crédito {config["card"]} con cupo disponible (mínimo USD 200)</li>
  <li>Tarjeta habilitada para compras internacionales</li>
  <li>Cuenta bancaria en Chile a tu nombre</li>
  <li>Ser titular de la tarjeta</li>
</ul>

<h2>¿Por qué es rápido y seguro?</h2>
<p>La operación se realiza como una compra online internacional. Tú coordinas con nosotros por WhatsApp, procesas el pago desde tu celular o computador, y recibes la transferencia en tu cuenta. Sin filas, sin papeles, sin horarios restrictivos. Todo en 15 minutos.</p>'''

    html = html.replace(old_content, new_content)

    # Reemplazar FAQ
    html = html.replace(
        '¿Cómo veo mi cupo en dólares disponible en Banco de Chile?',
        f'¿Cómo veo mi cupo disponible en {config["card"]}?'
    )

    # Reemplazar Service name en schema
    html = html.replace(
        '"name": "Cupo Dólar Banco de Chile Santiago"',
        f'"name": "{config["title"]}"'
    )

    # Reemplazar URL en schema
    html = html.replace(
        '"url": "https://dolarexpress.cl/cupo-dolar-banco-chile-santiago"',
        f'"url": "https://dolarexpress.cl/{config["slug"]}"'
    )

    # Reemplazar en Breadcrumb
    html = html.replace(
        '"name": "Cupo Dólar Banco de Chile Santiago"',
        f'"name": "{config["action"].title()}"'
    )

    html = html.replace(
        '"item": "https://dolarexpress.cl/cupo-dolar-banco-chile-santiago"',
        f'"item": "https://dolarexpress.cl/{config["slug"]}"'
    )

    return html

def main():
    template = read_template()
    output_dir = 'C:\\Users\\matte\\dolarexpress-final\\public'

    created_files = []

    # Crear páginas de vender
    for page_config in pages_config["vender"]:
        html = generate_page(template, page_config)
        filepath = os.path.join(output_dir, page_config["filename"])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        created_files.append(page_config["filename"])
        print(f"[OK] Creado: {page_config['filename']}")

    # Crear páginas de liquidar
    for page_config in pages_config["liquidar"]:
        html = generate_page(template, page_config)
        filepath = os.path.join(output_dir, page_config["filename"])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        created_files.append(page_config["filename"])
        print(f"[OK] Creado: {page_config['filename']}")

    # Crear páginas de urgencia
    for page_config in pages_config["urgencia"]:
        html = generate_page(template, page_config)
        filepath = os.path.join(output_dir, page_config["filename"])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        created_files.append(page_config["filename"])
        print(f"[OK] Creado: {page_config['filename']}")

    print(f"\n[SUCCESS] Se crearon {len(created_files)} paginas nuevas")
    return created_files

if __name__ == "__main__":
    created = main()
