import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://dolarexpress.cl';
const today = new Date().toISOString().split('T')[0];

// === SOLO PAGINAS CON VALOR SEO REAL (nada de thin content) ===

const pages = [
  // ── HOMEPAGE ──
  { slug: '', priority: '1.0', changefreq: 'daily', cat: 'Home' },

  // ── HIGH CONVERSION ──
  { slug: 'venta-usd', priority: '0.9', changefreq: 'daily', cat: 'Conversion' },
  { slug: 'venta-cupo-dolares', priority: '0.9', changefreq: 'daily', cat: 'Conversion' },
  { slug: 'compro-cupo-dolar', priority: '0.9', changefreq: 'daily', cat: 'Conversion' },
  { slug: 'compra-cupo-dolares', priority: '0.9', changefreq: 'daily', cat: 'Conversion' },
  { slug: 'cupo-internacional-a-pesos', priority: '0.9', changefreq: 'daily', cat: 'Conversion' },
  { slug: 'vender-cupo-dolar', priority: '0.9', changefreq: 'daily', cat: 'Conversion' },
  { slug: 'directorio-general', priority: '0.8', changefreq: 'weekly', cat: 'Conversion' },
  { slug: 'comisiones', priority: '0.7', changefreq: 'monthly', cat: 'Conversion' },
  { slug: 'contacto', priority: '0.7', changefreq: 'monthly', cat: 'Conversion' },

  // ── BANCOS ──
  { slug: 'cupo-dolar-banco-estado', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-banco-chile', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-bci', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-santander', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-scotiabank', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-bbva', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-itau', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-bice', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },
  { slug: 'cupo-dolar-security', priority: '0.8', changefreq: 'weekly', cat: 'Banco' },

  // ── RETAIL ──
  { slug: 'cupo-dolar-cmr', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'cupo-dolar-ripley', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'cupo-dolar-falabella', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'cmr', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'ripley', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'cencosud', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'lider', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'paris', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },
  { slug: 'abcdin', priority: '0.8', changefreq: 'weekly', cat: 'Retail' },

  // ── VENDER CUPO + BANCO/RETAIL ──
  { slug: 'vender-cupo-banco-estado', priority: '0.8', changefreq: 'weekly', cat: 'Vender+Banco' },
  { slug: 'vender-cupo-banco-chile', priority: '0.8', changefreq: 'weekly', cat: 'Vender+Banco' },
  { slug: 'vender-cupo-bci', priority: '0.8', changefreq: 'weekly', cat: 'Vender+Banco' },
  { slug: 'vender-cupo-santander', priority: '0.8', changefreq: 'weekly', cat: 'Vender+Banco' },
  { slug: 'vender-cupo-scotiabank', priority: '0.8', changefreq: 'weekly', cat: 'Vender+Banco' },
  { slug: 'vender-cupo-itau', priority: '0.8', changefreq: 'weekly', cat: 'Vender+Banco' },
  { slug: 'vender-cupo-cmr-falabella', priority: '0.7', changefreq: 'weekly', cat: 'Vender+Retail' },

  // ── TARJETAS (sin ciudad) ──
  { slug: 'cupo-dolar-visa', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-visa-gold', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-visa-platinum', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-visa-signature', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-mastercard', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-mastercard-gold', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-mastercard-platinum', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-mastercard-black', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },
  { slug: 'cupo-dolar-american-express', priority: '0.7', changefreq: 'weekly', cat: 'Tarjeta' },

  // ── CIUDADES: EXCLUIDAS (thin content geográfico). Solo se indexan las páginas principales sin geo. ──

  // ── MONTOS (USD→CLP, alta intención) ──
  { slug: 'cupo-dolar-500-usd', priority: '0.7', changefreq: 'weekly', cat: 'Montos' },
  { slug: 'cupo-dolar-1000-usd', priority: '0.7', changefreq: 'weekly', cat: 'Montos' },

  // ── AVANCE (principales) ──
  { slug: 'avance-efectivo', priority: '0.7', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-cupo-dolares', priority: '0.7', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-dolares', priority: '0.7', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-tarjeta-dolares', priority: '0.7', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjeta-cmr', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjeta-ripley', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjeta-lider', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjeta-paris', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjeta-la-polar', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjeta-hites', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjeta-abc', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-abc-visa', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-cmr-sin-avance-habilitado', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-ripley-cuotas', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-la-polar-cuotas', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-lider-bci-online', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-sin-avance-habilitado', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },
  { slug: 'avance-efectivo-tarjetas-grandes-tiendas-chile', priority: '0.6', changefreq: 'weekly', cat: 'Avance' },

  // ── GUÍAS / INFORMATIVAS ──
  { slug: 'que-es-cupo-dolar', priority: '0.7', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'como-vender-cupo-dolar', priority: '0.7', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-confiable', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-conviene', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-seguro', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'es-legal-vender-cupo-dolar', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'riesgos-vender-cupo-dolar', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'vender-cupo-tarjeta-credito', priority: '0.8', changefreq: 'weekly', cat: 'Vender+Tarjeta' },
  { slug: 'como-vender-cupo-tarjeta-credito', priority: '0.7', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cambiar-cupo-tarjeta-efectivo', priority: '0.7', changefreq: 'weekly', cat: 'Guia' },
  { slug: 'cupo-dolar-requisitos', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-monto-minimo', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-persona-natural', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-empresas', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-online', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-rapido', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-15-minutos', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-hoy-chile', priority: '0.7', changefreq: 'daily', cat: 'Guia' },
  { slug: 'cupo-dolar-urgente', priority: '0.6', changefreq: 'weekly', cat: 'Guia' },
  { slug: 'cupo-dolar-whatsapp', priority: '0.6', changefreq: 'weekly', cat: 'Guia' },
  { slug: 'cupo-dolar-a-pesos', priority: '0.7', changefreq: 'weekly', cat: 'Guia' },
  { slug: 'cupo-dolar-disponible', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-primera-vez', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'cupo-dolar-altos-montos', priority: '0.6', changefreq: 'monthly', cat: 'Guia' },
  { slug: 'mejor-tasa-cupo-dolar', priority: '0.6', changefreq: 'weekly', cat: 'Guia' },
  { slug: 'comparador-tasas-cupo-dolar', priority: '0.6', changefreq: 'weekly', cat: 'Guia' },

  // ── OTRAS PÁGINAS CON VALOR ──
  { slug: 'cupo-dolar-internacional', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'cupo-dolar-regiones-chile', priority: '0.6', changefreq: 'monthly', cat: 'Info' },
  { slug: 'cupo-dolar-fin-de-mes', priority: '0.6', changefreq: 'monthly', cat: 'Info' },
  { slug: 'cupo-dolar-recomendado', priority: '0.6', changefreq: 'monthly', cat: 'Info' },
  { slug: 'cupo-dolar-sin-monto-minimo', priority: '0.6', changefreq: 'monthly', cat: 'Info' },
  { slug: 'cupo-dolar-transferencia-inmediata', priority: '0.6', changefreq: 'monthly', cat: 'Info' },
  { slug: 'cupo-dolar-sin-avance', priority: '0.6', changefreq: 'monthly', cat: 'Info' },
  { slug: 'cambiar-cupo-dolar', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'cambiar-cupo-dolares-chile', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'cambiar-dolares-tarjeta', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'cambio-cupo-dolar', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'cambio-dolares-tarjeta-credito', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'comprar-cupo-dolar', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'convertir-cupo-dolar-pesos', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
  { slug: 'sacar-cupo-dolares', priority: '0.6', changefreq: 'weekly', cat: 'Info' },
  { slug: 'girar-cupo-dolares', priority: '0.6', changefreq: 'weekly', cat: 'Info' },
  { slug: 'girar-dolares-tarjeta', priority: '0.6', changefreq: 'weekly', cat: 'Info' },
  { slug: 'pasar-cupo-de-compras-a-efectivo', priority: '0.6', changefreq: 'weekly', cat: 'Info' },
  { slug: 'terminos', priority: '0.5', changefreq: 'monthly', cat: 'Legal' },
  { slug: 'privacidad', priority: '0.5', changefreq: 'monthly', cat: 'Legal' },

  // ── URGENCIA / CONVERSIÓN ──
  { slug: 'necesito-plata-hoy', priority: '0.7', changefreq: 'weekly', cat: 'Urgencia' },
  { slug: 'necesito-pesos-tengo-dolares', priority: '0.7', changefreq: 'weekly', cat: 'Urgencia' },
  { slug: 'necesito-plata-y-tengo-cupo-en-tarjeta', priority: '0.7', changefreq: 'weekly', cat: 'Urgencia' },
  { slug: 'dinero-urgente', priority: '0.7', changefreq: 'weekly', cat: 'Urgencia' },
  { slug: 'cupo-dolar-urgente', priority: '0.7', changefreq: 'weekly', cat: 'Urgencia' },
  { slug: 'efectivo-inmediato', priority: '0.6', changefreq: 'weekly', cat: 'Urgencia' },
  { slug: 'liquidez-inmediata', priority: '0.6', changefreq: 'weekly', cat: 'Urgencia' },

  // ── INTERNACIONAL ──
  { slug: 'internacional', priority: '0.7', changefreq: 'weekly', cat: 'Info' },
];

// Verify pages exist in /public/
const publicDir = path.join(__dirname, 'public');

function pageExists(slug) {
  if (!slug) return true; // homepage
  const fileName = slug + '.html';
  const filePath = path.join(publicDir, fileName);
  return fs.existsSync(filePath);
}

const validPages = pages.filter(p => {
  const exists = pageExists(p.slug);
  if (!exists) console.log(`  [SKIP] no existe: ${p.slug || '/'}`);
  return exists;
});

// Generate XML
const xmlLines = ['<?xml version="1.0" encoding="UTF-8"?>'];
xmlLines.push('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">');

for (const page of validPages) {
  const loc = page.slug ? `${baseUrl}/${page.slug}` : `${baseUrl}/`;
  xmlLines.push('  <url>');
  xmlLines.push(`    <loc>${loc}</loc>`);
  xmlLines.push(`    <lastmod>${today}</lastmod>`);
  xmlLines.push(`    <changefreq>${page.changefreq}</changefreq>`);
  xmlLines.push(`    <priority>${page.priority}</priority>`);
  xmlLines.push('  </url>');
}

xmlLines.push('</urlset>');
const xml = xmlLines.join('\n') + '\n';

fs.writeFileSync(path.join(publicDir, 'sitemap.xml'), xml, 'utf-8');

// Stats
const catCounts = {};
for (const page of validPages) {
  catCounts[page.cat] = (catCounts[page.cat] || 0) + 1;
}

console.log(`\n=== SITEMAP GENERADO (SOLO PAGINAS CON VALOR SEO) ===`);
console.log(`URLs totales: ${validPages.length}`);
console.log(`Excluidas (thin content banco+ciudad, etc.): ~${7133 - validPages.length}+`);
console.log(`Fecha: ${today}\n`);
console.log('Por categoria:');
const catOrder = ['Home', 'Conversion', 'Banco', 'Retail', 'Vender+Banco', 'Vender+Retail', 'Tarjeta', 'Ciudad', 'Montos', 'Avance', 'Guia', 'Info', 'Urgencia', 'Legal'];
let total = 0;
for (const cat of catOrder) {
  if (catCounts[cat]) {
    console.log(`  ${cat.padEnd(18)} ${String(catCounts[cat]).padStart(3)} URLs`);
    total += catCounts[cat];
  }
}
console.log(`  ${'TOTAL'.padEnd(18)} ${String(total).padStart(3)} URLs`);
