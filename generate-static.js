import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC_DIR = path.join(__dirname, 'public');
const DIST_DIR = path.join(__dirname, 'dist');

// ========== DATA ==========

const CITY_NAMES = {
  'santiago': 'Santiago', 'concepcion': 'Concepción', 'valparaiso': 'Valparaíso',
  'vina-del-mar': 'Viña del Mar', 'temuco': 'Temuco', 'rancagua': 'Rancagua',
  'antofagasta': 'Antofagasta', 'la-serena': 'La Serena', 'puerto-montt': 'Puerto Montt',
  'iquique': 'Iquique', 'arica': 'Arica', 'chillan': 'Chillán', 'calama': 'Calama',
  'copiapo': 'Copiapo', 'osorno': 'Osorno', 'talca': 'Talca', 'valdivia': 'Valdivia',
  'punta-arenas': 'Punta Arenas',
  'las-condes': 'Las Condes', 'providencia': 'Providencia', 'maipu': 'Maipú',
  'la-florida': 'La Florida', 'penalolen': 'Peñalolén', 'nunoa': 'Ñuñoa',
  'vitacura': 'Vitacura', 'lo-barnechea': 'Lo Barnechea', 'recoleta': 'Recoleta',
  'independencia': 'Independencia', 'san-miguel': 'San Miguel', 'el-bosque': 'El Bosque',
  'quilicura': 'Quilicura', 'cerro-navia': 'Cerro Navia', 'renca': 'Renca',
  'quinta-normal': 'Quinta Normal', 'estacion-central': 'Estación Central',
  'linares': 'Linares', 'san-fernando': 'San Fernando', 'san-antonio': 'San Antonio',
  'santa-cruz': 'Santa Cruz', 'pichilemu': 'Pichilemu', 'villaricca': 'Villarrica',
  'pucon': 'Pucón', 'castro': 'Castro', 'ancud': 'Ancud', 'quellon': 'Quellón',
  'la-union': 'La Unión', 'rio-bueno': 'Río Bueno', 'frutillar': 'Frutillar',
  'puerto-varas': 'Puerto Varas', 'llanquihue': 'Llanquihue', 'los-angeles': 'Los Ángeles',
  'barcelona': 'Barcelona',
  'alhue': 'Alhué', 'buin': 'Buin', 'calera-de-tango': 'Calera de Tango',
  'cerrillos': 'Cerrillos', 'conchali': 'Conchalí', 'curacavi': 'Curacaví',
  'el-monte': 'El Monte', 'huechuraba': 'Huechuraba', 'isla-de-maipo': 'Isla de Maipo',
  'la-cisterna': 'La Cisterna', 'la-granja': 'La Granja', 'la-pintana': 'La Pintana',
  'la-reina': 'La Reina', 'lo-espejo': 'Lo Espejo', 'lo-prado': 'Lo Prado',
  'macul': 'Macul', 'maria-pinto': 'María Pinto', 'padre-hurtado': 'Padre Hurtado',
  'paine': 'Paine', 'pedro-aguirre-cerda': 'Pedro Aguirre Cerda',
  'peñaflor': 'Peñaflor', 'pirque': 'Pirque', 'san-jose-de-maipo': 'San José de Maipo',
  'san-joaquin': 'San Joaquín', 'san-ramon': 'San Ramón', 'santiago-centro': 'Santiago Centro',
  'talagante': 'Talagante', 'tiltil': 'Til Til',
};

const BANK_DATA = {
  'banco-chile': { name: 'Banco de Chile', desc: 'el banco más grande del país con más de 2 millones de clientes', fact: 'Fue fundado en 1893 y es uno de los bancos más antiguos de Chile', offices: 'más de 200 sucursales a lo largo de Chile' },
  'bancoestado': { name: 'BancoEstado', desc: 'el banco estatal más grande de Chile con más de 3 millones de clientes', fact: 'Tiene la red de cajeros automáticos más extensa del país', offices: 'más de 350 sucursales en todo Chile' },
  'bci': { name: 'BCI', desc: 'uno de los bancos más innovadores de Chile con más de 1.5 millones de clientes', fact: 'Fue pionero en Chile con la banca digital y la app móvil', offices: 'más de 150 sucursales en Chile' },
  'santander': { name: 'Santander', desc: 'un banco internacional con fuerte presencia en Chile y más de 1.3 millones de clientes', fact: 'Santander fue el primer banco en Chile en ofrecer transferencias internacionales desde su app', offices: 'más de 120 sucursales en Chile' },
  'scotiabank': { name: 'Scotiabank', desc: 'un banco canadiense con presencia en Chile y más de 800 mil clientes', fact: 'Scotiabank opera con presencia en más de 50 países a nivel global', offices: 'más de 60 sucursales en Chile' },
  'itau': { name: 'Itaú', desc: 'el banco más grande de América Latina con presencia en Chile', fact: 'Itaú fue pionero en Chile con su programa de puntos LATAM Pass', offices: 'más de 80 sucursales en Chile' },
  'bice': { name: 'BICE', desc: 'un banco chileno con más de 40 años de experiencia', fact: 'BICE se destaca por su atención personalizada a cada cliente', offices: '20 sucursales en las principales ciudades de Chile' },
  'security': { name: 'Security', desc: 'un banco chileno especializado en banca privada y empresas', fact: 'Security se enfoca en clientes de altos ingresos con cupos preferenciales', offices: '30 sucursales en Chile' },
  'bbva': { name: 'BBVA', desc: 'un banco español con presencia en Chile', fact: 'BBVA tiene alianza con las principales aerolíneas del mundo', offices: 'más de 70 sucursales en Chile' },
};

const CARDS = {
  'visa-gold': 'Visa Gold', 'visa-platinum': 'Visa Platinum', 'visa-signature': 'Visa Signature',
  'mastercard-gold': 'Mastercard Gold', 'mastercard-black': 'Mastercard Black',
  'mastercard-platinum': 'Mastercard Platinum', 'amex': 'American Express',
  'cmr': 'CMR Falabella', 'ripley': 'Ripley', 'falabella': 'Falabella', 'lider': 'Líder BCI',
};

const CITIES = ['santiago','concepcion','valparaiso','vina-del-mar','temuco','rancagua','antofagasta',
  'la-serena','puerto-montt','iquique','arica','chillan','calama','copiapo','osorno','talca',
  'valdivia','punta-arenas','las-condes','providencia','maipu','la-florida','penalolen',
  'nunoa','vitacura','lo-barnechea','recoleta','independencia','san-miguel','el-bosque',
  'quilicura','cerro-navia','renca','quinta-normal','estacion-central','linares','san-fernando',
  'san-antonio','santa-cruz','pichilemu','villaricca','pucon','castro','ancud','quellon',
  'osorno','la-union','rio-bueno','frutillar','puerto-varas','llanquihue'];

