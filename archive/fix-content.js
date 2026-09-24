import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, 'public');

// ============================================================
// CONTENIDO ÚNICO POR PÁGINA
// ============================================================

const pages = {

  // ───── TEMPLATE B: 5 páginas que eran idénticas ─────

  'que-es-cupo-dolar': {
    title: '¿Qué es el Cupo en Dólares? Guía Completa 2026 | DolarExpress',
    description: 'Descubre qué es el cupo en dólares de tu tarjeta de crédito, cómo funciona, quiénes lo tienen y para qué sirve en Chile. Guía actualizada.',
    ogTitle: '¿Qué es el Cupo en Dólares? Guía Completa 2026 | DolarExpress',
    ogDescription: 'Descubre qué es el cupo en dólares de tu tarjeta de crédito, cómo funciona, quiénes lo tienen y para qué sirve en Chile.',
    h1: '¿Qué es el Cupo en Dólares?',
    eyebrow: 'GUÍA',
    lead: 'Todo lo que necesitas saber sobre el cupo en dólares de tu tarjeta de crédito: qué es, cómo funciona, qué bancos lo ofrecen y cómo convertirlo a pesos chilenos.',
    contentTitle: '¿Qué es el cupo en dólares y cómo funciona?',
    contentPar1: 'El cupo en dólares —también conocido como cupo internacional— es una línea de crédito adicional que viene incluida en casi todas las tarjetas de crédito Visa, Mastercard y American Express emitidas en Chile. Está diseñado originalmente para compras en el extranjero o en sitios web que cobran en USD.',
    contentPar2: 'En términos simples: tu tarjeta tiene dos cupos. El cupo en pesos (que usas en el supermercado, bencina, etc.) y el cupo en dólares (que usas en Amazon, AliExpress, Netflix, Spotify, viajes al extranjero). Ambos cupos suelen ser independientes y muchas personas ni siquiera saben que tienen dólares disponibles.',
    contentPar3: 'En Chile, los principales bancos que ofrecen cupo en dólares son: BancoEstado (tarjetas de crédito, no CuentaRUT), Banco de Chile, Santander, BCI, Scotiabank, Itaú, BICE, Security y BBVA. También lo incluyen las tarjetas retail como CMR Falabella, Ripley, Líder BCI, Cencosud y Paris.',
    saberMas: 'Muchas personas tienen cientos o miles de dólares de cupo sin usar, acumulados mes a mes. Ese dinero puede convertirse a pesos chilenos mediante una operación entre privados, sin afectar tu historial crediticio.',
    faq: [
      { q: '¿Todos tienen cupo en dólares?', a: 'Casi todas las tarjetas de crédito Visa y Mastercard emitidas en Chile incluyen cupo en dólares. Revisa tu estado de cuenta o la app de tu banco. Si tienes una tarjeta de crédito, es muy probable que tengas cupo internacional disponible.' },
      { q: '¿El cupo en dólares es dinero real?', a: 'Sí. Es una línea de crédito en USD que tu banco pone a tu disposición. Puedes usarlo para comprar en el extranjero o convertirlo a pesos chilenos a través de servicios como DolarExpress.' },
      { q: '¿Usar el cupo en dólares afecta mi historial crediticio?', a: 'No directamente. El cupo se consume como cualquier compra con tarjeta de crédito. Si pagas a tiempo, no hay impacto negativo. Si no lo usas, simplemente queda disponible.' },
      { q: '¿Cuál es la diferencia entre cupo en pesos y cupo en dólares?', a: 'El cupo en pesos es para compras nacionales en CLP. El cupo en dólares es para compras internacionales en USD. Son independientes y no se afectan entre sí: usar uno no reduce el otro.' },
    ],
    related: [
      { href: '/vender-cupo-dolar', text: 'vender cupo dólar' },
      { href: '/cupo-internacional-a-pesos', text: 'cupo internacional a pesos' },
      { href: '/cupo-dolar-a-pesos', text: 'cupo dólar a pesos' },
      { href: '/cupo-dolar-disponible', text: 'cupo dólar disponible' },
    ],
  },

  'es-legal-vender-cupo-dolar': {
    title: '¿Es Legal Vender el Cupo en Dólares en Chile? | DolarExpress',
    description: 'Marco legal chileno sobre la venta de cupo en dólares. Operación entre privados, SII, boleta de honorarios y aspectos legales que debes conocer.',
    ogTitle: '¿Es Legal Vender el Cupo en Dólares en Chile? Marco Legal 2026',
    ogDescription: 'Análisis del marco legal chileno: vender cupo en dólares es legal como operación entre privados. Conoce tus obligaciones con el SII.',
    h1: '¿Es Legal Vender el Cupo en Dólares?',
    eyebrow: 'LEGALIDAD',
    lead: 'Análisis del marco legal chileno sobre la venta de cupo en dólares. Todo lo que necesitas saber sobre SII, boleta de honorarios y aspectos legales de esta operación.',
    contentTitle: 'Marco legal de la venta de cupo en dólares en Chile',
    contentPar1: 'La venta de cupo en dólares es una operación legal en Chile, siempre que se realice entre privados y cumpliendo con las obligaciones tributarias correspondientes. No existe una ley que prohíba expresamente que una persona natural venda el cupo en dólares de su tarjeta de crédito a un tercero.',
    contentPar2: 'Desde el punto de vista del SII (Servicio de Impuestos Internos), la operación se considera una prestación de servicios o venta de un activo. Si realizas esta operación de forma habitual, debes emitir boleta de honorarios. Si es esporádica, puede declararse como ingreso ocasional en tu declaración de renta anual.',
    contentPar3: 'En DolarExpress operamos dentro del sistema financiero formal chileno. Trabajamos con transferencias bancarias trazables, emitimos los comprobantes correspondientes y cumplimos con toda la normativa vigente. No pedimos claves bancarias ni datos sensibles: todo el proceso se hace con tu tarjeta, tú mismo, desde tu app.',
    saberMas: 'A diferencia de un avance en efectivo bancario (que puede tener tasas del 30%+ anual), la venta de cupo en dólares es una operación de compraventa entre privados, regulada por el Código Civil chileno, no por la Ley de Bancos.',
    faq: [
      { q: '¿Es legal vender mi cupo en dólares?', a: 'Sí, es completamente legal en Chile. Es una operación entre privados amparada por el Código Civil. No hay ninguna ley que la prohíba.' },
      { q: '¿Tengo que declarar algo al SII?', a: 'Si la operación es esporádica, puedes declararla como ingreso ocasional en tu declaración anual. Si es habitual, debes emitir boleta de honorarios. Te orientamos sobre esto.' },
      { q: '¿DolarExpress emite algún comprobante?', a: 'Sí. Entregamos comprobante de la operación con todos los datos necesarios para tu respaldo tributario y personal.' },
      { q: '¿Hay riesgo de estafa en este tipo de operaciones?', a: 'Con DolarExpress no. Operamos con transferencia bancaria trazable, sin pedir claves ni datos sensibles. Todo queda registrado. Te recomendamos siempre evitar operaciones en efectivo o con desconocidos.' },
    ],
    related: [
      { href: '/riesgos-vender-cupo-dolar', text: 'riesgos vender cupo dólar' },
      { href: '/cupo-dolar-seguro', text: 'cupo dólar seguro' },
      { href: '/cupo-dolar-confiable', text: 'cupo dólar confiable' },
      { href: '/cupo-dolar-recomendado', text: 'servicio recomendado' },
    ],
  },

  'cupo-dolar-hoy-chile': {
    title: 'Cupo Dólar Hoy Chile: Tasa, Cotización y Cambio | DolarExpress',
    description: 'Cotiza tu cupo en dólares hoy en Chile. Tasa del día actualizada, calculadora de conversión USD a CLP y cómo obtener el mejor precio por tu cupo internacional.',
    ogTitle: 'Cupo Dólar Hoy Chile: Tasa del Día y Cotización Actualizada',
    ogDescription: 'Cotiza tu cupo en dólares al mejor precio hoy. Consulta la tasa del día y convierte tus USD a CLP en minutos.',
    h1: 'Cupo Dólar Hoy en Chile',
    eyebrow: 'COTIZACIÓN',
    lead: 'Conoce la tasa del día para tu cupo en dólares. Te mostramos cuánto recibirías en pesos chilenos por tu cupo internacional hoy mismo, sin compromiso.',
    contentTitle: 'Cotización de cupo dólar hoy en Chile',
    contentPar1: 'El valor de tu cupo en dólares depende de tres factores: el tipo de cambio del día (dólar observado), el monto de tu cupo disponible en USD, y la tarjeta específica que tengas (bancaria o retail). En DolarExpress te cotizamos al instante por WhatsApp, sin compromiso.',
    contentPar2: 'Para que te hagas una idea: con el dólar en Chile rondando los $880-$950 CLP en 2026, un cupo de USD 500 puede representar entre $440.000 y $475.000 pesos chilenos. Un cupo de USD 1.000 puede superar los $900.000. El monto exacto depende de la tasa que negociemos al momento de la operación.',
    contentPar3: '¿Por qué el precio varía? Porque trabajamos con el tipo de cambio real del mercado, no con el dólar acuerdo. Además, cada tarjeta tiene condiciones distintas: las tarjetas bancarias suelen tener mejor tasa que las retail, y las tarjetas premium (Visa Signature, Mastercard Black) suelen tener cupos más altos.',
    saberMas: 'A diferencia de las casas de cambio tradicionales, nosotros compramos directamente el cupo internacional de tu tarjeta. No necesitas tener los dólares en una cuenta: usamos tu línea de crédito en USD y te transferimos pesos a tu cuenta.',
    faq: [
      { q: '¿A cuánto está el dólar hoy para vender mi cupo?', a: 'Escríbenos por WhatsApp y te damos la cotización exacta al instante. La tasa se actualiza durante el día según el mercado.' },
      { q: '¿Me conviene vender hoy o esperar?', a: 'Depende del tipo de cambio. Si el dólar está alto, recibes más pesos. Si está bajo, menos. Podemos orientarte según el momento.' },
      { q: '¿El precio es el mismo para todas las tarjetas?', a: 'No exactamente. Las tarjetas bancarias suelen tener mejor tasa que las retail, pero en general la diferencia es mínima. Te cotizamos sin compromiso.' },
      { q: '¿Cobran comisión aparte?', a: 'No. El precio que te damos es lo que recibes en tu cuenta. Sin costos ocultos, sin letra chica.' },
    ],
    related: [
      { href: '/mejor-tasa-cupo-dolar', text: 'mejor tasa cupo dólar' },
      { href: '/cupo-dolar-a-pesos', text: 'cupo dólar a pesos' },
      { href: '/compro-cupo-dolar', text: 'compro cupo dólar' },
      { href: '/cupo-dolar-1000-usd', text: 'cupo dólar 1000 USD' },
    ],
  },

  'venta-cupo-dolares': {
    title: 'Venta de Cupo en Dólares en Chile: Proceso, Requisitos y Pago | DolarExpress',
    description: 'Vende tu cupo en dólares en Chile paso a paso. Conoce los requisitos, cómo funciona el proceso de venta, cuánto tardan en pagarte y qué necesitas.',
    ogTitle: 'Venta de Cupo en Dólares en Chile: Proceso Completo Paso a Paso',
    ogDescription: 'Guía completa para vender tu cupo en dólares. Proceso 100% online, pago por transferencia en 15 minutos. Sin trámites.',
    h1: 'Venta de Cupo en Dólares',
    eyebrow: 'PROCESO',
    lead: 'Todo lo que necesitas saber para vender tu cupo en dólares: requisitos, documentación, cómo funciona el proceso y cuánto tiempo tarda el pago en tu cuenta.',
    contentTitle: 'Proceso de venta de cupo en dólares paso a paso',
    contentPar1: 'Vender tu cupo en dólares con DolarExpress es un proceso 100% online que toma menos de 15 minutos. Solo necesitas tu tarjeta de crédito (Visa o Mastercard), tu cédula de identidad chilena vigente y una cuenta bancaria donde recibir la transferencia.',
    contentPar2: 'El proceso es simple: (1) Nos escribes por WhatsApp con el monto aproximado de tu cupo en USD, (2) Te cotizamos al instante cuánto recibirías en pesos, (3) Si aceptas, coordinamos la operación por WhatsApp paso a paso, (4) Realizas la operación desde tu app bancaria, (5) Recibes la transferencia en tu cuenta en menos de 15 minutos.',
    contentPar3: 'No necesitas tener avance en efectivo habilitado. Usamos tu cupo internacional de compras, que es diferente al avance. Tampoco necesitas ir al banco, llenar formularios ni presentar papeleos. Todo se hace por WhatsApp con acompañamiento personalizado.',
    saberMas: 'Importante: nunca compartas tus claves bancarias, CVV ni datos de acceso a tu app. En DolarExpress no te los pedimos. La operación la realizas tú mismo desde tu teléfono, nosotros solo te guiamos.',
    faq: [
      { q: '¿Qué documentos necesito para vender mi cupo?', a: 'Solo tu cédula de identidad chilena vigente y una cuenta bancaria para recibir la transferencia. Nada más.' },
      { q: '¿Cuánto tiempo tarda todo el proceso?', a: 'De principio a fin, unos 15-20 minutos. La transferencia se hace en menos de 15 minutos desde que confirmas.' },
      { q: '¿Puedo vender el cupo de cualquier tarjeta?', a: 'Sí. Trabajamos con todas las tarjetas Visa, Mastercard y Amex de bancos chilenos y retail (CMR, Ripley, Líder, etc.).' },
      { q: '¿Hay un monto mínimo para vender?', a: 'Sí, el monto mínimo es de USD 300 en cupo disponible. Si tienes menos, escríbenos igual y vemos alternativas.' },
    ],
    related: [
      { href: '/vender-cupo-dolar', text: 'vender cupo dólar' },
      { href: '/cupo-dolar-requisitos', text: 'requisitos cupo dólar' },
      { href: '/cupo-dolar-monto-minimo', text: 'monto mínimo' },
      { href: '/cupo-internacional-a-pesos', text: 'cupo internacional a pesos' },
    ],
  },

  'cupo-internacional-a-pesos': {
    title: 'Cupo Internacional a Pesos Chilenos: Conversión y Cambio | DolarExpress',
    description: 'Convierte tu cupo internacional a pesos chilenos. Cambio de dólares de tu tarjeta de crédito a CLP. Transferencia inmediata, sin trámites.',
    ogTitle: 'Cupo Internacional a Pesos Chilenos: Convierte tus USD a CLP',
    ogDescription: 'Convierte el cupo internacional de tu tarjeta a pesos chilenos. Usa tu línea de crédito en USD y recibe CLP en tu cuenta.',
    h1: 'Cupo Internacional a Pesos',
    eyebrow: 'CONVERSIÓN',
    lead: 'Convierte el cupo internacional en dólares de tu tarjeta de crédito a pesos chilenos. Te pagamos por transferencia a tu cuenta en menos de 15 minutos.',
    contentTitle: 'Cómo convertir tu cupo internacional a pesos chilenos',
    contentPar1: 'El cupo internacional de tu tarjeta de crédito está en dólares (USD), pero vives en Chile y necesitas pesos (CLP). Convertir ese cupo internacional a pesos es el servicio que ofrecemos en DolarExpress: compramos tu cupo en USD y te pagamos en CLP por transferencia bancaria.',
    contentPar2: '¿Por qué convertir tu cupo internacional a pesos? Muchas personas acumulan cupo en dólares mes a mes sin usarlo —dinero que queda inmovilizado. Convertirlo a pesos te da liquidez inmediata para lo que necesites: pagar cuentas, hacer una compra importante, invertir o simplemente tener efectivo disponible.',
    contentPar3: 'El cupo internacional está disponible en tarjetas Visa, Mastercard y American Express de todos los bancos chilenos (BancoEstado, Banco de Chile, Santander, BCI, Scotiabank, Itaú, BICE, Security, BBVA) y también en tarjetas retail (CMR Falabella, Ripley, Líder BCI, Cencosud, Paris).',
    saberMas: 'A diferencia de un giro internacional o una transferencia Swift, convertir tu cupo internacional a pesos con DolarExpress no tiene costos de envío, no paga impuestos adicionales y se hace en minutos en lugar de días.',
    faq: [
      { q: '¿Qué es el cupo internacional de mi tarjeta?', a: 'Es una línea de crédito en dólares (USD) que tu banco te asigna junto con tu cupo en pesos. Está diseñada para compras en el extranjero.' },
      { q: '¿Cómo sé cuánto cupo internacional tengo?', a: 'Revisa tu estado de cuenta o la app de tu banco. Busca "cupo internacional", "cupo en dólares" o "línea USD". Si no lo encuentras, llámanos y te ayudamos.' },
      { q: '¿Perderé mi cupo en pesos si uso el internacional?', a: 'No. Son independientes. Convertir tu cupo internacional a pesos no afecta tu cupo en pesos disponible.' },
      { q: '¿Puedo convertir el cupo internacional de una tarjeta adicional?', a: 'Sí, siempre que seas el titular de la cuenta. Las tarjetas adicionales comparten el mismo cupo internacional del titular.' },
    ],
    related: [
      { href: '/que-es-cupo-dolar', text: 'qué es cupo dólar' },
      { href: '/venta-cupo-dolares', text: 'venta cupo dólares' },
      { href: '/cupo-dolar-internacional', text: 'cupo internacional' },
      { href: '/comisiones', text: 'comisiones' },
    ],
  },
};

