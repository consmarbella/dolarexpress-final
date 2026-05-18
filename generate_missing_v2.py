#!/usr/bin/env python3
"""
Genera páginas HTML faltantes para dolarexpress.cl:
1. Préstamo tarjeta retail × ciudad (~400 páginas)
2. Cupo de compras a efectivo × ciudad (~200 páginas)
3. Cupo dólar billeteras digitales (~50 páginas)
4. Cupo dólar monto específico × banco (~120 páginas)
"""
import os, re, json

PUBLIC = os.path.join(os.path.dirname(__file__), 'public')
WA = "https://wa.me/56967658939"
BASE = "https://dolarexpress.cl"

existing = {f.replace('.html','') for f in os.listdir(PUBLIC) if f.endswith('.html')}

def slugify(s):
    s = s.lower()
    for a,b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ü','u'),('ñ','n')]:
        s = s.replace(a,b)
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')

def title_case(s):
    return ' '.join(w.capitalize() for w in s.replace('-',' ').split())

def make_html(slug, title, desc, h1, intro, faqs, related_slugs):
    canonical = f"{BASE}/{slug}"
    wa_url = f"{WA}?text=Hola,%20vengo%20de%20la%20web%20por%20{slug}"
    faq_schema = json.dumps({
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
    }, ensure_ascii=False)
    breadcrumb_schema = json.dumps({
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Inicio","item":f"{BASE}/"},
            {"@type":"ListItem","position":2,"name":title,"item":canonical}
        ]
    }, ensure_ascii=False)
    related_aside = '\n'.join(
        f'<li><a href="{BASE}/{r}" class="text-[#C8A045] hover:underline leading-snug block">{title_case(r)}</a></li>'
        for r in related_slugs[:5]
    )
    related_footer = '\n'.join(
        f'<a href="{BASE}/{r}" style="display:inline-block;margin:4px 8px 4px 0;">{title_case(r)}</a>'
        for r in related_slugs[:5]
    )
    faq_html = '\n'.join(f'''
        <details class="border border-gray-200 rounded-xl overflow-hidden group">
          <summary class="flex justify-between items-center px-5 py-4 cursor-pointer font-semibold text-[15px] hover:bg-gray-50 transition-colors list-none">
            {q}
            <svg class="w-4 h-4 text-gray-400 transition-transform group-open:rotate-180 shrink-0 ml-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </summary>
          <div class="px-5 py-4 text-sm text-gray-600 leading-relaxed border-t border-gray-100">{a}</div>
        </details>''' for q,a in faqs)

    return f'''<!DOCTYPE html>
<html lang="es-CL">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DolarExpress</title>
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:title" content="{title} | DolarExpress" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="es_CL" />
    <meta property="og:image" content="{BASE}/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary" />
    <meta name="robots" content="index, follow" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script defer src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{theme:{{extend:{{fontFamily:{{sans:['Inter','-apple-system','sans-serif']}}}}}}}}</script>
    <script type="application/ld+json">{faq_schema}</script>
    <script type="application/ld+json">{breadcrumb_schema}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FinancialService","name":"DolarExpress","url":"{BASE}","telephone":"+56967658939","address":{{"@type":"PostalAddress","addressCountry":"CL"}},"openingHours":"Mo-Sa 09:00-21:00","description":"Servicio de conversión de cupo de tarjetas a efectivo vía Transbank."}}</script>
</head>
<body class="bg-white text-[#1a1a1a] font-sans antialiased">
<nav class="seo-home-link" style="padding:8px 12px;font-family:Arial,sans-serif"><a href="/">Inicio</a> · <a href="/directorio-general">Directorio</a></nav>

<header class="bg-[#1a1a1a] text-white sticky top-0 z-50 shadow-lg">
  <nav class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center" aria-label="Navegación principal">
    <a href="{BASE}/" class="font-black text-2xl tracking-tight text-white hover:text-[#C8A045] transition-colors">DolarExpress<span class="text-[#C8A045]">.cl</span></a>
    <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="bg-[#C8A045] hover:bg-[#a88434] text-white font-bold py-2.5 px-6 rounded-full text-sm shadow-md transition-all hover:shadow-lg">Cotizar</a>
  </nav>
</header>

<div class="max-w-6xl mx-auto px-4 py-3">
  <nav aria-label="Breadcrumb" class="text-sm text-gray-400">
    <a href="{BASE}/" class="hover:text-[#C8A045]">Inicio</a>
    <span class="mx-2">›</span>
    <span class="text-gray-600">{title}</span>
  </nav>
</div>

<main class="max-w-6xl mx-auto px-4 py-8 flex flex-col md:flex-row gap-0">
  <article class="md:w-2/3">
    <header class="mb-10">
      <h1 class="text-3xl md:text-[2.5rem] font-extrabold leading-[1.15] tracking-tight mb-6">{h1}</h1>
      <p class="text-[15px] md:text-base text-gray-600 leading-relaxed max-w-prose">{intro}</p>
    </header>

    <div class="mb-10 flex flex-col sm:flex-row gap-4 items-start">
      <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-3 bg-[#C8A045] hover:bg-[#a88434] text-white font-bold py-4 px-8 rounded-full text-lg shadow-xl hover:shadow-2xl transition-all transform hover:-translate-y-0.5">
        <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Cotizar por WhatsApp
      </a>
      <span class="text-xs text-gray-400 mt-3">Comisión: 15% · Respuesta: &lt;2 min</span>
    </div>

    <section class="mb-10">
      <h2 class="text-xl font-bold mb-6 text-[#1a1a1a]">Preguntas frecuentes</h2>
      <div class="space-y-3">{faq_html}</div>
    </section>

    <div class="bg-[#1a1a1a] rounded-2xl p-8 text-center mb-10">
      <p class="text-white text-lg font-bold mb-2">¿Quieres cotizar tu operación?</p>
      <p class="text-gray-400 text-sm mb-5">Envíanos el monto y te respondemos en menos de 2 minutos.</p>
      <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="inline-block bg-[#C8A045] hover:bg-[#a88434] text-white font-bold py-3 px-8 rounded-full shadow-lg transition-all text-sm">Cotizar Ahora</a>
    </div>
  </article>

  <aside class="md:w-1/3 mt-12 md:mt-0 md:ml-10 space-y-8">
    <div class="bg-white rounded-2xl p-6 shadow-md border border-gray-100 sticky top-20">
      <h3 class="font-bold text-lg mb-4 text-[#1a1a1a] border-b border-gray-100 pb-3">Servicios relacionados</h3>
      <ul class="space-y-3 text-sm">{related_aside}</ul>
    </div>
  </aside>
</main>

<footer class="bg-[#1a1a1a] text-gray-400 py-10 mt-8">
  <div class="max-w-6xl mx-auto px-4 text-center text-xs space-y-2">
    <p class="font-semibold text-white text-sm">DolarExpress.cl</p>
    <p>&copy; 2026 DolarExpress. Chile. Este servicio no constituye una oferta de crédito. Las condiciones de pago en cuotas son determinadas por cada emisora de la tarjeta.</p>
    <div class="flex justify-center gap-4 mt-2">
      <a href="/privacidad" class="hover:text-white transition-colors">Privacidad</a>
      <a href="/terminos" class="hover:text-white transition-colors">Términos</a>
      <a href="/contacto" class="hover:text-white transition-colors">Contacto</a>
    </div>
  </div>
</footer>

<div id="interlinking-seo" style="margin:2rem 0;padding:1rem;border-top:1px solid #eee;">
  <p><strong>Artículos relacionados:</strong></p>
  <nav>{related_footer}</nav>
</div>
</body>
</html>'''

