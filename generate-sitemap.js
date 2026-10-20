import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://www.dolarexpress.cl';

// ─── PÁGINAS ACTIVAS (19 URLs) ───
// `src` = HTML fuente en public/ que alimenta cada ruta limpia (para lastmod por git)
const urls = [
  // Core
  { loc: `${baseUrl}/`, priority: '1.0', changefreq: 'weekly', src: 'index.html' },
  { loc: `${baseUrl}/avance-cupo-dolares`, priority: '0.9', changefreq: 'weekly', src: 'avance-cupo-dolares.html' },
  { loc: `${baseUrl}/vender-cupo-dolar`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-dolar.html' },
  { loc: `${baseUrl}/que-es-cupo-en-dolares`, priority: '0.9', changefreq: 'weekly', src: 'que-es-cupo-en-dolares.html' },
  { loc: `${baseUrl}/cuanto-pagan-por-cupo-dolar`, priority: '0.9', changefreq: 'weekly', src: 'cuanto-pagan-por-cupo-dolar.html' },
  // Guide
  { loc: `${baseUrl}/guia/vender-cupo-dolares`, priority: '0.8', changefreq: 'monthly', src: 'guia/vender-cupo-dolares.html' },
  // FAQ
  { loc: `${baseUrl}/preguntas-frecuentes`, priority: '0.8', changefreq: 'monthly', src: 'preguntas-frecuentes.html' },
  // Vender cupo - bancos
  { loc: `${baseUrl}/vender-cupo-banco-chile`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-banco-chile.html' },
  { loc: `${baseUrl}/vender-cupo-bci`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-bci.html' },
  { loc: `${baseUrl}/vender-cupo-santander`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-santander.html' },
  { loc: `${baseUrl}/vender-cupo-scotiabank`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-scotiabank.html' },
  { loc: `${baseUrl}/vender-cupo-itau`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-itau.html' },
  // Vender cupo - retail
  { loc: `${baseUrl}/vender-cupo-cmr-falabella`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-cmr-falabella.html' },
  { loc: `${baseUrl}/vender-cupo-ripley-rapido`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-ripley-rapido.html' },
  { loc: `${baseUrl}/vender-cupo-lider-santiago`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-lider-santiago.html' },
  // Vender cupo - bancos estado / empresas
  { loc: `${baseUrl}/vender-cupo-banco-estado`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-banco-estado.html' },
  { loc: `${baseUrl}/empresas-altos-montos`, priority: '0.8', changefreq: 'weekly', src: 'empresas-altos-montos.html' },
  // Vender cupo - franquicias y retail
  { loc: `${baseUrl}/vender-cupo-dolar-tarjeta-visa`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-dolar-tarjeta-visa.html' },
  { loc: `${baseUrl}/vender-cupo-dolar-tarjeta-mastercard`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-dolar-tarjeta-mastercard.html' },
  { loc: `${baseUrl}/vender-cupo-dolar-tarjeta-amex`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-dolar-tarjeta-amex.html' },
  { loc: `${baseUrl}/vender-cupo-dolar-tarjeta-paris`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-dolar-tarjeta-paris.html' },
  { loc: `${baseUrl}/vender-cupo-dolar-tarjeta-hites`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-dolar-tarjeta-hites.html' },
  { loc: `${baseUrl}/vender-cupo-dolar-tarjeta-abc`, priority: '0.9', changefreq: 'weekly', src: 'vender-cupo-dolar-tarjeta-abc.html' },
  // Institucionales
  { loc: `${baseUrl}/testimonios`, priority: '0.7', changefreq: 'monthly', src: 'testimonios.html' },
  { loc: `${baseUrl}/nosotros`, priority: '0.6', changefreq: 'monthly', src: 'nosotros.html' },
  { loc: `${baseUrl}/contacto`, priority: '0.7', changefreq: 'monthly', src: 'contacto.html' },
  { loc: `${baseUrl}/privacidad`, priority: '0.3', changefreq: 'yearly', src: 'privacidad.html' },
  { loc: `${baseUrl}/terminos`, priority: '0.3', changefreq: 'yearly', src: 'terminos.html' },
  // Blog
  { loc: `${baseUrl}/vender-cupo-dolar-comision-mas-baja`, priority: '0.8', changefreq: 'monthly', src: 'vender-cupo-dolar-comision-mas-baja.html' },
  { loc: `${baseUrl}/vender-cupo-dolar-sin-clave-bancaria`, priority: '0.8', changefreq: 'monthly', src: 'vender-cupo-dolar-sin-clave-bancaria.html' },
  { loc: `${baseUrl}/como-vender-cupo-dolar-rapido`, priority: '0.8', changefreq: 'monthly', src: 'como-vender-cupo-dolar-rapido.html' },
  { loc: `${baseUrl}/vender-cupo-dolar-sin-dicom`, priority: '0.8', changefreq: 'monthly', src: 'vender-cupo-dolar-sin-dicom.html' },
  { loc: `${baseUrl}/cuanto-sale-vender-cupo-dolar-hoy`, priority: '0.8', changefreq: 'monthly', src: 'cuanto-sale-vender-cupo-dolar-hoy.html' },
  // Comparación
  { loc: `${baseUrl}/tabla-comparativa`, priority: '0.8', changefreq: 'monthly', src: 'tabla-comparativa.html' },
];

const today = new Date().toISOString().split('T')[0];

// lastmod = fecha del último commit git del HTML fuente; fallback a hoy
function lastmodFor(srcRel) {
  if (!srcRel) return today;
  const abs = path.join(__dirname, 'public', srcRel);
  if (!fs.existsSync(abs)) return today;
  try {
    const iso = execSync(`git log -1 --format=%cI -- "public/${srcRel}"`, {
      cwd: __dirname,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    if (!iso) return today;
    return iso.split('T')[0];
  } catch {
    return today;
  }
}

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url>
    <loc>${u.loc}</loc>
    <lastmod>${lastmodFor(u.src)}</lastmod>
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
