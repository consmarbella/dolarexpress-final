#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime

# HTML Template
HTML_TEMPLATE = '''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="canonical" href="https://dolarexpress.cl{canonical_path}/" />
  <style>
    :root {{ --accent: #d4af37; --text: #f9fafb; --muted: #9ca3af; --wa: #25D366; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at top, #111827 0, #020617 55%, #000 100%); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    header {{ border-bottom: 1px solid rgba(31,41,55,0.9); backdrop-filter: blur(14px); background: radial-gradient(circle at top left, rgba(212,175,55,0.08), transparent 55%), linear-gradient(to right, rgba(15,23,42,0.96), rgba(3,7,18,0.98)); position: sticky; top: 0; z-index: 20; }}
    .nav {{ max-width: 960px; margin: 0 auto; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; }}
    .logo {{ display: inline-flex; align-items: center; gap: 10px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text); }}
    .logo-mark {{ width: 32px; height: 32px; border-radius: 999px; background: radial-gradient(circle at 30% 20%, #facc15, #d4af37 40%, #854d0e 100%); display: inline-flex; align-items: center; justify-content: center; color: #020617; font-weight: 900; font-size: 18px; box-shadow: 0 0 0 1px rgba(0,0,0,0.6), 0 16px 40px rgba(0,0,0,0.8); }}
    .logo-sub {{ font-size: 11px; color: var(--muted); text-transform: none; letter-spacing: 0.02em; }}
    main {{ flex: 1; max-width: 960px; width: 100%; margin: 0 auto; padding: 32px 16px 40px; display: grid; grid-template-columns: minmax(0, 3fr) minmax(280px, 2fr); gap: 28px; }}
    @media (max-width: 800px) {{ main {{ grid-template-columns: minmax(0, 1fr); }} header {{ position: static; }} }}
    .card {{ background: radial-gradient(circle at top left, rgba(148,163,184,0.12), transparent 55%), linear-gradient(to bottom right, rgba(15,23,42,0.96), rgba(2,6,23,0.98)); border-radius: 18px; border: 1px solid rgba(148,163,184,0.25); box-shadow: 0 22px 60px rgba(2,6,23,0.85); padding: 22px 20px; position: relative; overflow: hidden; }}
    .card::before {{ content: ""; position: absolute; inset: -2px; background: radial-gradient(circle at top, rgba(212,175,55,0.2), transparent 60%); opacity: 0.8; pointer-events: none; mix-blend-mode: soft-light; }}
    .card-inner {{ position: relative; z-index: 1; }}
    .eyebrow {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.16em; color: var(--muted); display: inline-flex; align-items: center; gap: 6px; margin-bottom: 8px; }}
    .eyebrow-line {{ width: 22px; height: 1px; background: linear-gradient(to right, transparent, rgba(148,163,184,0.8)); }}
    h1 {{ font-size: clamp(24px, 3vw, 30px); margin: 0 0 8px; letter-spacing: -0.03em; }}
    h2 {{ font-size: 18px; margin: 20px 0 12px; color: var(--text); }}
    .highlight {{ color: var(--accent); }}
    .lead {{ color: var(--muted); font-size: 14px; line-height: 1.6; margin: 0 0 16px; max-width: 460px; }}
    .metrics {{ display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 22px; }}
    .metric-item {{ padding: 10px 12px; border-radius: 12px; border: 1px solid rgba(31,41,55,0.9); background: radial-gradient(circle at top left, rgba(15,23,42,0.9), rgba(3,7,18,0.98)); min-width: 140px; }}
    .metric-label {{ color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 2px; }}
    .metric-value {{ font-size: 15px; color: var(--text); font-weight: 600; }}
    .cta-row {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 10px; }}
    .btn-wa {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 18px; border-radius: 999px; background: linear-gradient(to right, var(--wa), #128C7E); color: #f9fafb; font-size: 14px; font-weight: 600; border: none; cursor: pointer; box-shadow: 0 12px 30px rgba(5,150,105,0.65), 0 0 0 1px rgba(6,95,70,0.7); text-decoration: none; white-space: nowrap; }}
    .btn-wa:hover {{ text-decoration: none; opacity: 0.9; }}
    footer {{ border-top: 1px solid rgba(31,41,55,0.9); background: linear-gradient(to right, rgba(15,23,42,0.96), rgba(3,7,18,0.98)); padding: 20px 16px; text-align: center; color: var(--muted); font-size: 12px; }}
    .content {{ line-height: 1.8; color: var(--text); }}
    .content p {{ margin: 12px 0; }}
    .sidebar {{ display: flex; flex-direction: column; gap: 16px; }}
    ul, ol {{ margin: 12px 0; padding-left: 24px; }}
    li {{ margin: 8px 0; }}
    table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }}
    th, td {{ padding: 10px; text-align: left; border: 1px solid rgba(148,163,184,0.2); }}
    th {{ background: rgba(212,175,55,0.1); color: var(--accent); }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {json_ld_faqs}
    ]
  }}
  </script>
</head>
<body>
  <header>
    <div class="nav">
      <a href="/" class="logo">
        <span class="logo-mark">$</span>
        <span>DolarExpress<div class="logo-sub">Cupo a Pesos</div></span>
      </a>
      <a href="https://wa.me/56967658939" class="btn-wa">Cotizar</a>
    </div>
  </header>
  <main>
    <div class="card">
      <div class="card-inner">
        <div class="eyebrow"><span class="eyebrow-line"></span>CUPO DÓLAR</div>
        <h1>{h1}</h1>
        <p class="lead">{intro}</p>
        <div class="metrics">{metrics}</div>
        <div class="cta-row">
          <a href="https://wa.me/56967658939" class="btn-wa">{cta_text}</a>
        </div>
      </div>
    </div>
    <div class="sidebar">
      <div class="card">
        <div class="card-inner">
          <h2 style="margin-top: 0;">Info Rápida</h2>
          {sidebar_content}
        </div>
      </div>
    </div>
  </main>
  <div style="max-width: 960px; margin: 0 auto; padding: 40px 16px;">
    <div class="content">{main_content}</div>
  </div>
  <footer>
    <p>&copy; 2026 DolarExpress. | <a href="/" style="color: var(--accent);">Inicio</a></p>
  </footer>
</body>
</html>'''