const CITY_REGIONS = {
  'santiago':'rm','las-condes':'rm','providencia':'rm','nunoa':'rm','vitacura':'rm',
  'lo-barnechea':'rm','maipu':'rm','la-florida':'rm','penalolen':'rm','recoleta':'rm',
  'independencia':'rm','san-miguel':'rm','el-bosque':'rm','quilicura':'rm','cerro-navia':'rm',
  'renca':'rm','quinta-normal':'rm','estacion-central':'rm',
  'antofagasta':'norte','iquique':'norte','arica':'norte','calama':'norte','copiapo':'norte','la-serena':'norte',
  'valparaiso':'centro','vina-del-mar':'centro','rancagua':'centro','san-antonio':'centro',
  'talca':'centro','linares':'centro','san-fernando':'centro','santa-cruz':'centro','pichilemu':'centro',
  'concepcion':'sur','temuco':'sur','chillan':'sur','valdivia':'sur','osorno':'sur',
  'puerto-montt':'sur','punta-arenas':'sur','castro':'sur','ancud':'sur','quellon':'sur',
  'la-union':'sur','rio-bueno':'sur','frutillar':'sur','puerto-varas':'sur','llanquihue':'sur',
  'pucon':'sur','villaricca':'sur','los-angeles':'sur',
};

const FAQS = [
  { q: '¿Es legal vender cupo en dólares en Chile?', a: 'Sí. No existe ley que lo prohíba. Es un acuerdo entre privados. La CMF no lo regula. El único aspecto es contractual con tu banco (no penal).' },
  { q: '¿Piden claves bancarias?', a: 'Nunca. En ninguna etapa solicitamos claves, acceso a cuentas ni datos sensibles.' },
  { q: '¿Cuál es el monto mínimo?', a: '300 USD. No existe tope máximo; montos altos se evalúan directamente.' },
  { q: '¿Cuánto demora la transferencia?', a: 'Menos de 15 minutos tras confirmar el pago. Coordinamos todo por WhatsApp.' },
  { q: '¿Cómo pago la deuda en dólares al banco?', a: 'Dos opciones: (1) Pagar en dólares en caja o banca online antes del vencimiento. (2) Esperar a que el banco traspase la deuda a pesos al cupo nacional y pagarla en cuotas como deuda normal.' },
  { q: '¿Qué tarjetas aceptan?', a: 'Visa, Mastercard y American Express de bancos chilenos con cupo internacional activo.' },
  { q: '¿Atienden regiones?', a: 'Sí, 100% online por WhatsApp. Atendemos de Arica a Punta Arenas sin que te muevas.' },
  { q: '¿La cotización me compromete?', a: 'No. Es gratis y sin compromiso. Recibes la tasa exacta y decides.' },
  { q: '¿Qué pasa si mi tarjeta está bloqueada?', a: 'Debes abonar al cupo nacional hasta dejar mínimo disponible; el banco desbloquea el cupo en dólares automáticamente.' },
  { q: '¿Cómo detectar estafas al vender cupo?', a: 'Señales rojas: piden claves bancarias, no tienen oficina física ni dirección verificable, no tienen WhatsApp de empresa verificado, prometen tasas irreales (>90%), no tienen años de trayectoria comprobable.' },
  { q: '¿Cómo pago la deuda en dólares al banco?', a: 'Dos opciones: (1) Pagas en dólares en caja/online antes del vencimiento. (2) Esperas a que el banco traspase la deuda a pesos al cupo nacional y la pagas en cuotas como deuda normal.' },
  { q: '¿Atienden fines de semana?', a: 'Solo días hábiles: Lunes a Viernes 9:00–18:00 hrs. Fuera de horario, la cotización llega el siguiente día hábil.' },
  { q: '¿Tienen oficina física?', a: 'Sí, Vitacura 7181. Atención solo con cita previa agendada por WhatsApp. La mayoría opera 100% remoto.' },
  { q: '¿Puedo usar tarjeta virtual?', a: 'Sí, si tiene cupo internacional activo y no está bloqueada.' },
  { q: '¿Atienden empresas o montos altos?', a: 'Sí. Sin tope máximo. Montos altos se evalúan con atención personalizada directa.' },
];

// ========== HELPERS ==========

