import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── Replicate PSEOPage.tsx data & logic ─────────────────────
const BANK_DATA = {
  'banco-chile': { name: 'Banco de Chile', desc: 'el banco más grande del país con más de 2 millones de clientes', fact: 'Fue fundado en 1893 y es uno de los bancos más antiguos de Chile', offices: 'más de 200 sucursales a lo largo de Chile' },
  'banco-estado': { name: 'BancoEstado', desc: 'el banco estatal más grande de Chile con más de 3 millones de clientes', fact: 'Tiene la red de cajeros automáticos más extensa del país', offices: 'más de 350 sucursales en todo Chile' },
  'bci': { name: 'BCI', desc: 'uno de los bancos más innovadores de Chile con más de 1.5 millones de clientes', fact: 'Fue pionero en Chile con la banca digital y la app móvil', offices: 'más de 150 sucursales en Chile' },
  'santander': { name: 'Santander', desc: 'un banco internacional con fuerte presencia en Chile y más de 1.3 millones de clientes', fact: 'Santander fue el primer banco en Chile en ofrecer transferencias internacionales desde su app', offices: 'más de 120 sucursales en Chile' },
  'scotiabank': { name: 'Scotiabank', desc: 'un banco canadiense con presencia en Chile y más de 800 mil clientes', fact: 'Scotiabank opera con presencia en más de 50 países a nivel global', offices: 'más de 60 sucursales en Chile' },
  'itau': { name: 'Itaú', desc: 'el banco más grande de América Latina con presencia en Chile', fact: 'Itaú fue pionero en Chile con su programa de puntos LATAM Pass', offices: 'más de 80 sucursales en Chile' },
  'bice': { name: 'BICE', desc: 'un banco chileno con más de 40 años de experiencia', fact: 'BICE se destaca por su atención personalizada a cada cliente', offices: '20 sucursales en las principales ciudades de Chile' },
  'security': { name: 'Security', desc: 'un banco chileno especializado en banca privada y empresas', fact: 'Security se enfoca en clientes de altos ingresos con cupos preferenciales', offices: '30 sucursales en Chile' },
  'bbva': { name: 'BBVA', desc: 'un banco español con presencia en Chile', fact: 'BBVA tiene alianza con las principales aerolíneas del mundo', offices: 'más de 70 sucursales en Chile' },
  'cmr': { name: 'CMR Falabella', desc: 'la tarjeta retail más grande de Chile', fact: 'CMR es aceptada en más de 100 mil comercios en todo Chile', offices: 'tiendas Falabella en todo Chile' },
  'ripley': { name: 'Ripley', desc: 'un retail chileno con programa de puntos Duoc', fact: 'Ripley tiene más de 1.2 millones de tarjetahabientes', offices: 'tiendas Ripley en principales ciudades' },
  'paris': { name: 'Paris', desc: 'un retail del grupo Falabella', fact: 'Paris tiene promociones exclusivas en tiendas departamentales', offices: 'tiendas Paris en centros comerciales' },
  'lider': { name: 'Líder BCI', desc: 'la tarjeta del supermercado más grande de Chile', fact: 'Líder BCI pertenece al grupo Walmart Chile', offices: 'supermercados Líder en todo Chile' },
  'hites': { name: 'Hites', desc: 'un retail chileno especializado en crédito', fact: 'Hites se caracteriza por su fácil aprobación de crédito', offices: 'tiendas Hites en zonas céntricas' },
  'jumbo': { name: 'Jumbo', desc: 'la cadena de supermercados premium de Falabella', fact: 'Jumbo ofrece productos de alta calidad y marcas internacionales', offices: 'tiendas Jumbo en sectores premium' },
  'easy': { name: 'Easy', desc: 'un retail especializado en mejoramiento del hogar', fact: 'Easy pertenece al grupo Falabella', offices: 'tiendas Easy en principales ciudades' },
  'la-polar': { name: 'La Polar', desc: 'un retail chileno con más de 80 años de historia', fact: 'La Polar fue fundada en 1938 y es una institución en el retail chileno', offices: 'tiendas La Polar en Chile' },
  'abc-din': { name: 'ABC Din', desc: 'un retail de crédito fácil y accesible', fact: 'ABC Din es conocida por su rápida aprobación de crédito', offices: 'tiendas ABC Din en zonas comerciales' },
};