def create_page(folder, slug, title, description, keywords, h1, intro, metrics, cta, sidebar, content):
    """Create a single HTML page"""
    if folder:
        directory = f"public/{folder}"
        os.makedirs(directory, exist_ok=True)
        filepath = f"{directory}/{slug}/index.html"
        canonical = f"/{folder}/{slug}"
    else:
        directory = "public"
        os.makedirs(directory, exist_ok=True)
        filepath = f"{directory}/{slug}/index.html"
        canonical = f"/{slug}"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    faqs = [
        {"question": "¿Cuánto tiempo tarda?", "answer": "Máximo 15 minutos desde confirmación."},
        {"question": "¿Cuál es el costo?", "answer": "Solo el cambio del día, sin comisiones."},
        {"question": "¿Necesito documentos?", "answer": "Solo foto de cupo y número de cuenta."},
        {"question": "¿Es seguro?", "answer": "Sí, operamos dentro del sistema bancario formal."},
    ]

    faq_items = [json.dumps({
        "@type": "Question",
        "name": faq["question"],
        "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]}
    }) for faq in faqs]

    html = HTML_TEMPLATE.format(
        title=title,
        description=description,
        keywords=keywords,
        canonical_path=canonical,
        h1=h1,
        intro=intro,
        metrics=metrics,
        cta_text=cta,
        sidebar_content=sidebar,
        main_content=content,
        json_ld_faqs=", ".join(faq_items)
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return canonical

# URGENTES (10 pages)
urgentes = [
    ("necesito-plata-urgente", "Necesito Plata Urgente", "Necesitas dinero hoy? Convierte tu cupo dólar a pesos en 15 minutos sin tramites.", "necesito plata urgente, dinero urgente, plata rapida", "Necesito Plata <span class='highlight'>Urgente</span>", "Cuando necesitas dinero ahora mismo, DolarExpress es tu solución en 15 minutos.", '<div class="metric-item"><div class="metric-label">Tiempo</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Proceso</div><div class="metric-value">Online</div></div>', "Quiero Dinero Hoy", '<p style="font-size: 13px; margin: 0;"><strong>Urgente 24/7</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Sin papeles.</p>', "<h2>La Urgencia No Espera</h2><p>A veces necesitas dinero ahora, no en una semana. Tus opciones normales son: pedir un préstamo (tarda dias), pedir a amigos (incómodo), o aceptar intereses altos (injusto). Pero si tienes cupo dólar, hay una opción mejor: convertirlo a pesos en 15 minutos.</p><h2>¿Por qué DolarExpress es Urgente?</h2><ul><li>Sin trámites: No necesitas documentos ni idas al banco</li><li>Sin demoras: Dinero en 15 minutos garantizados</li><li>Sin comisiones ocultas: Solo el cambio del día</li><li>24/7: Abiertos todos los días, a toda hora</li></ul><h2>Casos de Uso Real</h2><p>Tu auto se daña, necesitas $400.000 para arreglarlo, es viernes a las 5 PM. Los bancos están cerrados. Los prestamistas no responden. Pero tienes USD $600 en tu cupo dólar. DolarExpress te lo convierte en $480.000 CLP. Problema resuelto.</p><h2>El Proceso es Simple</h2><p>1. Envía foto de tu cupo dólar por WhatsApp (2 min). 2. Recibid cotización (1 min). 3. Aceptas (1 min). 4. Dinero en tu cuenta (15 min máximo). Total: 15 minutos de tu vida.</p>"),
    ("necesito-dinero-urgente-chile", "Necesito Dinero Urgente Chile", "Dinero urgente en Chile sin préstamos. Convierte cupo dólar a pesos al instante.", "dinero urgente chile, plata urgente sin prestamo, efectivo rapido", "Dinero Urgente en <span class='highlight'>Chile</span>", "Dinero urgente sin deuda nueva, sin préstamos, sin intereses. Solo conversión de tu cupo dólar.", '<div class="metric-item"><div class="metric-label">Tipo</div><div class="metric-value">Conversión</div></div><div class="metric-item"><div class="metric-label">Sin deuda</div><div class="metric-value">Nueva</div></div>', "Dinero Urgente", '<p style="font-size: 13px; margin: 0;"><strong>No es prestamo</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Es dinero que ya tienes.</p>', "<h2>Chile y la Crisis de Dinero Urgente</h2><p>En Chile hay momentos cuando todos necesitamos dinero urgente. Gasto médico inesperado, reparación del auto, oportunidad de negocio que aparece hoy. Los bancos no se mueven rápido en esos casos.</p><h2>La Solución que Tiene Todo Chileno</h2><p>Casi todos los chilenos con tarjeta de crédito tienen cupo en dólares. Los bancos (BCI, Santander, Banco de Chile, ITAÚ, Scotiabank) lo dan automáticamente. Es dinero que ya tienes. Solo no está en pesos.</p><h2>Dinero Que Ya Es Tuyo</h2><p>Tu cupo dólar no es un préstamo nuevo. No es deuda adicional. Es una línea de crédito que el banco ya aprobó. Solo está en moneda equivocada. Convertirlo a pesos es legal, seguro, y toma 15 minutos.</p>"),
    ("necesito-plata-hoy", "Necesito Plata Hoy", "Plata hoy, no manana. Convierte cupo dólar a pesos al instante.", "necesito plata hoy, dinero hoy mismo, plata al instante", "Necesito Plata <span class='highlight'>Hoy</span>", "Hoy es el día. Dinero en tu cuenta en 15 minutos o no te llamamos.", '<div class="metric-item"><div class="metric-label">Velocidad</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Garantizado</div><div class="metric-value">Hoy</div></div>', "Plata Hoy", '<p style="font-size: 13px; margin: 0;"><strong>HOY</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">15 minutos máximo.</p>', "<h2>Hoy Significa Hoy</h2><p>Cuando dices "necesito plata hoy", no quieres esperar. No mañana. No en una semana. Hoy. DolarExpress entiende esto. Nuestro proceso está diseñado específicamente para hoy.</p><h2>¿Cuándo Funciona 'Hoy'?</h2><p>Entre 7 AM y 11 PM, día laboral o fin de semana, si tienes cupo disponible, funcionamos hoy. Después de las 11 PM, procesamos mañana por la mañana antes de las 8 AM.</p><h2>Diferencia con Otros Servicios</h2><p>Un banco promete "2-5 días". Una financiera dice "máximo 24 horas". DolarExpress dice "antes de 15 minutos, veas el dinero en tu cuenta". Y lo cumple.</p>"),
    ("dinero-rapido-chile", "Dinero Rápido Chile", "Dinero rápido en Chile sin esperas. 15 minutos máximo, sin trámites.", "dinero rapido chile, plata rapida, efectivo rapido", "Dinero <span class='highlight'>Rápido</span> en Chile", "Rápido=15 minutos. DolarExpress es el servicio más rápido de Chile para convertir cupo a pesos.", '<div class="metric-item"><div class="metric-label">Agilidad</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Nacional</div><div class="metric-value">Chile</div></div>', "Dinero Rápido", '<p style="font-size: 13px; margin: 0;"><strong>Más rapido que cualquiera</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Verificado por clientes.</p>', "<h2>Rápido en Chile: 15 Minutos</h2><p>En Chile, decir "rápido" normalmente significa "en horas". DolarExpress cambió eso. Rápido para nosotros es 15 minutos.</p><h2>Comparativa de Velocidad</h2><p>Banco: 3-5 días. Financiera: 4-8 horas. Prestamista: 1-2 horas. DolarExpress: 15 minutos. No hay competencia.</p><h2>¿Por Qué Somos Tan Rápido?</h2><p>Porque no hacemos nada complicado. No evaluamos tu historial crediticio. No verificamos tus ingresos. Solo vemos: ¿tienes cupo dólar disponible? Si sí, lo convertimos. Fin de la historia.</p>"),
    ("plata-al-tiro-chile", "Plata al Tiro Chile", "Plata al tiro, al instante, sin esperas. 15 minutos en tu cuenta.", "plata al tiro, dinero al tiro, efectivo al tiro", "Plata <span class='highlight'>Al Tiro</span>", "Al tiro significa ahora. Dinero en 15 minutos o no hacemos negocio.", '<div class="metric-item"><div class="metric-label">Al Tiro</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Garantizado</div><div class="metric-value">100%</div></div>', "Plata Al Tiro", '<p style="font-size: 13px; margin: 0;"><strong>Sin excusas</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">15 min garantizado.</p>', "<h2>Al Tiro Es Una Promesa</h2><p>En Chile, "al tiro" es un compromiso. No es una promesa vaga. Es un pacto: si dices "al tiro", es "en minutos", no "en horas".</p><h2>¿Cómo Hacemos 15 Minutos?</h2><p>Porque tu cupo dólar existe. Tu banco ya lo aprobó. Lo único que falta es convertir dólares a pesos. Eso es mecánico, no requiere aprobación. Por eso 15 minutos.</p><h2>Si No Es al Tiro, Te Lo Decimos</h2><p>Si por alguna razón no puede ser al tiro (tu cupo está bloqueado, es fin de semana después de las 11 PM, tu banco está lento), te lo decimos claramente. No te hacemos esperar con falsa esperanza.</p>"),
    ("liquidez-inmediata-chile", "Liquidez Inmediata Chile", "Liquidez inmediata. Acceso a tu dinero en 15 minutos. Convierte cupo a pesos ahora.", "liquidez inmediata, efectivo inmediato, dinero liquido", "Liquidez <span class='highlight'>Inmediata</span>", "Liquidez=acceso a dinero. En 15 minutos tienes tu cupo dólar convertido a pesos en tu cuenta.", '<div class="metric-item"><div class="metric-label">Acceso</div><div class="metric-value">Inmediato</div></div><div class="metric-item"><div class="metric-label">Conversión</div><div class="metric-value">USD→CLP</div></div>', "Liquidez Ahora", '<p style="font-size: 13px; margin: 0;"><strong>Acceso total</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Dinero usable al instante.</p>', "<h2>¿Qué es Liquidez?</h2><p>Liquidez es capacidad de acceder a dinero efectivo ahora. No en una semana. No "cuando se apruebe". Ahora. Tu cupo dólar es un activo con liquidez limitada (solo puedes usarlo en el exterior). DolarExpress lo convierte en liquidez total.</p><h2>Tu Cupo = Activo Sin Liquidez</h2><p>Tienes USD $3.000 en tu cupo. Eso es un activo. Pero no puedes usarlo en Chile en pesos. No puedes sacarlo como efectivo. Está congelado en una tarjeta de crédito. No tiene liquidez local.</p><h2>DolarExpress = Liquidez Inmediata</h2><p>Convertimos ese USD $3.000 a CLP $2.400.000 en tu cuenta bancaria. Ahora tienes liquidez total. Puedes: pagar deudas, invertir, ahorrar, gastar, lo que necesites.</p>"),
    ("dinero-urgente-sin-dicom", "Dinero Urgente Sin DICOM", "Dinero urgente sin consultar DICOM. Para personas en registro de cobranza.", "dinero sin dicom, plata sin dicom, credito sin consultar dicom", "Dinero Sin <span class='highlight'>DICOM</span>", "Si estás en DICOM o no quieres consultas, DolarExpress no lo verifica. Solo tu cupo.", '<div class="metric-item"><div class="metric-label">DICOM</div><div class="metric-value">No consultado</div></div><div class="metric-item"><div class="metric-label">Requisito</div><div class="metric-value">Cupo solo</div></div>', "Dinero Sin DICOM", '<p style="font-size: 13px; margin: 0;"><strong>No consultamos</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Antecedentes sin importancia.</p>', "<h2>DICOM: La Pesadilla Financiera Chilena</h2><p>Si estás en DICOM, cada consulta bancaria adicional te hunde más. Es un sistema donde el problema se autoperpeúa: más deudas = más consultas = peor situación = más imposible salir.</p><h2>DolarExpress No es Un Acreedor</h2><p>No te estamos dando crédito nuevo. No evaluamos riesgo. No consultamos DICOM porque no necesitamos. Solo usamos dinero que YA TIENES en tu tarjeta.</p><h2>¿Cómo Verificamos?</h2><p>Solo lo esencial: ¿Tienes cupo? (foto) ¿Cuenta bancaria? (número) ¿RUT válido? (verificación rápida). Eso es. DICOM no aparece en la ecuación.</p>"),
    ("necesito-efectivo-hoy", "Necesito Efectivo Hoy", "Efectivo hoy en tu cuenta. Convierte cupo dólar a pesos al instante.", "necesito efectivo hoy, dinero efectivo, transferencia hoy", "Necesito <span class='highlight'>Efectivo</span> Hoy", "Efectivo=dinero en tu cuenta que usas inmediatamente. En 15 minutos lo tienes.", '<div class="metric-item"><div class="metric-label">Forma</div><div class="metric-value">Transferencia</div></div><div class="metric-item"><div class="metric-label">Disponibilidad</div><div class="metric-value">15 min</div></div>', "Efectivo Hoy", '<p style="font-size: 13px; margin: 0;"><strong>Dinero en cuenta</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Usable al instante.</p>', "<h2>Efectivo: Dos Significados</h2><p>En Chile, "efectivo" puede significar: (1) Dinero físico (billetes), o (2) Dinero en cuenta usable. DolarExpress te da lo segundo: dinero en tu cuenta que es 100% tuyo.</p><h2>Por Qué No Efectivo Físico</h2><p>Porque es inseguro y lento. Cambiar dólares a pesos físicos en la calle es riesgoso. Además, ¿quién carga medio millón de pesos? Mejor transferencia a tu cuenta, segura y rastreable.</p><h2>Tu Efectivo en 15 Minutos</h2><p>Dinero entra a tu cuenta. Usas tu tarjeta débito o retiras de cualquier cajero. No hay riesgo. No hay inseguridad. Tu dinero está protegido por el sistema bancario chileno.</p>"),
    ("plata-rapida-sin-banco", "Plata Rápida Sin Banco", "Plata rápida sin ir a banco, sin papeles, 100% por WhatsApp.", "plata sin banco, dinero sin banco, efectivo sin ir al banco", "Plata <span class='highlight'>Sin Banco</span>", "Sin banco, sin sucursal, sin colas. Solo WhatsApp y dinero en 15 minutos.", '<div class="metric-item"><div class="metric-label">Canal</div><div class="metric-value">WhatsApp</div></div><div class="metric-item"><div class="metric-label">Sucursal</div><div class="metric-value">No necesaria</div></div>', "Plata Sin Banco", '<p style="font-size: 13px; margin: 0;"><strong>100% WhatsApp</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">De tu casa, en tu tiempo.</p>', "<h2>El Problema de los Bancos</h2><p>Cuando necesitas dinero rápido, ir al banco es lo peor: colas 1-2 horas, horarios limitados, ejecutivos ocupados, trámites innecesarios.</p><h2>DolarExpress: Lo Opuesto Total</h2><p>No hay banco. No hay sucursal. No hay colas. No hay horarios. Solo tu celular y WhatsApp. 3 AM? Funciona (responderemos cuando despiertes). Domingo? Funciona. Tu oficina? Funciona. Tu auto? Funciona. Desde donde estés.</p><h2>¿Qué Necesitas?</h2><p>Smartphone con WhatsApp, foto de tu cupo, número de cuenta, RUT. Eso es. Sin papeles. Sin firmas. Sin presentaciones. Sin ir a ningún lado.</p>"),
    ("como-conseguir-plata-rapido", "Cómo Conseguir Plata Rápido", "Guía paso a paso para conseguir plata rápido sin préstamos, sin deuda, sin tramites.", "como conseguir plata rapido, formas conseguir dinero rapido, plata rapida como", "Cómo Conseguir Plata <span class='highlight'>Rápido</span>", "Hay varias formas. Esta es rápida, barata, legal, y no requiere deuda nueva.", '<div class="metric-item"><div class="metric-label">Método</div><div class="metric-value">Cupo dólar</div></div><div class="metric-item"><div class="metric-label">Complejidad</div><div class="metric-value">Mínima</div></div>', "Ver Cómo", '<p style="font-size: 13px; margin: 0;"><strong>Método más rapido</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Comprobado con miles.</p>', "<h2>Las Opciones Tradicionales</h2><p>Banco (2-5 días), Prestamista (20-30% de interés), Tarjeta de crédito (ya estás endeudado), Amigos (incómodo). Todas tienen problemas.</p><h2>La Opción DolarExpress: Tu Cupo Dólar</h2><p>Si tienes tarjeta de crédito (cualquiera), tienes cupo en dólares. Dinero que ya es tuyo. Solo está en moneda equivocada. DolarExpress lo convierte.</p><h2>Paso a Paso</h2><p>1. Abre app de tu banco. 2. Busca "cupo internacional" o "límite dólar". 3. Si tienes saldo, toma foto. 4. Envía foto a DolarExpress por WhatsApp. 5. Recibe cotización. 6. Confirma. 7. Dinero en tu cuenta (15 min).</p><h2>¿Y Si No Tengo Cupo Dólar?</h2><p>Explora otras opciones (prestamo, pedir dinero, vender algo). Pero si tienes cupo, no hay nada más rápido en Chile.</p>"),
]

created_count = 0
urls = []

for slug, title, desc, keywords, h1, intro, metrics, cta, sidebar, content in urgentes:
    canonical = create_page("urgente", slug, title, desc, keywords, h1, intro, metrics, cta, sidebar, content)
    urls.append(f"https://dolarexpress.cl{canonical}/")
    created_count += 1

print(f"[1/9] Urgentes: {created_count} pages")

# Continue with other categories...
# For now, let's write generated URLs to file and then update sitemap

# Save progress
with open('generated_pages.txt', 'w') as f:
    for url in urls:
        f.write(url + '\n')

print(f"\nTotal creadas: {created_count} páginas")
print(f"URLs guardadas en: generated_pages.txt")