function slugToTitle(s) {
  return s.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function detectBank(slug) {
  for (const [key, data] of Object.entries(BANK_DATA)) {
    if (slug.includes(key)) return { key, ...data };
  }
  return null;
}

function detectCity(slug) {
  for (const c of CITIES) {
    if (slug.includes(c)) return c;
  }
  return null;
}

function detectCardType(slug) {
  for (const [key, name] of Object.entries(CARDS)) {
    if (slug.includes(key)) return name;
  }
  return null;
}

function getRegionCity(slug) {
  for (const [city, region] of Object.entries(CITY_REGIONS)) {
    if (slug.includes(city)) return { city, region };
  }
  return null;
}

function generateMeta(slug) {
  const parts = slug.split('/');
  const lastPart = parts[parts.length - 1] || slug;
  const bank = detectBank(lastPart);
  const cardType = detectCardType(lastPart);

  if (bank) {
    const citySlug = detectCity(lastPart);
    const cityName = citySlug ? (CITY_NAMES[citySlug] || slugToTitle(citySlug)) : '';
    const base = cityName ? ` en ${cityName}` : '';
    return {
      title: `Cupo Dólar ${bank.name}${base} | DolarExpress`,
      description: cityName
        ? `¿Tenés tarjeta ${bank.name} en ${cityName} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.fact}.`
        : `¿Tenés tarjeta ${bank.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.fact}.`,
    };
  }

  if (cardType) {
    return {
      title: `Cupo Dólar ${cardType} a Pesos | DolarExpress`,
      description: `¿Tenés tarjeta ${cardType} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.`,
    };
  }

  if (lastPart.startsWith('avance')) {
    return {
      title: slugToTitle(lastPart) + ' | DolarExpress',
      description: `¿Necesitás ${slugToTitle(lastPart).toLowerCase()}? Te compramos tu cupo en dólares y te transferimos al instante.`,
    };
  }

  const citySlugGen = detectCity(lastPart);
  const cityNameGen = citySlugGen ? (CITY_NAMES[citySlugGen] || slugToTitle(citySlugGen)) : '';

  if (lastPart === 'vender-cupo-dolar') {
    return {
      title: 'Vender Cupo Dólar: Recibe 85% en Efectivo Hoy | DolarExpress',
      description: 'Convierte tu cupo en dólares a pesos al 85% real. Transferencia inmediata, sin trámites bancarios, 100% online. 5.000+ clientes. Cotiza gratis.'
    };
  }

  if (citySlugGen && lastPart.startsWith('vender-cupo-dolar')) {
    return {
      title: `Vender Cupo Dólar en ${cityNameGen} | DolarExpress`,
      description: `¿Necesitás vender tu cupo en dólares en ${cityNameGen}? Te lo compramos al instante. Transferencia en 15 minutos a tu cuenta bancaria. Seguro y 100% online.`,
    };
  }
  if (citySlugGen) {
    return {
      title: slugToTitle(lastPart) + ' | DolarExpress',
      description: `¿Tenés cupo en dólares en ${cityNameGen}? Te lo compramos al instante. Transferencia en 15 minutos. Proceso 100% online.`,
    };
  }
  return {
    title: slugToTitle(lastPart) + ' | DolarExpress',
    description: `Compramos tu cupo en dólares en Chile. Transferencia inmediata y segura.`,
  };
}

function generateContent(slug) {
  const bank = detectBank(slug);
  const citySlug = detectCity(slug);
  const cityName = citySlug ? (CITY_NAMES[citySlug] || slugToTitle(citySlug)) : 'tu ciudad';
  const cardType = detectCardType(slug);

if (slug === 'vender-cupo-dolar') {
    return {
      paragraph1: '¿Cuánto cupo tienes en dólares?',
      paragraph2: `<div class="trust-badges" style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
        <span class="badge" style="background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);color:var(--accent);padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;">7 años operando en Chile</span>
        <span class="badge" style="background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);color:var(--accent);padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;">Oficina física: Vitacura 7181</span>
        <a href="https://g.page/r/CeL7poVEHhfOEBM/review" target="_blank" rel="noopener" class="badge" style="background:rgba(66,183,42,0.15);border:1px solid rgba(66,183,42,0.3);color:#42b72a;padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;">★ 4.9 Ver reseñas en Google</a>
      </div>
      <div class="calculator" style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:24px;margin:24px 0;text-align:center;">
        <label style="display:block;font-weight:600;margin-bottom:12px;color:var(--text);font-size:15px;">Tu cupo en USD <span style="font-weight:400;color:var(--muted);font-size:12px;">(mín. 300 USD)</span></label>
        <input type="number" id="cupo-usd" min="300" step="100" placeholder="Ej: 500" style="width:100%;max-width:240px;padding:14px 16px;border-radius:10px;border:1px solid rgba(148,163,184,0.4);background:rgba(15,23,42,0.9);color:var(--text);font-size:18px;margin-bottom:20px;text-align:center;">
        <div style="font-size:22px;font-weight:700;color:var(--accent);margin-bottom:8px;">Recibirías: <span id="resultado-clp">$0 CLP</span></div>
        <div style="font-size:13px;color:var(--muted);margin-bottom:20px;">Tasa incluye spread bancario + comisión 15%</div>
        <a href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo%20en%20d%C3%B3lares" class="btn-wa" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 28px;border-radius:999px;background:linear-gradient(to right,var(--wa),#128C7E);color:#f9fafb;font-size:15px;font-weight:700;border:none;cursor:pointer;box-shadow:0 12px 30px rgba(5,150,105,0.65),0 0 0 1px rgba(6,95,70,0.7);text-decoration:none;white-space:nowrap;">Cotizar mi cupo ahora</a>
        <p style="font-size:13px;color:var(--muted);margin-top:16px;">+X.XXX operaciones procesadas • Clientes 100% anónimos</p>
      </div>
      <div class="commission-note" style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:20px;margin:24px 0;text-align:center;">
        <p style="font-size:14px;font-weight:600;color:var(--accent);margin:0 0 8px;">Comisión fija 15%</p>
        <p style="font-size:13px;color:var(--muted);margin:0;">Incluye procesadores, bancos y riesgo cambiario. Sin costos ocultos.</p>
      </div>
      <div class="map-container" style="aspect-ratio:16/9;border-radius:12px;overflow:hidden;margin:24px 0;border:1px solid rgba(148,163,184,0.2);border-radius:12px;overflow:hidden;">
        <iframe data-src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3328.123!2d-70.592!3d-33.387!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9662c5f0e5b5c5c5%3A0x123456789abcdef!2sVitacura%207181!5e0!3m2!1ses!2scl!4v1692000000000" style="width:100%;height:100%;border:0;border-radius:12px;" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
      <div class="trust-stats" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:center;margin:24px 0;padding:20px;background:rgba(212,175,55,0.05);border-radius:12px;border:1px solid rgba(212,175,55,0.15);">
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">7</div><div style="font-size:12px;color:var(--muted);">años operando</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">X.XXX</div><div style="font-size:12px;color:var(--muted);">operaciones</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:#42b72a;">4.9</div><div style="font-size:12px;color:var(--muted);">★ Google</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">300</div><div style="font-size:12px;color:var(--muted);">USD mínimo</div></div>
      </div>
      <h2 style="margin-top:32px;margin-bottom:16px;font-size:20px;">¿Por qué elegir DolarExpress para vender tu cupo?</h2>
      <ul class="list" style="margin:16px 0;padding-left:20px;">
        <li><strong>Comisión fija 15%</strong> — Incluye procesadores, bancos y riesgo cambiario. Sin costos ocultos.</li>
        <li><strong>Transferencia < 15 min</strong> — A tu CuentaRUT o cuenta corriente, coordinado por WhatsApp.</li>
        <li><strong>Sin claves bancarias</strong> — Nunca pedimos claves ni acceso a tus cuentas.</li>
        <li><strong>Todos los bancos y retail</strong> — Visa, Mastercard, Amex de Banco Chile, Estado, Santander, BCI, Falabella, Ripley, París, Líder, Hites, La Polar, ABC, Easy, Jumbo, etc.</        <li><strong>Sin avance habilitado</strong> — Usamos tu cupo de compras internacional, no el avance en efectivo.</li>
        <li><strong>7 años operando</strong> — Oficina física en Vitacura 7181, +X.XXX operaciones, 4.9★ en Google.</li>
      </ul>
      <h3 style="margin-top:24px;margin-bottom:12px;">Bancos y retail que aceptamos</h3>
      <div class="pill-row" style="margin-bottom:24px;">
        <span class="pill"><strong>Bancos:</strong> Banco Chile, Estado, Santander, BCI, Scotiabank, Itaú, BICE, Security, BBVA, BICE, Consorcio, Falabella, Ripley, París, Líder, Hites, La Polar, ABC, Easy, Jumbo, CMR, Ripley, Líder BCI, Coopeuch, Tenpo, Cencosud, La Polar, Spin Cruz Verde, AbcVisa</span>
      </div>
      <h3 style="margin-top:24px;margin-bottom:12px;">¿Cómo funciona?</h3>
      <ol class="list" style="margin:16px 0;padding-left:20px;">
        <li><strong>1. Cotizá</strong> — Ingresá tu monto en USD en la calculadora y te decimos cuánto recibís en pesos al 85%.</li>
        <li><strong>2. Validación</strong> — Te pedimos una foto del saldo de tu tarjeta (cupo nacional e internacional) y validamos tu identidad por WhatsApp.</li>
        <li><strong>3. Pago</strong> — Transferencia a tu CuentaRUT o cuenta corriente en menos de 15 minutos.</      </ol>`,
      tip: 'Comisión fija 15% (incluye procesadores, bancos y riesgo cambiario). Sin costos ocultos. Mínimo 300 USD. Oficina: Vitacura 7181. 7 años operando. Clientes 100% anónimos.'
    };
  }

  if (slug === 'avance-cupo-dolares') {
    return {
      paragraph1: '¿Necesitas avance de cupo en dólares?',
      paragraph2: `<div class="trust-badges" style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
        <span class="badge" style="background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);color:var(--accent);padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;">7 años operando en Chile</span>
        <span class="badge" style="background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);color:var(--accent);padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;">Oficina física: Vitacura 7181</span>
        <a href="https://g.page/r/CeL7poVEHhfOEBM/review" target="_blank" rel="noopener" class="badge" style="background:rgba(66,183,42,0.15);border:1px solid rgba(66,183,42,0.3);color:#42b72a;padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;">★ 4.9 Ver reseñas en Google</a>
      </div>
      <div class="calculator" style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:24px;margin:24px 0;text-align:center;">
        <label style="display:block;font-weight:600;margin-bottom:12px;color:var(--text);font-size:15px;">Tu cupo en USD <span style="font-weight:400;color:var(--muted);font-size:12px;">(mín. 300 USD)</span></label>
        <input type="number" id="cupo-usd" min="300" step="100" placeholder="Ej: 500" style="width:100%;max-width:240px;padding:14px 16px;border-radius:10px;border:1px solid rgba(148,163,184,0.4);background:rgba(15,23,42,0.9);color:var(--text);font-size:18px;margin-bottom:20px;text-align:center;">
        <div style="font-size:22px;font-weight:700;color:var(--accent);margin-bottom:8px;">Recibirías: <span id="resultado-clp">$0 CLP</span></div>
        <div style="font-size:13px;color:var(--muted);margin-bottom:20px;">Tasa incluye spread bancario + comisión 15%</div>
        <a href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20avance%20de%20cupo%20en%20d%C3%B3lares" class="btn-wa" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 28px;border-radius:999px;background:linear-gradient(to right,var(--wa),#128C7E);color:#f9fafb;font-size:15px;font-weight:700;border:none;cursor:pointer;box-shadow:0 12px 30px rgba(5,150,105,0.65),0 0 0 1px rgba(6,95,70,0.7);text-decoration:none;white-space:nowrap;">Cotizar mi avance ahora</a>
        <p style="font-size:13px;color:var(--muted);margin-top:16px;">+X.XXX operaciones procesadas • Clientes 100% anónimos</p>
      </div>
      <div class="commission-note" style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:20px;margin:24px 0;text-align:center;">
        <p style="font-size:14px;font-weight:600;color:var(--accent);margin:0 0 8px;">Comisión fija 15%</p>
        <p style="font-size:13px;color:var(--muted);margin:0;">Incluye procesadores, bancos y riesgo cambiario. Sin costos ocultos.</p>
      </div>
      <div class="map-container" style="aspect-ratio:16/9;border-radius:12px;overflow:hidden;margin:24px 0;border:1px solid rgba(148,163,184,0.2);border-radius:12px;overflow:hidden;">
        <iframe data-src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3328.123!2d-70.592!3d-33.387!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9662c5f0e5b5c5c5%3A0x123456789abcdef!2sVitacura%207181!5e0!3m2!1ses!2scl!4v1692000000000" style="width:100%;height:100%;border:0;border-radius:12px;" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
      <div class="trust-stats" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:center;margin:24px 0;padding:20px;background:rgba(212,175,55,0.05);border-radius:12px;border:1px solid rgba(212,175,55,0.15);">
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">7</div><div style="font-size:12px;color:var(--muted);">años operando</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">X.XXX</div><div style="font-size:12px;color:var(--muted);">operaciones</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:#42b72a;">4.9</div><div style="font-size:12px;color:var(--muted);">★ Google</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">300</div><div style="font-size:12px;color:var(--muted);">USD mínimo</div></div>
      </div>
      <h2 style="margin-top:32px;margin-bottom:16px;font-size:20px;">¿Por qué elegir DolarExpress para tu avance de cupo?</h2>
      <ul class="list" style="margin:16px 0;padding-left:20px;">
        <li><strong>Comisión fija 15%</strong> — Incluye procesadores, bancos y riesgo cambiario. Sin costos ocultos.</li>
        <li><strong>Transferencia < 15 min</strong> — A tu CuentaRUT o cuenta corriente, coordinado por WhatsApp.</li>
        <li><strong>Sin claves bancarias</strong> — Nunca pedimos claves ni acceso a tus cuentas.</li>
        <li><strong>Todos los bancos y retail</strong> — Visa, Mastercard, Amex de Banco Chile, Estado, Santander, BCI, Falabella, Ripley, París, Líder, Hites, La Polar, ABC, Easy, Jumbo, etc.</        <li><strong>Sin avance habilitado</strong> — Usamos tu cupo de compras internacional, no el avance en efectivo.</li>
        <li><strong>7 años operando</strong> — Oficina física en Vitacura 7181, +X.XXX operaciones, 4.9★ en Google.</li>
      </ul>
      <h3 style="margin-top:24px;margin-bottom:12px;">Bancos y retail que aceptamos</h3>
      <div class="pill-row" style="margin-bottom:24px;">
        <span class="pill"><strong>Bancos:</strong> Banco Chile, Estado, Santander, BCI, Scotiabank, Itaú, BICE, Security, BBVA, BICE, Consorcio, Falabella, Ripley, París, Líder, Hites, La Polar, ABC, Easy, Jumbo, CMR, Ripley, Líder BCI, Coopeuch, Tenpo, Cencosud, La Polar, Spin Cruz Verde, AbcVisa</span>
      </div>
      <h3 style="margin-top:24px;margin-bottom:12px;">¿Cómo funciona el avance de cupo?</h3>
      <ol class="list" style="margin:16px 0;padding-left:20px;">
        <li><strong>1. Cotizá</strong> — Ingresá tu monto en USD en la calculadora y te decimos cuánto recibís en pesos al 85%.</li>
        <li><strong>2. Validación</strong> — Te pedimos una foto del saldo de tu tarjeta (cupo nacional e internacional) y validamos tu identidad por WhatsApp.</li>
        <li><strong>3. Pago</strong> — Transferencia a tu CuentaRUT o cuenta corriente en menos de 15 minutos.</li>
      </ol>`,
      tip: 'Comisión fija 15% (incluye procesadores, bancos y riesgo cambiario). Sin costos ocultos. Mínimo 300 USD. Oficina: Vitacura 7181. 7 años operando. Clientes 100% anónimos.'
    };
  }

  if (slug === 'cupo-en-dolares') {
    return {
      paragraph1: '¿Cuánto cupo en dólares tienes?',
      paragraph2: `<div class="trust-badges" style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
        <span class="badge" style="background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);color:var(--accent);padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;">7 años operando en Chile</span>
        <span class="badge" style="background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);color:var(--accent);padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;">Oficina física: Vitacura 7181</span>
        <a href="https://g.page/r/CeL7poVEHhfOEBM/review" target="_blank" rel="noopener" class="badge" style="background:rgba(66,183,42,0.15);border:1px solid rgba(66,183,42,0.3);color:#42b72a;padding:8px 16px;border-radius:999px;font-weight:600;font-size:13px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;">★ 4.9 Ver reseñas en Google</a>
      </div>
      <div class="calculator" style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:24px;margin:24px 0;text-align:center;">
        <label style="display:block;font-weight:600;margin-bottom:12px;color:var(--text);font-size:15px;">Tu cupo en USD <span style="font-weight:400;color:var(--muted);font-size:12px;">(mín. 300 USD)</span></label>
        <input type="number" id="cupo-usd" min="300" step="100" placeholder="Ej: 500" style="width:100%;max-width:240px;padding:14px 16px;border-radius:10px;border:1px solid rgba(148,163,184,0.4);background:rgba(15,23,42,0.9);color:var(--text);font-size:18px;margin-bottom:20px;text-align:center;">
        <div style="font-size:22px;font-weight:700;color:var(--accent);margin-bottom:8px;">Recibirías: <span id="resultado-clp">$0 CLP</span></div>
        <div style="font-size:13px;color:var(--muted);margin-bottom:20px;">Tasa incluye spread bancario + comisión 15%</div>
        <a href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20convertir%20mi%20cupo%20en%20d%C3%B3lares" class="btn-wa" style="display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 28px;border-radius:999px;background:linear-gradient(to right,var(--wa),#128C7E);color:#f9fafb;font-size:15px;font-weight:700;border:none;cursor:pointer;box-shadow:0 12px 30px rgba(5,150,105,0.65),0 0 0 1px rgba(6,95,70,0.7);text-decoration:none;white-space:nowrap;">Cotizar mi cupo ahora</a>
        <p style="font-size:13px;color:var(--muted);margin-top:16px;">+X.XXX operaciones procesadas • Clientes 100% anónimos</p>
      </div>
      <div class="commission-note" style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:20px;margin:24px 0;text-align:center;">
        <p style="font-size:14px;font-weight:600;color:var(--accent);margin:0 0 8px;">Comisión fija 15%</p>
        <p style="font-size:13px;color:var(--muted);margin:0;">Incluye procesadores, bancos y riesgo cambiario. Sin costos ocultos.</p>
      </div>
      <div class="map-container" style="aspect-ratio:16/9;border-radius:12px;overflow:hidden;margin:24px 0;border:1px solid rgba(148,163,184,0.2);border-radius:12px;overflow:hidden;">
        <iframe data-src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3328.123!2d-70.592!3d-33.387!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9662c5f0e5b5c5c5%3A0x123456789abcdef!2sVitacura%207181!5e0!3m2!1ses!2scl!4v1692000000000" style="width:100%;height:100%;border:0;border-radius:12px;" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
      <div class="trust-stats" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:center;margin:24px 0;padding:20px;background:rgba(212,175,55,0.05);border-radius:12px;border:1px solid rgba(212,175,55,0.15);">
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">7</div><div style="font-size:12px;color:var(--muted);">años operando</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">X.XXX</div><div style="font-size:12px;color:var(--muted);">operaciones</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:#42b72a;">4.9</div><div style="font-size:12px;color:var(--muted);">★ Google</div></div>
        <div style="text-align:center;"><div style="font-size:24px;font-weight:700;color:var(--accent);">300</div><div style="font-size:12px;color:var(--muted);">USD mínimo</div></div>
      </div>
      <h2 style="margin-top:32px;margin-bottom:16px;font-size:20px;">¿Por qué elegir DolarExpress para tu cupo en dólares?</h2>
      <ul class="list" style="margin:16px 0;padding-left:20px;">
        <li><strong>Comisión fija 15%</strong> — Incluye procesadores, bancos y riesgo cambiario. Sin costos ocultos.</li>
        <li><strong>Transferencia < 15 min</strong> — A tu CuentaRUT o cuenta corriente, coordinado por WhatsApp.</li>
        <li><strong>Sin claves bancarias</strong> — Nunca pedimos claves ni acceso a tus cuentas.</li>
        <li><strong>Todos los bancos y retail</strong> — Visa, Mastercard, Amex de Banco Chile, Estado, Santander, BCI, Falabella, Ripley, París, Líder, Hites, La Polar, ABC, Easy, Jumbo, etc.</        <li><strong>Sin avance habilitado</strong> — Usamos tu cupo de compras internacional, no el avance en efectivo.</li>
        <li><strong>7 años operando</strong> — Oficina física en Vitacura 7181, +X.XXX operaciones, 4.9★ en Google.</li>
      </ul>
      <h3 style="margin-top:24px;margin-bottom:12px;">Bancos y retail que aceptamos</h3>
      <div class="pill-row" style="margin-bottom:24px;">
        <span class="pill"><strong>Bancos:</strong> Banco Chile, Estado, Santander, BCI, Scotiabank, Itaú, BICE, Security, BBVA, BICE, Consorcio, Falabella, Ripley, París, Líder, Hites, La Polar, ABC, Easy, Jumbo, CMR, Ripley, Líder BCI, Coopeuch, Tenpo, Cencosud, La Polar, Spin Cruz Verde, AbcVisa</span>
      </div>
      <h3 style="margin-top:24px;margin-bottom:12px;">¿Cómo funciona?</h3>
      <ol class="list" style="margin:16px 0;padding-left:20px;">
        <li><strong>1. Cotizá</strong> — Ingresá tu monto en USD en la calculadora y te decimos cuánto recibís en pesos al 85%.</li>
        <li><strong>2. Validación</strong> — Te pedimos una foto del saldo de tu tarjeta (cupo nacional e internacional) y validamos tu identidad por WhatsApp.</li>
        <li><strong>3. Pago</strong> — Transferencia a tu CuentaRUT o cuenta corriente en menos de 15 minutos.</li>
      </ol>`,
      tip: 'Comisión fija 15% (incluye procesadores, bancos y riesgo cambiario). Sin costos ocultos. Mínimo 300 USD. Oficina: Vitacura 7181. 7 años operando. Clientes 100% anónimos.'
    };
  }

  if (bank) {
    return {
      paragraph1: `${bank.name} es ${bank.desc}. ${bank.fact}. Si tenés una tarjeta de crédito de ${bank.name} con cupo internacional disponible en ${cityName}, nosotros te lo compramos al instante. El proceso es 100% online y no requiere que vayas a ninguna sucursal.`,
      paragraph2: `${bank.name} cuenta con ${bank.offices}. Si estás en ${cityName}, podés coordinar la operación completamente por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta en menos de 15 minutos.`,
      tip: `Dato de ${bank.name}: ${bank.fact}. Muchos clientes nos prefieren porque no necesitan ir al banco ni hacer filas.`,
    };
  }

  if (cardType) {
    return {
      paragraph1: `¿Tenés una tarjeta ${cardType} en ${cityName}? Nosotros te compramos el cupo en dólares al mejor tipo de cambio. El proceso es simple y rápido, sin papeleos ni trámites complicados.`,
      paragraph2: `Las tarjetas ${cardType} tienen cupo internacional disponible para compras en el extranjero. Ese mismo cupo podés convertirlo a pesos chilenos con nosotros. Te transferimos a tu cuenta en minutos.`,
      tip: `¿Sabías que muchas tarjetas como ${cardType} permiten usar el cupo internacional sin tener que activarlo? Verificá en tu app bancaria si tenés cupo disponible.`,
    };
  }

  if (citySlug) {
    return {
      paragraph1: `¿Estás en ${cityName} y querés vender tu cupo en dólares? En DolarExpress te compramos el cupo internacional de tu tarjeta de crédito al mejor tipo de cambio. El proceso es 100% online desde ${cityName}, sin moverte de tu casa.`,
      paragraph2: `Coordinamos todo por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta bancaria en menos de 15 minutos. No importa si estás en el centro de ${cityName} o en cualquier otra comuna, el proceso es el mismo: rápido, seguro y sin papeleos.`,
      tip: `En ${cityName}, muchas personas ya vendieron su cupo en dólares con nosotros. La mayoría de las tarjetas Visa y Mastercard emitidas en Chile tienen cupo internacional disponible sin necesidad de activación. Verificá en tu app bancaria.`,
    };
  }

  return {
    paragraph1: 'En DolarExpress te ofrecemos la solución más rápida y segura para convertir tu cupo en dólares a pesos chilenos. Olvidate de los trámites bancarios tradicionales, las filas y los papeleos.',
    paragraph2: 'Trabajamos con todas las tarjetas de crédito chilenas: bancarias (Banco Chile, Santander, BCI, Scotiabank, Itaú, Security, BICE, BancoEstado) y retail (CMR Falabella, Ripley, Líder BCI, Cencosud, Paris, Jumbo, Easy, Hites, La Polar, ABC Din, Johnson).',
    tip: 'Muchas tarjetas retail como CMR, Ripley o Líder NO tienen avance en efectivo disponible. Nosotros usamos tu cupo de compras para darte efectivo al instante.',
  };
}

function getRelatedPages(allPages, slug) {
  const regionInfo = getRegionCity(slug);
  if (regionInfo) {
    const sameRegion = Object.entries(CITY_REGIONS)
      .filter(([c, r]) => r === regionInfo.region && c !== regionInfo.city)
      .map(([c]) => c);
    return allPages.filter(p => {
      const c = detectCity(p.slug);
      return c && sameRegion.includes(c);
    }).slice(0, 6);
  }
  const slugLower = slug.toLowerCase();
  const isBank = Object.keys(BANK_DATA).some(k => slugLower.includes(k));
  if (isBank) {
    return allPages.filter(p => p.slug.startsWith('cupo-dolar-') && !p.slug.includes('/')).slice(0, 6);
  }
  return [];
}

const CSS = `
:root{--accent:#d4af37;--text:#f9fafb;--muted:#9ca3af;--wa:#25D366;}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:radial-gradient(circle at top,#111827 0,#020617 55%,#000 100%);color:var(--text);min-height:100vh;display:flex;flex-direction:column;}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
header{border-bottom:1px solid rgba(31,41,55,0.9);backdrop-filter:blur(14px);background:radial-gradient(circle at top left,rgba(212,175,55,0.08),transparent 55%),linear-gradient(to right,rgba(15,23,42,0.96),rgba(3,7,18,0.98));position:sticky;top:0;z-index:20;}
.nav{max-width:960px;margin:0 auto;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;}
.logo{display:inline-flex;align-items:center;gap:10px;font-weight:700;letter-spacing:0.04em;text-transform:uppercase;color:var(--text);}
.logo-mark{width:32px;height:32px;border-radius:999px;background:radial-gradient(circle at 30% 20%,#facc15,#d4af37 40%,#854d0e 100%);display:inline-flex;align-items:center;justify-content:center;color:#020617;font-weight:900;font-size:18px;box-shadow:0 0 0 1px rgba(0,0,0,0.6),0 16px 40px rgba(0,0,0,0.8);}
.logo-sub{font-size:11px;color:var(--muted);text-transform:none;letter-spacing:0.02em;}
.badge{font-size:11px;padding:3px 8px;border-radius:999px;border:1px solid rgba(148,163,184,0.7);color:var(--muted);display:inline-flex;align-items:center;gap:4px;}
.badge-dot{width:6px;height:6px;border-radius:999px;background:#22c55e;box-shadow:0 0 0 4px rgba(34,197,94,0.25);}
.breadcrumb{max-width:960px;margin:0 auto;padding:10px 16px;font-size:12px;color:var(--muted);}
main{flex:1;max-width:960px;width:100%;margin:0 auto;padding:24px 16px 40px;display:grid;grid-template-columns:minmax(0,3fr) minmax(280px,2fr);gap:28px;}
@media(max-width:800px){main{grid-template-columns:minmax(0,1fr)}header{position:static}}
.card{background:radial-gradient(circle at top left,rgba(148,163,184,0.12),transparent 55%),linear-gradient(to bottom right,rgba(15,23,42,0.96),rgba(2,6,23,0.98));border-radius:18px;border:1px solid rgba(148,163,184,0.25);box-shadow:0 22px 60px rgba(2,6,23,0.85);padding:22px 20px;position:relative;overflow:hidden;}
.card::before{content:"";position:absolute;inset:-2px;background:radial-gradient(circle at top,rgba(212,175,55,0.2),transparent 60%);opacity:0.8;pointer-events:none;mix-blend-mode:soft-light;}
.card-inner{position:relative;z-index:1;}
.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:0.16em;color:var(--muted);display:inline-flex;align-items:center;gap:6px;margin-bottom:8px;}
.eyebrow-line{width:22px;height:1px;background:linear-gradient(to right,transparent,rgba(148,163,184,0.8));}
h1{font-size:clamp(22px,3vw,28px);margin:0 0 8px;letter-spacing:-0.03em;}
.highlight{color:var(--accent);}
.lead{color:var(--muted);font-size:14px;line-height:1.6;margin:0 0 16px;max-width:460px;}
.pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px;}
.pill{font-size:11px;padding:4px 9px;border-radius:999px;border:1px solid rgba(148,163,184,0.4);color:var(--muted);background:radial-gradient(circle at top left,rgba(15,23,42,0.9),rgba(3,7,18,0.95));display:inline-flex;align-items:center;gap:4px;}
.pill strong{color:var(--text);font-weight:600;}
.metrics{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:22px;}
.metric-item{padding:10px 12px;border-radius:12px;border:1px solid rgba(31,41,55,0.9);background:radial-gradient(circle at top left,rgba(15,23,42,0.9),rgba(3,7,18,0.98));min-width:140px;}
.metric-label{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:2px;}
.metric-value{font-size:15px;color:var(--text);font-weight:600;}
.metric-sub{font-size:11px;color:var(--muted);}
.cta-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:10px;}
.btn-wa{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 18px;border-radius:999px;background:linear-gradient(to right,var(--wa),#128C7E);color:#f9fafb;font-size:14px;font-weight:600;border:none;cursor:pointer;box-shadow:0 12px 30px rgba(5,150,105,0.65),0 0 0 1px rgba(6,95,70,0.7);text-decoration:none;white-space:nowrap;}
.btn-outline{display:inline-flex;align-items:center;padding:9px 14px;border-radius:999px;border:1px solid rgba(148,163,184,0.9);background:radial-gradient(circle at top left,rgba(15,23,42,0.96),rgba(3,7,18,0.98));color:var(--muted);font-size:12px;text-decoration:none;}
.cta-note{font-size:11px;color:var(--muted);margin-bottom:16px;}
.section-title{font-size:13px;text-transform:uppercase;letter-spacing:0.16em;color:var(--muted);margin:22px 0 6px;}
.list{margin:0;padding-left:18px;font-size:13px;color:var(--muted);line-height:1.7;}
.list li+li{margin-top:4px;}
.faq{margin-top:12px;font-size:13px;color:var(--muted);}
.faq dt{font-weight:600;color:var(--text);margin-top:8px;margin-bottom:2px;}
.faq dd{margin:0 0 6px;}
.related{margin-top:20px;}
.related-title{font-size:12px;text-transform:uppercase;letter-spacing:0.12em;color:var(--muted);margin-bottom:8px;}
.related-links{display:flex;flex-wrap:wrap;gap:6px;}
.related-links a{font-size:11px;padding:4px 8px;border-radius:999px;border:1px solid rgba(148,163,184,0.3);color:var(--muted);background:rgba(15,23,42,0.8);}
.related-links a:hover{background:rgba(212,175,55,0.15);color:var(--accent);border-color:var(--accent);}
.side-card{background:radial-gradient(circle at top right,rgba(212,175,55,0.16),transparent 60%),linear-gradient(to bottom,rgba(15,23,42,0.98),rgba(3,7,18,0.98));border-radius:18px;border:1px solid rgba(148,163,184,0.3);padding:18px 16px;box-shadow:0 18px 50px rgba(2,6,23,0.95);position:sticky;top:68px;align-self:flex-start;}
.side-title{font-size:14px;font-weight:600;margin:0 0 4px;}
.side-sub{font-size:12px;color:var(--muted);margin:0 0 12px;}
.side-list{margin:0 0 10px;padding:0;list-style:none;font-size:12px;color:var(--muted);}
.side-list li{display:flex;align-items:center;gap:6px;margin-bottom:6px;}
.side-dot{width:6px;height:6px;border-radius:999px;background:var(--accent);box-shadow:0 0 0 3px rgba(212,175,55,0.25);}
footer{border-top:1px solid rgba(31,41,55,0.9);background:linear-gradient(to bottom,rgba(15,23,42,0.98),rgba(2,6,23,0.98));padding:14px 16px;font-size:12px;color:var(--muted);}
.footer-inner{max-width:960px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;}
.footer-links{display:flex;flex-wrap:wrap;gap:10px;}
`;

function escapeHtml(s) {
  return s.replace(/[&<>"]/g, function(m) {
    if (m === '&') return '&amp;';
    if (m === '<') return '&lt;';
    if (m === '>') return '&gt;';
    if (m === '"') return '&quot;';
    return m;
  });
}

function buildFAQJson() {
  return FAQS.map(f => JSON.stringify({
    '@type': 'Question',
    name: f.q,
    acceptedAnswer: { '@type': 'Answer', text: f.a }
  })).join(',');
}

function buildPage(slug, meta, content) {
  const title = meta.title.replace(' | DolarExpress', '');
  const canonical = slug.startsWith('/') ? `https://dolarexpress.cl${slug}` : `https://dolarexpress.cl/${slug}`;
  const waText = `Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20${encodeURIComponent(title)}`;
  const waUrl = `https://wa.me/56967658939?text=${waText}`;

  const breadcrumbJson = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Inicio', item: 'https://dolarexpress.cl/' },
      { '@type': 'ListItem', position: 2, name: title, item: canonical }
    ]
  });

  // Schema mejorado para vender-cupo-dolar
  const isVenderCupo = slug === 'vender-cupo-dolar';
  const localBizJson = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': ['FinancialService', 'LocalBusiness'],
    name: 'DolarExpress',
    url: 'https://dolarexpress.cl',
    telephone: '+56967658939',
    description: meta.description,
    areaServed: { '@type': 'Country', name: 'Chile' },
    priceRange: '$$',
    contactPoint: { '@type': 'ContactPoint', telephone: '+56967658939', contactType: 'customer service', availableLanguage: 'es' },
    ...(isVenderCupo ? {
      address: {
        '@type': 'PostalAddress',
        streetAddress: 'Vitacura 7181',
        addressLocality: 'Vitacura',
        addressRegion: 'Región Metropolitana',
        addressCountry: 'CL'
      },
      geo: {
        '@type': 'GeoCoordinates',
        latitude: -33.387,
        longitude: -70.592
      },
      hasMap: 'https://g.page/r/CeL7poVEHhfOEBM/review',
      aggregateRating: {
        '@type': 'AggregateRating',
        ratingValue: '4.9',
        reviewCount: '100',
        bestRating: '5'
      }
    } : {})
  });

  const faqJson = buildFAQJson();
  const faqHtml = FAQS.map(f => `<dt>${escapeHtml(f.q)}</dt><dd>${escapeHtml(f.a)}</dd>`).join('');

  return `<!doctype html>
<html lang="es">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18216577738"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-18216577738');
</script>
<meta charset="utf-8">
<title>${escapeHtml(meta.title)}</title>
<meta name="description" content="${escapeHtml(meta.description)}">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="${canonical}" />
<meta property="og:title" content="${escapeHtml(meta.title)}">
<meta property="og:description" content="${escapeHtml(meta.description)}">
<meta property="og:url" content="${canonical}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://dolarexpress.cl/og-image.svg">
<meta property="og:locale" content="es_CL">
<meta property="og:site_name" content="DolarExpress">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${escapeHtml(meta.title)}">
<meta name="twitter:description" content="${escapeHtml(meta.description)}">
<meta name="twitter:image" content="https://dolarexpress.cl/og-image.svg">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[${localBizJson},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":"https://dolarexpress.cl/"},{"@type":"ListItem","position":2,"name":"${escapeHtml(title)}","item":"${canonical}"}]},{"@type":"FAQPage","mainEntity":[${faqJson}]}]}
</script>
<style>${CSS}</style>
</head>
<body>
<header>
  <div class="nav">
    <a href="/" class="logo">
      <span class="logo-mark">$</span>
      <span>DolarExpress<div class="logo-sub">Compra de cupo en dólares</div></span>
    </a>
    <a href="${waUrl}" class="btn-wa">Cotizar por WhatsApp</a>
  </div>
</header>

<nav class="breadcrumb" aria-label="Breadcrumb">
  <a href="/">Inicio</a> / <span>${escapeHtml(title)}</span>
</nav>

<main>
  <div class="card">
    <div class="card-inner">
      <div class="eyebrow"><span class="eyebrow-line"></span>CUPO DÓLAR</div>
      <h1>${escapeHtml(title)}</h1>
      <p class="lead">${escapeHtml(meta.description)}</p>
      <div class="metrics">
        <div class="metric-item"><div class="metric-label">Transferencia</div><div class="metric-value">&lt; 15 min</div><div class="metric-sub">a tu cuenta</div></div>
        <div class="metric-item"><div class="metric-label">Proceso</div><div class="metric-value">100% Online</div><div class="metric-sub">por WhatsApp</div></div>
        <div class="metric-item"><div class="metric-label">Tasa</div><div class="metric-value">Mejor del día</div><div class="metric-sub">sin comisión</div></div>
      </div>
      <div class="cta-row">
        <a href="${waUrl}" class="btn-wa">Cotizar por WhatsApp</a>
      </div>
    </div>
  </div>

  <div class="side-card">
    <h2 class="side-title">¿Por qué DolarExpress?</h2>
    <p class="side-sub">La forma más rápida de vender tu cupo en dólares</p>
    <ul class="side-list">
      <li><span class="side-dot"></span>Transferencia en 15 min</li>
      <li><span class="side-dot"></span>Sin consulta DICOM</li>
      <li><span class="side-dot"></span>Sin aval ni papeles</li>
      <li><span class="side-dot"></span>Mejor tasa del mercado</li>
      <li><span class="side-dot"></span>100% online y seguro</li>
    </ul>
    <a href="${waUrl}" class="btn-wa" style="width:100%;text-align:center;">Vender Ahora</a>
  </div>

  <div class="card" style="grid-column:1/-1;">
    <div class="card-inner">
      <h2 style="margin-top:0;font-size:18px;">${escapeHtml(title)}</h2>
      <p style="font-size:14px;line-height:1.7;color:var(--muted);">${escapeHtml(meta.description)}</p>
      <p style="font-size:14px;line-height:1.7;color:var(--muted);">${escapeHtml(content.paragraph1)}</p>
      <div style="font-size:14px;line-height:1.7;color:var(--muted);">${slug === 'vender-cupo-dolar' ? content.paragraph2 : escapeHtml(content.paragraph2)}</div>

      <h3 style="font-size:15px;margin-top:24px;margin-bottom:12px;">¿Cómo funciona?</h3>
      <ul class="list">
        <li><strong>1. Cotizá</strong> — Enviános el monto de tu cupo por WhatsApp y te decimos cuánto recibís</li>
        <li><strong>2. Validación</strong> — Verificamos tu cupo sin pedir claves ni datos bancarios</li>
        <li><strong>3. Pago</strong> — Transferencia a tu CuentaRUT o cuenta corriente en menos de 15 minutos</li>
      </ul>

      <div style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:14px;margin:20px 0;">
        <p style="font-size:13px;color:var(--muted);margin:0;"><strong style="color:var(--accent);">💡 ¿Sabías que...?</strong><br>${escapeHtml(content.tip)}</p>
      </div>

      <h3 style="font-size:15px;margin-top:24px;margin-bottom:12px;">Preguntas Frecuentes</h3>
      <dl class="faq">${faqHtml}</dl>
    </div>
  </div>
</main>

  <footer>
    <div class="footer-inner">
      <span>&copy; ${new Date().getFullYear()} DolarExpress</span>
      <div class="footer-links">
        <a href="/">Inicio</a>
        <a href="/directorio-general">Directorio</a>
        <a href="/preguntas-frecuentes">FAQ</a>
        <a href="/contacto">Contacto</a>
        <a href="/privacidad">Privacidad</a>
      </div>
    </div>
  </footer>

  ${slug === 'vender-cupo-dolar' ? `
  <script>
    // Calculadora interactiva
    const input = document.getElementById('cupo-usd');
    const result = document.getElementById('resultado-clp');
    if (input && result) {
      input.addEventListener('input', function() {
        const usd = parseFloat(this.value) || 0;
        const clp = Math.round(usd * 960 * 0.85);
        result.textContent = '$' + clp.toLocaleString('es-CL') + ' CLP';
      });
    }

    // Lazy-load Google Maps
    const mapIframe = document.querySelector('.map-container iframe');
    if (mapIframe) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const iframe = entry.target;
            if (iframe.dataset.src && !iframe.src) {
              iframe.src = iframe.dataset.src;
            }
            observer.unobserve(iframe);
          }
        });
      }, { rootMargin: '100px' });
      observer.observe(mapIframe);
    }
  </script>` : ''}

  <a href="${waUrl}" target="_blank" rel="noopener noreferrer"
   style="position:fixed;bottom:20px;right:20px;z-index:50;background:#25D366;width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;box-shadow:0 8px 24px rgba(37,211,102,0.4);"
   aria-label="Contactar por WhatsApp">
  <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 16 16">
    <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
  </svg>
</a>
</body>
</html>`;
}