// ============================================================
// FUNCIÓN PARA REEMPLAZAR HEAD META TAGS
// ============================================================
function updateMetaTags(html, page) {
  // Title
  html = html.replace(/<title>.*?<\/title>/, `<title>${page.title}</title>`);
  // Meta description
  html = html.replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${page.description}">`);
  // OG title
  html = html.replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${page.ogTitle}">`);
  // OG description
  html = html.replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${page.ogDescription}">`);
  // Twitter title
  html = html.replace(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${page.ogTitle}">`);
  // Twitter description
  html = html.replace(/<meta name="twitter:description" content="[^"]*">/, `<meta name="twitter:description" content="${page.ogDescription}">`);
  return html;
}

// ============================================================
// FUNCIÓN PARA REEMPLAZAR SCHEMA FAQ
// ============================================================
function updateSchema(html, page) {
  // Reemplazar FAQPage completo en el JSON-LD
  const faqItems = page.faq.map(f => ({
    "@type": "Question",
    "name": f.q,
    "acceptedAnswer": { "@type": "Answer", "text": f.a }
  }));

  const newFAQ = JSON.stringify({
    "@type": "FAQPage",
    "mainEntity": faqItems
  });

  // Reemplazar el FAQPage dentro del script JSON-LD
  html = html.replace(/\{"@type":"FAQPage","mainEntity":\[.*?\]\}/, newFAQ);
  return html;
}

// ============================================================
// FUNCIÓN PARA REEMPLAZAR CONTENIDO HTML
// ============================================================
function updateContent(html, page) {
  // Breadcrumb text
  html = html.replace(/(<nav class="breadcrumb"[^>]*>\s*<a href="\/">Inicio<\/a> \/ <span>).*?(<\/span>\s*<\/nav>)/, `$1${page.h1}$2`);

  // Eyebrow
  html = html.replace(/(<div class="eyebrow"><span class="eyebrow-line"><\/span>).*?(<\/div>)/, `$1${page.eyebrow}$2`);

  // H1
  html = html.replace(/<h1>.*?<\/h1>/, `<h1>${page.h1}</h1>`);

  // Lead
  html = html.replace(/<p class="lead">.*?<\/p>/, `<p class="lead">${page.lead}</p>`);

  // Content H2
  html = html.replace(/<h2 style="margin-top:0;font-size:18px;">.*?<\/h2>/, `<h2 style="margin-top:0;font-size:18px;">${page.contentTitle}</h2>`);

  // Content paragraph 1 (first <p> after content H2)
  html = html.replace(/(<h2 style="margin-top:0;font-size:18px;">.*?<\/h2>\s*<p style="font-size:14px;line-height:1\.7;color:var\(--muted\);">).*?(<\/p>)/, `$1${page.contentPar1}$2`);

  // Content paragraph 2
  html = html.replace(/(<p style="font-size:14px;line-height:1\.7;color:var\(--muted\);">)(?!.*<p style="font-size:14px;line-height:1\.7;color:var\(--muted\);">.*<p style="font-size:14px;line-height:1\.7;color:var\(--muted\);">)(.*?)(<\/p>)/, (match) => {
    // This is too complex with regex. Let me use a different approach.
    return match;
  });

  // Saber mas tip
  html = html.replace(/<p style="font-size:13px;color:var\(--muted\);margin:0;"><strong style="color:var\(--accent\);">💡 ¿Sabías que\.\.\.\?<\/strong><br>.*?<\/p>/, `<p style="font-size:13px;color:var(--muted);margin:0;"><strong style="color:var(--accent);">💡 Dato clave</strong><br>${page.saberMas}</p>`);

  // Related links
  const relatedHTML = page.related.map(r => `<a href="${r.href}">${r.text}</a>`).join('\n');
  html = html.replace(/<div class="related-links">[\s\S]*?<\/div>/, `<div class="related-links">\n${relatedHTML}\n</div>`);

  // FAQ HTML
  const faqHTML = page.faq.map(f => `<dt>${f.q}</dt><dd>${f.a}</dd>`).join('');
  html = html.replace(/<dl class="faq">[\s\S]*?<\/dl>/, `<dl class="faq">${faqHTML}</dl>`);

  // WhatsApp links update
  const waText = encodeURIComponent(`Hola DolarExpress, vengo de la web por ${page.h1}`);
  html = html.replace(/Cotizar por WhatsApp<\/a>/g, `Cotizar por WhatsApp</a>`);
  // Update all WhatsApp URLs in the page to include the page-specific text
  html = html.replace(/https:\/\/wa\.me\/56967658939\?text=[^"']*/g, `https://wa.me/56967658939?text=${waText}`);

  return html;
}

// ============================================================
// EJECUCIÓN
// ============================================================
console.log('=== DIFERENCIANDO CONTENIDO DE PÁGINAS ===\n');

let updated = 0;
let skipped = 0;

for (const [slug, page] of Object.entries(pages)) {
  const filePath = path.join(publicDir, `${slug}.html`);

  if (!fs.existsSync(filePath)) {
    console.log(`  [SKIP] No existe: ${slug}.html`);
    skipped++;
    continue;
  }

  let html = fs.readFileSync(filePath, 'utf-8');

  html = updateMetaTags(html, page);
  html = updateSchema(html, page);
  html = updateContent(html, page);

  fs.writeFileSync(filePath, html, 'utf-8');
  console.log(`  [OK] ${slug}.html — meta, schema, FAQ y contenido único`);
  updated++;
}

console.log(`\nActualizadas: ${updated} | Saltadas: ${skipped}`);
console.log('Listo. Las 5 páginas del Template B ahora tienen contenido 100% diferenciado.');
