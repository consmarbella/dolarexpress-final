import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://www.dolarexpress.cl';

// ─── PÁGINAS ACTIVAS (19 URLs) ───
const urls = [
  // Core
  { loc: `${baseUrl}/`, priority: '1.0', changefreq: 'weekly' },
  { loc: `${baseUrl}/avance-cupo-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/que-es-cupo-en-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cuanto-pagan-por-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cupo-dolares-por-banco`, priority: '0.9', changefreq: 'weekly' },
  // Guide
  { loc: `${baseUrl}/guia/vender-cupo-dolares`, priority: '0.8', changefreq: 'monthly' },
  // FAQ
  { loc: `${baseUrl}/preguntas-frecuentes`, priority: '0.8', changefreq: 'monthly' },
  // Vender cupo - bancos
  { loc: `${baseUrl}/vender-cupo-banco-chile`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-bci`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-santander`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-scotiabank`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-itau`, priority: '0.9', changefreq: 'weekly' },
  // Vender cupo - retail
  { loc: `${baseUrl}/vender-cupo-cmr-falabella`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-ripley-rapido`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-lider-santiago`, priority: '0.9', changefreq: 'weekly' },
  // Institucionales
  { loc: `${baseUrl}/testimonios`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/nosotros`, priority: '0.6', changefreq: 'monthly' },
   { loc: `${baseUrl}/contacto`, priority: '0.7', changefreq: 'monthly' },
   // Blog
   { loc: `${baseUrl}/vender-cupo-dolar-comision-mas-baja`, priority: '0.8', changefreq: 'monthly' },
   { loc: `${baseUrl}/vender-cupo-dolar-sin-clave-bancaria`, priority: '0.8', changefreq: 'monthly' },
   { loc: `${baseUrl}/como-vender-cupo-dolar-rapido`, priority: '0.8', changefreq: 'monthly' },
   { loc: `${baseUrl}/vender-cupo-dolar-sin-dicom`, priority: '0.8', changefreq: 'monthly' },
   { loc: `${baseUrl}/cuanto-sale-vender-cupo-dolar-hoy`, priority: '0.8', changefreq: 'monthly' },
   // Comparación
   { loc: `${baseUrl}/tabla-comparativa`, priority: '0.8', changefreq: 'monthly' },
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

console.log(`✅ Sitemap generado con ${urls.length} URLs`);