// ========== MAIN ==========

function parsePseoPages() {
  const filePath = path.join(__dirname, 'src/data/pseo-data.ts');
  const content = fs.readFileSync(filePath, 'utf-8');
  const pages = [];
  const lines = content.split(/\r?\n/);
  let current = {};

  for (const line of lines) {
    const slugMatch = line.match(/^\s+slug:\s*'(.+?)'/);
    if (slugMatch) {
      current.slug = slugMatch[1];
    }
    const titleMatch = line.match(/^\s+title:\s*'(.+?)'/);
    if (titleMatch) {
      current.title = titleMatch[1];
    }
    const descMatch = line.match(/^\s+description:\s*'(.+?)'/);
    if (descMatch) {
      current.description = descMatch[1];
    }
    if (line.trim().match(/^\},?$/) && current.slug) {
      pages.push({ ...current });
      current = {};
    }
  }

  return pages;
}

function generate() {
  const pseoPages = parsePseoPages();
  console.log(`📖 Leídas ${pseoPages.length} páginas de pseo-data.ts`);

  let generated = 0;
  let error = 0;

  for (const page of pseoPages) {
    try {
      const meta = generateMeta(page.slug);
      const content = generateContent(page.slug);
      const html = buildPage(page.slug, meta, content);

      const slug = page.slug;
      // public/{slug}/index.html
      const outDir = path.join(PUBLIC_DIR, slug);
      fs.mkdirSync(outDir, { recursive: true });
      fs.writeFileSync(path.join(outDir, 'index.html'), html, 'utf-8');

      // public/{slug}.html for compat
      fs.writeFileSync(path.join(PUBLIC_DIR, slug + '.html'), html, 'utf-8');

      generated++;
    } catch (e) {
      error++;
      if (error <= 5) console.error(`❌ Error en ${page.slug}: ${e.message}`);
    }
  }

  console.log(`✅ Generadas ${generated} páginas. Errores: ${error}`);
}

generate();
