import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://www.dolarexpress.cl';

// ─── SOLO PÁGINAS CON CONTENIDO REAL (30 páginas) ───
const urls = [
  // Core
  { loc: `${baseUrl}/`, priority: '1.0', changefreq: 'weekly' },
  { loc: `${baseUrl}/avance-cupo-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cupo-dolares-por-banco`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cuanto-pagan-por-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/que-es-cupo-en-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/preguntas-frecuentes`, priority: '0.8', changefreq: 'monthly' },
  // Vender cupo - banco
  { loc: `${baseUrl}/vender-cupo-banco-chile`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-banco-estado`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-bci`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-santander`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-scotiabank`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-itau`, priority: '0.9', changefreq: 'weekly' },
  // Vender cupo - tarjeta
  { loc: `${baseUrl}/vender-cupo-cmr-falabella`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-ripley-rapido`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-lider-santiago`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-paris-efectivo`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-hites-ahora`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-abcdin-urgente`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-easy-mismo-dia`, priority: '0.9', changefreq: 'weekly' },
  // Vender cupo core
  { loc: `${baseUrl}/vender-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-tarjeta-credito`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-usd`, priority: '0.9', changefreq: 'weekly' },
  // Guide
  { loc: `${baseUrl}/guia/vender-cupo-dolares`, priority: '0.8', changefreq: 'monthly' },
  // Institucionales
  { loc: `${baseUrl}/directorio-general`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/testimonios`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/nosotros`, priority: '0.6', changefreq: 'monthly' },
  { loc: `${baseUrl}/contacto`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/seguridad`, priority: '0.6', changefreq: 'monthly' },
  // Widget
  { loc: `${baseUrl}/widget`, priority: '0.6', changefreq: 'monthly' },
  // Legales
  { loc: `${baseUrl}/privacidad`, priority: '0.3', changefreq: 'yearly' },
  { loc: `${baseUrl}/terminos`, priority: '0.3', changefreq: 'yearly' },
];

const today = new Date().toISOString().split('T')[0];
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url>
    <loc>${u.loc}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

const outputPaths = [
  path.join(__dirname, 'public', 'sitemap.xml'),
  path.join(__dirname, 'dist', 'sitemap.xml'),
];

outputPaths.forEach(outputPath => {
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(outputPath, sitemap);
});

console.log(`✅ Sitemap generado con ${urls.length} URLs (solo páginas core)`);
