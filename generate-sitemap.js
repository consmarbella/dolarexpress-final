import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://www.dolarexpress.cl';

// ─── SOLO PÁGINAS CORE CON CONTENIDO REAL ───
const urls = [
  // Home
  { loc: `${baseUrl}/`, priority: '1.0', changefreq: 'weekly' },

  // Páginas principales de conversión
  { loc: `${baseUrl}/vender-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/venta-cupo-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-tarjeta-credito`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cupo-internacional-a-pesos`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/avance-cupo-dolares`, priority: '0.9', changefreq: 'weekly' },

  // Directorio y contacto
  { loc: `${baseUrl}/directorio-general`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/contacto`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/comisiones`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/preguntas-frecuentes`, priority: '0.7', changefreq: 'monthly' },

  // Bancos
  { loc: `${baseUrl}/banco-estado`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/banco-chile`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/santander`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/bci`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/scotiabank`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/bbva`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/itau`, priority: '0.8', changefreq: 'weekly' },

  // Tarjetas retail
  { loc: `${baseUrl}/cmr`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/ripley`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/cencosud`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/lider`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/la-polar`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/paris`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/hites`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/abcdin`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/jumbo`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/easy`, priority: '0.8', changefreq: 'weekly' },

  // Internacional
  { loc: `${baseUrl}/internacional`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/vender-cupo-internacional`, priority: '0.8', changefreq: 'weekly' },

  // Guías de contenido
  { loc: `${baseUrl}/cuanto-pagan-por-cupo-dolar`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/guia/vender-cupo-dolares`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/cupo-dolares-por-banco`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/que-es-cupo-en-dolares`, priority: '0.9', changefreq: 'weekly' },

  // Legales
  { loc: `${baseUrl}/privacidad`, priority: '0.3', changefreq: 'yearly' },
  { loc: `${baseUrl}/terminos`, priority: '0.3', changefreq: 'yearly' },

  // Institucionales
  { loc: `${baseUrl}/nosotros`, priority: '0.6', changefreq: 'monthly' },
  { loc: `${baseUrl}/seguridad`, priority: '0.6', changefreq: 'monthly' },
  { loc: `${baseUrl}/testimonios`, priority: '0.7', changefreq: 'monthly' },
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
