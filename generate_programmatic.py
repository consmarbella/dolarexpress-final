#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Programático Avanzado para DolarExpress
Genera páginas únicas con contenido basado en datos estructurados.
Mantiene diseño visual existente y botón de WhatsApp.
"""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
DATA_FILE = ROOT / "src" / "data" / "seo_data.json"

# WhatsApp business
WHATSAPP_NUMBER = "56967658939"

def load_data():
    data = {}
    with open(ROOT / "src" / "data" / "bancos.json", 'r', encoding='utf-8') as f:
        data['bancos'] = json.load(f)
    with open(ROOT / "src" / "data" / "ciudades.json", 'r', encoding='utf-8') as f:
        data['ciudades'] = json.load(f)
    return data

def slugify(text):
    """Convierte texto a slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def format_currency_clp(usd_amount):
    """Formatea monto USD a CLP estimado"""
    rate = 760  # Tasa aproximada
    clp = usd_amount * rate
    return f"${clp:,.0f}".replace(",", ".")

# Plantilla base - mantiene diseño original
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="keywords" content="{keywords}">
<meta name="description" content="{meta_description}">
<title>{title}</title>
<link rel="canonical" href="{canonical}" />
{schema_jsonld}
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;color:#1a1a1a;background:linear-gradient(135deg,#1a1a1a 0%,#2d2d2d 100%)}}
header{{background:#1a1a1a;padding:20px;text-align:center;border-bottom:2px solid #d4af37}}
h1{{color:#d4af37;font-size:2.5rem;font-weight:bold}}
.hero{{background:#2d2d2d;color:white;padding:60px 20px;text-align:center}}
.hero h2{{font-size:2rem;margin-bottom:20px}}
.hero .highlight{{color:#d4af37}}
.cta{{background:#d4af37;color:#1a1a1a;padding:15px 40px;font-size:1.1rem;border:none;border-radius:5px;cursor:pointer;font-weight:bold;text-decoration:none;display:inline-block;margin:20px 0}}
.cta:hover{{background:#c49d2f}}
.content{{max-width:1200px;margin:40px auto;padding:20px;background:white;border-radius:10px}}
h3{{color:#1a1a1a;margin:30px 0 15px}}
p{{line-height:1.8;margin-bottom:15px}}
ul{{margin:15px 0;padding-left:20px}}
li{{margin:10px 0;line-height:1.6}}
footer{{background:#1a1a1a;color:#999;text-align:center;padding:30px}}
.whatsapp{{position:fixed;bottom:20px;right:20px;background:#25d366;color:white;padding:15px 25px;border-radius:50px;text-decoration:none;font-weight:bold;box-shadow:0 4px 10px rgba(0,0,0,0.3);z-index:1000}}
.whatsapp:hover{{background:#1fb855}}
.metric{{display:inline-block;background:#2d2d2d;color:white;padding:10px 20px;margin:5px;border-radius:8px}}
.metric strong{{color:#d4af37}}
.breadcrumb{{padding:10px 20px;background:#1a1a1a;color:#999;font-size:14px}}
.breadcrumb a{{color:#d4af37;text-decoration:none}}
.interlinking{{margin:30px 0;padding:20px;background:#f5f5f5;border-radius:10px}}
.interlinking h4{{color:#1a1a1a;margin-bottom:15px}}
.interlinking a{{color:#d4af37;margin-right:15px;text-decoration:none;font-size:14px}}
.interlinking a:hover{{text-decoration:underline}}
.location-info{{background:#f8f8f8;padding:15px;border-radius:8px;margin:20px 0;border-left:4px solid #d4af37}}
</style>
</head>
<body>
<nav class="breadcrumb">
<a href="/">Inicio</a> · <a href="/directorio-general.html">Directorio</a> · {breadcrumb}
</nav>

<header><h1>DolarExpress</h1></header>
<div class="hero">
<h2>{hero_title}</h2>
<p>{hero_subtitle}</p>
<a href="https://wa.me/{whatsapp}?text={whatsapp_message}" class="cta">{cta_text}</a>
</div>

<div class="content">
{content_sections}
</div>

<div class="content interlinking">
<h4>Servicios Relacionados</h4>
{interlinking}
</div>

<footer><p>© 2026 DolarExpress.Especialistas en compra de cupo dolar.</p></footer>

<a href="https://wa.me/{whatsapp}?text={whatsapp_message}" class="whatsapp">💬 WhatsApp</a>

{schema_footer}
</body>
</html>'''

def generate_bank_page(data, bank_key, bank_info):
    """Genera página única para banco"""
    slug = slugify(f"vender-cupo-{bank_key}")
    title = f"Vender Cupo {bank_info['nombre_largo']} | DolarExpress"
    meta_desc = f"Vende tu cupo dólar de {bank_info['nombre']}. Transferencia inmediata en 15 min. {bank_info['descripcion'][:100]}..."
    
    keywords = f"vender cupo {bank_info['nombre'].lower()}, vender cupo {bank_key}, cambiar cupo {bank_info['nombre'].lower()}, vender tarjeta {bank_info['nombre'].lower()}, cupo internacional {bank_key}"
    
    hero_title = f"Vender Cupo <span class='highlight'>{bank_info['nombre']}</span>"
    hero_subtitle = f"¿Necesitas efectivo? Compramos tu cupo dólar de {bank_info['nombre']} con la mejor tasa del mercado. Transferencia en menos de 15 minutos."
    
    whatsapp_msg = f"Hola, quiero vender mi cupo de {bank_info['nombre']}"
    cta_text = "Vender mi Cupo Ahora"
    
    # Contenido único por banco
    content = f"""
<h3>¿Por qué vender tu Cupo {bank_info['nombre']}?</h3>
<p>{bank_info['descripcion']}</p>

<h3>Beneficios de operar con {bank_info['nombre']}</h3>
<ul>
<li>🎯 <strong>Clientes {bank_info['clientes']}</strong> confían en nosotros</li>
<li>⚡ <strong>Proceso 100% digital</strong> - sin ir a sucursal</li>
<li>💰 <strong>Mejor tasa del mercado</strong> - sin comisiones ocultas</li>
<li>🕐 <strong>Transferencia en 15 minutos</strong> - dinero disponible al instante</li>
<li>🔒 <strong>100% seguro</strong> - transferencia bancaria verificada</li>
</ul>

<h3>Tarjetas {bank_info['nombre']} con Cupo Internacional</h3>
<p>{bank_info['nombre']} ofrece tarjetas de crédito con cupo internacional disponible para transacciones en dólares. Las principales incluyen Visa Classic, Oro, Platinum y Black según el tipo de cliente.</p>

<h3>Ventajas de vender tu Cupo {bank_info['nombre']}</h3>
<ul>
<li>Cupo disponible se convierte en efectivo inmediatamente</li>
<li>No necesitas ir a sucursal - todo por WhatsApp</li>
<li>Transferencia directa a tu cuenta bancaria</li>
<li>Sin antecedentes crediticios requeridos</li>
<li>Atención personalizada 24/7</li>
</ul>

<h3>Preguntas Frecuentes sobre {bank_info['nombre']}</h3>
<p><strong>¿Cuánto tiempo tarda el proceso en {bank_info['nombre']}?</strong></p>
<p>Máximo 15 minutos desde que confirmas la operación. La transferencia se realiza de inmediato a tu cuenta.</p>

<p><strong>¿Qué necesito para vender mi cupo {bank_info['nombre']}?</strong></p>
<p>Necesitas: 1) Foto del cupo disponible en tu app del banco, 2) Número de cuenta bancaria propia, 3) Tu RUT.</p>

<p><strong>¿Es seguro vender en {bank_info['nombre']}?</strong></p>
<p>100% seguro. Trabajamos con transferencia bancaria formal, verificada y rastreable. Tenemos cientos de clientes satisfechos.</p>

<p><strong>¿Qué tasa me ofrecen en {bank_info['nombre']}?</strong></p>
<p>La mejor tasa del mercado. Contáctanos por WhatsApp para darte una cotización exacta basada en el monto y momento.</p>
"""
    
    # Breadcrumb
    breadcrumb = f"<a href='/bancos/'>Bancos</a> · {bank_info['nombre']}"
    
    # Interlinking - otros bancos
    interlinking = ""
    for other_key, other_info in data['bancos'].items():
        if other_key != bank_key:
            interlinking += f"<a href='/vender-cupo-{slugify(other_key)}.html'>{other_info['nombre']}</a> "
    
    # Schema
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FinancialProduct",
        "name": f"Venta de Cupo {bank_info['nombre']}",
        "description": meta_desc,
        "provider": {
            "@type": "Organization",
            "name": "DolarExpress",
            "url": "https://dolarexpress.cl"
        },
        "areaServed": {
            "@type": "Country",
            "name": "Chile"
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "CLP",
            "description": "Venta de cupo dólar"
        }
    })
    
    return HTML_TEMPLATE.format(
        keywords=keywords,
        meta_description=meta_desc,
        title=title,
        canonical=f"https://www.dolarexpress.cl/vender-cupo-{slugify(bank_key)}/",
        schema_jsonld=f'<script type="application/ld+json">{schema}</script>',
        hero_title=hero_title,
        hero_subtitle=hero_subtitle,
        whatsapp=WHATSAPP_NUMBER,
        whatsapp_message=whatsapp_msg,
        cta_text=cta_text,
        content_sections=content,
        breadcrumb=breadcrumb,
        interlinking=interlinking,
        schema_footer=f'<script type="application/ld+json">{schema}</script>'
    )

def generate_city_page(data, city_key, city_info):
    """Genera página única para ciudad"""
    slug = slugify(f"vender-cupo-{city_key}")
    title = f"Vender Cupo Dólar en {city_info['nombre']} | DolarExpress"
    meta_desc = f"Vende tu cupo dólar en {city_info['nombre']}, {city_info['region']}. Transferencia inmediata en 15 minutos. Servicio disponible en toda la región."
    
    keywords = f"vender cupo {city_info['nombre'].lower()}, vender dolar {city_info['nombre'].lower()}, cambiar cupo {city_info['region'].lower()}, dinero urgente {city_info['nombre'].lower()}"
    
    hero_title = f"Vender Cupo en <span class='highlight'>{city_info['nombre']}</span>"
    hero_subtitle = f"¿Estás en {city_info['nombre']} ({city_info['region']})? Convierte tu cupo dólar en pesos en menos de 15 minutos. Servicio disponible para toda la región."
    
    whatsapp_msg = f"Hola, quiero vender mi cupo en {city_info['nombre']}"
    cta_text = "Vender mi Cupo en " + city_info['nombre']
    
    # Contenido único por ciudad
    content = f"""
<h3>Servicio en {city_info['nombre']}, {city_info['region']}</h3>
<p>{city_info['descripcion']}</p>

<h3>¿Por qué vender tu Cupo en {city_info['nombre']}?</h3>
<ul>
<li>🏙️ <strong>Ciudad principal de {city_info['region']}</strong> - gran demanda de servicios financieros</li>
<li>⚡ <strong>Proceso 100% digital</strong> - sin importar tu ubicación exacta</li>
<li>💰 <strong>Mejor tasa del mercado</strong> en la región</li>
<li>🕐 <strong>15 minutos</strong> - transferencia inmediata</li>
<li>🔒 <strong>Seguro</strong> - transferencia bancaria formal</li>
</ul>

<h3>Ventajas del Servicio en {city_info['nombre']}</h3>
<ul>
<li>Todo el proceso por WhatsApp - sin salir de casa</li>
<li>Transferencia directa a tu cuenta bancaria</li>
<li>Sin ir a sucursales o hacer filas</li>
<li>Atención 24/7 disponible</li>
<li>Mejor tasa garantizada</li>
</ul>

<h3>Requisitos para vender en {city_info['nombre']}</h3>
<ul>
<li>Tener cupo disponible en tu tarjeta de crédito</li>
<li>Tener cuenta bancaria a tu nombre</li>
<li>Tener WhatsApp para recibir la cotización</li>
<li>Tener tu RUT vigente</li>
</ul>

<h3>Preguntas Frecuentes</h3>
<p><strong>¿El servicio está disponible en {city_info['nombre']}?</strong></p>
<p>Sí, operamos en toda {city_info['nombre']} y la región de {city_info['region']}. El proceso es 100% digital, así que puedes estar en cualquier punto de la ciudad.</p>

<p><strong>¿Cuánto tiempo tarda en {city_info['nombre']}?</strong></p>
<p>Máximo 15 minutos desde la confirmación. La transferencia se hace de inmediato a tu cuenta.</p>

<p><strong>¿Qué necesito para vender en {city_info['nombre']}?</strong></p>
<p>Solo tu foto del cupo disponible y número de cuenta bancaria. Todo por WhatsApp.</p>

<p><strong>¿Es seguro vender en {city_info['nombre']}?</strong></p>
<p>100% seguro. Transferencia bancaria formal con comprobante de transferencia.</p>
"""
    
    breadcrumb = f"<a href='/ciudades/'>Ciudades</a> · {city_info['nombre']}"
    
    # Interlinking - otras ciudades
    interlinking = ""
    for other_key, other_info in data['ciudades'].items():
        if other_key != city_key:
            interlinking += f"<a href='/vender-cupo-{slugify(other_key)}.html'>{other_info['nombre']}</a> "
    
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Venta de Cupo Dólar en {city_info['nombre']}",
        "description": meta_desc,
        "provider": {
            "@type": "Organization",
            "name": "DolarExpress"
        },
        "areaServed": {
            "@type": "City",
            "name": city_info['nombre'],
            "addressRegion": city_info['region']
        }
    })
    
    return HTML_TEMPLATE.format(
        keywords=keywords,
        meta_description=meta_desc,
        title=title,
        canonical=f"https://www.dolarexpress.cl/vender-cupo-{slug}/",
        schema_jsonld=f'<script type="application/ld+json">{schema}</script>',
        hero_title=hero_title,
        hero_subtitle=hero_subtitle,
        whatsapp=WHATSAPP_NUMBER,
        whatsapp_message=whatsapp_msg,
        cta_text=cta_text,
        content_sections=content,
        breadcrumb=breadcrumb,
        interlinking=interlinking,
        schema_footer=f'<script type="application/ld+json">{schema}</script>'
    )

def generate_urgente_page(data, service_key, service_info):
    """Genera página de servicio urgente"""
    title = f"{service_info['nombre']} | DolarExpress"
    meta_desc = service_info['descripcion_larga']
    
    keywords = ", ".join(service_info['palabras_clave'])
    
    hero_title = f"<span class='highlight'>{service_info['nombre']}</span> en Chile"
    hero_subtitle = service_info['descripcion_larga']
    
    whatsapp_msg = "Hola, necesito dinero urgente"
    cta_text = "Necesito Dinero Ahora"
    
    content = f"""
<h3>{service_info['descripcion_corta']}</h3>
<p>{service_info['descripcion_larga']}</p>

<h3>¿Cómo funciona?</h3>
<ol>
<li>Envíanos foto de tu cupo disponible por WhatsApp</li>
<li>Te cotizamos al instante la tasa de cambio</li>
<li>Confirmas la operación</li>
<li>Recibes el dinero en máximo 15 minutos</li>
</ol>

<h3>¿Por qué elegirnos?</h3>
<ul>
<li>⚡ <strong>15 minutos</strong> - el servicio más rápido de Chile</li>
<li>🕐 <strong>24/7</strong> - disponible día y noche, incluso festivos</li>
<li>💰 <strong>Mejor tasa</strong> - sin comisiones ocultas</li>
<li>🔒 <strong>100% seguro</strong> - transferencia bancaria verificada</li>
<li>📱 <strong>100% WhatsApp</strong> - sin perder tiempo en oficinas</li>
</ul>

<h3>Requisitos</h3>
<ul>
<li>Cupo disponible en tu tarjeta de crédito</li>
<li>Cuenta bancaria a tu nombre</li>
<li>RUT válido</li>
<li>WhatsApp para comunicación</li>
</ul>

<h3>Preguntas Frecuentes</h3>
"""
    
    for faq in service_info['preguntas_faq']:
        content += f"<p><strong>{faq['q']}</strong></p><p>{faq['a']}</p>\n"
    
    breadcrumb = service_info['nombre']
    
    interlinking = ""
    for key, info in data['servicios'].items():
        if key != service_key:
            interlinking += f"<a href='/{info['slug']}.html'>{info['nombre']}</a> "
    
    interlinking += "<a href='/vender-cupo-banco-chile.html'>Banco de Chile</a> "
    interlinking += "<a href='/vender-cupo-bci.html'>BCI</a> "
    
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FinancialService",
        "name": service_info['nombre'],
        "description": meta_desc,
        "provider": {
            "@type": "Organization",
            "name": "DolarExpress"
        },
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": "https://wa.me/" + WHATSAPP_NUMBER
        }
    })
    
    return HTML_TEMPLATE.format(
        keywords=keywords,
        meta_description=meta_desc,
        title=title,
        canonical=f"https://www.dolarexpress.cl/{service_info['slug']}/",
        schema_jsonld=f'<script type="application/ld+json">{schema}</script>',
        hero_title=hero_title,
        hero_subtitle=hero_subtitle,
        whatsapp=WHATSAPP_NUMBER,
        whatsapp_message=whatsapp_msg,
        cta_text=cta_text,
        content_sections=content,
        breadcrumb=breadcrumb,
        interlinking=interlinking,
        schema_footer=f'<script type="application/ld+json">{schema}</script>'
    )

def generate_all_pages():
    """Genera todas las páginas"""
    data = load_data()
    
    # Crear directorio public si no existe
    PUBLIC.mkdir(parents=True, exist_ok=True)
    
    generated = []
    
    # Generar páginas de bancos
    print("Generando paginas de bancos...")
    for bank_key, bank_info in data['bancos'].items():
        html = generate_bank_page(data, bank_key, bank_info)
        filename = f"vender-cupo-{slugify(bank_key)}.html"
        filepath = PUBLIC / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        generated.append(f"https://dolarexpress.cl/{filename}")
        print(f"  ✓ {filename}")
    
    # Generar páginas de ciudades
    print("\nGenerando paginas de ciudades...")
    for city_key, city_info in data['ciudades'].items():
        html = generate_city_page(data, city_key, city_info)
        filename = f"vender-cupo-{slugify(city_key)}.html"
        filepath = PUBLIC / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        generated.append(f"https://dolarexpress.cl/{filename}")
        print(f"  ✓ {filename}")
    
    # Generar páginas de servicios urgentes
    print("\n⚡ Generando páginas de servicios...")
    for service_key, service_info in data['servicios'].items():
        html = generate_urgente_page(data, service_key, service_info)
        filename = f"{service_info['slug']}.html"
        filepath = PUBLIC / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        generated.append(f"https://dolarexpress.cl/{filename}")
        print(f"  ✓ {filename}")
    
    # Generar sitemap
    print("\n🗺️ Generando sitemap...")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in generated:
        sitemap += f'  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'
    
    with open(PUBLIC / "sitemap-seo-programmatic.xml", 'w', encoding='utf-8') as f:
        f.write(sitemap)
    
    print(f"\n✅ Total: {len(generated)} páginas generadas")
    print(f"📄 Sitemap: {len(generated)} URLs")
    
    # Guardar URLs
    with open(ROOT / "urls_programmatic.txt", 'w', encoding='utf-8') as f:
        for url in generated:
            f.write(url + '\n')
    
    print(f"\n📝 URLs guardadas en urls_programmatic.txt")
    return generated

if __name__ == "__main__":
    generate_all_pages()