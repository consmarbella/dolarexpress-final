#!/usr/bin/env python3
"""
Regenera páginas thin content con la estructura completa del template profesional.
Solo modifica páginas < 5KB que no sean 404.html ni nosotros.html.
Mantiene los mismos nombres de archivo (Google ya las descubrió).
"""
import os
import re
import json

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

BANK_DATA = {
    'banco-chile': 'Banco de Chile', 'bancoestado': 'BancoEstado',
    'bci': 'BCI', 'santander': 'Santander', 'scotiabank': 'Scotiabank',
    'itau': 'Itaú', 'bice': 'BICE', 'security': 'Security', 'bbva': 'BBVA',
}
RETAIL_DATA = {
    'la-polar': 'La Polar', 'abcdin': 'ABCDin', 'cencosud': 'Cencosud',
    'johnson': 'Johnson', 'corona': 'Corona', 'ripley': 'Ripley',
    'paris': 'Paris', 'hites': 'Hites', 'jumbo': 'Jumbo',
    'easy': 'Easy', 'lider': 'Líder', 'cmr': 'CMR Falabella',
}
CITY_NAMES = {
    'santiago': 'Santiago', 'concepcion': 'Concepción', 'valparaiso': 'Valparaíso',
    'vina-del-mar': 'Viña del Mar', 'temuco': 'Temuco', 'rancagua': 'Rancagua',
    'antofagasta': 'Antofagasta', 'la-serena': 'La Serena',
    'puerto-montt': 'Puerto Montt', 'iquique': 'Iquique', 'arica': 'Arica',
    'chillan': 'Chillán', 'calama': 'Calama', 'osorno': 'Osorno', 'talca': 'Talca',
}

def detect_bank(slug):
    for k, v in BANK_DATA.items():
        if k in slug: return k, v
    return None, None

def detect_retail(slug):
    order = ['la-polar','abcdin','cencosud','johnson','corona','ripley','paris','hites','jumbo','easy','lider','cmr']
    for k in order:
        if k in slug: return k, RETAIL_DATA[k]
    return None, None

def detect_city(slug):
    for k, v in CITY_NAMES.items():
        if k in slug: return v
    return None

def slug_to_title(slug):
    return ' '.join(w.capitalize() for w in slug.split('-'))

def generate_meta(slug):
    bank_key, bank_name = detect_bank(slug)
    retail_key, retail_name = detect_retail(slug)
    city = detect_city(slug)

    if retail_name and city:
        t = f"Obtén Efectivo con Tarjeta {retail_name} en {city} | DolarExpress"
        d = f"Convierte tu cupo de la tarjeta {retail_name} en efectivo en {city}. Sin avance habilitado. Transferencia en 15 minutos a cualquier banco de Chile. Cotiza por WhatsApp."
    elif retail_name:
        t = f"Cupo {retail_name} a Efectivo – Sin Avance Habilitado | DolarExpress"
        d = f"Usamos el cupo de compras de tu tarjeta {retail_name} para darte efectivo al instante. No necesitas avance habilitado. Transferencia en 15 minutos. Sin DICOM."
    elif bank_name and city:
        t = f"Compra de Cupo Dólar {bank_name} en {city} | DolarExpress"
        d = f"Convertimos tu cupo en dólares de {bank_name} a pesos chilenos en {city}. 100% online, sin ir a sucursales. Transferencia inmediata. Cotiza ahora por WhatsApp."
    elif bank_name:
        t = f"Vender Cupo Dólar {bank_name} – Efectivo al Instante | DolarExpress"
        d = f"Compramos tu cupo en dólares de {bank_name}. Proceso seguro 100% online. Transferencia a tu cuenta en menos de 15 minutos. Mejor tasa del mercado."
    elif 'vender-cupo' in slug or 'liquidar-cupo' in slug:
        t = f"{slug_to_title(slug)} | DolarExpress"
        d = "Vende o liquida tu cupo en dólares de forma rápida y segura. DolarExpress te transfiere el dinero a tu cuenta en menos de 15 minutos. Sin papeleo."
    elif 'dicom' in slug:
        t = f"{slug_to_title(slug)} | DolarExpress"
        d = "¿Estás en DICOM? No importa. Si tienes cupo disponible en tu tarjeta, DolarExpress te da efectivo igual. Sin revisar historial crediticio. Transferencia en 15 min."
    else:
        t = f"{slug_to_title(slug)} | DolarExpress"
        d = "Convierte tu cupo de tarjeta a efectivo con DolarExpress. Proceso rápido, seguro y 100% online. Transferencia en menos de 15 minutos a cualquier banco en Chile."

    return t, d

