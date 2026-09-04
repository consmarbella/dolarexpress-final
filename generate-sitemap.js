import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://www.dolarexpress.cl';

// ─── SOLO PÁGINAS CORE CON CONTENIDO REAL ───
const urls = [
  // Home
  { loc: `${baseUrl}/`, priority: '1.0', changefreq: 'weekly' },

  // Páginas principales de conversión (TIER 1 - tienen clicks reales)
  { loc: `${baseUrl}/vender-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-tarjeta-credito`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cupo-internacional-a-pesos`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/avance-cupo-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/sacar-plata-tarjeta-lider`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/sacar-dinero-tarjeta-hites`, priority: '0.9', changefreq: 'weekly' },

  // Páginas informacionales que convierten (TIER 2 - tienen clicks reales)
  { loc: `${baseUrl}/guia/vender-cupo-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cuanto-pagan-por-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/que-es-cupo-en-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/testimonios`, priority: '0.8', changefreq: 'monthly' },

  // Hubs que agrupan doorway pages (TIER 3 - autoridad temática)
  { loc: `${baseUrl}/cupo-dolares-por-banco`, priority: '0.9', changefreq: 'weekly' },

  // Directorio y contacto
  { loc: `${baseUrl}/directorio-general`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/contacto`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/comisiones`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/preguntas-frecuentes`, priority: '0.7', changefreq: 'monthly' },

  // Legales
  { loc: `${baseUrl}/privacidad`, priority: '0.3', changefreq: 'yearly' },
  { loc: `${baseUrl}/terminos`, priority: '0.3', changefreq: 'yearly' },

  // Institucionales
  { loc: `${baseUrl}/nosotros`, priority: '0.6', changefreq: 'monthly' },
  { loc: `${baseUrl}/seguridad`, priority: '0.6', changefreq: 'monthly' },
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
];

outputPaths.forEach(outputPath => {
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(outputPath, sitemap);
});

console.log(`✅ Sitemap generado con ${urls.length} URLs (solo páginas core)`);
