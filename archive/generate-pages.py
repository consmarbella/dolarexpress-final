#!/usr/bin/env python3
"""Generate remaining SEO pages for dolarexpress.cl"""
import os

PUBLIC = r"c:\Users\matte\OneDrive\Escritorio\dolarexpress-final-main\public"

def fix_mastercard_platinum():
    """Fix the truncated mastercard-platinum page"""
    path = os.path.join(PUBLIC, "cupo-dolar-mastercard-platinum.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "div class=\"metrics\"" in content and "</main>" not in content:
        # Page is truncated, rewrite it
        pass
    return content

def make_page(filename, title, desc, canonical, breadcrumb, eyebrow, h1, lead, faqs, related):
    """Generate a complete HTML page"""
    faq_items = "\n".join(f'<dt>{q}</dt><dd>{a}</dd>' for q, a in faqs)
    related_items = "\n".join(
        f'<a href="{url}" style="font-size:12px;color:#d4af37;border:1px solid rgba(212,175,55,0.3);padding:4px 10px;border-radius:999px;text-decoration:none;white-space:nowrap;">{text}</a>'
        for url, text in related
    )
    
    faq_json = ",".join(
        '{"@type":"Question","name":"' + q + '","acceptedAnswer":{"@type":"Answer","text":"' + a + '"}}'
        for q, a in faqs
    )
    
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="https://dolarexpress.cl{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://dolarexpress.cl{canonical}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://dolarexpress.cl/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"LocalBusiness","name":"DolarExpress","url":"https://dolarexpress.cl","telephone":"+56967658939","address":{{"@type":"PostalAddress","addressCountry":"CL","addressLocality":"Santiago"}},"description":"Servicio de cambio de cupo en dólares a pesos chilenos","priceRange":"$$"}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Inicio","item":"https://dolarexpress.cl"}},{{"@type":"ListItem","position":2,"name":"{breadcrumb}","item":"https://dolarexpress.cl{canonical}"}}]}},
{{"@type":"FAQPage","mainEntity":[{faq_json}]}}
]}}
</script>
<style>
:root{{--accent:#d4af37;--text:#f9fafb;--muted:#9ca3af;--wa:#25D366;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:radial-gradient(circle at top,#111827 0,#020617 55%,#000 100%);color:var(--text);min-height:100vh;display:flex;flex-direction:column;}}
a{{color:var(--accent);text-decoration:none;}}a:hover{{text-decoration:underline;}}
header{{border-bottom:1px solid rgba(31,41,55,0.9);backdrop-filter:blur(14px);background:radial-gradient(circle at top left,rgba(212,175,55,0.08),transparent 55%),linear-gradient(to right,rgba(15,23,42,0.96),rgba(3,7,18,0.98));position:sticky;top:0;z-index:20;}}
.nav{{max-width:960px;margin:0 auto;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;}}
.logo{{display:inline-flex;align-items:center;gap:10px;font-weight:700;letter-spacing:0.04em;text-transform:uppercase;color:var(--text);}}
.logo-mark{{width:32px;height:32px;border-radius:999px;background:radial-gradient(circle at 30% 20%,#facc15,#d4af37 40%,#854d0e 100%);display:inline-flex;align-items:center;justify-content:center;color:#020617;font-weight:900;font-size:18px;box-shadow:0 0 0 1px rgba(0,0,0,0.6),0 16px 40px rgba(0,0,0,0.8);}}
.logo-sub{{font-size:11px;color:var(--muted);text-transform:none;letter-spacing:0.02em;}}
.badge{{font-size:11px;padding:3px 8px;border-radius:999px;border:1px solid rgba(148,163,184,0.7);color:var(--muted);display:inline-flex;align-items:center;gap:4px;}}
.badge-dot{{width:6px;height:6px;border-radius:999px;background:#22c55e;box-shadow:0 0 0 4px rgba(34,197,94,0.25);}}
.breadcrumb{{max-width:960px;margin:0 auto;padding:10px 16px;font-size:12px;color:var(--muted);}}
main{{flex:1;max-width:960px;width:100%;margin:0 auto;padding:24px 16px 40px;display:grid;grid-template-columns:minmax(0,3fr) minmax(280px,2fr);gap:28px;}}
@media(max-width:800px){{main{{grid-template-columns:minmax(0,1fr);}}header{{position:static;}}}}
.card{{background:radial-gradient(circle at top left,rgba(148,163,184,0.12),transparent 55%),linear-gradient(to bottom right,rgba(15,23,42,0.96),rgba(2,6,23,0.98));border-radius:18px;border:1px solid rgba(148,163,184,0.25);box-shadow:0 22px 60px rgba(2,6,23,0.85);padding:22px 20px;position:relative;overflow:hidden;}}
.card::before{{content:"";position:absolute;inset:-2px;background:radial-gradient(circle at top,rgba(212,175,55,0.2),transparent 60%);opacity:0.8;pointer-events:none;mix-blend-mode:soft-light;}}
.card-inner{{position:relative;z-index:1;}}
.eyebrow{{font-size:11px;text-transform:uppercase;letter-spacing:0.16em;color:var(--muted);display:inline-flex;align-items:center;gap:6px;margin-bottom:8px;}}
.eyebrow-line{{width:22px;height:1px;background:linear-gradient(to right,transparent,rgba(148,163,184,0.8));}}
h1{{font-size:clamp(22px,3vw,28px);margin:0 0 8px;letter-spacing:-0.03em;}}
.highlight{{color:var(--accent);}}
.lead{{color:var(--muted);font-size:14px;line-height:1.6;margin:0 0 16px;max-width:460px;}}
.pill-row{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px;}}
.pill{{font-size:11px;padding:4px 9px;border-radius:999px;border:1px solid rgba(148,163,184,0.4);color:var(--muted);background:radial-gradient(circle at top left,rgba(15,23,42,0.9),rgba(3,7,18,0.95));display:inline-flex;align-items:center;gap:4px;}}
.pill strong{{color:var(--text);font-weight:600;}}
.metrics{{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:22px;}}
.metric-item{{padding:10px 12px;border-radius:12px;border:1px solid rgba(31,41,55,0.9);background:radial-gradient(circle at top left,rgba(15,23,42,0.9),rgba(3,7,18,0.98));min-width:140px;}}
.metric-label{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:2px;}}
.metric-value{{font-size:15px;color:var(--text);font-weight:600;}}
.metric-sub{{font-size:11px;color:var(--muted);}}
.cta-row{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:10px;}}
.btn-wa{{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 18px;border-radius:999px;background:linear-gradient(to right,var(--wa),#128C7E);color:#f9fafb;font-size:14px;font-weight:600;border:none;cursor:pointer;box-shadow:0 12px 30px rgba(5,150,105,0.65),0 0 0 1px rgba(6,95,70,0.7);text-decoration:none;white-space:nowrap;}}
.btn-outline{{display:inline-flex;align-items:center;padding:9px 14px;border-radius:999px;border:1px solid rgba(148,163,184,0.9);background:radial-gradient(circle at top left,rgba(15,23,42,0.96),rgba(3,7,18,0.98));color:var(--muted);font-size:12px;text-decoration:none;}}
.cta-note{{font-size:11px;color:var(--muted);margin-bottom:16px;}}
.section-title{{font-size:13px;text-transform:uppercase;letter-spacing:0.16em;color:var(--muted);margin:22px 0 6px;}}
.list{{margin:0;padding-left:18px;font-size:13px;color:var(--muted);line-height:1.7;}}
.list li+li{{margin-top:4px;}}
.faq{{font-size:13px;color:var(--muted);margin-top:12px;}}
.faq dt{{font-weight:600;color:var(--text);margin-top:8px;margin-bottom:2px;}}
.faq dd{{margin:0 0 6px;}}
.related{{margin-top:20px;}}
.related-title{{font-size:12px;text-transform:uppercase;letter-spacing:0.12em;color:var(--muted);margin-bottom:8px;}}
.related-links{{display:flex;flex-wrap:wrap;gap:6px;}}
.side-card{{background:radial-gradient(circle at top right,rgba(212,175,55,0.16),transparent 60%),linear-gradient(to bottom,rgba(15,23,42,0.98),rgba(3,7,18,0.98));border-radius:18px;border:1px solid rgba(148,163,184,0.3);padding:18px 16px;box-shadow:0 18px 50px rgba(2,6,23,0.95);position:sticky;top:68px;align-self:flex-start;}}
.side-title{{font-size:14px;font-weight:600;margin:0 0 4px;}}
.side-sub{{font-size:12px;color:var(--muted);margin:0 0 12px;}}
.side-list{{margin:0 0 10px;padding:0;list-style:none;font-size:12px;color:var(--muted);}}
.side-list li{{display:flex;align-items:center;gap:6px;margin-bottom:6px;}}
.side-dot{{width:6px;height:6px;border-radius:999px;background:var(--accent);box-shadow:0 0 0 3px rgba(212,175,55,0.25);}}
footer{{border-top:1px solid rgba(31,41,55,0.9);background:linear-gradient(to bottom,rgba(15,23,42,0.98),rgba(2,6,23,0.98));padding:14px 16px;font-size:12px;color:var(--muted);}}
.footer-inner{{max-width:960px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;}}
.footer-links{{display:flex;flex-wrap:wrap;gap:10px;}}
</style>
</head>
<body>
<header>
  <div class="nav">
    <a href="/" class="logo">
      <span class="logo-mark">$</span>
      <span>DolarExpress<div class="logo-sub">Cambio de cupo en dólares a pesos chilenos</div></span>
    </a>
    <span class="badge"><span class="badge-dot"></span>Transferencia inmediata en Chile</span>
  </div>
</header>
<div class="breadcrumb">
  <a href="/">Inicio</a> › {breadcrumb}
</div>
<main>
  <section class="card">
    <div class="card-inner">
      <div class="eyebrow"><span class="eyebrow-line"></span>{eyebrow}</div>
      <h1><span class="highlight">{h1}</span></h1>
      <p class="lead">{lead}</p>
      <div class="pill-row">
        <span class="pill"><strong>✔</strong> Proceso transparente</span>
        <span class="pill"><strong>✔</strong> Tasa del día</span>
        <span class="pill"><strong>✔</strong> Respuesta inmediata</span>
      </div>
      <div class="metrics">
        <div class="metric-item"><div class="metric-label">Operaciones</div><div class="metric-value">+1.800</div><div class="metric-sub">Transacciones realizadas</div></div>
        <div class="metric-item"><div class="metric-label">Tiempo promedio</div><div class="metric-value">2 horas</div><div class="metric-sub">De inicio a transferencia</div></div>
      </div>
      <div class="cta-row">
        <a class="btn-wa" href="https://wa.me/56967658939?text=Hola%20quiero%20vender%20mi%20cupo%20en%20d%C3%B3lares" target="_blank" rel="noopener noreferrer">✆ Cotizar por WhatsApp</a>
        <a href="/" class="btn-outline">Volver al inicio</a>
      </div>
      <p class="cta-note">Te explicamos todo antes de avanzar. Sin compromiso.</p>
      <h2 class="section-title">Cómo funciona</h2>
      <ol class="list">
        <li>Escríbenos por WhatsApp con tu monto disponible en USD.</li>
        <li>Revisamos la tasa vigente y te informamos el CLP a recibir.</li>
        <li>Coordinamos la operación con tu banco paso a paso.</li>
        <li>Recibes los pesos en tu cuenta bancaria en Chile.</li>
      </ol>
      <h2 class="section-title">Preguntas frecuentes</h2>
      <dl class="faq">
{faq_items}
      </dl>
      <div class="related">
        <div class="related-title">Servicios relacionados</div>
        <div class="related-links">
{related_items}
        </div>
      </div>
    </div>
  </section>
  <aside class="side-card">
    <h2 class="side-title">¿Primera vez?</h2>
    <p class="side-sub">Te explicamos todo el proceso sin compromiso.</p>
    <ul class="side-list">
      <li><span class="side-dot"></span>Más de 1.800 operaciones</li>
      <li><span class="side-dot"></span>Clientes en todo Chile</li>
      <li><span class="side-dot"></span>Proceso 100% online</li>
      <li><span class="side-dot"></span>Sin letra chica</li>
    </ul>
    <a class="btn-wa" href="https://wa.me/56967658939?text=Hola%20quiero%20vender%20mi%20cupo%20en%20d%C3%B3lares" target="_blank" rel="noopener noreferrer">✆ Hablar por WhatsApp</a>
  </aside>
</main>
<footer>
  <div class="footer-inner">
    <span>DolarExpress · Cambio de cupo en dólares a pesos chilenos</span>
    <div class="footer-links">
      <a href="/privacidad">Política de privacidad</a>
      <a href="/terminos">Términos y condiciones</a>
      <a href="/contacto">Contacto</a>
    </div>
  </div>
</footer>
</body>
</html>'''

# Pages to generate
pages = [
    # Fix mastercard-platinum (truncated)
    {
        "filename": "cupo-dolar-mastercard-platinum.html",
        "title": "Cupo en Dólares Mastercard Platinum → Vende hoy | DolarExpress",
        "desc": "Vende tu cupo en dólares Mastercard Platinum y recibe pesos chilenos al instante. Cupo en dólares mastercard platinum a pesos. Cotiza por WhatsApp.",
        "canonical": "/cupo-dolar-mastercard-platinum",
        "breadcrumb": "Cupo en Dólares Mastercard Platinum",
        "eyebrow": "Tarjeta Mastercard Platinum",
        "h1": "Cupo en Dólares Mastercard Platinum → Vende hoy",
        "lead": "¿Tienes cupo en dólares en tu Mastercard Platinum? Conviértelo a pesos chilenos con DolarExpress. Rápido, seguro y sin complicaciones.",
        "faqs": [
            ("¿Funciona con Mastercard Platinum?", "Sí, aceptamos Mastercard Platinum con cupo internacional activo."),
            ("¿Cuánto cupo puedo vender?", "Depende del cupo disponible en tu tarjeta Mastercard Platinum."),
            ("¿Cuánto tarda la operación?", "Normalmente el mismo día si contactas en horario hábil."),
        ],
        "related": [
            ("/cupo-dolar-mastercard", "cupo dolar mastercard"),
            ("/cupo-dolar-visa", "cupo dolar visa"),
            ("/cupo-dolar-american-express", "cupo dolar american express"),
            ("/vender-cupo-dolar", "vender cupo dolar"),
        ]
    },
    {
        "filename": "cupo-dolar-visa-gold.html",
        "title": "Cupo en Dólares Visa Gold → Vende tu cupo hoy | DolarExpress",
        "desc": "Vende tu cupo en dólares Visa Gold y recibe pesos chilenos al instante. Cupo en dólares visa gold a pesos chilenos. Cotiza por WhatsApp.",
        "canonical": "/cupo-dolar-visa-gold",
        "breadcrumb": "Cupo en Dólares Visa Gold",
        "eyebrow": "Tarjeta Visa Gold",
        "h1": "Cupo en Dólares Visa Gold → Vende tu cupo hoy",
        "lead": "¿Tienes cupo en dólares en tu Visa Gold? Conviértelo a pesos chilenos con DolarExpress. Proceso rápido, seguro y 100% online.",
        "faqs": [
            ("¿Funciona con Visa Gold?", "Sí, aceptamos Visa Gold con cupo internacional activo."),
            ("¿Qué bancos emiten Visa Gold?", "La mayoría de los bancos chilenos emiten Visa Gold. Consulta por el tuyo."),
            ("¿Cuánto tarda la operación?", "Normalmente el mismo día si contactas en horario hábil."),
        ],
        "related": [
            ("/cupo-dolar-visa", "cupo dolar visa"),
            ("/cupo-dolar-mastercard", "cupo dolar mastercard"),
            ("/cupo-dolar-american-express", "cupo dolar american express"),
            ("/vender-cupo-dolar", "vender cupo dolar"),
        ]
    },
    {
        "filename": "cupo-dolar-mastercard-black.html",
        "title": "Cupo en Dólares Mastercard Black → Vende hoy | DolarExpress",
        "desc": "Vende tu cupo en dólares Mastercard Black y recibe pesos chilenos al instante. Cupo en dólares mastercard black a pesos. Cotiza por WhatsApp.",
        "canonical": "/cupo-dolar-mastercard-black",
        "breadcrumb": "Cupo en Dólares Mastercard Black",
        "eyebrow": "Tarjeta Mastercard Black",
        "h1": "Cupo en Dólares Mastercard Black → Vende hoy",
        "lead": "¿Tienes cupo en dólares en tu Mastercard Black? Conviértelo a pesos chilenos con DolarExpress. Atención personalizada y rápida.",
        "faqs": [
            ("¿Funciona con Mastercard Black?", "Sí, aceptamos Mastercard Black con cupo internacional activo."),
            ("¿Hay montos máximos?", "Trabajamos con montos desde USD 300 hasta montos mayores. Consulta por tu caso."),
            ("¿Cuánto tarda la operación?", "Normalmente el mismo día si contactas en horario hábil."),
        ],
        "related": [
            ("/cupo-dolar-mastercard", "cupo dolar mastercard"),
            ("/cupo-dolar-visa", "cupo dolar visa"),
            ("/cupo-dolar-altos-montos", "cupo dolar altos montos"),
            ("/vender-cupo-dolar", "vender cupo dolar"),
        ]
    },
    {
        "filename": "cupo-dolar-cencosud.html",
        "title": "Cupo en Dólares Cencosud → Vende tu cupo hoy | DolarExpress",
        "desc": "Vende tu cupo en dólares tarjeta Cencosud y recibe pesos chilenos al instante. Cupo en dólares cencosud a pesos. Cotiza por WhatsApp.",
        "canonical": "/cupo-dolar-cencosud",
        "breadcrumb": "Cupo en Dólares Cencosud",
        "eyebrow": "Tarjeta Cencosud",
        "h1": "Cupo en Dólares Cencosud → Vende tu cupo hoy",
        "lead": "¿Tienes cupo en dólares en tu tarjeta Cencosud? Conviértelo a pesos chilenos con DolarExpress. Proceso rápido y sin complicaciones.",
        "faqs": [
            ("¿Funciona con tarjeta Cencosud?", "Sí, aceptamos tarjetas Cencosud (Paris) con cupo internacional activo."),
            ("¿Cómo activo el cupo internacional Cencosud?", "En la app Cencosud o llamando al banco."),
            ("¿Cuánto cupo puedo usar?", "El disponible en tu tarjeta Cencosud."),
        ],
        "related": [
            ("/cupo-dolar-cmr", "cupo dolar cmr"),
            ("/cupo-dolar-ripley", "cupo dolar ripley"),
            ("/cupo-dolar-falabella", "cupo dolar falabella"),
            ("/vender-cupo-dolar", "vender cupo dolar"),
        ]
    },
    {
        "filename": "cupo-dolar-consorcio.html",
        "title": "Cupo en Dólares Consorcio → Vende tu cupo hoy | DolarExpress",
        "desc": "Vende tu cupo en dólares Consorcio y recibe pesos chilenos al instante. Cupo en dólares consorcio a pesos chilenos. Cotiza por WhatsApp.",
        "canonical": "/cupo-dolar-consorcio",
        "breadcrumb": "Cupo en Dólares Consorcio",
        "eyebrow": "Tarjeta Consorcio",
        "h1": "Cupo en Dólares Consorcio → Vende tu cupo hoy",
        "lead": "¿Tienes cupo en dólares en tu tarjeta Consorcio? Conviértelo a pesos chilenos con DolarExpress. Rápido, seguro y online.",
        "faqs": [
            ("¿Funciona con tarjeta Consorcio?", "Sí, aceptamos tarjetas Consorcio con cupo internacional activo."),
            ("¿Cómo verifico mi cupo Consorcio?", "En la app Consorcio o llamando al banco."),
            ("¿Cuánto tarda la operación?", "Normalmente el mismo día si contactas en horario hábil."),
        ],
        "related": [
            ("/cupo-dolar-cmr", "cupo dolar cmr"),
            ("/cupo-dolar-ripley", "cupo dolar ripley"),
            ("/cupo-dolar-falabella", "cupo dolar falabella"),
            ("/vender-cupo-dolar", "vender cupo dolar"),
        ]
    },
    {
        "filename": "cupo-dolar-coopeuch.html",
        "title": "Cupo en Dólares Coopeuch → Vende tu cupo hoy | DolarExpress",
        "desc": "Vende tu cupo en dólares Coopeuch y recibe pesos chilenos al instante. Cupo en dólares coopeuch a pesos chilenos. Cotiza por WhatsApp.",
        "canonical": "/cupo-dolar-coopeuch",
        "breadcrumb": "Cupo en Dólares Coopeuch",
        "eyebrow": "Tarjeta Coopeuch",
        "h1": "Cupo en Dólares Coopeuch → Vende tu cupo hoy",
        "lead": "¿Tienes cupo en dólares en tu tarjeta Coopeuch? Conviértelo a pesos chilenos con DolarExpress. Proceso simple y acompañamiento personalizado.",
        "faqs": [
            ("¿Funciona con Coopeuch?", "Sí, aceptamos tarjetas Coopeuch con cupo internacional activo."),
            ("¿Cómo activo el cupo internacional Coopeuch?", "En la app Coopeuch o llamando a la cooperativa."),
            ("¿Cuánto tarda la operación?", "Normalmente el mismo día si contactas en horario hábil."),
        ],
        "related": [
            ("/cupo-dolar-cmr", "cupo dolar cmr"),
            ("/cupo-dolar-ripley", "cupo dolar ripley"),
            ("/cupo-dolar-falabella", "cupo dolar falabella"),
            ("/vender-cupo-dolar", "vender cupo dolar"),
        ]
    },
    {
        "filename": "cupo-dolar-lider.html",
        "title": "Cupo en Dólares Tarjeta Líder → Vende tu cupo hoy | DolarExpress",
        "desc": "Vende tu cupo en dólares tarjeta Líder BCI y recibe pesos chilenos al instante. Cupo en dólares tarjeta líder a pesos. Cotiza por WhatsApp.",
        "canonical": "/cupo-dolar-lider",
        "breadcrumb": "Cupo en Dólares Tarjeta Líder",
        "eyebrow": "Tarjeta Líder BCI",
        "h1": "Cupo en Dólares Tarjeta Líder → Vende tu cupo hoy",
        "lead": "¿Tienes cupo en dólares en tu tarjeta Líder BCI? Conviértelo a pesos chilenos con DolarExpress. Proceso rápido y sin complicaciones.",
        "faqs": [
            ("¿Funciona con tarjeta Líder BCI?", "Sí, aceptamos tarjetas Líder BCI con cupo internacional activo."),
            ("¿Cómo activo el cupo internacional Líder?", "En la app BCI o en tiendas Líder."),
            ("¿Cuánto tarda la operación?", "Normalmente el mismo día si contactas en horario hábil."),
        ],
        "related": [
            ("/cupo-dolar-bci", "cupo dolar bci"),
            ("/cupo-dolar-cmr", "cupo dolar cmr"),
            ("/cupo-dolar-ripley", "cupo dolar ripley"),
            ("/vender-cupo-dolar", "vender cupo dolar"),
        ]
    },
]

# Generate all pages
for p in pages:
    html = make_page(
        p["filename"], p["title"], p["desc"], p["canonical"],
        p["breadcrumb"], p["eyebrow"], p["h1"], p["lead"],
        p["faqs"], p["related"]
    )
    filepath = os.path.join(PUBLIC, p["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Created {p['filename']}")

print("\n[DONE] All pages generated successfully!")