def get_related_links(slug):
    bank_key, bank_name = detect_bank(slug)
    retail_key, retail_name = detect_retail(slug)
    links = []

    if bank_key:
        for city_k, city_v in list(CITY_NAMES.items())[:6]:
            s = f"cupo-dolar-{bank_key}-{city_k}"
            if s != slug:
                links.append((s, f"Cupo Dólar {bank_name} {city_v}"))
        for other_k, other_v in list(BANK_DATA.items())[:4]:
            if other_k != bank_key:
                links.append((f"cupo-dolar-{other_k}", f"Cupo Dólar {other_v}"))
    elif retail_key:
        for other_k, other_v in list(RETAIL_DATA.items())[:4]:
            if other_k != retail_key:
                links.append((f"vender-cupo-{other_k}-hoy" if other_k != 'cmr' else "plata-rapida-tarjeta-cmr", f"Cupo {other_v} a Efectivo"))
        for bank_k, bank_v in list(BANK_DATA.items())[:3]:
            links.append((f"cupo-dolar-{bank_k}", f"Cupo Dólar {bank_v}"))
    else:
        links = [
            ("cupo-dolar-banco-chile", "Cupo Dólar Banco de Chile"),
            ("cupo-dolar-bci", "Cupo Dólar BCI"),
            ("cupo-dolar-santander", "Cupo Dólar Santander"),
            ("plata-rapida-tarjeta-cmr", "Cupo CMR Falabella"),
            ("vender-cupo-ripley-rapido", "Cupo Ripley a Efectivo"),
            ("prestamo-tarjeta-cmr-sin-dicom", "Sin DICOM CMR"),
        ]

    return links[:8]

def generate_faq(slug):
    bank_key, bank_name = detect_bank(slug)
    retail_key, retail_name = detect_retail(slug)

    if retail_name:
        return [
            (f"¿Necesito avance habilitado en mi tarjeta {retail_name}?",
             f"No. DolarExpress usa el cupo de compras de tu tarjeta {retail_name}, no el cupo de avance. Aunque tengas el avance bloqueado, puedes convertir tu cupo en efectivo sin problema."),
            ("¿Cuánto demora la transferencia?",
             "La transferencia llega a tu cuenta en menos de 15 minutos desde que confirmas la operación. El proceso completo, desde el primer contacto hasta recibir el dinero, toma menos de 30 minutos."),
            ("¿Revisan mi DICOM o historial crediticio?",
             "No revisamos DICOM ni historial crediticio. Lo único que necesitas es tener cupo disponible en tu tarjeta. Atendemos a clientes con todo tipo de historial."),
            ("¿Cuál es el costo del servicio?",
             "Nuestra comisión es del 15% del monto procesado. Recibes el 85% en tu cuenta. No hay cargos ocultos ni comisiones adicionales. Te informamos el monto exacto antes de confirmar."),
        ]
    elif bank_name:
        return [
            (f"¿Cómo veo mi cupo en dólares disponible en {bank_name}?",
             f"Ingresa a la app de {bank_name}, ve a tu tarjeta de crédito y busca 'cupo internacional' o 'línea en dólares'. También puedes llamar al servicio al cliente del banco."),
            ("¿Es legal convertir el cupo en dólares a pesos?",
             "Sí, es completamente legal. Usas tu propia línea de crédito internacional para realizar una compra. Es equivalente a comprar en un comercio internacional en línea."),
            ("¿Cuánto demora la transferencia a mi cuenta?",
             "En promedio menos de 15 minutos desde que se confirma el cargo en tu tarjeta. En horario bancario puede ser incluso más rápido."),
            ("¿Cuál es el monto mínimo y máximo?",
             "El mínimo es USD 200 y no hay máximo definido. Depende del cupo disponible en tu tarjeta. Hemos procesado operaciones hasta USD 15.000 en una sola transacción."),
        ]
    else:
        return [
            ("¿Cómo funciona el servicio de DolarExpress?",
             "Nos contactas por WhatsApp con el monto, te enviamos la cotización al instante, autorizas la operación con tu tarjeta y recibes la transferencia en tu cuenta en menos de 15 minutos."),
            ("¿Cuáles son los requisitos?",
             "Solo necesitas cupo disponible en tu tarjeta de crédito y una cuenta bancaria en Chile. No revisamos DICOM ni historial crediticio."),
            ("¿Cuánto cobra DolarExpress?",
             "Nuestra comisión es del 15% del monto. Recibes el 85% en tu cuenta bancaria. Sin costos ocultos."),
            ("¿Atienden fines de semana?",
             "Sí, atendemos de lunes a domingo incluyendo festivos. Respondemos en menos de 2 minutos por WhatsApp."),
        ]

