import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, 'public');

// ============================================================
// 1. BANCOS — FAQ único por banco (7 páginas, Template C)
// ============================================================

const banks = {
  'cupo-dolar-banco-estado': {
    description: 'Convierte tu cupo en dólares de BancoEstado a pesos. Tarjetas Visa y Mastercard (no CuentaRUT). Transferencia en 15 min. +400 sucursales.',
    lead: 'BancoEstado es el banco más grande de Chile por número de clientes, con presencia en las 346 comunas del país. Si tenés una tarjeta de crédito BancoEstado Visa o Mastercard con cupo internacional, podemos convertirlo a pesos en menos de 15 minutos. Importante: la CuentaRUT no tiene cupo en dólares, solo las tarjetas de crédito del banco.',
    tip: 'BancoEstado tiene más de 14 millones de clientes y la red de sucursales más grande de Chile. Sus tarjetas de crédito incluyen cupo internacional que muchos clientes no saben que tienen.',
    faq: [
      { q: '¿La CuentaRUT tiene cupo en dólares?', a: 'No. La CuentaRUT es una cuenta vista, no incluye línea de crédito internacional. Necesitás una tarjeta de crédito BancoEstado (Visa o Mastercard) para tener cupo en dólares.' },
      { q: '¿Cómo activo el cupo internacional en BancoEstado?', a: 'Podés hacerlo en sucursal o en algunos casos desde la app. Si necesitás ayuda, te orientamos sin costo.' },
      { q: '¿BancoEstado tiene buena tasa para el cupo?', a: 'Como banco público, sus condiciones pueden variar. Nosotros trabajamos con una tasa competitiva independiente del banco emisor de tu tarjeta.' },
    ],
    related: ['cupo-dolar-banco-chile','cupo-dolar-bci','cupo-dolar-santander','vender-cupo-banco-estado'],
  },
  'cupo-dolar-banco-chile': {
    description: 'Convertí tu cupo en dólares de Banco de Chile a pesos. Tarjetas Visa Signature, Mastercard Black, Amex. Transferencia inmediata.',
    lead: 'Banco de Chile es uno de los bancos privados más grandes del país, con fuerte presencia en segmentos premium. Sus tarjetas Visa Signature, Mastercard Black y American Express suelen tener cupos internacionales altos. Convertí ese cupo a pesos chilenos con DolarExpress en minutos.',
    tip: 'Las tarjetas premium de Banco de Chile (Visa Signature, Mastercard Black) suelen tener cupos en dólares de USD 2.000 o más. Un cupo que muchos clientes acumulan sin usar.',
    faq: [
      { q: '¿Las tarjetas premium de Banco de Chile tienen más cupo?', a: 'Sí. Las tarjetas Visa Signature y Mastercard Black de Banco de Chile suelen tener cupos internacionales más altos que las tarjetas estándar, a veces desde USD 2.000.' },
      { q: '¿Puedo convertir el cupo de mi Amex de Banco de Chile?', a: 'Sí. Trabajamos con todas las tarjetas de Banco de Chile, incluida American Express.' },
      { q: '¿Cuánto tarda la transferencia a mi cuenta del Banco de Chile?', a: 'Menos de 15 minutos. La transferencia es inmediata una vez confirmada la operación.' },
    ],
    related: ['cupo-dolar-banco-estado','cupo-dolar-bci','cupo-dolar-santander','vender-cupo-banco-chile'],
  },
  'cupo-dolar-bci': {
    description: 'Vendé tu cupo en dólares BCI a pesos. Tarjetas Visa Infinite, Mastercard Black. Transferencia a tu cuenta en 15 minutos.',
    lead: 'BCI es conocido por su innovación digital y su app BCI Móvil, una de las mejores evaluadas de Chile. Si tenés una tarjeta de crédito BCI (Visa o Mastercard) con cupo internacional, convertilo a pesos desde tu celular con nuestro acompañamiento por WhatsApp.',
    tip: 'BCI fue pionero en Chile en servicios de pago internacional. Sus tarjetas Visa Infinite incluyen beneficios de viaje y cupos en dólares que pueden superar los USD 5.000.',
    faq: [
      { q: '¿Puedo usar la app BCI Móvil para la operación?', a: 'Sí. Todo el proceso lo hacés desde tu app BCI Móvil. Nosotros te guiamos paso a paso por WhatsApp.' },
      { q: '¿Las tarjetas BCI tienen buen cupo internacional?', a: 'Sí, especialmente las Visa Infinite y Mastercard Black. BCI es uno de los bancos con mejores cupos internacionales del mercado chileno.' },
      { q: '¿BCI cobra comisión por usar el cupo internacional?', a: 'El banco no cobra comisión adicional por usar el cupo. La operación con DolarExpress no tiene costos ocultos para vos.' },
    ],
    related: ['cupo-dolar-banco-chile','cupo-dolar-santander','cupo-dolar-scotiabank','vender-cupo-bci'],
  },
  'cupo-dolar-santander': {
    description: 'Convierte tu cupo en dólares Santander Chile. Tarjetas WorldMember, LATAM Pass. Pago por transferencia en 15 minutos.',
    lead: 'Santander es uno de los bancos privados más grandes del mundo y tiene fuerte presencia en Chile. Sus tarjetas incluyen programas de fidelidad como WorldMember y LATAM Pass. Si tenés cupo internacional en tu tarjeta Santander, te lo compramos al instante.',
    tip: 'Las tarjetas Santander WorldMember y LATAM Pass acumulan millas y puntos. Al convertir tu cupo en dólares, no perdés esos beneficios: la operación no afecta tus puntos ni tu categoría.',
    faq: [
      { q: '¿Pierdo mis puntos LATAM Pass al vender el cupo?', a: 'No. La operación es independiente de tu programa de puntos. Tus millas y beneficios se mantienen intactos.' },
      { q: '¿Santander tiene límites altos de cupo internacional?', a: 'Sí, especialmente en tarjetas WorldMember y LATAM Pass, donde los cupos pueden superar los USD 3.000.' },
      { q: '¿Cómo se hace la operación con Santander?', a: 'Todo desde la app Santander Chile. Te guiamos por WhatsApp en tiempo real.' },
    ],
    related: ['cupo-dolar-banco-chile','cupo-dolar-bci','cupo-dolar-scotiabank','vender-cupo-santander'],
  },
  'cupo-dolar-scotiabank': {
    description: 'Vende tu cupo en dólares Scotiabank Chile. Tarjetas Visa Signature, Gold. Transferencia a tu cuenta en minutos.',
    lead: 'Scotiabank Chile tiene una presencia sólida en el país, con tarjetas Visa Signature y Gold que incluyen cupo internacional. Convertí tu cupo en dólares a pesos chilenos con DolarExpress: sin trámites, sin papeleos, 100% online.',
    tip: 'Scotiabank ofrece el servicio Scotchase para avances en efectivo, pero usar el cupo internacional para venderlo a través de DolarExpress suele ser más rápido y conveniente.',
    faq: [
      { q: '¿Es mejor Scotchase o vender el cupo internacional?', a: 'Scotchase es un avance en efectivo tradicional del banco con sus propias tasas. Vender el cupo internacional con DolarExpress es una operación entre privados, sin afectar tu línea de crédito en pesos.' },
      { q: '¿Qué tarjetas Scotiabank aceptan?', a: 'Todas las tarjetas de crédito Scotiabank Visa y Mastercard emitidas en Chile.' },
      { q: '¿Cuánto demora la transferencia a Scotiabank?', a: 'Menos de 15 minutos, igual que a cualquier otro banco chileno.' },
    ],
    related: ['cupo-dolar-bci','cupo-dolar-santander','cupo-dolar-bbva','vender-cupo-scotiabank'],
  },
  'cupo-dolar-cmr': {
    description: 'Convierte tu cupo en dólares CMR Falabella a pesos. Sin avance habilitado. Transferencia inmediata a tu cuenta.',
    lead: 'CMR Falabella es la tarjeta retail más grande de Chile, con millones de clientes. Muchas personas no saben que su CMR incluye cupo en dólares. Nosotros usamos ese cupo internacional de compras para darte efectivo: no necesitás tener avance habilitado.',
    tip: 'La mayoría de las CMR no tienen avance en efectivo disponible, pero igual tienen cupo internacional. Nosotros usamos ese cupo de compras para convertir tus dólares a pesos, sin necesidad de avance.',
    faq: [
      { q: '¿Mi CMR tiene cupo en dólares si no tengo avance?', a: 'Sí. El cupo en dólares es independiente del avance en efectivo. Aunque no tengas avance habilitado, probablemente tengas cupo internacional disponible.' },
      { q: '¿Cómo reviso mi cupo internacional de la CMR?', a: 'En la app Falabella o en tu estado de cuenta, buscá "cupo internacional" o "línea USD". Si no lo encontrás, contactanos y te ayudamos.' },
      { q: '¿Pierdo mis puntos CMR al vender el cupo?', a: 'No. La operación no afecta tus puntos CMR ni tu categoría en el programa de fidelidad.' },
    ],
    related: ['cupo-dolar-ripley','cupo-dolar-falabella','cupo-dolar-mastercard','avance-efectivo-tarjeta-cmr'],
  },
  'cupo-dolar-ripley': {
    description: 'Vende tu cupo en dólares Ripley a pesos chilenos. Tarjetas Ripley con cupo internacional. Pago por transferencia.',
    lead: 'La tarjeta Ripley incluye cupo internacional en dólares, parte de su programa RipleyPuntos GO. Convertí ese cupo a pesos chilenos con DolarExpress: sin trámites, desde tu celular, con pago en menos de 15 minutos.',
    tip: 'Las tarjetas Ripley suelen tener cupos internacionales más bajos que las bancarias, pero igual representan liquidez inmediata. Desde USD 300 ya podés operar.',
    faq: [
      { q: '¿La tarjeta Ripley tiene cupo en dólares?', a: 'Sí, la mayoría de las tarjetas Ripley Visa incluyen cupo internacional. Revisá en la app Ripley o en tu estado de cuenta.' },
      { q: '¿Cuál es el monto mínimo para vender cupo Ripley?', a: 'El mínimo general es USD 300. Si tenés menos, contactanos igual y vemos alternativas.' },
      { q: '¿Afecta mis RipleyPuntos GO?', a: 'No. Tus puntos y beneficios del programa RipleyPuntos GO no se ven afectados por la operación.' },
    ],
    related: ['cupo-dolar-cmr','cupo-dolar-falabella','avance-efectivo-tarjeta-ripley','avance-ripley-cuotas'],
  },
};