# ─── DATOS ────────────────────────────────────────────────────────────────────

TARJETAS_RETAIL = {
    'cmr': {'nombre': 'CMR Falabella', 'banco': 'Banco Falabella', 'slug_base': 'cmr'},
    'ripley': {'nombre': 'Ripley', 'banco': 'Banco Ripley', 'slug_base': 'ripley'},
    'lider': {'nombre': 'Líder BCI', 'banco': 'BCI', 'slug_base': 'lider'},
    'paris': {'nombre': 'París Cencosud', 'banco': 'Banco Paris', 'slug_base': 'paris'},
    'la-polar': {'nombre': 'La Polar', 'banco': 'Banco La Polar', 'slug_base': 'la-polar'},
    'hites': {'nombre': 'Hites', 'banco': 'Hites', 'slug_base': 'hites'},
    'cencosud': {'nombre': 'Cencosud (Jumbo/Santa Isabel)', 'banco': 'Banco Paris', 'slug_base': 'cencosud'},
    'abcdin': {'nombre': 'ABCDin', 'banco': 'Walmart Financial', 'slug_base': 'abcdin'},
}

CIUDADES = [
    'antofagasta','arica','calama','chillan','concepcion','copiapo','coquimbo',
    'iquique','la-serena','los-angeles','osorno','puerto-montt','punta-arenas',
    'rancagua','talca','talcahuano','temuco','valdivia','valparaiso','vina-del-mar',
    'viña-del-mar',
]
# Normalizar
CIUDADES_NORM = list({slugify(c): c for c in CIUDADES}.items())  # (slug, display)

