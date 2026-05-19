#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Read pseo-data.ts and extract slugs using regex
const pseoDataFile = fs.readFileSync(path.join(__dirname, 'src/data/pseo-data.ts'), 'utf8');
const slugMatches = pseoDataFile.match(/slug:\s*'([^']+)'/g) || [];
const slugs = slugMatches.map(m => m.replace(/slug:\s*'([^']+)'/, '$1'));

console.log(`Found ${slugs.length} slugs from pseo-data.ts`);

const BANK_DATA = {
  'banco-chile': { name: 'Banco de Chile' },
  'bancoestado': { name: 'BancoEstado' },
  'bci': { name: 'BCI' },
  'santander': { name: 'Santander' },
  'scotiabank': { name: 'Scotiabank' },
  'itau': { name: 'Itaú' },
  'bice': { name: 'BICE' },
  'security': { name: 'Security' },
  'bbva': { name: 'BBVA' },
};

const RETAIL_CARD_DATA = {
  'lider': { name: 'Líder' },
  'cmr': { name: 'CMR Falabella' },
  'ripley': { name: 'Ripley' },
  'paris': { name: 'Paris' },
  'la-polar': { name: 'La Polar' },
  'hites': { name: 'Hites' },
  'abcdin': { name: 'ABCDin' },
  'cencosud': { name: 'Cencosud' },
  'johnson': { name: 'Johnson' },
  'easy': { name: 'Easy' },
  'jumbo': { name: 'Jumbo' },
  'corona': { name: 'Corona' },
};

function detectBank(slug) {
  for (const [key, data] of Object.entries(BANK_DATA)) {
    if (slug.includes(key)) return data;
  }
  return null;
}

function detectRetailCard(slug) {
  const order = ['la-polar', 'abcdin', 'cencosud', 'johnson', 'corona', 'ripley', 'paris', 'hites', 'jumbo', 'easy', 'lider', 'cmr'];
  for (const key of order) {
    if (slug.includes(key)) return RETAIL_CARD_DATA[key];
  }
  return null;
}

function generateMetaTitle(slug) {
  const card = detectRetailCard(slug);
  if (card) return `${card.name} - Obtén Efectivo | DolarExpress`;

  const bank = detectBank(slug);
  if (bank) return `${bank.name} - Compra de Cupo Dólar | DolarExpress`;

  return `${slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} | DolarExpress`;
}

function generateMetaDescription(slug) {
  const card = detectRetailCard(slug);
  if (card) {
    return `Obtén efectivo con tu tarjeta ${card.name}. Conversión rápida de cupo a pesos chilenos en 15 minutos sin avance habilitado. Servicio de DolarExpress.`;
  }

  const bank = detectBank(slug);
  if (bank) {
    return `Compra de cupo en dólares de ${bank.name}. Conversión al mejor tipo de cambio con transferencia inmediata. Servicio seguro de DolarExpress.`;
  }

  return `Servicio de conversión de cupo a efectivo. Proceso rápido y seguro con DolarExpress. Transferencia en menos de 15 minutos.`;
}

function generateHTML(slug, title, description) {
  const titleForBreadcrumb = title.replace(' | DolarExpress', '');

  return `<!DOCTYPE html>
<html lang="es-CL">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <meta name="description" content="${description}" />
    <link rel="canonical" href="https://dolarexpress.cl/${slug}" />
    <meta property="og:title" content="${title}" />
    <meta property="og:description" content="${description}" />
    <meta property="og:url" content="https://dolarexpress.cl/${slug}" />
    <meta property="og:type" content="website" />
    <meta name="robots" content="index, follow" />
    <script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://dolarexpress.cl/"}, {"@type": "ListItem", "position": 2, "name": "${titleForBreadcrumb}", "item": "https://dolarexpress.cl/${slug}"}]}<\/script>
</head>
<body>
<nav style="padding:8px 12px"><a href="/">Inicio</a> · <a href="/directorio">Directorio</a></nav>
<header style="background:#1a1a1a;color:white;padding:16px;text-align:center">
  <h1 style="margin:0">${titleForBreadcrumb}</h1>
</header>
<main style="max-width:800px;margin:40px auto;padding:20px">
  <p>${description}</p>
  <a href="https://wa.me/56967658939?text=Hola,%20vengo%20de%20${slug}" style="background:#C8A045;color:white;padding:12px 24px;text-decoration:none;border-radius:8px;display:inline-block;margin:20px 0">Cotizar por WhatsApp</a>
  <h2>¿Cómo funciona?</h2>
  <ol>
    <li>Contacta por WhatsApp</li>
    <li>Te mostramos la tasa</li>
    <li>Autorizas la operación</li>
    <li>Recibis en tu cuenta en 15 min</li>
  </ol>
</main>
</body>
</html>`;
}

async function generateAllHTML() {
  const publicDir = path.join(__dirname, 'public');
  const existingFiles = new Set(fs.readdirSync(publicDir).filter(f => f.endsWith('.html')));

  let created = 0;
  let skipped = 0;

  console.log(`\n📝 Generando ${slugs.length} HTMLs estáticas...\n`);

  for (let i = 0; i < slugs.length; i++) {
    const slug = slugs[i];
    const filename = `${slug}.html`;

    if (existingFiles.has(filename)) {
      skipped++;
      if (i % 300 === 0 && i > 0) {
        console.log(`  ${i}/${slugs.length} (${created} nuevos)`);
      }
      continue;
    }

    const title = generateMetaTitle(slug);
    const description = generateMetaDescription(slug);
    const html = generateHTML(slug, title, description);
    const filepath = path.join(publicDir, filename);

    try {
      fs.writeFileSync(filepath, html, 'utf8');
      created++;
    } catch (e) {
      console.error(`Error: ${filename}`, e.message);
    }

    if ((i + 1) % 300 === 0) {
      console.log(`  ${i + 1}/${slugs.length} ✓`);
    }
  }

  console.log(`\n✅ Completado!\n`);
  console.log(`Total: ${created + skipped} HTMLs en /public/`);
  console.log(`Nuevos: ${created}\n`);
}

generateAllHTML().catch(console.error);