// ============================================================
// APLICAR FAQ A BANCOS (Template C)
// ============================================================
function fixBankPages() {
  console.log('\n=== BANCOS: AGREGANDO FAQ ÚNICO ===');
  let count = 0;
  for (const [slug, bank] of Object.entries(banks)) {
    const filePath = path.join(publicDir, `${slug}.html`);
    if (!fs.existsSync(filePath)) { console.log(`  [SKIP] ${slug}`); continue; }
    let html = fs.readFileSync(filePath, 'utf-8');

    // Update meta description
    html = html.replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${bank.description}">`);
    html = html.replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${bank.description}">`);

    // Replace lead paragraph (the first <p class="lead">)
    html = html.replace(/<p class="lead">.*?<\/p>/, `<p class="lead">${bank.lead}</p>`);

    // Replace the tip/sabias section
    html = html.replace(/<div class="tip"><strong>💡 ¿Sabías que\.\.\.\?<\/strong><br>.*?<\/div>/, `<div class="tip"><strong>💡 Dato clave</strong><br>${bank.tip}</div>`);

    // Replace related links
    const relatedHTML = bank.related.map(r => `<a href="/${r}">${r.replace(/-/g,' ').replace(/cupo dolar /,'').replace(/vender cupo /,'vender ')}</a>`).join('\n');
    html = html.replace(/<div class="related">[\s\S]*?<\/div>/, (match) => {
      const start = match.indexOf('<p><strong>Servicios relacionados:</strong></p>');
      if (start === -1) return match;
      const beforeLinks = match.substring(0, start);
      return `${beforeLinks}<p><strong>Servicios relacionados:</strong></p>\n${relatedHTML}\n`;
    });

    // Add FAQ section before second CTA button (before last <a class="btn-wa">)
    const faqHTML = `
    <h2>Preguntas Frecuentes</h2>
    ${bank.faq.map(f => `<p><strong>${f.q}</strong><br>${f.a}</p>`).join('\n')}
`;
    // Insert FAQ before the last btn-wa
    html = html.replace(/(<a class="btn-wa".*?Cotizar por WhatsApp<\/a>)\s*(<\/div>\s*<\/main>)/, `$1\n${faqHTML}\n$2`);

    fs.writeFileSync(filePath, html, 'utf-8');
    console.log(`  [OK] ${slug} — FAQ único agregado`);
    count++;
  }
  console.log(`  Total: ${count} páginas`);
}