const cityNames = {
  'santiago': 'Santiago', 'concepcion': 'Concepción', 'valparaiso': 'Valparaíso',
  'vina-del-mar': 'Viña del Mar', 'temuco': 'Temuco', 'rancagua': 'Rancagua',
  'antofagasta': 'Antofagasta', 'la-serena': 'La Serena', 'puerto-montt': 'Puerto Montt',
  'iquique': 'Iquique', 'arica': 'Arica', 'chillan': 'Chillán', 'calama': 'Calama',
  'copiapo': 'Copiapó', 'osorno': 'Osorno', 'talca': 'Talca', 'valdivia': 'Valdivia',
  'punta-arenas': 'Punta Arenas', 'las-condes': 'Las Condes', 'providencia': 'Providencia',
  'nunoa': 'Ñuñoa', 'vitacura': 'Vitacura', 'lo-barnechea': 'Lo Barnechea', 'maipu': 'Maipú',
  'la-florida': 'La Florida', 'penalolen': 'Peñalolén', 'san-miguel': 'San Miguel',
  'quilicura': 'Quilicura', 'recoleta': 'Recoleta', 'independencia': 'Independencia',
  'el-bosque': 'El Bosque', 'cerro-navia': 'Cerro Navia', 'renca': 'Renca',
  'quinta-normal': 'Quinta Normal', 'estacion-central': 'Estación Central',
  'linares': 'Linares', 'san-fernando': 'San Fernando', 'san-antonio': 'San Antonio',
  'santa-cruz': 'Santa Cruz', 'pichilemu': 'Pichilemu', 'villaricca': 'Villarrica',
  'pucon': 'Pucón', 'castro': 'Castro', 'ancud': 'Ancud', 'quellon': 'Quellón',
  'la-union': 'La Unión', 'rio-bueno': 'Río Bueno', 'frutillar': 'Frutillar',
  'puerto-varas': 'Puerto Varas', 'llanquihue': 'Llanquihue', 'curico': 'Curicó',
  'coquimbo': 'Coquimbo', 'los-angeles': 'Los Ángeles',
};

const CARD_MAP = {
  'visa-classic': 'Visa Classic', 'visa-gold': 'Visa Gold', 'visa-platinum': 'Visa Platinum',
  'visa-signature': 'Visa Signature', 'mastercard-gold': 'Mastercard Gold',
  'mastercard-black': 'Mastercard Black', 'mastercard-platinum': 'Mastercard Platinum',
  'american-express': 'American Express', 'amex': 'American Express',
};

function detectItem(slug, map) {
  for (const [key, data] of Object.entries(map)) {
    if (slug.includes(key)) return { key, data };
  }
  return null;
}

function detectCity(slug) {
  const slugs = Object.keys(cityNames);
  const longFirst = [...slugs].sort((a, b) => b.length - a.length);
  for (const c of longFirst) {
    if (slug.includes(c)) return c;
  }
  return null;
}

function detectCardType(slug) {
  const longFirst = [...Object.keys(CARD_MAP)].sort((a, b) => b.length - a.length);
  for (const key of longFirst) {
    if (slug.includes(key)) return CARD_MAP[key];
  }
  const extra = { 'cmr': 'CMR Falabella', 'ripley': 'Ripley', 'falabella': 'Falabella', 'lider': 'Líder BCI' };
  for (const [k, n] of Object.entries(extra)) {
    if (slug.includes(k)) return n;
  }
  return null;
}

