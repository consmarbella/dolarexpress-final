# -*- coding: utf-8 -*-
import io, re
BASE = r'C:\Users\matte\OneDrive\Escritorio\legalhelser\reborn\dolarexpress-final\public'

ITAU = '''<h3 style="font-size:15px;margin-top:24px;margin-bottom:12px;">Verificar un cupo Ita&uacute; sin ruido</h3>
      <ul class="list">
        <li><strong>Lectura exacta en la app:</strong> la app de Ita&uacute; muestra el saldo internacional con precisi&oacute;n de centavos y cotizamos con ese n&uacute;mero exacto, no un redondeo estimado.</li>
        <li><strong>Estados en USD y en pesos:</strong> el banco procesa ambos balances en paralelo; corroboramos el dato del saldo internacional antes de pactar el cierre.</li>
        <li><strong>Liquidaci&oacute;n de una sola vez:</strong> la venta se liquida de una sola partida, evitando tramos escalonados que complican tu cronograma de pagos.</li>
      </ul>'''

CMR = '''<h3 style="font-size:15px;margin-top:24px;margin-bottom:12px;">Saldo CMR alto: c&oacute;mo conviene operar</h3>
      <ul class="list">
        <li><strong>Liquidez conjunta:</strong> si tu cupo disponible acompa&ntilde; a compras de departamental, la venta liquida todo junto y deja despejado tu plan de pagos del mes.</li>
        <li><strong>Ventana de cierre calculada:</strong> coordinamos la operaci&oacute;n antes del corte de ciclo, para que el traspaso a pesos del remanente parta limpio.</li>
        <li><strong>Discreci&oacute;n reforzada:</strong> montos de segmento alto se coordinan con horario especial y un solo asesor asignado.</li>
      </ul>'''

for slug, block in (('vender-cupo-itau.html', ITAU), ('vender-cupo-cmr-falabella.html', CMR)):
    p = BASE + '\\' + slug
    h = io.open(p, encoding='utf-8').read()
    m = re.search(r'<h3[^>]*>(?:Casos tipicos\?*|Lo primero|Verificar un cupo Ita\S*|Saldo CMR alto)', h)
    if m:
        h = h[:m.start()] + block + '\n\n      ' + h[m.start():]
    else:
        m = re.search(r'<h3[^>]*>Preguntas', h)
        h = h[:m.start()] + block + '\n      ' + h[m.start():]
    io.open(p, 'w', encoding='utf-8').write(h)
print('ok')
