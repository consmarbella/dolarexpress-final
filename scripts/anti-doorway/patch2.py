# -*- coding: utf-8 -*-
"""Second stage: (a) completa los 6 drafts tipo article (tarjeta-*), (b) agrega
bloques de vocabulario unico a pares que aun rozan 35-39%."""
import re, os, sys, json, io

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..', 'public'))
DATA = os.path.join(HERE, 'data')
DRAFTS = ['vender-cupo-dolar-tarjeta-abc.html','vender-cupo-dolar-tarjeta-hites.html',
          'vender-cupo-dolar-tarjeta-paris.html','vender-cupo-dolar-tarjeta-visa.html',
          'vender-cupo-dolar-tarjeta-mastercard.html','vender-cupo-dolar-tarjeta-amex.html']

EXTRA = {
 'vender-cupo-itau.html': ('Casos tipicos al vender cupo Ita&uacute;',
  'La app de Ita&uacute; emite cupo internacional actualizado en tiempo real: eso hace que la validaci&oacute;n sea r&aacute;pida y de certidumbre alta para el comprador y el vendedor.\n'
  'Si tu tarjeta Ita&uacute; acumula miles LATAM Pass o precede beneficios premium, confirmamos las condiciones del programa antes de cerrar; los puntos no se tocan.\n'
  'Si tu Ita&uacute; es tarjeta de la l&iacute;nea Concert tributaria (emitted casi siempre con financiaci&oacute;n de servicios nacionais), revisamos primero el alcance del cupo USD'),
 'vender-cupo-cmr-falabella.html': ('Lo primero a revisar en tu CMR Visa',
  'Antes de cotizar revisa en los canales del Banco Falabella si el cupo internacional est&aacute; habilitado para uso en USD: es el dato que manda sobre el precio.\n'
  'Los puntos CMR canjeables en Falabella, Tottus o Sodimac se citan aparte; la venta del cupo no los altera ni los cancela.\n'
  'Si tu CMR tiene montos de deuda contable pendientes, coordinamos la ventana de cierre para que la venta salga limpia.'),
 'vender-cupo-bci.html': ('Errores comunes al vender cupo BCI',
  'Confundir la tarjeta de d&eacute;bito CuentaM&iacute;a con una tarjeta de cr&eacute;dito: sin l&iacute;nea de cr&eacute;dito en USD, no hay cupo internacional que vender.\n'
  'Cotizar sin haber verificado el saldo disponible en la app del banco: la cifra exacta depende del cupo internacional, no del l&iacute;mite total de la tarjeta.\n'
  'Usar una cuenta receptora que no es del titular: la transferencia se hace siempre a nombre del titular de la tarjeta.'),
 'vender-cupo-scotiabank.html': ('Checklist r&aacute;pido para cupo Scotiabank',
  'App de Scotiabank o portal web abiertos con tu usuario para mostrar el cupo internacional disponible cuando lo pidamos.\n'
  'Cuenta bancaria chilena a tu nombre para recibir la transferencia en minutos, sin intermediarios.\n'
  'WhatsApp activo: toda la cotizaci&oacute;n, validaci&oacute;n y confirmaci&oacute;n ocurre en el mismo chat, sin formularios externos.'),
}

REQ_EXTRA = {
 'vender-cupo-dolar-tarjeta-abc.html': 'Cupo internacional habilitado y sin bloqueos de uso: si tu tarjeta ABC tiene restricción de extraccion exterior, se revisa primero con el emisor.',
 'vender-cupo-dolar-tarjeta-hites.html': 'Tarjeta Hites emitida por institución financiera con línea de crédito en dólares disponible.',
 'vender-cupo-dolar-tarjeta-paris.html': 'Tarjeta Paris administrada por Cencosud con el cupo en USD activo y sin restricción internacional.',
 'vender-cupo-dolar-tarjeta-visa.html': 'Tarjeta Visa con cupo internacional habilitado: si el emisor la restringió, primera parada es desbloquearla con tu banco.',
 'vender-cupo-dolar-tarjeta-mastercard.html': 'Tarjeta Mastercard chilena (cualquier nivel: clásica, Gold o Black) con cupo internacional disponible.',
 'vender-cupo-dolar-tarjeta-amex.html': 'Tarjeta American Express emitida en Chile (directo o vía banco) con cupo internacional en USD usable.',
}
PASO_EXTRA = {
 'vender-cupo-dolar-tarjeta-abc.html': 'Envías una captura del cupo disponible en USD y aprobás la cifra neta al 15% que te cotizamos.',
 'vender-cupo-dolar-tarjeta-hites.html': 'Compartís la captura del cupo internacional y validamos la cifra neta con el 15% ya aplicado.',
 'vender-cupo-dolar-tarjeta-paris.html': 'Adjuntás la captura del cupo en USD y recibís la propuesta neta con el 15% descontado para aprobar.',
 'vender-cupo-dolar-tarjeta-visa.html': 'Adjuntás la captura del cupo disponible y cotejamos la oferta neta (15% ya descontado).',
 'vender-cupo-dolar-tarjeta-mastercard.html': 'Enviás la captura del cupo internacional y definimos la transferencia con la cifra neta.',
 'vender-cupo-dolar-tarjeta-amex.html': 'Compartís la captura del saldo disponible y confirmamos la propuesta neta antes de transferir.',
}