function slugToTitle(s) {
  return s.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function buildMeta(slug) {
  const bank = detectItem(slug, BANK_DATA);
  const citySlug = detectCity(slug);
  const cityName = citySlug ? (cityNames[citySlug] || slugToTitle(citySlug)) : '';
  const cardType = detectCardType(slug);

  if (bank) {
    const base = cityName ? ` en ${cityName}` : '';
    if (slug.startsWith('vender')) return {
      title: `Vender Cupo Dólar ${bank.data.name}${base} | DolarExpress`,
      description: cityName ? `Vendé tu cupo en dólares de ${bank.data.name} en ${cityName}. Transferencia inmediata y segura. ${bank.data.fact}.` : `Vendé tu cupo en dólares de ${bank.data.name}. Transferencia inmediata y segura. ${bank.data.fact}.`,
    };
    return {
      title: `Cupo Dólar ${bank.data.name}${base} | DolarExpress`,
      description: cityName ? `¿Tenés tarjeta ${bank.data.name} en ${cityName} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.data.fact}.` : `¿Tenés tarjeta ${bank.data.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.data.fact}.`,
    };
  }
  if (cardType) {
    const base = cityName ? ` en ${cityName}` : '';
    return { title: `Cupo Dólar ${cardType}${base} | DolarExpress`, description: `¿Tenés tarjeta ${cardType}${base} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.` };
  }
  if (slug.startsWith('avance')) {
    return {
      title: `${slugToTitle(slug)} | DolarExpress`,
      description: `¿Necesitás ${slugToTitle(slug).toLowerCase()}${cityName ? ` en ${cityName}` : ''}? Te compramos tu cupo en dólares y te transferimos al instante.`,
    };
  }
  if (slug.startsWith('vender')) {
    return {
      title: `${slugToTitle(slug)} | DolarExpress`,
      description: `¿Necesitás ${slugToTitle(slug).toLowerCase()}${cityName ? ` en ${cityName}` : ''}? Te compramos tu cupo en dólares al instante. Transferencia en 15 minutos.`,
    };
  }
  if (slug.startsWith('vender')) {
    const base = cityName ? ` en ${cityName}` : '';
    return { title: `${slugToTitle(slug)}${base} | DolarExpress`, description: `¿Necesitás ${slugToTitle(slug).toLowerCase()}${base}? Te compramos tu cupo en dólares al instante. Transferencia en 15 minutos.` };
  }
  if (cityName) return { title: `Cupo Dólar en ${cityName} | DolarExpress`, description: `¿Tenés cupo en dólares en ${cityName}? Te lo compramos al instante. Transferencia en 15 minutos. Proceso 100% online.` };
  return { title: `${slugToTitle(slug)} | DolarExpress`, description: 'Compramos tu cupo en dólares en Chile. Transferencia inmediata y segura.' };
}

function buildContent(slug) {
  const bank = detectItem(slug, BANK_DATA);
  const citySlug = detectCity(slug);
  const cityName = citySlug ? (cityNames[citySlug] || slugToTitle(citySlug)) : 'tu ciudad';
  const cardType = detectCardType(slug);

  if (bank) return {
    p1: `${bank.data.name} es ${bank.data.desc}. ${bank.data.fact}. Si tenés una tarjeta de crédito de ${bank.data.name} con cupo internacional disponible en ${cityName}, nosotros te lo compramos al instante.`,
    p2: `${bank.data.name} cuenta con ${bank.data.offices}. Si estás en ${cityName}, podés coordinar la operación completamente por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta en menos de 15 minutos.`,
    tip: `Dato de ${bank.data.name}: ${bank.data.fact}. Muchos clientes nos prefieren por la rapidez y seguridad del proceso.`,
  };
  if (cardType) return {
    p1: `¿Tenés una tarjeta ${cardType} en ${cityName}? Nosotros te compramos el cupo en dólares al mejor tipo de cambio. El proceso es simple y rápido, sin papeleos ni trámites complicados.`,
    p2: `Las tarjetas ${cardType} tienen cupo internacional disponible para compras en el extranjero. Ese mismo cupo podés convertirlo a pesos chilenos con nosotros. Te transferimos a tu cuenta en minutos.`,
    tip: `¿Sabías que muchas tarjetas como ${cardType} permiten usar el cupo internacional sin tener que activarlo? Verificá en tu app bancaria si tenés cupo disponible.`,
  };
  if (citySlug) return {
    p1: `¿Estás en ${cityName} y querés vender tu cupo en dólares? En DolarExpress te compramos el cupo internacional de tu tarjeta de crédito al mejor tipo de cambio. El proceso es 100% online desde ${cityName}, sin moverte de tu casa.`,
    p2: `Coordinamos todo por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta bancaria en menos de 15 minutos. No importa si estás en ${cityName}, el proceso es rápido, seguro y sin papeleos.`,
    tip: `En ${cityName}, muchas personas ya vendieron su cupo en dólares con nosotros. La mayoría de las tarjetas tienen cupo internacional disponible sin necesidad de activación.`,
  };
  return {
    p1: 'En DolarExpress te ofrecemos la solución más rápida y segura para convertir tu cupo en dólares a pesos chilenos. Olvidate de los trámites bancarios tradicionales.',
    p2: 'Trabajamos con todas las tarjetas de crédito chilenas: bancarias y retail. Te transferimos en 15 minutos.',
    tip: 'Muchas tarjetas retail NO tienen avance en efectivo disponible. Nosotros usamos tu cupo de compras para darte efectivo al instante.',
  };
}

// ── HTML template ────────────────────────────────────────────
const CSS = `
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#0f172a;color:#f1f5f9;min-height:100vh;display:flex;flex-direction:column}
a{color:#d4af37;text-decoration:none}
header{background:linear-gradient(135deg,#0f172a,#1e293b);border-bottom:1px solid #334155;padding:12px 16px;position:sticky;top:0;z-index:10}
.nav{max-width:960px;margin:0 auto;display:flex;align-items:center;justify-content:space-between}
.logo{font-weight:700;font-size:18px;color:#f1f5f9}
.logo span{color:#d4af37}
.breadcrumb{max-width:960px;margin:0 auto;padding:10px 16px;font-size:13px;color:#94a3b8}
.breadcrumb a{color:#d4af37}
main{flex:1;max-width:960px;margin:0 auto;padding:32px 16px;width:100%}
.card{background:linear-gradient(135deg,#1e293b,#0f172a);border-radius:16px;border:1px solid #334155;padding:24px}
h1{font-size:28px;margin-bottom:12px;line-height:1.3}
h1 span{color:#d4af37}
.lead{color:#94a3b8;font-size:15px;line-height:1.6;margin-bottom:16px}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}
.pill{font-size:12px;padding:4px 10px;border-radius:999px;border:1px solid #475569;color:#94a3b8}
.btn-wa{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:999px;background:linear-gradient(135deg,#25D366,#128C7E);color:#fff;font-weight:600;font-size:15px;margin:12px 0}
.btn-wa:hover{opacity:.9}
h2{font-size:20px;margin:20px 0 8px;color:#d4af37}
p{color:#94a3b8;font-size:14px;line-height:1.7;margin-bottom:12px}
ul{padding-left:20px;color:#94a3b8;font-size:14px;line-height:1.8;margin-bottom:16px}
.tip{background:rgba(212,175,55,.1);border:1px solid rgba(212,175,55,.3);border-radius:12px;padding:16px;margin:16px 0;color:#f1f5f9;font-size:14px}
.tip strong{color:#d4af37}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:20px 0}
.step{background:#1e293b;border-radius:10px;padding:16px;border:1px solid #334155}
.step h3{color:#d4af37;font-size:15px;margin-bottom:4px}
.step p{font-size:13px;margin:0}
.related{margin-top:24px}
.related a{display:inline-block;font-size:12px;color:#d4af37;border:1px solid rgba(212,175,55,.3);padding:4px 10px;border-radius:999px;margin:3px}
footer{background:#0f172a;border-top:1px solid #334155;padding:16px;text-align:center;font-size:12px;color:#64748b}
`;

function generateHTML(slug, title, description) {
  const meta = buildMeta(slug);
  const content = buildContent(slug);
  const displayTitle = meta.title.replace(' | DolarExpress', '');
  const waText = `Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20${encodeURIComponent(displayTitle)}`;

  return `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${meta.title}</title>
<meta name="description" content="${meta.description}">
<link rel="canonical" href="https://dolarexpress.cl/${slug}" />
<meta property="og:title" content="${meta.title}">
<meta property="og:description" content="${meta.description}">
<meta property="og:url" content="https://dolarexpress.cl/${slug}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://dolarexpress.cl/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FinancialService","name":"${meta.title}","description":"${meta.description}","url":"https://dolarexpress.cl/${slug}","provider":{"@type":"Organization","name":"DolarExpress","url":"https://dolarexpress.cl"},"areaServed":{"@type":"Country","name":"CL"}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":"https://dolarexpress.cl"},{"@type":"ListItem","position":2,"name":"${meta.title}","item":"https://dolarexpress.cl/${slug}"}]}
</script>
<style>${CSS}</style>
</head>
<body>
<header>
  <div class="nav">
    <a href="/" class="logo">Dolar<span>Express</span></a>
    <a href="https://wa.me/56967658939?text=${waText}" target="_blank" rel="noopener" style="color:#d4af37;font-size:13px;font-weight:600">Vender Cupo</a>
  </div>
</header>
<div class="breadcrumb"><a href="/">Inicio</a> › ${displayTitle}</div>
<main>
  <div class="card">
    <h1><span>${displayTitle}</span></h1>
    <p class="lead">${meta.description}</p>
    <div class="pills"><span class="pill">Transferencia 15 min</span><span class="pill">Tasa del mercado</span><span class="pill">100% online</span></div>
    <a class="btn-wa" href="https://wa.me/56967658939?text=${waText}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
    
    <h2>¿Cómo funciona?</h2>
    <p>${content.p1}</p>
    <p>${content.p2}</p>

    <div class="steps">
      <div class="step"><h3>1. Cotizá</h3><p>Contactanos por WhatsApp y te mostramos la mejor tasa.</p></div>
      <div class="step"><h3>2. Validación</h3><p>Procesamos tu solicitud de forma segura.</p></div>
      <div class="step"><h3>3. Pago</h3><p>Recibís la transferencia en 15 minutos.</p></div>
    </div>

    <h2>¿Por qué elegir DolarExpress?</h2>
    <ul>
      <li><strong>Transferencia en 15 minutos:</strong> El dinero llega al instante a tu cuenta.</li>
      <li><strong>Sin Dicom ni aval:</strong> Solo necesitás cupo disponible en tu tarjeta.</li>
      <li><strong>100% online:</strong> Todo desde tu celular, sin sucursales.</li>
      <li><strong>Mejor tasa del mercado:</strong> Te mostramos la tasa antes de aceptar.</li>
      <li><strong>Seguro y transparente:</strong> Miles de operaciones realizadas.</li>
    </ul>

    <div class="tip"><strong>💡 ¿Sabías que...?</strong><br>${content.tip}</div>

    <div class="related">
      <p><strong>Servicios relacionados:</strong></p>
      <a href="/venta-cupo-dolares">Venta de Cupo</a>
      <a href="/cupo-dolar-banco-chile">Banco de Chile</a>
      <a href="/cupo-dolar-santander">Santander</a>
      <a href="/cupo-dolar-bci">BCI</a>
      <a href="/vender-cupo-dolar-santiago">Santiago</a>
      <a href="/vender-cupo-dolar-concepcion">Concepción</a>
    </div>

    <a class="btn-wa" href="https://wa.me/56967658939?text=${waText}" target="_blank" rel="noopener">Cotizar por WhatsApp</a>
  </div>
</main>
<footer>DolarExpress &copy; ${new Date().getFullYear()} · Especialistas en compra de cupo en dólares · <a href="/privacidad">Privacidad</a> · <a href="/contacto">Contacto</a></footer>
</body>
</html>`;
}

// ── Main ─────────────────────────────────────────────────────
const pseoPath = path.join(__dirname, 'src', 'data', 'pseo-data.ts');
const publicDir = path.join(__dirname, 'public');
const content = fs.readFileSync(pseoPath, 'utf8');

const force = process.argv.includes('--force');

// Parse slug, title, description from the data file
const entries = [];
const regex = /slug: '([^']+)',\s*\n\s*title: '([^']+)',\s*\n\s*description: '([^']+)'/g;
let match;
while ((match = regex.exec(content)) !== null) {
  entries.push({ slug: match[1], title: match[2], description: match[3] });
}

console.log(`Generando HTML estático para ${entries.length} páginas...`);

let count = 0;
let skipped = 0;
for (const entry of entries) {
  const filePath = path.join(publicDir, `${entry.slug}.html`);
  if (!force && fs.existsSync(filePath)) {
    skipped++;
    continue;
  }
  const html = generateHTML(entry.slug, entry.title, entry.description);
  fs.writeFileSync(filePath, html, 'utf8');
  count++;
  if (count % 500 === 0) console.log(`  ${count} generadas...`);
}

console.log(`✅ Generadas ${count} páginas HTML estáticas en public/`);
if (!force) console.log(`   Omitidas ${skipped} (ya existían)`);
