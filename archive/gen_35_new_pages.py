#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_35_new_pages.py
Genera las 35 páginas pSEO nuevas para dolarexpress.cl
Solo CREA archivos nuevos, no toca los existentes.
"""
import os
import json

HTML_TPL = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{t}</title><meta name="description" content="{d}"><meta name="keywords" content="{k}"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="canonical" href="https://dolarexpress.cl{c}/" /><style>:root{{--a:#d4af37;--t:#f9fafb}}*{{box-sizing:border-box}}body{{margin:0;font-family:system-ui;background:radial-gradient(circle,#111827,#000);color:var(--t);min-height:100vh;display:flex;flex-direction:column}}a{{color:var(--a)}}header{{position:sticky;top:0;background:linear-gradient(90deg,rgba(15,23,42,.96),rgba(3,7,18,.98));padding:12px 16px}}.nav{{max-width:960px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}}.logo{{display:flex;align-items:center;gap:10px;text-transform:uppercase}}.logo-mark{{width:32px;height:32px;border-radius:50%;background:radial-gradient(circle,#facc15,#d4af37 40%);display:flex;align-items:center;justify-content:center;color:#000;font-weight:900}}.btn-wa{{background:linear-gradient(90deg,#25D366,#128C7E);color:#fff;padding:10px 18px;border-radius:999px;text-decoration:none;border:none;cursor:pointer;font-weight:600}}main{{flex:1;max-width:960px;width:100%;margin:0 auto;padding:32px 16px;display:grid;grid-template-columns:3fr 2fr;gap:28px}}@media(max-width:800px){{main{{grid-template-columns:1fr}}}}.card{{background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(2,6,23,.98));border-radius:18px;border:1px solid rgba(148,163,184,.25);padding:22px}}h1{{font-size:28px;margin:0 0 8px}}.highlight{{color:var(--a)}}.lead{{color:#9ca3af;font-size:14px;line-height:1.6}}.metrics{{display:flex;gap:16px;margin:16px 0;flex-wrap:wrap}}.metric{{padding:10px 12px;border-radius:12px;border:1px solid rgba(31,41,55,.9);min-width:130px;font-size:12px}}.metric-v{{font-size:15px;font-weight:600}}.cta-row{{margin:20px 0}}.content{{max-width:960px;margin:0 auto;padding:40px 16px;line-height:1.8}}h2{{font-size:18px;margin:20px 0 12px;color:var(--t)}}p{{margin:12px 0}}ul,ol{{margin:12px 0;padding-left:24px}}li{{margin:8px 0}}footer{{border-top:1px solid rgba(31,41,55,.9);padding:20px;text-align:center;color:#9ca3af;font-size:12px}}</style><script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{f}]}}</script></head><body><header><div class="nav"><a href="/" class="logo"><span class="logo-mark">$</span><span>DolarExpress<div style="font-size:11px;color:#9ca3af">Cupo a Pesos</div></span></a><a href="https://wa.me/56967658939" class="btn-wa">Cotizar</a></div></header><main><div class="card"><div><h1>{h}</h1><p class="lead">{i}</p><div class="metrics">{m}</div><div class="cta-row"><a href="https://wa.me/56967658939" class="btn-wa">{b}</a></div></div></div><div><div class="card"><h2 style="margin-top:0">Info Rapida</h2><p style="font-size:13px">{s}</p></div></div></main><div class="content">{x}</div><footer><p>&copy; 2026 DolarExpress | <a href="/">Inicio</a></p></footer></body></html>'''

METRICS_STD = "<div class='metric'><div>Tiempo</div><div class='metric-v'>15 min</div></div><div class='metric'><div>Comision</div><div class='metric-v'>0%</div></div><div class='metric'><div>Seguridad</div><div class='metric-v'>100%</div></div>"
SIDEBAR_STD = "Transferencia inmediata. Sin comisiones ocultas. Solo foto del cupo y numero de cuenta. Operamos en sistema bancario formal."

def create_page(slug, title, desc, keywords, h1, intro, content, btn="Cotizar Ahora", metrics=METRICS_STD, sidebar=SIDEBAR_STD):
    canon = f"/{slug}"
    path = f"public/{slug}/index.html"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    faqs = ', '.join([json.dumps({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}) for q, a in [
        ("¿Cuanto tiempo tarda?", "Maximo 15 minutos desde confirmacion."),
        ("¿Cual es el costo?", "Solo el cambio del dia, sin comisiones."),
        ("¿Necesito documentos?", "Solo foto de cupo y numero de cuenta."),
        ("¿Es seguro?", "Si, operamos en sistema bancario formal."),
    ]])

    html = HTML_TPL.format(t=title, d=desc, k=keywords, c=canon, h=h1, i=intro,
                           m=metrics, b=btn, s=sidebar, x=content, f=faqs)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return canon


pages = [
    # ── GRUPO 1: vender cupo dolar + banco ──────────────────────────────────────
    ("vender-cupo-dolar-bci",
     "Vender Cupo Dólar BCI | DolarExpress",
     "Vendé tu cupo en dólares BCI de forma rápida y segura. Transferencia inmediata, sin comisiones.",
     "vender cupo dolar bci,cupo dolar bci venta,cambiar cupo bci",
     "Vender Cupo Dólar <span class='highlight'>BCI</span>",
     "BCI es el segundo banco de Chile. Si tienes tarjeta BCI, probablemente tienes cupo en dólares disponible ahora.",
     "<h2>¿Por Qué BCI Tiene Cupo en Dólares?</h2><p>BCI asigna automáticamente cupo internacional a todas sus tarjetas de crédito. Es parte del límite de tu tarjeta, no requiere activación especial.</p><h2>¿Cómo Ver Tu Cupo BCI?</h2><ul><li>App BCI → Mis Productos → Tu tarjeta → Cupo internacional</li><li>Web BCI → Mis cuentas → Ver cupo disponible</li><li>Cajero BCI → Consultar cupo internacional</li></ul><h2>Proceso de Venta</h2><ol><li>Toma foto del cupo disponible en app BCI</li><li>Envíala por WhatsApp a DolarExpress</li><li>Recibe cotización en pesos en 1 minuto</li><li>Confirma y recibe transferencia en 15 minutos</li></ol><h2>Tarjetas BCI con Cupo en Dólares</h2><ul><li>Visa BCI Clásica</li><li>Visa BCI Oro</li><li>Visa BCI Platinum</li><li>Mastercard BCI (todas las categorías)</li></ul>"),

    ("vender-cupo-dolar-banco-chile",
     "Vender Cupo Dólar Banco de Chile | DolarExpress",
     "Vendé tu cupo en dólares Banco de Chile. Pago en minutos, operación 100% segura.",
     "vender cupo dolar banco chile,cupo banco chile venta,cambiar cupo banco de chile",
     "Vender Cupo Dólar <span class='highlight'>Banco de Chile</span>",
     "Banco de Chile es el banco más grande del país. Si tienes tarjeta BdC, tu cupo en dólares está disponible ahora mismo.",
     "<h2>Cupo en Dólares de Banco de Chile</h2><p>Banco de Chile asigna cupo en dólares a todas sus tarjetas de crédito de forma automática. No necesitas activarlo.</p><h2>¿Cómo Ver Tu Cupo BdC?</h2><ul><li>App Banco de Chile → Mis productos → Tarjeta → Cupo internacional</li><li>Web BdC → Mis cuentas → Estado de cuenta</li></ul><h2>Tipos de Tarjeta BdC con Mayor Cupo</h2><ul><li>Visa BdC Clásica: USD 1.000-3.000</li><li>Visa BdC Oro: USD 3.000-10.000</li><li>Visa BdC Infinite/Black: USD 10.000+</li><li>Mastercard BdC: igual a Visa según categoría</li></ul><h2>¿Cuánto Recibes en Pesos?</h2><p>El monto depende del tipo de cambio del día. DolarExpress usa el cambio del mercado formal sin comisiones adicionales.</p>"),

    ("vender-cupo-dolar-banco-estado",
     "Vender Cupo Dólar BancoEstado | DolarExpress",
     "Vendé tu cupo en dólares BancoEstado. Sin comisiones, transferencia inmediata.",
     "vender cupo dolar bancoestado,cupo bancoestado venta,cambiar cupo banco estado",
     "Vender Cupo Dólar <span class='highlight'>BancoEstado</span>",
     "BancoEstado es el único banco estatal de Chile. Sus tarjetas de crédito incluyen cupo en dólares automáticamente.",
     "<h2>BancoEstado y el Cupo en Dólares</h2><p>Las tarjetas de crédito de BancoEstado incluyen cupo internacional en dólares. Es común en la CuentaRUT con tarjeta crédito asociada.</p><h2>¿Cómo Ver Tu Cupo BancoEstado?</h2><ul><li>App BancoEstado → Tarjeta de crédito → Ver cupo disponible</li><li>Sitio BancoEstado → Mis productos → Estado de cuenta</li><li>Sucursal BancoEstado → Consultar cupo</li></ul><h2>Ventaja BancoEstado</h2><p>Al ser banco estatal, las transacciones son reguladas y seguras. DolarExpress trabaja con clientes BancoEstado en todo Chile.</p><h2>Proceso en 15 Minutos</h2><ol><li>Verifica cupo en app BancoEstado</li><li>Foto del cupo disponible</li><li>WhatsApp a DolarExpress</li><li>Cotización inmediata</li><li>Transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-santander",
     "Vender Cupo Dólar Santander | DolarExpress",
     "Vendé tu cupo en dólares Santander. Mejor precio del mercado garantizado.",
     "vender cupo dolar santander,cupo santander venta,cambiar cupo santander",
     "Vender Cupo Dólar <span class='highlight'>Santander</span>",
     "Santander es uno de los principales bancos de Chile. Sus tarjetas tienen cupo en dólares disponible para conversión inmediata.",
     "<h2>Cupo en Dólares Santander</h2><p>Santander Chile asigna cupo internacional en dólares a todas sus tarjetas de crédito. El monto depende de tu categoría de cliente.</p><h2>¿Cómo Ver Tu Cupo Santander?</h2><ul><li>App Santander → Mis productos → Tarjeta → Cupo disponible</li><li>Web Santander → Estado de cuenta</li><li>Cajero Santander → Consulta de cupo</li></ul><h2>Tarjetas Santander con Cupo</h2><ul><li>Visa Santander Clásica</li><li>Visa Santander Infinite</li><li>Mastercard Santander Gold/Platinum</li><li>Tarjeta Santander Universitaria</li></ul><h2>Proceso de Venta con DolarExpress</h2><ol><li>Toma screenshot del cupo en app Santander</li><li>Envíalo por WhatsApp</li><li>Cotización en 1 minuto</li><li>Confirmación y transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-scotiabank",
     "Vender Cupo Dólar Scotiabank | DolarExpress",
     "Vendé tu cupo en dólares Scotiabank. Rápido, seguro y sin burocracia.",
     "vender cupo dolar scotiabank,cupo scotiabank venta,cambiar cupo scotiabank",
     "Vender Cupo Dólar <span class='highlight'>Scotiabank</span>",
     "Scotiabank tiene presencia importante en Chile. Sus tarjetas de crédito incluyen cupo en dólares listo para convertir.",
     "<h2>Scotiabank en Chile</h2><p>Scotiabank Chile opera con múltiples productos de crédito. Las tarjetas Visa y Mastercard de Scotiabank incluyen cupo en dólares automático.</p><h2>¿Cómo Ver Tu Cupo Scotiabank?</h2><ul><li>App Scotiabank → Mis cuentas → Tarjeta de crédito → Cupo internacional</li><li>Web Scotiabank → Portal cliente</li></ul><h2>Tarjetas Scotiabank con Cupo</h2><ul><li>Visa Scotiabank Clásica</li><li>Visa Scotiabank Oro</li><li>Visa Scotiabank Platinum</li><li>Mastercard Scotiabank</li></ul><h2>¿Por Qué DolarExpress?</h2><p>Mejor cambio que cajeros automáticos, sin comisiones adicionales, operación en 15 minutos desde tu celular.</p>"),

    ("vender-cupo-dolar-falabella",
     "Vender Cupo Dólar CMR Falabella | DolarExpress",
     "Vendé tu cupo en dólares CMR Falabella. Cotización inmediata, pago en minutos.",
     "vender cupo dolar falabella,cupo cmr falabella venta,cambiar cupo cmr",
     "Vender Cupo Dólar <span class='highlight'>CMR Falabella</span>",
     "La tarjeta CMR Falabella es una de las más populares de Chile. También tiene cupo en dólares disponible para conversión.",
     "<h2>CMR Falabella y el Cupo en Dólares</h2><p>La tarjeta CMR Falabella asigna cupo internacional en dólares a sus clientes. Muchos titulares no saben que lo tienen.</p><h2>¿Cómo Ver Tu Cupo CMR?</h2><ul><li>App CMR → Mi tarjeta → Cupo disponible</li><li>Web CMR → Mis productos → Estado de cuenta</li></ul><h2>Tipos CMR Falabella con Cupo</h2><ul><li>CMR Falabella Clásica</li><li>CMR Falabella Platinum</li><li>CMR Falabella Black</li></ul><h2>Requisito Principal</h2><p>Necesitas tener cupo en dólares habilitado (cupo internacional). Si ves 'Cupo internacional: USD XXX' en tu app, está habilitado y listo.</p>"),

    ("vender-cupo-dolar-ripley",
     "Vender Cupo Dólar Ripley | DolarExpress",
     "Vendé tu cupo en dólares Ripley. Pago en minutos vía transferencia bancaria.",
     "vender cupo dolar ripley,cupo ripley venta,cambiar cupo tarjeta ripley",
     "Vender Cupo Dólar <span class='highlight'>Ripley</span>",
     "La tarjeta de crédito Ripley tiene cupo en dólares para clientes con habilitación internacional. Conviértelo a pesos en minutos.",
     "<h2>Tarjeta Ripley y Cupo en Dólares</h2><p>Ripley ofrece cupo internacional en dólares a sus clientes de crédito. Es independiente del límite en pesos.</p><h2>¿Cómo Ver Tu Cupo Ripley?</h2><ul><li>App Ripley → Mi tarjeta → Cupo internacional</li><li>Web Ripley → Mi cuenta → Estado de cuenta</li><li>Atención al cliente Ripley</li></ul><h2>Condiciones</h2><ul><li>Tener tarjeta de crédito Ripley vigente</li><li>Tener cupo internacional habilitado</li><li>No tener bloqueos en la tarjeta</li></ul><h2>Proceso DolarExpress</h2><ol><li>Confirma cupo disponible en app Ripley</li><li>Foto del cupo</li><li>WhatsApp DolarExpress</li><li>Cotización y transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-itau",
     "Vender Cupo Dólar Itaú | DolarExpress",
     "Vendé tu cupo en dólares Itaú. Operación 100% segura y confiable.",
     "vender cupo dolar itau,cupo itau venta,cambiar cupo itau chile",
     "Vender Cupo Dólar <span class='highlight'>Itaú</span>",
     "Itaú Chile tiene una base importante de clientes con tarjetas de crédito internacionales. Tu cupo en dólares está disponible.",
     "<h2>Itaú Chile y el Cupo en Dólares</h2><p>Las tarjetas de crédito Itaú incluyen cupo en dólares automáticamente. Itaú es uno de los bancos con mejor servicio digital para verificar el cupo.</p><h2>¿Cómo Ver Tu Cupo Itaú?</h2><ul><li>App Itaú → Mis productos → Tarjeta → Cupo internacional</li><li>Web Itaú → Estado de cuenta → Cupo disponible</li></ul><h2>Tarjetas Itaú con Cupo en Dólares</h2><ul><li>Visa Itaú Clásica</li><li>Visa Itaú Oro</li><li>Mastercard Itaú</li><li>Itaú Personnalité</li></ul><h2>Por Qué DolarExpress</h2><p>Sin visitar sucursales, mejor cambio que cajeros Itaú, operación en 15 minutos desde donde estés.</p>"),

    ("vender-cupo-dolar-hites",
     "Vender Cupo Dólar Hites | DolarExpress",
     "Vendé tu cupo en dólares Hites. Transferencia inmediata sin comisiones.",
     "vender cupo dolar hites,cupo hites venta,cambiar cupo tarjeta hites",
     "Vender Cupo Dólar <span class='highlight'>Hites</span>",
     "La tarjeta Hites tiene cupo en dólares para sus clientes con habilitación internacional. Conviértelo a pesos en 15 minutos.",
     "<h2>Hites y el Cupo en Dólares</h2><p>Hites ofrece crédito internacional a sus clientes con tarjeta activa. Si tienes cupo en dólares disponible, DolarExpress lo convierte a pesos de inmediato.</p><h2>¿Cómo Ver Tu Cupo Hites?</h2><ul><li>App Hites → Mi tarjeta → Cupo disponible</li><li>Web Hites → Mi cuenta</li><li>Atención al cliente Hites</li></ul><h2>Proceso Sencillo</h2><ol><li>Confirma cupo en app Hites</li><li>Foto del cupo disponible</li><li>WhatsApp DolarExpress</li><li>Transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-bice",
     "Vender Cupo Dólar Bice | DolarExpress",
     "Vendé tu cupo en dólares Bice. Mejor cotización garantizada en el mercado.",
     "vender cupo dolar bice,cupo bice venta,cambiar cupo banco bice",
     "Vender Cupo Dólar <span class='highlight'>Bice</span>",
     "Banco Bice es conocido por sus altos cupos en dólares para clientes premium. Conviértelo a pesos con DolarExpress.",
     "<h2>Banco Bice y Sus Cupos en Dólares</h2><p>Bice es conocido por ofrecer altos límites en dólares a sus clientes. Es un banco orientado a perfiles de mayor ingreso con cupos internacionales significativos.</p><h2>¿Cómo Ver Tu Cupo Bice?</h2><ul><li>App Bice → Mis productos → Tarjeta → Cupo internacional</li><li>Web Bice → Estado de cuenta</li></ul><h2>Tarjetas Bice con Cupo</h2><ul><li>Visa Bice Clásica</li><li>Visa Bice Oro</li><li>Visa Bice Signature</li><li>Bice Amex (American Express)</li></ul><h2>Montos Habituales</h2><p>Clientes Bice suelen tener cupos de USD 5.000 a USD 30.000. DolarExpress maneja altos montos sin problemas.</p>"),

    ("vender-cupo-dolar-security",
     "Vender Cupo Dólar Banco Security | DolarExpress",
     "Vendé tu cupo en dólares Banco Security. Rápido, seguro y confiable.",
     "vender cupo dolar security,cupo banco security venta,cambiar cupo security",
     "Vender Cupo Dólar <span class='highlight'>Banco Security</span>",
     "Banco Security ofrece cupos en dólares competitivos para sus clientes. Conviértelo a pesos en 15 minutos.",
     "<h2>Banco Security: Cupo en Dólares</h2><p>Banco Security es reconocido por sus productos de crédito internacional. Sus tarjetas incluyen cupo en dólares de forma automática.</p><h2>¿Cómo Ver Tu Cupo Security?</h2><ul><li>App Security → Mis productos → Tarjeta → Cupo disponible</li><li>Web Security → Portal cliente</li></ul><h2>Tarjetas Security con Cupo</h2><ul><li>Visa Security Clásica</li><li>Visa Security Platinum</li><li>Mastercard Security</li><li>Amex Security</li></ul><h2>Por Qué DolarExpress</h2><p>Mejor tipo de cambio que sucursales, sin comisiones, operación 100% online en 15 minutos.</p>"),

    # ── GRUPO 2: cambiar cupo dolar + banco ─────────────────────────────────────
    ("cambiar-cupo-dolar-bci",
     "Cambiar Cupo Dólar BCI | DolarExpress",
     "Cambiá tu cupo en dólares BCI a pesos chilenos. Operación en minutos.",
     "cambiar cupo dolar bci,convertir cupo bci,cupo bci a pesos",
     "Cambiar Cupo Dólar <span class='highlight'>BCI</span>",
     "¿Tienes cupo en dólares BCI? Cámbialo a pesos chilenos en 15 minutos, sin comisiones y con el mejor tipo de cambio.",
     "<h2>¿Qué Significa Cambiar Cupo BCI?</h2><p>Cambiar tu cupo en dólares BCI significa convertir ese límite internacional a pesos chilenos. No es un avance en efectivo. Es una conversión de moneda.</p><h2>Diferencia con Avance en Efectivo</h2><ul><li>Avance BCI: 3-5% comisión + tasa alta</li><li>DolarExpress: Solo cambio del día, sin comisiones adicionales</li></ul><h2>Proceso</h2><ol><li>Verifica cupo en app BCI</li><li>Foto del cupo disponible</li><li>WhatsApp DolarExpress</li><li>Cotización inmediata en pesos</li><li>Transferencia en 15 minutos</li></ol><h2>¿Es Legal?</h2><p>Sí. Es una operación de conversión de divisas que opera dentro del sistema bancario formal de Chile.</p>"),

    ("cambiar-cupo-dolar-banco-chile",
     "Cambiar Cupo Dólar Banco de Chile | DolarExpress",
     "Cambiá tu cupo en dólares Banco de Chile a pesos. Sin comisiones.",
     "cambiar cupo dolar banco chile,convertir cupo banco chile,cupo banco chile a pesos",
     "Cambiar Cupo Dólar <span class='highlight'>Banco de Chile</span>",
     "Convierte tu cupo en dólares Banco de Chile a pesos chilenos. Sin ir a sucursal, sin comisiones, en 15 minutos.",
     "<h2>Cambiar Cupo Banco de Chile</h2><p>Si tienes cupo en dólares de Banco de Chile, puedes convertirlo a pesos a través de DolarExpress de forma rápida y segura.</p><h2>¿Cuánto Recibes?</h2><p>El monto en pesos depende del tipo de cambio del día (dólar observado o bancario). DolarExpress te da cotización exacta antes de confirmar.</p><h2>Ventajas vs Canal Oficial BdC</h2><ul><li>Sin comisión de avance (3-5%)</li><li>Sin tasa mensual adicional</li><li>Operación inmediata 24/7</li><li>Sin necesidad de ir a sucursal</li></ul>"),

    ("cambiar-cupo-dolar-banco-estado",
     "Cambiar Cupo Dólar BancoEstado | DolarExpress",
     "Cambiá tu cupo en dólares BancoEstado a pesos chilenos. Rápido y seguro.",
     "cambiar cupo dolar bancoestado,convertir cupo bancoestado,cupo bancoestado a pesos",
     "Cambiar Cupo Dólar <span class='highlight'>BancoEstado</span>",
     "Convierte tu cupo en dólares BancoEstado a pesos en 15 minutos. Operación segura dentro del sistema bancario formal.",
     "<h2>Cambiar Cupo BancoEstado</h2><p>BancoEstado tiene millones de clientes en Chile. Muchos tienen cupo en dólares en su tarjeta de crédito pero no saben cómo convertirlo eficientemente.</p><h2>¿Por Qué No Usar el Canal Oficial?</h2><ul><li>Avance en efectivo BancoEstado: Comisión alta + intereses</li><li>DolarExpress: Solo tipo de cambio del día, sin comisiones</li></ul><h2>Proceso</h2><ol><li>App BancoEstado → Cupo internacional disponible</li><li>Foto del cupo</li><li>WhatsApp DolarExpress</li><li>Cotización y transferencia en 15 minutos</li></ol>"),

    ("cambiar-cupo-dolar-santander",
     "Cambiar Cupo Dólar Santander | DolarExpress",
     "Cambiá tu cupo en dólares Santander a pesos. Transferencia inmediata.",
     "cambiar cupo dolar santander,convertir cupo santander,cupo santander a pesos",
     "Cambiar Cupo Dólar <span class='highlight'>Santander</span>",
     "Convierte tu cupo en dólares Santander a pesos chilenos. Sin comisiones, sin trámites, en 15 minutos.",
     "<h2>Cambiar Cupo Santander</h2><p>Santander Chile es uno de los bancos con mayor cupo en dólares para sus clientes. Convertirlo a pesos con DolarExpress es la opción más rápida y económica.</p><h2>Comparativa de Costos</h2><ul><li>Avance Santander directo: 3-5% comisión + tasa de interés</li><li>DolarExpress: 0% comisión adicional, solo cambio del día</li></ul><h2>Montos Aceptados</h2><p>DolarExpress acepta desde USD 200 hasta USD 50.000 de cupo Santander. Para montos altos, coordina con antelación.</p>"),

    ("cambiar-cupo-dolar-falabella",
     "Cambiar Cupo Dólar CMR Falabella | DolarExpress",
     "Cambiá tu cupo en dólares CMR Falabella. Cotización en segundos.",
     "cambiar cupo dolar falabella,convertir cupo cmr,cupo cmr a pesos",
     "Cambiar Cupo Dólar <span class='highlight'>CMR Falabella</span>",
     "Convierte tu cupo en dólares CMR Falabella a pesos. Cotización instantánea, transferencia en 15 minutos.",
     "<h2>CMR Falabella: Cupo en Dólares</h2><p>La tarjeta CMR tiene cupo internacional en dólares que muchos titulares no utilizan. DolarExpress lo convierte a pesos de forma inmediata.</p><h2>¿Cómo Verificar Tu Cupo CMR?</h2><ul><li>App CMR Falabella → Cupo disponible → Internacional</li><li>Web CMR → Estado de cuenta</li></ul><h2>Proceso Simple</h2><ol><li>Verifica cupo CMR</li><li>Foto + WhatsApp DolarExpress</li><li>Cotización en 1 minuto</li><li>Transferencia en 15 minutos</li></ol>"),

    ("cambiar-cupo-dolar-ripley",
     "Cambiar Cupo Dólar Ripley | DolarExpress",
     "Cambiá tu cupo en dólares Ripley a pesos chilenos. Rápido y seguro.",
     "cambiar cupo dolar ripley,convertir cupo ripley,cupo ripley a pesos",
     "Cambiar Cupo Dólar <span class='highlight'>Ripley</span>",
     "Convierte tu cupo en dólares Ripley a pesos. Sin comisiones, sin ir a la tienda, en 15 minutos.",
     "<h2>Cambiar Cupo Ripley</h2><p>La tarjeta de crédito Ripley incluye cupo internacional en dólares para sus clientes. DolarExpress lo convierte a pesos al mejor precio.</p><h2>Condiciones</h2><ul><li>Tarjeta Ripley vigente</li><li>Cupo internacional habilitado</li><li>Sin bloqueos en la tarjeta</li></ul><h2>Proceso</h2><ol><li>App Ripley → Cupo disponible</li><li>Foto del cupo</li><li>WhatsApp DolarExpress</li><li>Transferencia en 15 minutos</li></ol><h2>¿Es Seguro?</h2><p>Sí. La operación se realiza dentro del sistema bancario formal. Tú recibes transferencia a tu cuenta, sin riesgo.</p>"),

    # ── GRUPO 3: bancos/tarjetas nuevos ─────────────────────────────────────────
    ("cupo-dolar-coopeuch",
     "Cupo Dólar Coopeuch | DolarExpress",
     "Vendé tu cupo en dólares Coopeuch. Pago inmediato sin comisiones.",
     "cupo dolar coopeuch,coopeuch dolares,vender cupo coopeuch",
     "Cupo Dólar <span class='highlight'>Coopeuch</span>",
     "Coopeuch es la cooperativa de ahorro y crédito más grande de Chile. Sus tarjetas de crédito también tienen cupo en dólares.",
     "<h2>Coopeuch y el Cupo en Dólares</h2><p>Coopeuch ofrece tarjetas de crédito con acceso internacional. Muchos socios tienen cupo en dólares disponible en su tarjeta Coopeuch.</p><h2>¿Cómo Ver Tu Cupo Coopeuch?</h2><ul><li>App Coopeuch → Mi tarjeta → Cupo internacional</li><li>Web Coopeuch → Mis productos</li><li>Sucursal Coopeuch</li></ul><h2>Tarjetas Coopeuch con Cupo</h2><ul><li>Visa Coopeuch Clásica</li><li>Visa Coopeuch Oro</li><li>Mastercard Coopeuch</li></ul><h2>Proceso de Venta</h2><ol><li>Verifica cupo en app Coopeuch</li><li>Foto del cupo disponible</li><li>WhatsApp DolarExpress</li><li>Cotización y transferencia en 15 minutos</li></ol>"),

    ("cupo-dolar-tenpo",
     "Cupo Dólar Tenpo | DolarExpress",
     "Cupo en dólares Tenpo: cotización y venta rápida. Transferencia inmediata.",
     "cupo dolar tenpo,tenpo dolares,vender cupo tenpo",
     "Cupo Dólar <span class='highlight'>Tenpo</span>",
     "Tenpo es una de las fintechs más populares de Chile. Su tarjeta de crédito incluye cupo en dólares para transacciones internacionales.",
     "<h2>Tenpo y el Cupo en Dólares</h2><p>Tenpo ofrece una tarjeta de crédito digital con cupo en dólares. Es parte de las nuevas opciones fintech en Chile con acceso internacional.</p><h2>¿Cómo Ver Tu Cupo Tenpo?</h2><ul><li>App Tenpo → Tarjeta de crédito → Cupo disponible</li><li>Sección 'Mi cuenta' → Límites</li></ul><h2>Características Tenpo</h2><ul><li>Tarjeta 100% digital</li><li>Cupo en dólares para compras internacionales</li><li>Gestión vía app móvil</li></ul><h2>Vender Cupo Tenpo con DolarExpress</h2><p>Si tienes cupo en dólares en tu tarjeta Tenpo, DolarExpress puede convertirlo a pesos chilenos en 15 minutos. Envía foto del cupo disponible por WhatsApp.</p>"),

    ("cupo-dolar-credichile",
     "Cupo Dólar CredíChile | DolarExpress",
     "Vendé tu cupo en dólares CredíChile. Transferencia inmediata, sin comisiones.",
     "cupo dolar credichile,credichile dolares,vender cupo credichile",
     "Cupo Dólar <span class='highlight'>CredíChile</span>",
     "CredíChile es una de las principales financieras de Chile. Sus tarjetas de crédito incluyen cupo en dólares para sus clientes.",
     "<h2>CredíChile y el Cupo en Dólares</h2><p>CredíChile, perteneciente al Grupo BCI, ofrece tarjetas de crédito con acceso internacional en dólares. Es común en clientes con historial crediticio bueno.</p><h2>¿Cómo Ver Tu Cupo CredíChile?</h2><ul><li>App CredíChile → Mi tarjeta → Cupo internacional</li><li>Web CredíChile → Estado de cuenta</li><li>Atención al cliente CredíChile</li></ul><h2>Proceso de Venta</h2><ol><li>Confirma cupo en app CredíChile</li><li>Foto del cupo disponible</li><li>WhatsApp DolarExpress</li><li>Cotización en 1 minuto</li><li>Transferencia en 15 minutos</li></ol>"),

    ("cupo-dolar-consorcio",
     "Cupo Dólar Banco Consorcio | DolarExpress",
     "Cupo en dólares Banco Consorcio: venta segura y rápida. Mejor precio.",
     "cupo dolar consorcio,banco consorcio dolares,vender cupo consorcio",
     "Cupo Dólar <span class='highlight'>Banco Consorcio</span>",
     "Banco Consorcio ofrece productos financieros premium. Sus tarjetas de crédito tienen cupo en dólares con límites competitivos.",
     "<h2>Banco Consorcio: Cupo en Dólares</h2><p>Banco Consorcio es reconocido por sus productos financieros para clientes de mayor poder adquisitivo. Sus tarjetas incluyen cupo internacional significativo.</p><h2>¿Cómo Ver Tu Cupo Consorcio?</h2><ul><li>App Consorcio → Mis productos → Tarjeta → Cupo disponible</li><li>Web Banco Consorcio → Portal cliente</li></ul><h2>Tarjetas Consorcio con Cupo</h2><ul><li>Visa Consorcio Clásica</li><li>Visa Consorcio Oro/Platinum</li><li>Mastercard Consorcio</li></ul><h2>Altos Montos</h2><p>Clientes Banco Consorcio frecuentemente tienen cupos en dólares elevados. DolarExpress maneja montos desde USD 500 hasta USD 50.000.</p>"),

    ("cupo-dolar-latam-pass",
     "Cupo Dólar LATAM Pass | DolarExpress",
     "Vendé tu cupo en dólares LATAM Pass. Mejor precio garantizado.",
     "cupo dolar latam pass,latam pass dolares,vender cupo latam",
     "Cupo Dólar <span class='highlight'>LATAM Pass</span>",
     "La tarjeta LATAM Pass te acumula millas y también tiene cupo en dólares. Convierte ese cupo a pesos con DolarExpress.",
     "<h2>LATAM Pass y el Cupo en Dólares</h2><p>Las tarjetas LATAM Pass (emitidas por distintos bancos) incluyen cupo en dólares además de acumular puntos para vuelos. Ese cupo puede convertirse a pesos.</p><h2>¿Cuál es Tu Banco Emisor?</h2><ul><li>LATAM Pass Banco de Chile → Ver cupo en app BdC</li><li>LATAM Pass BCI → Ver cupo en app BCI</li><li>LATAM Pass Santander → Ver cupo en app Santander</li></ul><h2>Proceso</h2><ol><li>Identifica tu banco emisor LATAM Pass</li><li>Verifica cupo en la app del banco</li><li>Foto + WhatsApp DolarExpress</li><li>Transferencia en 15 minutos</li></ol>"),

    # ── GRUPO 4: informacionales ─────────────────────────────────────────────────
    ("cuanto-pagan-cupo-dolar",
     "¿Cuánto Pagan por Cupo Dólar? | DolarExpress",
     "Precio actual del cupo en dólares en Chile. Cotización en tiempo real sin comisiones.",
     "cuanto pagan cupo dolar,precio cupo dolar,cotizacion cupo dolar chile",
     "¿Cuánto Pagan por <span class='highlight'>Cupo Dólar</span>?",
     "El precio del cupo en dólares varía diariamente según el tipo de cambio. DolarExpress te da cotización exacta en tiempo real.",
     "<h2>¿Cómo se Calcula el Precio del Cupo en Dólares?</h2><p>El precio que recibes por tu cupo en dólares depende principalmente del tipo de cambio dólar/peso del día (dólar observado del Banco Central de Chile).</p><h2>Factores que Influyen en el Precio</h2><ul><li>Tipo de cambio del día (fluctúa diariamente)</li><li>Monto del cupo (mayor monto, mejor tasa)</li><li>Banco emisor de tu tarjeta</li><li>Operador (DolarExpress ofrece mejor precio)</li></ul><h2>Ejemplo de Cálculo</h2><p>Si tienes USD 1.000 en cupo y el dólar está a $950 CLP, recibirías aproximadamente $950.000 CLP (menos el diferencial del operador).</p><h2>¿Por Qué DolarExpress Paga Más?</h2><ul><li>Sin comisión de intermediario</li><li>Operamos con tipo de cambio del mercado</li><li>Volumen alto nos permite mejores tasas</li><li>Sin costo de sucursal</li></ul><h2>¿Cómo Obtener Cotización Exacta?</h2><p>Envíanos foto de tu cupo disponible por WhatsApp y te cotizamos en 1 minuto. Sin compromiso.</p>",
     "Cotizar Ahora"),

    ("cupo-dolar-mismo-dia",
     "Cupo Dólar Mismo Día | DolarExpress",
     "Vendé tu cupo en dólares y cobrate el mismo día. Transferencia inmediata garantizada.",
     "cupo dolar mismo dia,cobrar cupo dolar hoy,vender cupo mismo dia",
     "Cupo Dólar <span class='highlight'>Mismo Día</span>",
     "Con DolarExpress, vendes tu cupo en dólares y recibes la transferencia el mismo día — en menos de 15 minutos.",
     "<h2>¿Por Qué Cobrar el Mismo Día?</h2><p>Cuando necesitas dinero urgente, esperar 24-48 horas no es opción. DolarExpress garantiza que recibes la transferencia el mismo día que inicias la operación.</p><h2>¿Cómo es Posible en 15 Minutos?</h2><ul><li>Operación 100% digital (sin papeles, sin sucursal)</li><li>Ejecutivos disponibles 7 AM a 11 PM</li><li>Proceso simplificado al máximo</li><li>Transferencia bancaria inmediata vía TEF</li></ul><h2>Disponibilidad</h2><ul><li>Lunes a viernes: 7 AM - 11 PM</li><li>Fines de semana: 8 AM - 10 PM</li><li>Feriados: disponible con demora mínima</li></ul><h2>Horario Bancario</h2><p>Las transferencias TEF se procesan en horario bancario. Si operas después de las 11 PM, el dinero llega al inicio del siguiente día hábil.</p>"),

    ("cupo-dolar-cencosud",
     "Cupo Dólar Cencosud | DolarExpress",
     "Cupo en dólares Cencosud: venta rápida y segura. Transferencia inmediata.",
     "cupo dolar cencosud,cencosud dolares,vender cupo cencosud",
     "Cupo Dólar <span class='highlight'>Cencosud</span>",
     "Las tarjetas de Cencosud (Paris, Jumbo, Easy) tienen cupo en dólares disponible. Conviértelo a pesos en minutos.",
     "<h2>Cencosud y Sus Tarjetas con Cupo en Dólares</h2><p>Cencosud opera múltiples tarjetas de retail en Chile: Paris, Jumbo, Easy. Todas bajo el paraguas de 'Tarjeta Cencosud' o 'Mastercard Cencosud'. Incluyen cupo internacional.</p><h2>¿Cuál es Tu Tarjeta Cencosud?</h2><ul><li>Tarjeta Paris → Cupo en dólares disponible</li><li>Tarjeta Jumbo → Cupo en dólares disponible</li><li>Tarjeta Easy → Cupo en dólares disponible</li><li>Mastercard Cencosud → Cupo en dólares disponible</li></ul><h2>Proceso de Venta</h2><ol><li>App Cencosud o del banco → Cupo internacional</li><li>Foto del cupo disponible</li><li>WhatsApp DolarExpress</li><li>Transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-precio",
     "Precio al Vender Cupo Dólar Hoy | DolarExpress",
     "Precio de compra de cupo en dólares hoy en Chile. Sin comisiones ocultas.",
     "precio vender cupo dolar,cuanto vale cupo dolar,precio cupo dolar hoy",
     "Precio al Vender Cupo Dólar <span class='highlight'>Hoy</span>",
     "El precio que recibes al vender tu cupo en dólares depende del tipo de cambio del día. Cotizamos sin compromiso.",
     "<h2>Precio de Compra de Cupo en Dólares</h2><p>DolarExpress compra tu cupo en dólares al precio del mercado. Usamos el tipo de cambio del día del Banco Central de Chile como referencia.</p><h2>¿Cómo Saber el Precio Exacto?</h2><p>El precio varía diariamente. Envíanos foto de tu cupo por WhatsApp y en 1 minuto te decimos exactamente cuántos pesos recibes. Sin compromiso.</p><h2>Variables del Precio</h2><ul><li>USD/CLP del día (fluctúa)</li><li>Tu banco emisor</li><li>Monto del cupo (mayor monto = mejor precio)</li></ul><h2>Diferencial de DolarExpress</h2><p>Pagamos más que casas de cambio tradicionales porque operamos sin locales físicos. Ese ahorro lo traspasamos a ti.</p>",
     "Cotizar Precio"),

    ("cupo-dolar-precio-hoy",
     "Precio Cupo Dólar Hoy | DolarExpress",
     "Precio del cupo en dólares hoy en Chile. Actualizado en tiempo real.",
     "precio cupo dolar hoy,cotizacion cupo dolar,cupo dolar valor hoy",
     "Precio Cupo Dólar <span class='highlight'>Hoy</span>",
     "El precio del cupo en dólares cambia cada día según el tipo de cambio. Cotiza gratis y sin compromiso ahora.",
     "<h2>¿Cuál es el Precio del Cupo en Dólares Hoy?</h2><p>El precio se determina por el dólar observado del Banco Central de Chile. DolarExpress actualiza su cotización diariamente al inicio de operaciones.</p><h2>¿Por Qué Varía el Precio?</h2><ul><li>El dólar sube y baja cada día</li><li>Factores internacionales (Fed, economía USA)</li><li>Factores locales (economía chilena, política)</li></ul><h2>Cómo Obtener el Precio Exacto</h2><p>Envíanos foto de tu cupo disponible por WhatsApp. Te cotizamos en 1 minuto con el precio del día. Sin compromiso de venta.</p><h2>Rango Habitual</h2><p>El tipo de cambio dólar/peso suele oscilar entre $900 y $1.000 CLP por USD (en 2024-2025). Si tienes USD 1.000 en cupo, recibirías entre $900.000 y $1.000.000 CLP aproximadamente.</p>"),

    ("vender-cupo-dolar-santiago",
     "Vender Cupo Dólar en Santiago | DolarExpress",
     "Vendé tu cupo en dólares en Santiago. Transferencia inmediata, mejor precio.",
     "vender cupo dolar santiago,cambiar cupo dolar santiago,cupo dolar santiago",
     "Vender Cupo Dólar en <span class='highlight'>Santiago</span>",
     "Santiago concentra la mayor cantidad de operaciones de cupo en dólares de Chile. DolarExpress opera en toda la región metropolitana.",
     "<h2>Santiago: Capital del Cupo en Dólares</h2><p>La mayoría de los clientes de DolarExpress están en Santiago. La alta concentración bancaria y de tarjetas de crédito en la capital hace de Santiago el mercado principal.</p><h2>Comunas de Santiago donde Operamos</h2><ul><li>Las Condes, Providencia, Vitacura (alta concentración)</li><li>Santiago Centro, Ñuñoa, La Florida</li><li>Todo el Gran Santiago vía transferencia bancaria</li></ul><h2>Ventajas en Santiago</h2><ul><li>Mayor rapidez (bancos en la misma zona horaria)</li><li>Más ejecutivos disponibles</li><li>Operaciones de lunes a domingo</li></ul>"),

    ("vender-cupo-dolar-concepcion",
     "Vender Cupo Dólar en Concepción | DolarExpress",
     "Vendé tu cupo en dólares en Concepción. Pago en minutos vía transferencia.",
     "vender cupo dolar concepcion,cambiar cupo dolar concepcion,cupo dolar concepcion",
     "Vender Cupo Dólar en <span class='highlight'>Concepción</span>",
     "DolarExpress opera en Concepción y toda la región del Biobío. Sin sucursal física, todo por WhatsApp en 15 minutos.",
     "<h2>Cupo en Dólares en Concepción</h2><p>Concepción es la segunda ciudad más importante de Chile. DolarExpress tiene clientes activos en la región del Biobío y opera sin necesidad de sucursal física.</p><h2>¿Necesito ir a algún Lugar?</h2><p>No. La operación es 100% online vía WhatsApp. Estés en Concepción, Chiguayante, San Pedro de la Paz o cualquier punto de la región, recibes tu transferencia igual.</p><h2>Proceso en Concepción</h2><ol><li>Verifica cupo en app de tu banco</li><li>WhatsApp DolarExpress</li><li>Cotización en 1 minuto</li><li>Transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-valparaiso",
     "Vender Cupo Dólar en Valparaíso | DolarExpress",
     "Vendé tu cupo en dólares en Valparaíso. Cotización inmediata, sin comisiones.",
     "vender cupo dolar valparaiso,cambiar cupo dolar valparaiso,cupo dolar valparaiso",
     "Vender Cupo Dólar en <span class='highlight'>Valparaíso</span>",
     "Valparaíso y Viña del Mar son una de las zonas con más clientes de DolarExpress. Operamos en toda la región de Valparaíso.",
     "<h2>Cupo en Dólares en Valparaíso</h2><p>La región de Valparaíso tiene una alta penetración bancaria. Clientes de Valparaíso, Viña del Mar, Villa Alemana y toda la región usan DolarExpress.</p><h2>Sin Sucursal Física</h2><p>No hay oficina en Valparaíso, pero tampoco la necesitas. Todo el proceso es por WhatsApp. El dinero llega a tu cuenta bancaria en 15 minutos.</p><h2>Proceso</h2><ol><li>App de tu banco → Cupo en dólares</li><li>Foto + WhatsApp DolarExpress</li><li>Cotización inmediata</li><li>Transferencia en 15 minutos a cualquier banco de Valparaíso</li></ol>"),

    # ── GRUPO 5: ciudades + vender ───────────────────────────────────────────────
    ("vender-cupo-dolar-temuco",
     "Vender Cupo Dólar en Temuco | DolarExpress",
     "Vendé tu cupo en dólares en Temuco. Transferencia rápida y segura.",
     "vender cupo dolar temuco,cambiar cupo dolar temuco,cupo dolar temuco",
     "Vender Cupo Dólar en <span class='highlight'>Temuco</span>",
     "DolarExpress opera en Temuco y toda la Araucanía. Convierte tu cupo en dólares a pesos en 15 minutos.",
     "<h2>Cupo en Dólares en Temuco</h2><p>Temuco es la capital de la Araucanía y una ciudad importante del sur de Chile. DolarExpress tiene clientes activos en Temuco y opera sin sucursal física.</p><h2>Servicio Regional</h2><p>No importa si estás en Temuco centro, Padre Las Casas, Villarrica o cualquier localidad de la región. La operación es 100% por WhatsApp.</p><h2>Proceso</h2><ol><li>Verifica cupo en app de tu banco</li><li>WhatsApp DolarExpress</li><li>Cotización en 1 minuto</li><li>Transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-antofagasta",
     "Vender Cupo Dólar en Antofagasta | DolarExpress",
     "Vendé tu cupo en dólares en Antofagasta. Sin comisiones, pago inmediato.",
     "vender cupo dolar antofagasta,cambiar cupo dolar antofagasta,cupo dolar antofagasta",
     "Vender Cupo Dólar en <span class='highlight'>Antofagasta</span>",
     "Antofagasta tiene alta actividad minera y financiera. DolarExpress opera en toda la región de Antofagasta.",
     "<h2>Cupo en Dólares en Antofagasta</h2><p>La región de Antofagasta tiene alta actividad económica gracias a la minería. Muchos trabajadores y profesionales tienen tarjetas con cupo en dólares.</p><h2>Características de la Región</h2><ul><li>Alta concentración de ingreso por minería</li><li>Acceso a tarjetas de crédito premium</li><li>Cupos en dólares generalmente más altos</li></ul><h2>Proceso DolarExpress en Antofagasta</h2><ol><li>App de tu banco → Cupo internacional</li><li>Foto + WhatsApp</li><li>Cotización y transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-iquique",
     "Vender Cupo Dólar en Iquique | DolarExpress",
     "Vendé tu cupo en dólares en Iquique. Operación segura y rápida.",
     "vender cupo dolar iquique,cambiar cupo dolar iquique,cupo dolar iquique",
     "Vender Cupo Dólar en <span class='highlight'>Iquique</span>",
     "Iquique es zona franca y tiene alta actividad comercial con divisas. DolarExpress opera en toda la región de Tarapacá.",
     "<h2>Cupo en Dólares en Iquique</h2><p>Iquique, con su zona franca ZOFRI, tiene alta actividad en divisas. Muchos residentes están acostumbrados a manejar dólares y tienen cupo internacional en sus tarjetas.</p><h2>Zona Franca y Cupo en Dólares</h2><p>Aunque ZOFRI opera con pesos, muchos comerciantes y trabajadores tienen cupo en dólares disponible en sus tarjetas que pueden convertir a pesos con DolarExpress.</p><h2>Proceso en Iquique</h2><ol><li>Verifica cupo en app de tu banco</li><li>WhatsApp DolarExpress</li><li>Cotización en 1 minuto</li><li>Transferencia en 15 minutos</li></ol>"),

    ("vender-cupo-dolar-vina-del-mar",
     "Vender Cupo Dólar en Viña del Mar | DolarExpress",
     "Vendé tu cupo en dólares en Viña del Mar. Pago inmediato sin comisiones.",
     "vender cupo dolar vina del mar,cambiar cupo dolar vina,cupo dolar vina del mar",
     "Vender Cupo Dólar en <span class='highlight'>Viña del Mar</span>",
     "Viña del Mar es una de las ciudades con más clientes de DolarExpress. Operamos en toda la región de Valparaíso.",
     "<h2>Cupo en Dólares en Viña del Mar</h2><p>Viña del Mar tiene alta densidad de profesionales y ejecutivos con tarjetas de crédito premium. Es una de las ciudades con más operaciones de cupo en dólares en DolarExpress.</p><h2>Cobertura</h2><p>Servicio disponible en toda la región de Valparaíso: Viña del Mar, Valparaíso, Quilpué, Villa Alemana, Casablanca y alrededores.</p><h2>Proceso</h2><ol><li>App de tu banco → Cupo internacional</li><li>Foto + WhatsApp DolarExpress</li><li>Cotización inmediata</li><li>Transferencia a cualquier banco en Viña del Mar</li></ol>"),

    ("vender-cupo-dolar-rancagua",
     "Vender Cupo Dólar en Rancagua | DolarExpress",
     "Vendé tu cupo en dólares en Rancagua. Transferencia inmediata garantizada.",
     "vender cupo dolar rancagua,cambiar cupo dolar rancagua,cupo dolar rancagua",
     "Vender Cupo Dólar en <span class='highlight'>Rancagua</span>",
     "Rancagua es la capital de O'Higgins. DolarExpress opera en toda la región, sin necesidad de sucursal.",
     "<h2>Cupo en Dólares en Rancagua</h2><p>Rancagua y la región de O'Higgins tienen actividad agrícola e industrial importante. DolarExpress tiene clientes en toda la región que usan el servicio de forma remota.</p><h2>Servicio 100% Online</h2><p>No hay sucursal en Rancagua, pero no la necesitas. Todo el proceso es por WhatsApp. Recibes la transferencia en tu cuenta bancaria de Rancagua en 15 minutos.</p><h2>Proceso</h2><ol><li>App de tu banco → Cupo internacional</li><li>Foto del cupo disponible</li><li>WhatsApp DolarExpress</li><li>Transferencia en 15 minutos</li></ol>"),
]


os.chdir(os.path.dirname(os.path.abspath(__file__)))

created = []
skipped = []
for args in pages:
    slug = args[0]
    path = f"public/{slug}/index.html"
    if os.path.exists(path):
        skipped.append(slug)
        print(f"  SKIP (already exists): {slug}")
        continue
    canon = create_page(*args)
    created.append(slug)
    print(f"  OK: {canon}")

print(f"\nTotal creadas: {len(created)}")
print(f"Total omitidas (ya existían): {len(skipped)}")