CIUDADES_DISPLAY = {
    'antofagasta': 'Antofagasta', 'arica': 'Arica', 'calama': 'Calama',
    'chillan': 'Chillán', 'concepcion': 'Concepción', 'copiapo': 'Copiapó',
    'coquimbo': 'Coquimbo', 'iquique': 'Iquique', 'la-serena': 'La Serena',
    'los-angeles': 'Los Ángeles', 'osorno': 'Osorno', 'puerto-montt': 'Puerto Montt',
    'punta-arenas': 'Punta Arenas', 'rancagua': 'Rancagua', 'talca': 'Talca',
    'talcahuano': 'Talcahuano', 'temuco': 'Temuco', 'valdivia': 'Valdivia',
    'valparaiso': 'Valparaíso', 'vina-del-mar': 'Viña del Mar',
    'concepcion': 'Concepción',
}

BANCOS_DOLAR = {
    'banco-chile': 'Banco Chile', 'bancoestado': 'BancoEstado', 'bci': 'BCI',
    'santander': 'Santander', 'itau': 'Itaú', 'scotiabank': 'Scotiabank',
    'security': 'Banco Security', 'bice': 'Banco BICE', 'falabella': 'Banco Falabella',
    'ripley': 'Banco Ripley',
}

MONTOS_USD = [200, 500, 1000, 2000, 3000, 5000, 7000]

BILLETERAS = {
    'mach': 'MACH (BCI)', 'mercadopago': 'Mercado Pago', 'tenpo': 'Tenpo',
    'tapp': 'TAPP Caja Los Andes', 'cuenta-rut': 'Cuenta RUT BancoEstado',
    'coopeuch': 'Coopeuch',
}

created = 0
skipped = 0