// ============================================================
// 2. URGENCIA — Agregar schema + breadcrumb + FAQ (3 páginas)
// ============================================================

const urgenciaPages = {
  'necesito-plata-hoy': {
    title: 'Necesito Plata Hoy: Soluciones con Cupo en Dólares | DolarExpress',
    description: '¿Necesitás plata hoy? Convertí tu cupo en dólares a efectivo en 15 minutos. Sin DICOM, sin aval. Pago por transferencia inmediata.',
    h1: 'Necesito Plata Hoy',
    lead: 'Si necesitás plata hoy y tenés una tarjeta de crédito, tu cupo en dólares puede ser la solución. Convertilo a pesos chilenos en menos de 15 minutos, sin DICOM, sin aval y 100% online.',
    faq: [
      { q: '¿Cómo consigo plata hoy mismo?', a: 'Contactanos por WhatsApp con el monto de tu cupo en dólares. Te cotizamos al instante y si aceptás, recibís la transferencia en 15 minutos.' },
      { q: '¿Necesito tener avance en efectivo?', a: 'No. Usamos tu cupo internacional de compras, no necesitás avance habilitado. Funciona con la mayoría de las tarjetas de crédito chilenas.' },
      { q: '¿Piden DICOM o antecedentes?', a: 'No. No consultamos DICOM ni pedimos aval. Solo necesitás tu cédula de identidad y una cuenta bancaria para recibir la transferencia.' },
    ],
  },
  'dinero-urgente': {
    title: 'Dinero Urgente: Convertí tu Cupo en Dólares Hoy | DolarExpress',
    description: '¿Necesitás dinero urgente? Usá tu cupo en dólares para obtener efectivo hoy. Transferencia en 15 minutos, sin DICOM, sin trámites.',
    h1: 'Dinero Urgente',
    lead: 'Cuando necesitás dinero urgente, cada minuto cuenta. Convertí el cupo en dólares de tu tarjeta de crédito a pesos chilenos hoy mismo. Proceso 100% online, sin salir de tu casa.',
    faq: [
      { q: '¿Cuánto tarda en llegar el dinero urgente?', a: 'Máximo 15 minutos desde que confirmás la operación. Coordinamos todo por WhatsApp en tiempo real.' },
      { q: '¿Puedo recibir el dinero en cualquier banco?', a: 'Sí. Transferimos a CuentaRUT, cuenta corriente o cuenta vista de cualquier banco chileno.' },
      { q: '¿Hay un monto mínimo para operar?', a: 'El monto mínimo es USD 300 en cupo disponible. Para montos más bajos, contactanos y evaluamos alternativas.' },
    ],
  },
  'cupo-dolar-urgente': {
    title: 'Cupo Dólar Urgente: Venta Express en 15 Minutos | DolarExpress',
    description: 'Vendé tu cupo en dólares urgente. Conversión express a pesos chilenos en 15 minutos. Atención personalizada por WhatsApp.',
    h1: 'Cupo Dólar Urgente',
    lead: '¿Tenés cupo en dólares y necesitás los pesos urgente? En DolarExpress te damos atención prioritaria. Convertimos tu cupo internacional a pesos chilenos en 15 minutos con acompañamiento personalizado.',
    faq: [
      { q: '¿Hay atención urgente fuera de horario?', a: 'Atendemos de lunes a domingo. Si necesitás vender tu cupo urgente, escribinos y te respondemos a la brevedad.' },
      { q: '¿El proceso urgente es diferente?', a: 'Es el mismo proceso seguro, pero con prioridad en la atención. Mismos pasos, misma seguridad, respuesta más rápida.' },
      { q: '¿Puedo vender el cupo de cualquier tarjeta urgente?', a: 'Sí. Visa, Mastercard y Amex de todos los bancos y retail de Chile. El proceso es igual de rápido para todas.' },
    ],
  },
};

