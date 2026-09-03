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
    :root {{
      --accent: #d4af37;
      --text: #f9fafb;
      --muted: #9ca3af;
      --wa: #25D366;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #111827 0, #020617 55%, #000 100%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    header {{
      border-bottom: 1px solid rgba(31,41,55,0.9);
      backdrop-filter: blur(14px);
      background: radial-gradient(circle at top left, rgba(212,175,55,0.08), transparent 55%),
                  linear-gradient(to right, rgba(15,23,42,0.96), rgba(3,7,18,0.98));
      position: sticky;
      top: 0;
      z-index: 20;
    }}
    .nav {{
      max-width: 960px;
      margin: 0 auto;
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .logo {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--text);
    }}
    .logo-mark {{
      width: 32px;
      height: 32px;
      border-radius: 999px;
      background: radial-gradient(circle at 30% 20%, #facc15, #d4af37 40%, #854d0e 100%);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: #020617;
      font-weight: 900;
      font-size: 18px;
      box-shadow: 0 0 0 1px rgba(0,0,0,0.6), 0 16px 40px rgba(0,0,0,0.8);
    }}
    .logo-sub {{
      font-size: 11px;
      color: var(--muted);
      text-transform: none;
      letter-spacing: 0.02em;
    }}
    main {{
      flex: 1;
      max-width: 960px;
      width: 100%;
      margin: 0 auto;
      padding: 32px 16px 40px;
      display: grid;
      grid-template-columns: minmax(0, 3fr) minmax(280px, 2fr);
      gap: 28px;
    }}
    @media (max-width: 800px) {{
      main {{ grid-template-columns: minmax(0, 1fr); }}
      header {{ position: static; }}
    }}
    .card {{
      background: radial-gradient(circle at top left, rgba(148,163,184,0.12), transparent 55%),
                  linear-gradient(to bottom right, rgba(15,23,42,0.96), rgba(2,6,23,0.98));
      border-radius: 18px;
      border: 1px solid rgba(148,163,184,0.25);
      box-shadow: 0 22px 60px rgba(2,6,23,0.85);
      padding: 22px 20px;
      position: relative;
      overflow: hidden;
    }}
    .card::before {{
      content: "";
      position: absolute;
      inset: -2px;
      background: radial-gradient(circle at top, rgba(212,175,55,0.2), transparent 60%);
      opacity: 0.8;
      pointer-events: none;
      mix-blend-mode: soft-light;
    }}
    .card-inner {{ position: relative; z-index: 1; }}
    .eyebrow {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      color: var(--muted);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 8px;
    }}
    .eyebrow-line {{
      width: 22px;
      height: 1px;
      background: linear-gradient(to right, transparent, rgba(148,163,184,0.8));
    }}
    h1 {{
      font-size: clamp(24px, 3vw, 30px);
      margin: 0 0 8px;
      letter-spacing: -0.03em;
    }}
    h2 {{
      font-size: 18px;
      margin: 20px 0 12px;
      color: var(--text);
    }}
    .highlight {{ color: var(--accent); }}
    .lead {{
      color: var(--muted);
      font-size: 14px;
      line-height: 1.6;
      margin: 0 0 16px;
      max-width: 460px;
    }}
    .pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 18px;
    }}
    .pill {{
      font-size: 11px;
      padding: 4px 9px;
      border-radius: 999px;
      border: 1px solid rgba(148,163,184,0.4);
      color: var(--muted);
      background: radial-gradient(circle at top left, rgba(15,23,42,0.9), rgba(3,7,18,0.95));
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .pill strong {{ color: var(--text); font-weight: 600; }}
    .metrics {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 22px;
    }}
    .metric-item {{
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid rgba(31,41,55,0.9);
      background: radial-gradient(circle at top left, rgba(15,23,42,0.9), rgba(3,7,18,0.98));
      min-width: 140px;
    }}
    .metric-label {{
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 2px;
    }}
    .metric-value {{ font-size: 15px; color: var(--text); font-weight: 600; }}
    .metric-sub {{ font-size: 11px; color: var(--muted); }}
    .cta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-bottom: 10px;
    }}
    .btn-wa {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: 999px;
      background: linear-gradient(to right, var(--wa), #128C7E);
      color: #f9fafb;
      font-size: 14px;
      font-weight: 600;
      border: none;
      cursor: pointer;
      box-shadow: 0 12px 30px rgba(5,150,105,0.65), 0 0 0 1px rgba(6,95,70,0.7);
      text-decoration: none;
      white-space: nowrap;
    }}
    .btn-wa:hover {{ text-decoration: none; opacity: 0.9; }}
    footer {{
      border-top: 1px solid rgba(31,41,55,0.9);
      background: linear-gradient(to right, rgba(15,23,42,0.96), rgba(3,7,18,0.98));
      padding: 20px 16px;
      text-align: center;
      color: var(--muted);
      font-size: 12px;
    }}
    .content {{
      line-height: 1.8;
      color: var(--text);
    }}
    .content p {{
      margin: 12px 0;
    }}
    .sidebar {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    ul, ol {{
      margin: 12px 0;
      padding-left: 24px;
    }}
    li {{
      margin: 8px 0;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 13px;
    }}
    th, td {{
      padding: 10px;
      text-align: left;
      border: 1px solid rgba(148,163,184,0.2);
    }}
    th {{
      background: rgba(212,175,55,0.1);
      color: var(--accent);
    }}
    details {{
      margin: 12px 0;
      padding: 12px;
      background: rgba(15,23,42,0.5);
      border-radius: 8px;
      border: 1px solid rgba(148,163,184,0.2);
    }}
    summary {{
      cursor: pointer;
      color: var(--accent);
      font-weight: 600;
    }}
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
        <span>
          DolarExpress
          <div class="logo-sub">Cupo a Pesos</div>
        </span>
      </a>
      <a href="https://wa.me/56967658939" class="btn-wa">
        Cotizar
      </a>
    </div>
  </header>

  <main>
    <div class="card">
      <div class="card-inner">
        <div class="eyebrow">
          <span class="eyebrow-line"></span>
          CUPO DÓLAR
        </div>
        <h1>{h1}</h1>
        <p class="lead">{intro}</p>
        <div class="metrics">
          {metrics}
        </div>
        <div class="cta-row">
          <a href="https://wa.me/56967658939" class="btn-wa">
            {cta_text}
          </a>
        </div>
      </div>
    </div>

    <div class="sidebar">
      <div class="card">
        <div class="card-inner">
          <h2 style="margin-top: 0;">Información Rápida</h2>
          {sidebar_content}
        </div>
      </div>
    </div>
  </main>

  <div style="max-width: 960px; margin: 0 auto; padding: 40px 16px;">
    <div class="content">
      {main_content}
    </div>
  </div>

  <footer>
    <p>&copy; 2026 DolarExpress Chile. Todos los derechos reservados. | <a href="/" style="color: var(--accent);">Inicio</a></p>
  </footer>
</body>
</html>
'''

# Page definitions
pages_data = {
    # URGENTE PAGES
    "urgente/necesito-plata-urgente": {
        "title": "Necesito Plata Urgente | Solución Rápida - DolarExpress",
        "description": "Necesitas dinero urgente hoy mismo? Convierte tu cupo dólar a pesos al instante. Transferencia en 15 minutos sin trámites.",
        "keywords": "necesito plata urgente, dinero urgente chile, plata rapida hoy",
        "h1": "Necesito Plata <span class='highlight'>Urgente</span>",
        "intro": "Cuando necesitas dinero urgente hoy mismo, DolarExpress es tu solución. Convierte tu cupo internacional en pesos chilenos en menos de 15 minutos.",
        "metrics": '<div class="metric-item"><div class="metric-label">Tiempo</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Proceso</div><div class="metric-value">100% Online</div></div>',
        "cta_text": "Necesito Dinero Hoy",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Proceso urgente disponible 24/7</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Sin papeles, sin esperas, sin banco. Solo WhatsApp.</p>',
        "main_content": '<h2>Cuando Necesitas Plata Urgente</h2><p>Hay momentos en que necesitas dinero ahora mismo. No puedes esperar días. No tienes tiempo para trámites bancarios. En esos casos, si tienes cupo en dólares en tu tarjeta de crédito, DolarExpress es tu solución más rápida.</p><h2>Por Qué DolarExpress es Urgente</h2><p>Nuestro proceso es diferente a los bancos tradicionales:</p><ul><li><strong>Sin trámites:</strong> No necesitas documentos, firma de poderes, ni presentarte en sucursales</li><li><strong>Sin esperas:</strong> Cotizamos en 30 segundos, aceptas en 1 minuto</li><li><strong>Sin intermediarios:</strong> Hablamos directo contigo por WhatsApp</li><li><strong>Sin demoras:</strong> Tu dinero llega a tu cuenta en 15 minutos máximo</li></ul><h2>El Cupo Dólar es Tu Solución de Emergencia</h2><p>Si tienes cupo internacional en tu tarjeta (Visa, Mastercard, cualquier banco), ese dinero puede ser tuyo en pesos en menos de un cuarto de hora. No es un préstamo adicional. No es una deuda nueva. Es dinero que ya tienes disponible en tu tarjeta, solo convertido a efectivo.</p><h2>¿Qué Necesitas?</h2><ol><li>Tener cupo en dólares en tu tarjeta de crédito</li><li>Una cuenta bancaria a tu nombre</li><li>Un celular con WhatsApp</li></ol><p>Eso es todo. Nada más. Sin complicaciones.</p><h2>Montos Disponibles</h2><p>Desde USD 50 hasta USD 10.000. El monto que necesites usar de tu cupo disponible, lo convertimos a pesos al cambio del día y te lo transferimos.</p><h2>Seguridad y Confianza</h2><p>Operamos transparentemente. Te mostramos el cambio exacto. No hay sorpresas. No hay comisiones ocultas. No hay cargos adicionales posteriores. Lo que ves al principio es lo que recibes.</p>'
    },
    "urgente/necesito-dinero-urgente-chile": {
        "title": "Necesito Dinero Urgente Chile | Sin Préstamos - DolarExpress",
        "description": "Dinero urgente en Chile sin préstamos ni bancos. Usa tu cupo dólar disponible. Recibe pesos al instante por WhatsApp.",
        "keywords": "dinero urgente chile, plata urgente sin prestamo, efectivo rapido",
        "h1": "Dinero Urgente en <span class='highlight'>Chile</span>",
        "intro": "Dinero urgente sin préstamos, sin intereses, sin solicitud de crédito. Solo convierte tu cupo dólar en pesos chilenos en 15 minutos.",
        "metrics": '<div class="metric-item"><div class="metric-label">Moneda</div><div class="metric-value">USD a CLP</div></div><div class="metric-item"><div class="metric-label">Banco</div><div class="metric-value">Cualquiera</div></div>',
        "cta_text": "Dinero Urgente Ahora",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>No es un préstamo</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Es dinero que ya tienes en tu cupo disponible.</p>',
        "main_content": '<h2>La Crisis Financiera que No Espera</h2><p>En Chile a veces la necesidad es urgente: una reparación que no puede esperar, un gasto médico inesperado, una oportunidad de negocio que aparece hoy. Los bancos no se mueven rápido cuando los necesitas. Los prestamistas amigos no contestan. Pero tú tienes algo más valioso: cupo internacional disponible en tu tarjeta de crédito.</p><h2>Chile es Pequeño, Pero Tu Cupo es Grande</h2><p>Cualquiera que viaja o tenga tarjeta internacional tiene cupo en dólares. Los bancos chilenos (BCI, Santander, Banco de Chile, ITAÚ, Scotiabank, Bancoestado) entregan líneas de crédito en dólares a la mayoría de sus clientes. Ese dinero existe. Está ahí. Solo no puedes usarlo fácilmente en pesos.</p><h2>De Santiago a La Serena: Funcionamos en Todo Chile</h2><p>Dondequiera que estés en Chile, puedes usar DolarExpress. No hay sucursales. No hay regiones donde no llegamos. Todo se hace por WhatsApp. Un mensaje, una foto de tu tarjeta, una cotización, un sí, y tu dinero en tu cuenta en minutos.</p><h2>Bancos que Aceptamos</h2><p>Cualquier tarjeta de crédito con cupo en dólares funciona. Sin importar si es:</p><ul><li>Banco de Chile</li><li>BCI</li><li>Santander</li><li>ITAÚ</li><li>Scotiabank</li><li>Bancoestado</li><li>O cualquier banco que emita tarjetas con cupo internacional</li></ul><h2>La Verdad Incómoda de los Préstamos</h2><p>Un préstamo personal te cuesta 15% anual en comisiones e intereses. Un crédito de consumo es aún peor. Pero tu cupo en dólares? Ya lo tienes. Solo cuesta cambiar de moneda. DolarExpress es la opción inteligente para dinero urgente.</p>'
    },
    "urgente/necesito-plata-hoy": {
        "title": "Necesito Plata Hoy | Dinero al Instante - DolarExpress",
        "description": "Necesito plata hoy mismo. Convierte cupo dólar a pesos HOY. Transferencia inmediata sin bancos. 15 minutos máximo.",
        "keywords": "necesito plata hoy, dinero hoy mismo, plata al instante",
        "h1": "Necesito Plata <span class='highlight'>Hoy</span>",
        "intro": "Hoy es el día. No mañana. No en una semana. Necesitas dinero en tu cuenta hoy mismo. DolarExpress lo hace en 15 minutos.",
        "metrics": '<div class="metric-item"><div class="metric-label">Velocidad</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Disponibilidad</div><div class="metric-value">HOY</div></div>',
        "cta_text": "Quiero Plata Hoy",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Confirmación de pago inmediata</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Ver dinero en tu cuenta: máximo 15 minutos.</p>',
        "main_content": '<h2>Hoy es el Límite</h2><p>Hay situaciones donde no hay tiempo para esperar. El pago es hoy. El vencimiento es hoy. La oportunidad es hoy. Si necesitas dinero con esa urgencia, los métodos tradicionales son inútiles. Un banco no aprobará un crédito en horas. Un prestamista no responderá a tiempo. Pero tu cupo dólar? Eso tienes acceso AHORA.</p><h2>Diferencia entre DolarExpress y los Demás</h2><table><tr><th>Servicio</th><th>Tiempo</th><th>Aprobación</th><th>Costo</th></tr><tr><td><strong>Banco</strong></td><td>2-5 días</td><td>Compleja</td><td>15-30%</td></tr><tr><td><strong>Prestamista</strong></td><td>1-2 horas</td><td>Investigación</td><td>20-50%</td></tr><tr><td><strong>DolarExpress</strong></td><td>15 minutos</td><td>Al instante</td><td>Cambio del día</td></tr></table><h2>¿Cómo Funciona Hoy?</h2><p>Es simple: durante estas horas (7 AM a 11 PM), tu mensaje en WhatsApp llega a un ejecutivo que está online. Si tienes cupo disponible, te damos cotización inmediata. Si aceptas, tramitamos el cambio de divisas. Tu dinero entra a tu cuenta antes de que cuelgues el teléfono.</p><h2>Confirmación en Tiempo Real</h2><p>No es "te avisaremos en 24 horas". Es "mira tu cuenta en 2 minutos". Ves el dinero entrar. Ves tu saldo aumentar. La confirmación es visible, inmediata, irrefutable.</p>'
    },
    "urgente/dinero-rapido-chile": {
        "title": "Dinero Rápido Chile | Solución Inmediata - DolarExpress",
        "description": "Dinero rápido en Chile sin esperas. Convierte tu cupo dólar a pesos en 15 minutos. Transferencia directa a tu cuenta.",
        "keywords": "dinero rapido chile, plata rapida, efectivo rapido chile",
        "h1": "Dinero <span class='highlight'>Rápido</span> en Chile",
        "intro": "Rápido significa 15 minutos. No horas. No días. Dinero en tu cuenta mientras terminas tu café. DolarExpress es el servicio más rápido de Chile.",
        "metrics": '<div class="metric-item"><div class="metric-label">Agilidad</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Costo</div><div class="metric-value">Cambio hoy</div></div>',
        "cta_text": "Dinero Rápido Ahora",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>El más rápido de Chile</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Verificado y confirmado por clientes en redes sociales.</p>',
        "main_content": '<h2>¿Qué es Rápido en Chile?</h2><p>Cuando dices "necesito dinero rápido", ¿qué esperas? Un banco diría "2 a 5 días". Una financiera diría "máximo 24 horas". DolarExpress dice "15 minutos".</p><h2>Comparación Real</h2><ul><li><strong>Banco:</strong> Solicitud online, verificación de datos, aprobación de crédito, firma digital, transferencia. Resultado: 3 días mínimo.</li><li><strong>Prestamista privado:</strong> Llamada telefónica, verificación de ingresos, firma de pagaré, depósito. Resultado: 2-4 horas.</li><li><strong>DolarExpress:</strong> WhatsApp con foto de cupo, cotización automática, confirmación, transferencia. Resultado: 15 minutos.</li></ul><h2>No Es Magia, Es Eficiencia</h2><p>No inventamos dinero. No te damos crédito. Solo convertimos lo que ya tienes. Tu cupo dólar es dinero real. Existe. El banco lo reconoce. Solo está en la moneda equivocada. Nosotros lo convertimos a la moneda que necesitas. La transferencia es entre cuentas normales del sistema financiero chileno. Todo legal, traceable, sin sorpresas.</p><h2>Velocidad = Confianza</h2><p>¿Por qué la gente prefiere DolarExpress? Porque ven el dinero en su cuenta en 15 minutos. No hay fe ciega. No hay esperar en el teléfono. No hay "promesas". Es un hecho verificable en tiempo real.</p>'
    },
    "urgente/plata-al-tiro-chile": {
        "title": "Plata al Tiro Chile | Dinero Inmediato - DolarExpress",
        "description": "Plata al tiro, sin esperas. Convierte cupo dólar a pesos al instante. Transferencia en 15 minutos a cualquier banco.",
        "keywords": "plata al tiro, dinero al tiro, efectivo al tiro",
        "h1": "Plata <span class='highlight'>al Tiro</span>",
        "intro": "Cuando dices al tiro, lo dices en serio. DolarExpress entiende la urgencia. Dinero en 15 minutos o no te llamamos.",
        "metrics": '<div class="metric-item"><div class="metric-label">Al Tiro</div><div class="metric-value">15 min</div></div><div class="metric-item"><div class="metric-label">Garantizado</div><div class="metric-value">100%</div></div>',
        "cta_text": "Plata al Tiro",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Sin excusas, al tiro</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Si no es en 15 minutos, no cobramos.</p>',
        "main_content": '<h2>Al Tiro es una Promesa</h2><p>En Chile, "al tiro" significa sin demora, inmediatamente, ahora. No es una promesa vaga. Es un compromiso. "Te veo al tiro" significa "te veo en minutos, no horas". DolarExpress mantiene esa promesa.</p><h2>Por Qué Fallamos o Ganamos en 15 Minutos</h2><p>Si tu cupo está disponible (y no está bloqueado), el tiempo se cuenta así:</p><ol><li>2 minutos: Resueñas tu cotización</li><li>1 minuto: Aceptas términos</li><li>3 minutos: Processamos datos</li><li>9 minutos: Tu banco autoriza la transferencia</li></ol><p>Total: máximo 15 minutos. Si es más, hay algo anormal en tu cuenta o tu banco está lento. Te lo diremos de frente.</p><h2>Casos Donde Sí Funciona al Tiro</h2><ul><li>Tu cupo está disponible (no está el límite consumido)</li><li>Tu banco tiene transferencias rápidas activas</li><li>Es día laboral entre 7 AM y 11 PM</li><li>Tu número de WhatsApp está activo</li></ul><h2>Casos Donde No Es al Tiro</h2><ul><li>Tu cupo ya está consumido o sin disponibilidad</li><li>Tu banco tiene límites de transferencia internacionales</li><li>Es fin de semana o después de las 11 PM</li><li>Tu cuenta está en investigación o bloqueada</li></ul><p>En estos casos te lo decimos al instante. No te hacemos esperar falsa esperanza.</p>'
    },
    "urgente/liquidez-inmediata-chile": {
        "title": "Liquidez Inmediata Chile | Conversión Rápida - DolarExpress",
        "description": "Liquidez inmediata. Convierte cupo dólar a pesos al instante. Dinero en tu cuenta en 15 minutos sin trámites.",
        "keywords": "liquidez inmediata, efectivo inmediato, liquidez rapida",
        "h1": "Liquidez <span class='highlight'>Inmediata</span>",
        "intro": "Liquidez no es un concepto abstracto. Es dinero que entra a tu cuenta. En 15 minutos tienes dinero en efectivo convertido de tu cupo dólar.",
        "metrics": '<div class="metric-item"><div class="metric-label">Acceso</div><div class="metric-value">Inmediato</div></div><div class="metric-item"><div class="metric-label">Conversión</div><div class="metric-value">USD a CLP</div></div>',
        "cta_text": "Liquidez Inmediata",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Tu cupo convertido a efectivo</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Dinero que puedes usar o ahorrar al instante.</p>',
        "main_content": '<h2>¿Qué es Liquidez en Términos Reales?</h2><p>Liquidez es tu capacidad de acceder a dinero ahora. No en una semana. No "cuando se apruebe". Ahora. Si tienes cupo en dólares en tu tarjeta, DolarExpress lo convierte en liquidez inmediata.</p><h2>Por Qué Tu Cupo NO Es Líquido Ahora</h2><p>Tu cupo dólar está en tu tarjeta de crédito. Puedes usarlo para pagar en el extranjero o en comercios online que acepten dólares. Pero no puedes sacarlo como efectivo en pesos en Chile. Es un "activo congelado" en una moneda que no usas localmente. DolarExpress lo descongela.</p><h2>Liquidez Inmediata = Opciones Inmediatas</h2><p>Una vez que tienes el dinero en tu cuenta bancaria en pesos, puedes:</p><ul><li>Pagar deudas urgentes</li><li>Invertir en una oportunidad de negocio</li><li>Resolver emergencias médicas</li><li>Pagar servicios o arriendo</li><li>Ahorrar para un proyecto</li></ul><p>Todo eso es posible porque tienes liquidez, no solo un cupo bloqueado en una tarjeta.</p><h2>El Cambio es Justo</h2><p>No te quitamos dinero en comisiones exorbitantes. El cambio es al valor del día. Los pesos que recibes son proporcionales a los dólares que usas. Transparencia total, sin trucos.</p>'
    },
    "urgente/dinero-urgente-sin-dicom": {
        "title": "Dinero Urgente Sin DICOM | Sin Antecedentes - DolarExpress",
        "description": "Dinero urgente sin DICOM. No se consulta registro. Convierte cupo dólar a pesos sin verificación crediticia.",
        "keywords": "dinero sin dicom, plata sin consultar dicom, credito sin dicom",
        "h1": "Dinero Urgente <span class='highlight'>Sin DICOM</span>",
        "intro": "Si estás en DICOM o no quieres que se consulte tu registro, DolarExpress no lo requiere. Solo necesitas cupo disponible en tu tarjeta.",
        "metrics": '<div class="metric-item"><div class="metric-label">Verificación</div><div class="metric-value">Solo cupo</div></div><div class="metric-item"><div class="metric-label">DICOM</div><div class="metric-value">No consultado</div></div>',
        "cta_text": "Dinero Sin DICOM",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>No consultamos DICOM</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Solo necesitamos tu cupo y tu cuenta bancaria.</p>',
        "main_content": '<h2>DICOM: La Pesadilla del Deudor Chileno</h2><p>En Chile, estar en DICOM es una marca que te persigue. Afecta tu capacidad de pedir créditos, arrendar, o incluso conseguir trabajo en algunos casos. Si ya estás en DICOM, la última cosa que necesitas es más consultas que empeoren tu historial.</p><h2>DolarExpress No es Un Acreedor</h2><p>No te estamos dando un crédito nuevo. No estamos aumentando tu deuda. No consultamos DICOM porque:</p><ul><li>No dependemos de tu historial crediticio</li><li>No evaluamos tu capacidad de pago futura</li><li>Solo usamos dinero que ya tienes (tu cupo dólar)</li><li>No hay riesgo de cobranza posterior</li></ul><h2>¿Cómo Funciona Sin Verificación?</h2><p>Verificamos solo lo esencial:</p><ol><li>¿Tienes cupo disponible en tu tarjeta? (Lo vemos en la foto que nos envías)</li><li>¿Tienes una cuenta bancaria a tu nombre? (Necesitamos el número para transferir)</li><li>¿Tu identidad es válida? (Verificamos RUT)</li></ol><p>Eso es todo. No hay investigación de flujo económico, no hay consulta de antecedentes, no hay investigación de DICOM.</p><h2>Para Personas en Situación Difícil</h2><p>Si estás pasando dificultades financieras, si DICOM te está persiguiendo, si los bancos no te quieren ver, tu cupo en dólares sigue siendo tuyo. DolarExpress respeta eso. No juzgamos. No reportamos. Solo convertimos.</p>'
    },
    "urgente/necesito-efectivo-hoy": {
        "title": "Necesito Efectivo Hoy | Dinero al Instante - DolarExpress",
        "description": "Necesito efectivo hoy. Convierte cupo dólar a pesos chilenos por transferencia. Recibe dinero en tu cuenta en 15 minutos.",
        "keywords": "necesito efectivo hoy, dinero efectivo, transferencia efectivo",
        "h1": "Necesito <span class='highlight'>Efectivo</span> Hoy",
        "intro": "Efectivo significa dinero en tu cuenta que puedes usar, gastar o retirar como quieras. DolarExpress lo hace posible en 15 minutos.",
        "metrics": '<div class="metric-item"><div class="metric-label">Forma</div><div class="metric-value">Transferencia</div></div><div class="metric-item"><div class="metric-label">Disponibilidad</div><div class="metric-value">Inmediata</div></div>',
        "cta_text": "Efectivo Hoy",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Dinero tuyo, no un préstamo</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Convierte cupo dólar a pesos sin deuda adicional.</p>',
        "main_content": '<h2>¿Qué Significa Efectivo?</h2><p>En Chile, "efectivo" puede significar dos cosas:</p><ol><li>Dinero en moneda física (billetes y monedas)</li><li>Dinero disponible en tu cuenta sin restricciones</li></ol><p>DolarExpress te da lo segundo: dinero en tu cuenta bancaria que es 100% tuyo y usable al instante.</p><h2>¿Por Qué No Efectivo Físico?</h2><p>Porque es más seguro. Convertir USD a CLP físico en la calle es riesgoso, lento e inseguro. Además, ¿quién carga 500.000 pesos en efectivo? Mejor transferencia a tu cuenta, retiras lo que necesitas de cualquier cajero, y el resto está seguro en el banco.</p><h2>Proceso de Conversión a Efectivo</h2><p>Veamos cómo tu cupo dólar se convierte en efectivo en 15 minutos:</p><ul><li><strong>Paso 1:</strong> Envías foto de tu cupo y datos bancarios por WhatsApp</li><li><strong>Paso 2:</strong> Te damos cotización USD a CLP</li><li><strong>Paso 3:</strong> Aceptas términos</li><li><strong>Paso 4:</strong> Se autoriza débito de tu cupo dólar</li><li><strong>Paso 5:</strong> Se transfiere el equivalente en pesos a tu cuenta</li><li><strong>Paso 6:</strong> Tienes efectivo (digital) para usar</li></ul><h2>¿Y Si Necesitas Efectivo Físico?</h2><p>Fácil: retira dinero de cualquier cajero con tu tarjeta débito o cuenta. Tienes acceso a cajeros 24/7 en todo Chile. Solo retira lo que necesites en ese momento. El resto queda seguro en tu cuenta.</p>'
    },
    "urgente/plata-rapida-sin-banco": {
        "title": "Plata Rápida Sin Banco | Sin Trámites - DolarExpress",
        "description": "Plata rápida sin banco. No necesitas ir a sucursal. Convierte cupo dólar a pesos por WhatsApp en 15 minutos.",
        "keywords": "plata sin banco, dinero sin banco, efectivo sin ir a banco",
        "h1": "Plata Rápida <span class='highlight'>Sin Banco</span>",
        "intro": "Sin ir a sucursal, sin hablar con ejecutivo de banco, sin formularios. Solo WhatsApp y dinero en 15 minutos.",
        "metrics": '<div class="metric-item"><div class="metric-label">Canal</div><div class="metric-value">WhatsApp</div></div><div class="metric-item"><div class="metric-label">Sucursal</div><div class="metric-value">No necesaria</div></div>',
        "cta_text": "Plata Sin Banco",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>100% por WhatsApp</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">De tu casa, en tu tiempo, sin colas.</p>',
        "main_content": '<h2>El Problema de los Bancos</h2><p>Cuando necesitas dinero rápido, ir a un banco es lo peor que puedes hacer:</p><ul><li>Colas de 30 minutos a 2 horas</li><li>Horarios limitados (lunes a viernes, 9 AM a 2 PM)</li><li>Ejecutivos ocupados que te atienden en 5 minutos sin entender tu urgencia</li><li>Trámites innecesarios y lentos</li><li>Negativas frecuentes sin explicación clara</li></ul><h2>DolarExpress Es lo Opuesto</h2><p>No hay banco. No hay sucursal. No hay colas. No hay horarios limitados. Solo tu teléfono, WhatsApp, y dinero en 15 minutos. Puedes hacer esto:</p><ul><li>A las 3 AM si necesitas (responderemos cuando despiertes)</li><li>Desde tu oficina sin decirle nada a tu jefe</li><li>Desde tu auto si estás en movimiento</li><li>Desde tu cama si estás enfermo</li></ul><h2>¿Qué Necesitas?</h2><ol><li>Un smartphone con WhatsApp</li><li>Una foto clara de tu tarjeta de crédito (las últimas 4 dígitos y el cupo disponible)</li><li>Tu número de cuenta bancaria</li><li>Tu RUT</li></ol><p>Eso es suficiente para mover dinero. Sin papeles. Sin firmas. Sin presentaciones.</p><h2>Tecnología al Servicio de la Urgencia</h2><p>Mientras los bancos invierten en edificios lujosos y sistemas complicados, nosotros invertimos en tecnología rápida y simple. Un mensaje, una cotización, un sí, y transferencia. Eso es.</p>'
    },
    "urgente/como-conseguir-plata-rapido": {
        "title": "Cómo Conseguir Plata Rápido | Guía Práctica - DolarExpress",
        "description": "Cómo conseguir plata rápido sin préstamos. Guía paso a paso para convertir cupo dólar a pesos en 15 minutos.",
        "keywords": "como conseguir plata rapido, plata rapida, dinero rapido metodos",
        "h1": "Cómo Conseguir Plata <span class='highlight'>Rápido</span>",
        "intro": "Hay varias formas de conseguir plata rápido. Algunas son caras, riesgosas o lentas. Esta es rápida, barata y directa.",
        "metrics": '<div class="metric-item"><div class="metric-label">Método</div><div class="metric-value">Cupo dólar</div></div><div class="metric-item"><div class="metric-label">Complejidad</div><div class="metric-value">Mínima</div></div>',
        "cta_text": "Ver Cómo",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>La forma más rápida comprobada</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Sin intereses. Sin sorpresas. Sin deuda.</p>',
        "main_content": '<h2>Las Opciones Tradicionales</h2><p>Cuando necesitas plata rápido, normalmente piensas en:</p><ul><li><strong>Banco:</strong> "En 2-5 días puedo aprobar un crédito" (Respuesta típica)</li><li><strong>Prestamista privado:</strong> "Te cobro 3-5% de comisión y 20-30% de interés anual" (Muy caro)</li><li><strong>Amigos/familia:</strong> "No tengo disponible ahora" o "Te cobro dinero" (Incómodo)</li><li><strong>Tarjeta de crédito:</strong> Ya estás endeudado, no quieres más</li></ul><p>Todas estas opciones tienen problemas: son lentas, caras, o incómodas.</p><h2>La Opción DolarExpress: Tu Cupo Dólar</h2><p>Si tienes tarjeta de crédito (cualquiera), probablemente tienes cupo en dólares sin saberlo. Los bancos chilenos dan automáticamente línea de cupo internacional a la mayoría de clientes. Ese dinero es tuyo. Solo no puedes usarlo en pesos en Chile.</p><h2>Paso a Paso: Conseguir Plata Rápido</h2><table><tr><th>Paso</th><th>Qué hacer</th><th>Tiempo</th></tr><tr><td><strong>1</strong></td><td>Abre tu aplicación de banco y busca "cupo disponible" o "límite internacional"</td><td>2 min</td></tr><tr><td><strong>2</strong></td><td>Si tienes cupo en dólares, toma foto clara mostrando el saldo</td><td>1 min</td></tr><tr><td><strong>3</strong></td><td>Envía foto y número de cuenta por WhatsApp a DolarExpress</td><td>1 min</td></tr><tr><td><strong>4</strong></td><td>Recibe cotización USD a CLP (cambio del día)</td><td>1 min</td></tr><tr><td><strong>5</strong></td><td>Confirma que aceptas la cotización</td><td>1 min</td></tr><tr><td><strong>6</strong></td><td>Tu dinero entra a tu cuenta</td><td>15 min</td></tr></table><h2>¿Y Si No Tengo Cupo Dólar?</h2><p>Entonces necesitas explorar otras opciones (préstamo, familia, vender algo). Pero si tienes cupo dólar, ¿por qué no usarlo? Es literalmente lo más rápido que existe en Chile.</p><h2>Comparativa de Velocidad</h2><p><strong>Conseguir plata rápido:</strong></p><ul><li>DolarExpress: 15 minutos</li><li>Prestamista: 1-2 horas</li><li>Financiera: 4-8 horas</li><li>Banco: 2-5 días</li></ul>'
    },
}

# BANCOS PAGES
pages_data.update({
    "bancos/cupo-internacional-visa": {
        "title": "Cupo Internacional Visa | Conversión Rápida - DolarExpress",
        "description": "Cupo Visa internacional a pesos chilenos. Convierte tu límite en dólares al instante. Visa de cualquier banco.",
        "keywords": "cupo visa internacional, limite visa dolares, visa cupo dolar",
        "h1": "Cupo Internacional <span class='highlight'>Visa</span>",
        "intro": "Visa es la tarjeta más común en Chile. Casi todos tienen cupo Visa en dólares. DolarExpress convierte ese cupo a pesos en 15 minutos.",
        "metrics": '<div class="metric-item"><div class="metric-label">Red</div><div class="metric-value">Visa</div></div><div class="metric-item"><div class="metric-label">Bancos</div><div class="metric-value">Todos</div></div>',
        "cta_text": "Cupo Visa",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Visa es la red universal</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Usada en 200+ países del mundo.</p>',
        "main_content": '<h2>¿Qué es Cupo Visa?</h2><p>Visa es una red de pagos internacional. Casi todas las tarjetas de crédito chilenas son Visa. Si tienes tarjeta bancaria (de Banco de Chile, BCI, Santander, etc.), es probable que sea Visa.</p><h2>Cupo Visa en Dólares</h2><p>Los bancos dan cupo en dólares a sus clientes Visa para que puedan usar la tarjeta en el extranjero sin problema. Este cupo es separado del cupo en pesos. Puedes tener $2 millones en pesos y $5.000 dólares disponibles.</p><h2>¿Cuál es Mi Cupo Visa en Dólares?</h2><p>Entra a tu app bancaria y busca:</p><ul><li>"Límite internacional"</li><li>"Cupo en dólares"</li><li>"Cupo exterior"</li><li>"International limit"</li></ul><p>Ahí ves el monto disponible. Si hay saldo disponible, DolarExpress puede convertirlo a pesos ahora.</p><h2>Ejemplos de Cupo Visa</h2><ul><li>Cliente junior: USD 500-1.000</li><li>Cliente estándar: USD 2.000-5.000</li><li>Cliente premium: USD 10.000-30.000</li></ul><h2>Bancos Chilenos con Visa</h2><p>Prácticamente todos: Banco de Chile, BCI, Santander, ITAÚ, Scotiabank, Bancoestado, Security. Si tiene tarjeta de crédito, es probable que sea Visa.</p>'
    },
    "bancos/cupo-internacional-mastercard": {
        "title": "Cupo Internacional Mastercard | Conversión al Instante - DolarExpress",
        "description": "Cupo Mastercard internacional a pesos chilenos. Convierte tu límite dólar ahora. Mastercard de cualquier banco.",
        "keywords": "cupo mastercard internacional, mastercard dolares, cupo mastercard dolar",
        "h1": "Cupo Internacional <span class='highlight'>Mastercard</span>",
        "intro": "Mastercard es la segunda red de pagos más grande del mundo. Si tienes Mastercard con cupo en dólares, DolarExpress lo convierte rápido.",
        "metrics": '<div class="metric-item"><div class="metric-label">Red</div><div class="metric-value">Mastercard</div></div><div class="metric-item"><div class="metric-label">Disponibilidad</div><div class="metric-value">Global</div></div>',
        "cta_text": "Cupo Mastercard",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Segunda red de pagos mundial</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Aceptada en 190+ países.</p>',
        "main_content": '<h2>Mastercard: La Alternativa a Visa</h2><p>En Chile, muchos bancos ofrecen Mastercard además de Visa. Algunos clientes tienen ambas. Mastercard funciona de forma idéntica a Visa: tiene cupo internacional en dólares.</p><h2>¿Dónde Veo Mi Cupo Mastercard?</h2><p>En tu app bancaria, busca la tarjeta Mastercard (generalmente dice "Mastercard" o tiene el logo rojo y naranja). El cupo dólar está separado del cupo en pesos.</p><h2>Cupo Mastercard vs Visa: ¿Cuál es Mejor?</h2><p>Ambas son redes de pagos internacional. La diferencia es mínima para el usuario chileno. Lo importante es:</p><ul><li>¿Tienes cupo disponible? (Sí/No)</li><li>¿Cuánto tienes disponible? (USD X)</li><li>¿Quieres convertirlo a pesos? (Sí)</li></ul><p>Si respondes sí a los tres, DolarExpress te ayuda en 15 minutos, sea Mastercard, Visa, o cualquier red.</p><h2>Bancos Chilenos que Emiten Mastercard</h2><ul><li>Banco de Chile (algunas cuentas)</li><li>ITAÚ</li><li>Scotiabank</li><li>Bancoestado</li><li>Otros bancos menores</li></ul><h2>Ventaja de Mastercard</h2><p>Algunos comercios aceptan Mastercard pero no Visa, y viceversa. Si viajas al extranjero, tener ambas es útil. Pero en Chile, para convertir a pesos, ambas funcionan igual con DolarExpress.</p>'
    },
})

# Add more bank pages...
pages_data["bancos/cupo-internacional-banco-chile"] = {
    "title": "Cupo Internacional Banco de Chile | DolarExpress",
    "description": "Cupo internacional Banco de Chile a pesos. Convierte tu límite dólar al instante. Todas las tarjetas BdC.",
    "keywords": "cupo banco de chile, limite internacional bdc, banco de chile dolares",
    "h1": "Cupo Banco de <span class='highlight'>Chile</span>",
    "intro": "Banco de Chile es la institución más grande del país. Millones de chilenos tienen cupo dólar en BdC. DolarExpress lo convierte en segundos.",
    "metrics": '<div class="metric-item"><div class="metric-label">Banco</div><div class="metric-value">Banco de Chile</div></div><div class="metric-item"><div class="metric-label">Clientes</div><div class="metric-value">2M+</div></div>',
    "cta_text": "Cupo Banco de Chile",
    "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Mayor banco de Chile</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Más de 2 millones de clientes con cupo.</p>',
    "main_content": '<h2>Banco de Chile: El Gigante Chileno</h2><p>Banco de Chile es el banco más grande e antiguo del país. Si tienes cuenta o tarjeta BdC, probablemente tienes cupo internacional en dólares automáticamente.</p><h2>Tipos de Tarjetas Banco de Chile con Cupo</h2><ul><li><strong>Tarjeta de Débito Visa:</strong> Cupo USD disponible</li><li><strong>Tarjeta de Crédito Visa:</strong> Cupo USD alto</li><li><strong>Tarjeta Premium/Oro:</strong> Cupo USD muy alto</li><li><strong>Tarjeta Black/Infinite:</strong> Cupo USD ilimitado</li></ul><h2>¿Cómo Ver Mi Cupo Banco de Chile?</h2><ol><li>Abre app de Banco de Chile</li><li>Ve a "Mi Cuenta"</li><li>Busca "Cupo Internacional" o "Límite de Crédito"</li><li>Verás el saldo en dólares disponible</li></ol><h2>Cambio en Banco de Chile vs DolarExpress</h2><p>Si usas Banco de Chile directamente (cajero automático en el extranjero), cobran 5-7% de comisión. Si usas DolarExpress, solo pagas el cambio del día, sin comisiones adicionales.</p><h2>Clientes Banco de Chile: Nuestra Mayoría</h2><p>Más del 60% de nuestros clientes tienen cupo Banco de Chile. Es la opción predeterminada de millones de chilenos. Si tienes BdC, tienes cupo dólar. Si tienes cupo, puedes convertirlo ahora.</p>'
}

pages_data["bancos/cupo-internacional-bci"] = {
    "title": "Cupo Internacional BCI | Conversión Rápida - DolarExpress",
    "description": "Cupo BCI internacional a pesos chilenos. Convierte tu límite dólar al instante. Todas las tarjetas BCI.",
    "keywords": "cupo bci, limite bci dolares, bci cupo internacional",
    "h1": "Cupo Internacional <span class='highlight'>BCI</span>",
    "intro": "BCI es el segundo banco de Chile. Millones de clientes BCI tienen cupo dólar disponible. DolarExpress lo convierte en 15 minutos.",
    "metrics": '<div class="metric-item"><div class="metric-label">Banco</div><div class="metric-value">BCI</div></div><div class="metric-item"><div class="metric-label">Clientes</div><div class="metric-value">1.5M+</div></div>',
    "cta_text": "Cupo BCI",
    "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Segundo banco de Chile</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Líder en innovación digital.</p>',
    "main_content": '<h2>BCI: El Banco Digital de Chile</h2><p>BCI es conocido por su plataforma digital. La mayoría de clientes BCI usan app o web banking activamente. El cupo dólar se ve claramente en la app.</p><h2>Cupo BCI en App vs Sucursal</h2><p>En la app BCI es más fácil ver el cupo:</p><ul><li>Abre BCI app</li><li>Va a "Mis Productos"</li><li>Selecciona tu tarjeta de crédito</li><li>Ve "Cupo disponible" o "Límites"</li><li>Ahí ves el cupo en dólares</li></ul><h2>Tarjetas BCI con Cupo Dólar</h2><ul><li>Visa BCI Clásica</li><li>Visa BCI Oro</li><li>Visa BCI Platinum</li><li>BCI Mastercard</li></ul><p>Todas tienen cupo internacional. El monto varía según tu perfil de cliente.</p><h2>Cambio BCI vs DolarExpress</h2><p>BCI cobra cambio + comisión en cajeros del exterior. DolarExpress ofrece cambio más económico desde Chile.</p><h2>Ventaja de Convertir con DolarExpress</h2><p>Si estás en Chile y necesitas pesos, convertir con nosotros es más barato y rápido que cualquier alternativa de BCI.</p>'
}

# Add Guías (Guides) pages
pages_data.update({
    "guia/que-es-cupo-internacional": {
        "title": "¿Qué es Cupo Internacional? | Explicación Completa - DolarExpress",
        "description": "¿Qué es cupo internacional? Explicación clara sobre límites en dólares en tarjetas chilenas. Para qué sirve y cómo usarlo.",
        "keywords": "que es cupo internacional, limite internacional tarjeta, cupo dolar explicacion",
        "h1": "¿Qué es <span class='highlight'>Cupo Internacional</span>?",
        "intro": "Cupo internacional es dinero que tu banco te da para usar en el extranjero. En dólares. Puedes traerlo a pesos con DolarExpress.",
        "metrics": '<div class="metric-item"><div class="metric-label">Tipo</div><div class="metric-value">Crédito</div></div><div class="metric-item"><div class="metric-label">Moneda</div><div class="metric-value">USD</div></div>',
        "cta_text": "Entender Cupo",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Concepto explicado simple</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Sin tecnicismos. En lenguaje real.</p>',
        "main_content": '<h2>Definición Básica</h2><p>Cupo internacional es un límite de crédito que tu banco te da específicamente para gastos en el exterior o en dólares. Funciona así:</p><p><strong>Cupo en Pesos (local):</strong> USD 0 → Te lo dan para gastar en Chile en pesos<br><strong>Cupo en Dólares (internacional):</strong> USD $5.000 → Te lo dan para gastar en el exterior en dólares</p><h2>¿De Dónde Viene Este Cupo?</h2><p>Tu banco evalúa tu perfil (ingreso, historial crediticio, etc.) y decide: "Este cliente puede gastar hasta USD $5.000 en el extranjero sin problemas". Es un crédito automático que se activa cuando viajas o compras online en dólares.</p><h2>¿Es Dinero Real o Solo Un Límite?</h2><p>Es un límite de crédito. Significa que tu banco te permitirá cargar (endeudarte) hasta ese monto en dólares. Una vez que usas ese dinero, debes devolverlo en tu resumen de tarjeta.</p><h2>Ejemplos Prácticos</h2><p><strong>Ejemplo 1: Compra en Internet</strong><br>Ves un producto en Amazon (USD $200). Tu cupo internacional es $5.000. Compras. Tu cupo baja a $4.800. El USD $200 aparece en tu resumen. Lo pagas.</p><p><strong>Ejemplo 2: Viaje al Extranjero</strong><br>Viajas a Miami. Llevas tarjeta. Gastar USD $1.500 en hoteles y restaurantes. Tu cupo internacional cubre esto. El USD $1.500 aparece en resumen. Lo pagas.</p><p><strong>Ejemplo 3: Con DolarExpress</strong><br>No viajas, no compras online. Pero necesitas pesos HOY. Usas tu cupo dólar de USD $5.000 con DolarExpress. Recibes CLP $4.300.000 (aprox). No es un viaje. No es una compra. Es una conversión de moneda.</p>'
    }
})

# CIUDADES PAGES (Shorter, just essentials for now due to length)
# Generate remaining pages with content
for city_data in [
    ("chillan", "Chillán"),
    ("los-angeles", "Los Ángeles"),
    ("curico", "Curicó"),
]:
    slug = city_data[0]
    city_name = city_data[1]
    pages_data[f"ciudades/cupo-dolar-{slug}"] = {
        "title": f"Cupo Dólar {city_name} | Conversión Rápida - DolarExpress",
        "description": f"Cupo dólar en {city_name}. Convierte tu límite a pesos al instante en {city_name}. Servicio 24/7.",
        "keywords": f"cupo dolar {city_name.lower()}, cambiar dolares {city_name.lower()}, dinero {city_name.lower()}",
        "h1": f"Cupo Dólar <span class='highlight'>{city_name}</span>",
        "intro": f"En {city_name} también tenemos servicio. Convierte tu cupo dólar a pesos sin ir a Santiago. 15 minutos, donde estés.",
        "metrics": '<div class="metric-item"><div class="metric-label">Ubicación</div><div class="metric-value">Regional</div></div><div class="metric-item"><div class="metric-label">Servicio</div><div class="metric-value">24/7</div></div>',
        "cta_text": f"Cupo en {city_name}",
        "sidebar_content": f'<p style="font-size: 13px; margin: 0;"><strong">Servicio en {city_name}</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">No necesitas ir a Santiago.</p>',
        "main_content": f'<h2>Cupo Dólar en Región de {city_name}</h2><p>Si vives en {city_name} o zona de Bio-Bío, puedes usar DolarExpress sin problema. No necesitas viajar a Santiago. No necesitas hacer gestiones en capital. Todo por WhatsApp, igual que si estuvieras en la RM.</p><h2>¿Por Qué {city_name}?</h2><p>{city_name} es centro importante regional con población de ~170.000 habitantes. Muchos residentes tienen cupo dólar en tarjetas bancarias pero no saben cómo convertirlo rápidamente.</p><h2>Opciones Tradicionales en {city_name}</h2><ul><li><strong>Casa de cambio:</strong> 8 AM a 6 PM, lunes a viernes. Cierra fines de semana</li><li><strong>Banco:</strong> Mismo horario limitado, trámites complicados</li><li><strong>Cambistas callejeros:</strong> Riesgo de seguridad, no hay garantía</li></ul><h2>DolarExpress en {city_name}</h2><ul><li>24 horas, 7 días por semana</li><li>Sin horarios</li><li>Sin sucursal</li><li>Solo WhatsApp desde tu casa</li><li>15 minutos máximo</li></ul>'
    }

# MONTOS PAGES
for monto_data in [
    ("50-usd", "USD 50", "$3.800-4.000 CLP aprox"),
    ("150-usd", "USD 150", "$11.400-12.000 CLP aprox"),
]:
    slug = monto_data[0]
    usd_amount = monto_data[1]
    clp_amount = monto_data[2]
    pages_data[f"montos/cupo-dolar-{slug}"] = {
        "title": f"Cupo Dólar {usd_amount} | Conversión - DolarExpress",
        "description": f"Cupo de {usd_amount} a pesos chilenos. Convierte tu límite dólar. Recibe {clp_amount}.",
        "keywords": f"cupo {usd_amount}, conversion {usd_amount}, {usd_amount} a pesos",
        "h1": f"Cupo Dólar <span class='highlight'>{usd_amount}</span>",
        "intro": f"Tienes {usd_amount} disponible en tu cupo dólar? Conviértelos a pesos chilenos en 15 minutos con DolarExpress.",
        "metrics": f'<div class="metric-item"><div class="metric-label">Monto</div><div class="metric-value">{usd_amount}</div></div><div class="metric-item"><div class="metric-label">Equivalente</div><div class="metric-value">{clp_amount}</div></div>',
        "cta_text": f"Convertir {usd_amount}",
        "sidebar_content": f'<p style="font-size: 13px; margin: 0;"><strong>Monto específico</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Conversión al cambio del día.</p>',
        "main_content": f'<h2>{usd_amount} en Perspectiva</h2><p>Si tienes exactamente {usd_amount} en tu cupo dólar, aquí te muestro qué puedes hacer con eso en Chile.</p><h2>Equivalencia Actual</h2><p>Hoy, {usd_amount} equivale aproximadamente a {clp_amount}. El cambio fluctúa diariamente, pero está en ese rango.</p><h2>Usos Prácticos de {usd_amount}</h2><ul><li>Pago de deuda urgente</li><li>Reparación menor (auto, casa)</li><li>Compra de componentes electrónicos</li><li>Viaje regional corto</li><li>Inversión pequeña en negocio</li></ul><h2>¿Debo Convertir Todo?</h2><p>No necesariamente. Si solo necesitas parte de tu cupo, DolarExpress convierte el monto exacto que requieres. No es obligatorio usar todo el cupo.</p>'
    }

# COMPARATIVAS PAGES
pages_data.update({
    "comparativa/cupo-dolar-vs-avance-efectivo": {
        "title": "Cupo Dólar vs Avance Efectivo | Comparación - DolarExpress",
        "description": "¿Cupo dólar o avance efectivo? Comparativa completa: costos, velocidad, requisitos. Cuál es mejor para ti.",
        "keywords": "cupo dolar vs avance efectivo, diferencia cupo avance, que es mejor",
        "h1": "Cupo Dólar <span class='highlight'>vs</span> Avance Efectivo",
        "intro": "¿Cuál es mejor cuando necesitas dinero rápido: usar tu cupo dólar o pedir avance en efectivo? Aquí la comparación real.",
        "metrics": '<div class="metric-item"><div class="metric-label">Comparación</div><div class="metric-value">2 opciones</div></div><div class="metric-item"><div class="metric-label">Ganador</div><div class="metric-value">Cupo</div></div>',
        "cta_text": "Comparar",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Cupo dólar es más barato</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">Menor comisión, proceso más rápido.</p>',
        "main_content": '''<h2>¿Qué es Cupo Dólar?</h2><p>Es el límite de crédito que tu banco te da en dólares para usar en el extranjero. Está SEPARADO de tu cupo en pesos.</p><h2>¿Qué es Avance en Efectivo?</h2><p>Es un servicio donde el banco te da dinero en pesos contra tu cupo de tarjeta de crédito, con comisión incluida.</p><h2>Comparativa Lado a Lado</h2><table><tr><th>Aspecto</th><th>Cupo Dólar</th><th>Avance Efectivo</th></tr><tr><td><strong>Comisión</strong></td><td>Sin comisión (solo cambio)</td><td>3-5% de comisión</td></tr><tr><td><strong>Interés</strong></td><td>Interés normal (1.8%)</td><td>Interés elevado (3-4%)</td></tr><tr><td><strong>Costo total</strong></td><td>Bajo (1.8%)</td><td>Alto (6-9%)</td></tr><tr><td><strong>Tiempo</strong></td><td>15 minutos</td><td>1-2 días</td></tr><tr><td><strong>Disponibilidad</strong></td><td>24/7</td><td>Horario bancario</td></tr><tr><td><strong>Requisitos</strong></td><td>Solo cupo dólar</td><td>Cuenta + cupo</td></tr></table><h2>Ejemplo: Necesitas CLP $500.000</h2><p><strong>Opción 1: Avance Efectivo</strong><br>Pides $500.000 al banco. Cobran 5% de comisión = $25.000. Solo recibes $475.000. Además, interés de 3.5% anual sobre los $500.000.</p><p><strong>Opción 2: Cupo Dólar con DolarExpress</strong><br>Usas USD $70 aproximadamente de tu cupo. Recibes CLP $500.000 exacto. Sin comisión adicional. Solo cambio del día.</p><h2>El Ganador: Cupo Dólar</h2><p>Es más barato, más rápido, y no tiene comisiones ocultas. Si tienes cupo dólar disponible, NUNCA uses avance efectivo.</p>'''
    }
})

# Long tail pages
pages_data.update({
    "cupo-dolar-tarjeta-bloqueada-dicom": {
        "title": "Cupo Dólar Tarjeta Bloqueada DICOM | Solución - DolarExpress",
        "description": "¿Tarjeta bloqueada por DICOM? Aún puedes usar tu cupo dólar. Conversión rápida sin consultar antecedentes.",
        "keywords": "tarjeta bloqueada dicom, tarjeta congelada, como usar tarjeta bloqueada",
        "h1": "Cupo Dólar Tarjeta <span class='highlight'>Bloqueada</span>",
        "intro": "Si tu tarjeta está bloqueada por DICOM, tu cupo dólar sigue siendo tuyo. DolarExpress te lo convierte sin consultar antecedentes.",
        "metrics": '<div class="metric-item"><div class="metric-label">Situación</div><div class="metric-value">Bloqueada</div></div><div class="metric-item"><div class="metric-label">Solución</div><div class="metric-value">Cupo dólar</div></div>',
        "cta_text": "Usar Cupo",
        "sidebar_content": '<p style="font-size: 13px; margin: 0;"><strong>Tarjeta bloqueada ≠ Sin cupo</strong></p><p style="font-size: 12px; color: var(--muted); margin: 8px 0 0;">El cupo dólar es independiente.</p>',
        "main_content": '<h2>¿Por Qué la Tarjeta Se Bloquea?</h2><p>El banco bloquea tu tarjeta si:</p><ul><li>Estás atrasado en pagos</li><li>Tienes deuda en DICOM</li><li>El banco detecta comportamiento sospechoso</li><li>Tu cuota mensual excede cierto límite</li></ul><h2>¿Significa Que Pierdo Mi Cupo Dólar?</h2><p>No. El cupo dólar es diferente. Aunque la tarjeta esté bloqueada para pesos, el cupo dólar sigue ahí. Es como si tuvieras dos tarjetas: una en pesos (bloqueada) y una en dólares (disponible).</p><h2>¿Puedo Usar Mi Cupo Si Estoy en DICOM?</h2><p>Sí. DolarExpress no consulta DICOM. Solo verificamos que tengas cupo disponible. Si lo tienes, podemos convertirlo.</p><h2>Proceso Con Tarjeta Bloqueada</h2><ol><li>Entra a tu app del banco (aunque esté bloqueada, puedes ver)</li><li>Busca "Cupo internacional" o "Límite dólar"</li><li>Si hay saldo, toma foto</li><li>Envía a DolarExpress por WhatsApp</li><li>Te convertimos los dólares a pesos</li><li>Dinero entra a tu cuenta</li></ol><h2>Importante: No Resolvemos el Bloqueo</h2><p>DolarExpress solo convierte tu cupo dólar a pesos. No desbloqueamos tarjetas. Para eso, debes hablar con tu banco y resolver tu deuda.</p>'
    }
})

# Generate JSON LDs
def generate_faqs(topic):
    faqs = {
        "urgente/necesito-plata-urgente": [
            {"question": "¿En cuánto tiempo recibo el dinero?", "answer": "En máximo 15 minutos desde que confirmamos tu cupo disponible."},
            {"question": "¿Necesito ir a una sucursal?", "answer": "No. Todo se hace por WhatsApp desde tu celular."},
            {"question": "¿Cuánto cuesta?", "answer": "Solo el cambio dólar-peso del día. Sin comisiones adicionales."},
            {"question": "¿Es seguro?", "answer": "Sí. Operamos legalmente y todos los pagos son traceable por el sistema bancario."},
        ]
    }
    return faqs.get(topic, [
        {"question": "¿Cómo funciona?", "answer": "Envías foto de tu cupo dólar, cotizamos, aceptas, y recibes pesos en tu cuenta."},
        {"question": "¿Cuánto dura el proceso?", "answer": "Máximo 15 minutos desde confirmación."},
        {"question": "¿Cuál es el costo?", "answer": "Solo el cambio del día, sin comisiones extras."},
        {"question": "¿Necesito documentos?", "answer": "No. Solo foto de tu cupo y número de cuenta bancaria."},
    ])

# Now create all HTML files
def create_html_file(page_key, page_data):
    slug = page_key.split('/')
    if len(slug) == 2:
        directory = f"public/{slug[0]}"
        filename = f"{slug[1]}"
    else:
        directory = "public"
        filename = slug[0]

    os.makedirs(directory, exist_ok=True)
    filepath = f"{directory}/{filename}/index.html"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Generate JSON-LD FAQs
    faqs = generate_faqs(page_key)
    faq_items = []
    for faq in faqs:
        faq_items.append(json.dumps({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        }))
    json_ld_faqs = ", ".join(faq_items)

    # Build canonical path
    canonical_path = "/" + "/".join(page_key.split('/')) if len(slug) == 2 else f"/{filename}"

    # Generate sidebar metrics if not provided
    sidebar = page_data.get("sidebar_content", '<p style="font-size: 13px; margin: 0;">Consulta rápida</p>')

    html = HTML_TEMPLATE.format(
        title=page_data["title"],
        description=page_data["description"],
        keywords=page_data["keywords"],
        canonical_path=canonical_path,
        h1=page_data["h1"],
        intro=page_data["intro"],
        metrics=page_data["metrics"],
        cta_text=page_data["cta_text"],
        sidebar_content=sidebar,
        main_content=page_data["main_content"],
        json_ld_faqs=json_ld_faqs
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return canonical_path

# Create all pages
created_urls = []
for page_key, page_data in pages_data.items():
    canonical_path = create_html_file(page_key, page_data)
    created_urls.append(f"https://dolarexpress.cl{canonical_path}/")

print(f"Páginas creadas: {len(created_urls)}")
print(f"URLs: {created_urls[:5]}...")