# ─── 1. PRÉSTAMO TARJETA RETAIL × CIUDAD ─────────────────────────────────────
for t_slug, t_data in TARJETAS_RETAIL.items():
    nombre = t_data['nombre']
    banco = t_data['banco']
    for c_slug, c_display in CIUDADES_DISPLAY.items():
        slug = f"prestamo-tarjeta-{t_slug}-{c_slug}"
        if slug in existing:
            skipped += 1
            continue
        title = f"Préstamo con Tarjeta {nombre} en {c_display}"
        desc = f"Convierte el cupo de tu tarjeta {nombre} en efectivo en {c_display}. Operamos vía Transbank, sin avance habilitado. Transferencia en 15 minutos a cualquier cuenta bancaria."
        h1 = f"Préstamo con Tarjeta {nombre} en {c_display}"
        intro = f"Si estás en {c_display} y necesitas efectivo rápido, DolarExpress convierte el cupo de compras de tu tarjeta {nombre} en pesos directamente a tu cuenta. No necesitas tener el avance habilitado: usamos el cupo de compras a través de Transbank. Recibes el 85% del monto solicitado en menos de 15 minutos. El cargo queda como compra en cuotas en {banco}."
        faqs = [
            (f"¿Puedo usar mi tarjeta {nombre} aunque esté en {c_display} y no en Santiago?",
             f"Sí. El servicio es 100% remoto. Desde {c_display} solo necesitas tu tarjeta {nombre}, el número y CVV. Autorizas la compra en Transbank y recibis la transferencia en tu cuenta bancaria en cualquier banco de Chile."),
            (f"¿Necesito tener el avance habilitado en mi tarjeta {nombre}?",
             f"No. DolarExpress trabaja con el cupo de compras, no con el avance. Aunque el avance esté bloqueado o nunca lo hayas activado, puedes operar si tienes cupo de compras disponible en tu tarjeta {nombre}."),
            (f"¿Cuánto demora la operación desde {c_display}?",
             f"Menos de 30 minutos desde el primer contacto por WhatsApp hasta que el dinero llega a tu cuenta. La transferencia en sí tarda menos de 15 minutos una vez autorizada la transacción en Transbank."),
            (f"¿Qué comisión cobra DolarExpress por usar la tarjeta {nombre}?",
             f"La comisión es del 15% del monto operado. Si solicitas $100.000, recibes $85.000 en tu cuenta. El total ($100.000) queda registrado como compra en cuotas en {banco}."),
        ]
        related = [
            f"prestamo-con-tarjeta-{t_slug}",
            f"avance-efectivo-tarjeta-{t_slug}",
            f"cupo-compras-a-efectivo-{t_slug}",
            f"credito-con-tarjeta-{t_slug}",
            f"prestamo-tarjeta-{t_slug}-online",
        ]
        html = make_html(slug, title, desc, h1, intro, faqs, related)
        with open(f"{PUBLIC}/{slug}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        existing.add(slug)
        created += 1
    if created % 50 == 0 and created > 0:
        print(f"  Progreso: {created} archivos creados...")

# ─── 2. CUPO DE COMPRAS A EFECTIVO × CIUDAD ──────────────────────────────────
for t_slug, t_data in TARJETAS_RETAIL.items():
    nombre = t_data['nombre']
    banco = t_data['banco']
    for c_slug, c_display in CIUDADES_DISPLAY.items():
        slug = f"cupo-compras-efectivo-{t_slug}-{c_slug}"
        if slug in existing:
            skipped += 1
            continue
        title = f"Cupo de Compras a Efectivo {nombre} en {c_display}"
        desc = f"Convierte el cupo de compras de tu tarjeta {nombre} en efectivo en {c_display}. Sin avance, sin banco, sin DICOM. Vía Transbank, transferencia en 15 minutos."
        h1 = f"Cupo de Compras {nombre} a Efectivo en {c_display}"
        intro = f"El cupo de compras de tu tarjeta {nombre} puede convertirse en pesos en efectivo aunque no tengas avance habilitado. DolarExpress opera desde {c_display} de forma 100% remota: autorizas una compra vía Transbank y recibis el 85% del monto en tu cuenta bancaria en menos de 15 minutos. Sin DICOM, sin liquidaciones, sin garante."
        faqs = [
            (f"¿Qué diferencia hay entre cupo de compras y avance en la tarjeta {nombre}?",
             f"El avance es efectivo directo del banco con su propia tasa de interés. El cupo de compras es el límite para comprar en comercios. DolarExpress usa el cupo de compras (no el avance) procesándolo como una compra en Transbank, lo que permite operar incluso sin avance habilitado."),
            (f"¿Puedo operar desde {c_display} sin ir a ninguna sucursal?",
             f"Sí, el proceso es 100% remoto. Desde {c_display} solo necesitas WhatsApp y tu tarjeta {nombre}. Te guiamos para autorizar la compra en Transbank y enviamos el dinero a tu cuenta en cualquier banco de Chile."),
            (f"¿Cuánto cupo de compras necesito tener disponible?",
             f"El monto mínimo operado es generalmente $50.000. El máximo depende del cupo disponible en tu tarjeta {nombre}. Puedes verificar tu cupo disponible en la app de {banco} o llamando al número de atención al cliente de tu tarjeta."),
            (f"¿Aparece como compra en cuotas en mi tarjeta {nombre}?",
             f"Sí. La operación aparece como una compra en cuotas en tu estado de cuenta de {banco}. Puedes elegir el número de cuotas disponibles para esa compra según las opciones que ofrece {banco}."),
        ]
        related = [
            f"cupo-compras-a-efectivo-{t_slug}",
            f"prestamo-tarjeta-{t_slug}-{c_slug}",
            f"avance-efectivo-tarjeta-{t_slug}",
            f"convertir-cupo-{t_slug}-efectivo",
            f"prestamo-con-tarjeta-{t_slug}",
        ]
        html = make_html(slug, title, desc, h1, intro, faqs, related)
        with open(f"{PUBLIC}/{slug}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        existing.add(slug)
        created += 1
    if created % 50 == 0:
        print(f"  Progreso: {created} archivos creados...")

# ─── 3. CUPO DÓLAR BILLETERAS DIGITALES ──────────────────────────────────────
for b_slug, b_nombre in BILLETERAS.items():
    slug = f"cupo-dolar-{b_slug}"
    if slug not in existing:
        title = f"Cupo Dólar con {b_nombre}"
        desc = f"Vende tu cupo dólar de {b_nombre} y recibe pesos al instante. DolarExpress compra cupos dólar de billeteras digitales y tarjetas prepago. Transferencia inmediata."
        h1 = f"Cupo Dólar {b_nombre} a Pesos"
        intro = f"Si tienes cupo dólar disponible en {b_nombre} y necesitas pesos, DolarExpress te compra ese cupo de forma segura y rápida. El proceso es 100% remoto: contacta por WhatsApp, indicamos el tipo de cambio del día, autorizas la operación y recibes los pesos en tu cuenta en menos de 15 minutos. Sin complicaciones ni riesgos."
        faqs = [
            (f"¿DolarExpress compra cupo dólar de {b_nombre}?",
             f"Sí. Compramos cupo dólar de {b_nombre} al tipo de cambio de mercado del día. Contáctanos por WhatsApp con el monto disponible y te cotizamos de inmediato."),
            ("¿Cómo funciona la operación de cupo dólar?",
             "Nos indicas el monto en dólares disponible en tu cuenta. Te enviamos el tipo de cambio aplicable. Autorizas la transacción desde tu cuenta y recibis los pesos en tu cuenta bancaria chilena en menos de 15 minutos."),
            ("¿Es seguro vender el cupo dólar?",
             "Sí. DolarExpress opera de forma transparente: siempre recibes el pago antes o simultáneamente a la operación. Nunca pedimos claves bancarias ni acceso a tu cuenta. Solo autorizas desde tu propia aplicación."),
            ("¿Qué tipo de cambio aplican?",
             "Aplicamos el tipo de cambio de mercado del momento, similar al dólar observado. El precio exacto se informa al inicio de cada operación y es fijo para esa transacción. No hay costos ocultos."),
        ]
        related = [
            "cupo-dolar-online", "vender-cupo-dolar", "cupo-dolar-rapido",
            "cupo-dolar-transferencia-inmediata", "cupo-dolar-sin-cuenta-bancaria",
        ]
        html = make_html(slug, title, desc, h1, intro, faqs, related)
        with open(f"{PUBLIC}/{slug}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        existing.add(slug)
        created += 1

    # Ciudad × billetera
    for c_slug, c_display in list(CIUDADES_DISPLAY.items())[:10]:
        slug2 = f"cupo-dolar-{b_slug}-{c_slug}"
        if slug2 in existing:
            skipped += 1
            continue
        title2 = f"Cupo Dólar {b_nombre} en {c_display}"
        desc2 = f"Vende tu cupo dólar de {b_nombre} en {c_display} y recibe pesos al instante. DolarExpress opera 100% remoto desde cualquier ciudad de Chile."
        h1_2 = f"Cupo Dólar {b_nombre} en {c_display} — Pesos al Instante"
        intro2 = f"Desde {c_display} puedes vender el cupo dólar de tu cuenta {b_nombre} a DolarExpress sin moverte de tu casa. Operamos 100% por WhatsApp: cotizamos el tipo de cambio del momento, autorizas la transacción y recibes los pesos en tu cuenta bancaria en menos de 15 minutos."
        faqs2 = [
            (f"¿Puedo vender mi cupo dólar {b_nombre} estando en {c_display}?",
             f"Sí. El servicio es completamente remoto. Desde {c_display} solo necesitas tu cuenta {b_nombre} y WhatsApp. No es necesario ir a ninguna oficina ni sucursal."),
            ("¿Qué documentos necesito para la operación?",
             "Ningún documento. Solo necesitas tener la aplicación de tu billetera digital activa y cupo dólar disponible. El proceso completo se realiza desde tu teléfono."),
            ("¿Cuánto tiempo demora la transferencia a mi cuenta?",
             f"Menos de 15 minutos desde que autorizas la operación. La transferencia llega a cualquier banco de Chile, incluyendo los principales bancos con sucursales en {c_display}."),
            ("¿Hay monto mínimo para operar?",
             "El monto mínimo es USD 100. No hay monto máximo, aunque para montos mayores a USD 5.000 te pedimos coordinar con anticipación para confirmar disponibilidad."),
        ]
        related2 = [
            f"cupo-dolar-{b_slug}", "cupo-dolar-online", "vender-cupo-dolar",
            f"vender-cupo-dolar-{c_slug}", "cupo-dolar-rapido",
        ]
        html2 = make_html(slug2, title2, desc2, h1_2, intro2, faqs2, related2)
        with open(f"{PUBLIC}/{slug2}.html", 'w', encoding='utf-8') as f:
            f.write(html2)
        existing.add(slug2)
        created += 1

# ─── 4. CUPO DÓLAR MONTO ESPECÍFICO × BANCO ──────────────────────────────────
for monto in MONTOS_USD:
    for b_slug, b_nombre in BANCOS_DOLAR.items():
        slug = f"cupo-dolar-{monto}-usd-{b_slug}"
        if slug in existing:
            skipped += 1
            continue
        monto_clp = f"${monto * 950:,}".replace(',','.')  # approx
        title = f"Cupo Dólar USD {monto:,} {b_nombre}".replace(',','.')
        desc = f"Vende {monto} USD de cupo dólar de {b_nombre} y recibe pesos hoy. DolarExpress compra tu cupo dólar al mejor precio. Transferencia en 15 minutos."
        h1 = f"Cupo Dólar USD {monto} con {b_nombre} — Cotiza Ahora"
        intro = f"Si tienes USD {monto} disponibles en el cupo dólar de tu tarjeta {b_nombre} y necesitas pesos, DolarExpress te compra ese cupo al tipo de cambio del momento. Recibes aproximadamente {monto_clp} pesos (varía según dólar del día) directamente en tu cuenta bancaria en menos de 15 minutos. El proceso es 100% por WhatsApp, sin papeleos."
        faqs = [
            (f"¿Cuántos pesos recibo por USD {monto} del cupo dólar de {b_nombre}?",
             f"Depende del tipo de cambio del día. Con el dólar en torno a $950 CLP, USD {monto} equivale aproximadamente a {monto_clp} pesos. Te damos el precio exacto al inicio de cada operación."),
            (f"¿Puedo vender exactamente USD {monto} o debo vender todo el cupo?",
             f"Puedes vender el monto que quieras, no es necesario vender todo el cupo disponible. Si tienes USD 2.000 pero solo quieres vender USD {monto}, operamos por ese monto específico."),
            (f"¿{b_nombre} cobra comisión por usar el cupo dólar?",
             f"Eso depende de tu contrato con {b_nombre}. Algunos bancos cobran una comisión por transacción en dólares. Te recomendamos verificar con tu banco antes de operar. El precio que te damos en DolarExpress es el neto que recibes tú."),
            ("¿Cómo se autoriza la operación de cupo dólar?",
             "Desde tu banca online o app de tu banco, autorizas una compra o retiro en dólares según las instrucciones que te enviamos por WhatsApp. El proceso es igual a como usarías tu tarjeta para una compra internacional."),
        ]
        related = [
            f"cupo-dolar-{b_slug}", f"cupo-dolar-{monto}-usd" if f"cupo-dolar-{monto}-usd" in existing else "cupo-dolar-online",
            "vender-cupo-dolar", "cupo-dolar-rapido", "cupo-dolar-transferencia-inmediata",
        ]
        html = make_html(slug, title, desc, h1, intro, faqs, related)
        with open(f"{PUBLIC}/{slug}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        existing.add(slug)
        created += 1

print(f"\n=== DONE ===")
print(f"Archivos creados: {created}")
print(f"Archivos omitidos (ya existían): {skipped}")
print(f"Total HTML en /public/ ahora: {len([f for f in os.listdir(PUBLIC) if f.endswith('.html')])}")