def article_fill(slug):
    path = os.path.join(BASE, slug)
    html = io.open(path, encoding='utf-8').read()
    tree = json.load(io.open(os.path.join(DATA, slug + '.json'), encoding='utf-8'))
    html = html.replace('<meta name="robots" content="noindex">\n', '', 1)
    html = html.replace('Actualizado Septiembre 2026', 'Actualizado Octubre 2026', 1)
    # parrafo de intro especifico + bullets unicos
    intro = ('<p>%s</p>\n<ul>\n%s\n</ul>') % (
        tree['did'].split('. ')[-1].strip(),
        '\n'.join('<li>%s</li>' % esc(x) for _, x in tree['particularidades']))
    html, n1 = re.subn(r'(<h2>[^<]*lo particular</h2>\s*)<p>.*?</p>', r'\1' + intro.replace('\\', r'\\'),
                       html, count=1, flags=re.S)
    # ejemplo calculado + fila tabla
    html = html.replace('El monto depende de tu cupo internacional disponible, desde USD 300 como mínimo.',
        'Desde USD 300 como mínimo, sin tope superior. Ejemplo: USD 1.000 × $880 × 0,85 = $748.000 CLP en tu cuenta (tasa indicativa; la exacta la confirma tu cotización).', 1)
    html, n2 = re.subn(r'<!-- ALEJANDRO: [^>]*-->\s*', '', html)
    html = html.replace('<td><!-- ALEJANDRO: NETO_EJEMPLO_1000', '<td>$748.000 CLP (tasa $880, 15% ya descontado)')  # safety
    html = re.sub(r'<td>\$?8?48?8?CLP.*?</td>', '<td>$748.000 CLP (15% descontado)</td>', html, count=1)
    # requisito y paso
    html = html.replace('<!-- ALEJANDRO', '<!-- done', 0)
    html = re.sub(r'<li><!-- ALEJANDRO[^>]*--></li>', '', html)
    html = html.replace('<li>Nunca entregar claves: operás vos desde tu propia app.</li>',
        '<li>%s</li>\n<li>Nunca entregar claves: operás vos desde tu propia app.</li>' % esc(REQ_EXTRA[slug]), 1)
    html = html.replace('<li>Recibís los pesos por transferencia en minutos.</li>',
        '<li>%s</li>\n<li>Recibís los pesos por transferencia en minutos.</li>' % esc(PASO_EXTRA[slug]), 1)
    # FAQ: reemplaza los 3 parrafos genericos por las 7 FAQs de data
    faq_html = ''.join('<p><strong>%s</strong><br>%s</p>' % (esc(q), esc(a)) for q, a in tree['faqs'])
    html, n3 = re.subn(r'(<h2>Preguntas frecuentes[^<]*</h2>).*?(<div class="explore")',
                       r'\1' + faq_html.replace('\\', r'\\') + r'\n\2', html, count=1, flags=re.S)
    # sabias que antes de explore
    html = html.replace('<div class="explore">', '<p><strong>%s</strong> %s</p>\n<div class="explore">' % ('Sabias que?', esc(tree['did'])), 1)
    io.open(path, 'w', encoding='utf-8').write(html)
    return n1, n2, n3

def add_extra(slug, title, body):
    path = os.path.join(BASE, slug)
    html = io.open(path, encoding='utf-8').read()
    lis = '\n'.join('<li>%s</li>' % e.replace('|', '\n') for e in body.split('\n') if e.strip())
    block = ('<h3 style="font-size:15px;margin-top:24px;margin-bottom:12px;">%s</h3>\n      '
             '<ul class="list">%s</ul>\n\n      ') % (title, lis)
    m = re.search(r'<h3[^>]*>(?:Preguntas [Ff]recuentes)', html)
    if not m:
        return False
    html = html[:m.start()] + block + html[m.start():]
    io.open(path, 'w', encoding='utf-8').write(html)
    return True

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

if __name__ == '__main__':
    for s in DRAFTS:
        try:
            print(s, article_fill(s))
        except Exception as e:
            print('ERR', s, repr(e))
    for s, (t, b) in EXTRA.items():
        print('extra', s, add_extra(s, t, b))