function fixUrgenciaPages() {
  console.log('\n=== URGENCIA: AGREGANDO SCHEMA + FAQ ===');
  let count = 0;
  for (const [slug, page] of Object.entries(urgenciaPages)) {
    const filePath = path.join(publicDir, `${slug}.html`);
    if (!fs.existsSync(filePath)) { console.log(`  [SKIP] ${slug}`); continue; }
    let html = fs.readFileSync(filePath, 'utf-8');

    // Update meta
    html = html.replace(/<title>.*?<\/title>/, `<title>${page.title}</title>`);
    html = html.replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${page.description}">`);

    // Replace H1 and lead
    html = html.replace(/<h1>.*?<\/h1>/, `<h1>${page.h1}</h1>`);
    html = html.replace(/<p class="lead">.*?<\/p>/, `<p class="lead">${page.lead}</p>`);

    // Add BreadcrumbList + FAQ schema before </head>
    const schema = `
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":"https://dolarexpress.cl"},{"@type":"ListItem","position":2,"name":"${page.h1}","item":"https://dolarexpress.cl/${slug}"}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":${JSON.stringify(page.faq.map(f => ({"@type":"Question","name":f.q,"acceptedAnswer":{"@type":"Answer","text":f.a}})))}
</script>`;
    html = html.replace('</head>', `${schema}\n</head>`);

    // Replace thin content with proper content
    const faqHTML = page.faq.map(f => `<p><strong>${f.q}</strong><br>${f.a}</p>`).join('\n');
    // Add FAQ section and interlinking before footer
    html = html.replace(/<footer>/, `<div style="max-width:960px;margin:20px auto;padding:0 16px"><h2 style="color:#d4af37">Preguntas Frecuentes</h2>${faqHTML}<div style="margin-top:20px"><p><strong>Servicios relacionados:</strong></p><a href="/vender-cupo-dolar" style="display:inline-block;color:#d4af37;border:1px solid rgba(212,175,55,.3);padding:4px 10px;border-radius:999px;margin:3px;font-size:12px">vender cupo dólar</a><a href="/cupo-dolar-a-pesos" style="display:inline-block;color:#d4af37;border:1px solid rgba(212,175,55,.3);padding:4px 10px;border-radius:999px;margin:3px;font-size:12px">cupo dólar a pesos</a><a href="/avance-cupo-dolares" style="display:inline-block;color:#d4af37;border:1px solid rgba(212,175,55,.3);padding:4px 10px;border-radius:999px;margin:3px;font-size:12px">avance cupo dólares</a></div></div>\n<footer>`);

    fs.writeFileSync(filePath, html, 'utf-8');
    console.log(`  [OK] ${slug} — schema + FAQ + interlinking`);
    count++;
  }
  console.log(`  Total: ${count} páginas`);
}

// ============================================================
// EJECUTAR
// ============================================================
fixBankPages();
fixUrgenciaPages();