def build_html(slug, title, desc, faqs, related_links):
    breadcrumb_name = title.replace(' | DolarExpress', '')
    faq_schema = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    schema = [
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://dolarexpress.cl"},
            {"@type": "ListItem", "position": 2, "name": breadcrumb_name, "item": f"https://dolarexpress.cl/{slug}"}
        ]},
        {"@context": "https://schema.org", "@type": "FinancialService",
         "name": "DolarExpress", "url": "https://dolarexpress.cl",
         "telephone": "+56967658939",
         "address": {"@type": "PostalAddress", "addressCountry": "CL"},
         "openingHours": "Mo-Su 09:00-21:00",
         "description": "Servicio de conversión de cupo de tarjetas a efectivo en Chile."}
    ]
    faq_html = '\n'.join([
        f'''<details class="faq-item">
  <summary>{q}</summary>
  <p>{a}</p>
</details>''' for q, a in faqs])

    related_html = '\n'.join([
        f'<a href="https://dolarexpress.cl/{s}" class="link-rel">{label}</a>'
        for s, label in related_links
    ])

    wa_url = f"https://wa.me/56967658939?text=Hola,%20quiero%20cotizar%20el%20cambio%20de%20mi%20cupo%20%E2%80%94%20llegué%20desde%20https://dolarexpress.cl/{slug}"

    return f'''<!DOCTYPE html>
<html lang="es-CL">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://dolarexpress.cl/{slug}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://dolarexpress.cl/{slug}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="es_CL" />
  <meta property="og:image" content="https://dolarexpress.cl/og-image.png" />
  <meta name="robots" content="index, follow" />
  {chr(10).join([f'  <script type="application/ld+json">{json.dumps(s)}</script>' for s in schema])}
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --verde: #00b159; --verde-dark: #007a3d; --gris: #1a1a2e;
      --gris-claro: #f5f5f5; --texto: #222; --blanco: #fff;
      --sombra: 0 2px 12px rgba(0,0,0,0.08);
    }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; color: var(--texto); background: var(--blanco); line-height: 1.7; }}
    header {{ background: var(--gris); padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; }}
    header a.logo {{ color: var(--verde); font-size: 1.4rem; font-weight: 700; text-decoration: none; }}
    header a.cta-header {{ background: var(--verde); color: #fff; padding: 8px 18px; border-radius: 24px; font-weight: 600; font-size: 0.9rem; text-decoration: none; }}
    .hero {{ background: linear-gradient(135deg, var(--gris) 0%, #16213e 100%); color: #fff; padding: 60px 20px 50px; text-align: center; }}
    .hero h1 {{ font-size: clamp(1.6rem, 4vw, 2.6rem); font-weight: 800; line-height: 1.2; margin-bottom: 16px; }}
    .hero h1 span {{ color: var(--verde); }}
    .hero p.intro {{ max-width: 640px; margin: 0 auto 28px; font-size: 1.05rem; opacity: 0.88; }}
    .hero .badges {{ display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 32px; }}
    .hero .badge {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 20px; font-size: 0.82rem; }}
    .btn-ws {{ display: inline-flex; align-items: center; gap: 10px; background: #25D366; color: #fff; padding: 14px 28px; border-radius: 50px; font-weight: 700; font-size: 1rem; text-decoration: none; box-shadow: 0 4px 20px rgba(37,211,102,0.35); }}
    .btn-ws svg {{ width: 22px; height: 22px; fill: #fff; }}
    .container {{ max-width: 820px; margin: 0 auto; padding: 0 20px; }}
    .pasos {{ background: var(--gris-claro); padding: 48px 20px; }}
    .pasos h2 {{ text-align: center; font-size: 1.5rem; margin-bottom: 32px; }}
    .pasos-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; max-width: 820px; margin: 0 auto; }}
    .paso {{ background: var(--blanco); border-radius: 12px; padding: 24px; box-shadow: var(--sombra); text-align: center; }}
    .paso .num {{ width: 44px; height: 44px; background: var(--verde); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; margin: 0 auto 12px; }}
    .paso h3 {{ font-size: 1rem; font-weight: 700; margin-bottom: 8px; }}
    .paso p {{ font-size: 0.88rem; color: #555; }}
    .content {{ padding: 48px 20px; }}
    .content h2 {{ font-size: 1.3rem; font-weight: 700; margin: 32px 0 12px; color: var(--gris); border-left: 4px solid var(--verde); padding-left: 12px; }}
    .content p {{ margin-bottom: 14px; }}
    .content ul {{ margin: 10px 0 16px 20px; }}
    .content ul li {{ margin-bottom: 6px; }}
    .faq {{ background: var(--gris-claro); padding: 48px 20px; }}
    .faq h2 {{ text-align: center; font-size: 1.5rem; margin-bottom: 28px; }}
    .faq-item {{ background: var(--blanco); border-radius: 10px; overflow: hidden; box-shadow: var(--sombra); max-width: 820px; margin: 0 auto 12px; }}
    .faq-item summary {{ padding: 16px 20px; font-weight: 600; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; }}
    .faq-item summary::after {{ content: '+'; font-size: 1.4rem; color: var(--verde); }}
    .faq-item[open] summary::after {{ content: '−'; }}
    .faq-item p {{ padding: 0 20px 16px; color: #444; }}
    .cta-final {{ background: var(--gris); color: #fff; padding: 56px 20px; text-align: center; }}
    .cta-final h2 {{ font-size: 1.7rem; margin-bottom: 12px; }}
    .cta-final p {{ opacity: 0.8; margin-bottom: 28px; max-width: 520px; margin-left: auto; margin-right: auto; }}
    .relacionados {{ padding: 40px 20px; border-top: 1px solid #eee; }}
    .relacionados h3 {{ font-size: 1rem; font-weight: 700; margin-bottom: 16px; color: #555; }}
    .links-grid {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .link-rel {{ background: var(--gris-claro); color: var(--gris); padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; text-decoration: none; border: 1px solid #ddd; }}
    .link-rel:hover {{ background: var(--verde); color: #fff; border-color: var(--verde); }}
    footer {{ background: #111; color: #aaa; padding: 24px 20px; text-align: center; font-size: 0.82rem; }}
    footer a {{ color: var(--verde); text-decoration: none; }}
    nav.breadcrumb {{ padding: 10px 20px; background: #f9f9f9; font-size: 0.85rem; color: #666; }}
    nav.breadcrumb a {{ color: var(--verde); text-decoration: none; }}
  </style>
</head>
<body>
<nav class="breadcrumb"><a href="/">Inicio</a> › <span>{breadcrumb_name}</span></nav>

<header>
  <a href="https://dolarexpress.cl" class="logo">DolarExpress</a>
  <a href="{wa_url}" class="cta-header" target="_blank" rel="noopener">Cotizar ahora →</a>
</header>

<section class="hero">
  <div class="container">
    <h1>{breadcrumb_name.replace("DolarExpress", "<span>DolarExpress</span>")}</h1>
    <p class="intro">{desc}</p>
    <div class="badges">
      <span class="badge">✓ Transferencia en 15 min</span>
      <span class="badge">✓ 100% online</span>
      <span class="badge">✓ Sin DICOM</span>
      <span class="badge">✓ Atención personalizada</span>
    </div>
    <a href="{wa_url}" class="btn-ws" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.117.554 4.103 1.523 5.828L0 24l6.338-1.498A11.955 11.955 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.007-1.374l-.36-.214-3.727.881.936-3.618-.235-.372A9.818 9.818 0 1112 21.818z"/></svg>
      Cotizar por WhatsApp
    </a>
  </div>
</section>

<section class="pasos">
  <div class="container">
    <h2>¿Cómo funciona?</h2>
    <div class="pasos-grid">
      <div class="paso"><div class="num">1</div><h3>Escríbenos</h3><p>Contáctanos por WhatsApp con el monto que quieres convertir.</p></div>
      <div class="paso"><div class="num">2</div><h3>Cotización al instante</h3><p>Te enviamos la tasa vigente y el monto exacto que recibirás.</p></div>
      <div class="paso"><div class="num">3</div><h3>Autorizas</h3><p>Confirmas la operación con tu tarjeta de forma segura.</p></div>
      <div class="paso"><div class="num">4</div><h3>Recibes</h3><p>La transferencia llega a tu cuenta bancaria en menos de 15 minutos.</p></div>
    </div>
  </div>
</section>

<section class="faq">
  <div class="container">
    <h2>Preguntas frecuentes</h2>
    {faq_html}
  </div>
</section>

<section class="cta-final">
  <div class="container">
    <h2>¿Listo para cotizar?</h2>
    <p>Escríbenos ahora y recibe tu cotización en menos de 2 minutos. Sin compromiso.</p>
    <a href="{wa_url}" class="btn-ws" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.117.554 4.103 1.523 5.828L0 24l6.338-1.498A11.955 11.955 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.007-1.374l-.36-.214-3.727.881.936-3.618-.235-.372A9.818 9.818 0 1112 21.818z"/></svg>
      Cotizar por WhatsApp
    </a>
  </div>
</section>

<section class="relacionados">
  <div class="container">
    <h3>También te puede interesar</h3>
    <div class="links-grid">
      {related_html}
    </div>
  </div>
</section>

<footer>
  <p>© 2026 DolarExpress.cl — Especialistas en compra de cupo en dólares.<br>
  <a href="https://dolarexpress.cl">Inicio</a> · <a href="https://dolarexpress.cl/directorio-general">Directorio</a> · <a href="https://dolarexpress.cl/sitemap.xml">Sitemap</a></p>
</footer>
</body>
</html>'''

def main():
    SKIP = {'404.html', 'nosotros.html'}
    upgraded = 0

    for fname in os.listdir(PUBLIC_DIR):
        if not fname.endswith('.html'):
            continue
        if fname in SKIP:
            continue

        filepath = os.path.join(PUBLIC_DIR, fname)
        # Only upgrade if it's a direct file (not in subdirectory) and is small
        if os.path.getsize(filepath) > 5000:
            continue

        slug = fname.replace('.html', '')
        title, desc = generate_meta(slug)
        faqs = generate_faq(slug)
        related = get_related_links(slug)
        html = build_html(slug, title, desc, faqs, related)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        upgraded += 1
        print(f"  ✅ Upgraded: {fname}")

    print(f"\n✨ {upgraded} páginas actualizadas con contenido completo")

if __name__ == '__main__':
    main()
