import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://dolarexpress.cl';
const publicDir = path.join(__dirname, 'public');

// ─── 1. Páginas principales ───
const urls = [
  { loc: `${baseUrl}/`, priority: '1.0', changefreq: 'weekly' },
  { loc: `${baseUrl}/venta-usd`, priority: '0.9', changefreq: 'weekly' },
  { loc: `${baseUrl}/directorio-general`, priority: '0.8', changefreq: 'weekly' },
  { loc: `${baseUrl}/contacto`, priority: '0.7', changefreq: 'monthly' },
  { loc: `${baseUrl}/privacidad`, priority: '0.3', changefreq: 'yearly' },
  { loc: `${baseUrl}/terminos`, priority: '0.3', changefreq: 'yearly' },
];

// ─── 2. Escanear recursivamente public/ para HTML files ───
function scanHtmlFiles(dir, basePath = '') {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const results = [];

  entries.forEach(entry => {
    if (entry.name.startsWith('.')) return; // skip hidden files
    const fullPath = path.join(dir, entry.name);
    const relPath = basePath ? `${basePath}/${entry.name}` : entry.name;

    if (entry.isDirectory()) {
      results.push(...scanHtmlFiles(fullPath, relPath));
    } else if (entry.name.endsWith('.html') && entry.name !== 'index.html') {
      const slug = relPath.replace(/\.html$/, '');
      results.push({
        loc: `${baseUrl}/${slug}`,
        priority: '0.7',
        changefreq: 'monthly'
      });
    }
  });

  return results;
}

const staticPages = scanHtmlFiles(publicDir);
urls.push(...staticPages);

// ─── 3. Páginas PSEO dinámicas (tarjeta x ciudad) ───
const cards = ["CMR Falabella", "Cencosud", "Ripley", "Lider Bci"];
const cities = [
  "Santiago", "Valparaiso", "Concepcion", "La Serena", "Antofagasta", 
  "Temuco", "Iquique", "Rancagua", "Puerto Montt", "Talca", 
  "Arica", "Chillan", "Copiapo", "Quillota", "Valdivia", 
  "Osorno", "Los Angeles", "Calama", "Punta Arenas", "Vina del Mar"
];

cards.forEach(card => {
  cities.forEach(city => {
    const cardSlug = card.toLowerCase().replace(/\s+/g, '-');
    const citySlug = city.toLowerCase().replace(/\s+/g, '-');
    urls.push({
      loc: `${baseUrl}/vender-cupo-${cardSlug}-${citySlug}`,
      priority: '0.8',
      changefreq: 'monthly'
    });
  });
});

// ─── 4. Generar sitemap.xml ───
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

// Escribir en public/ y también en dist/ si existe
const outputPaths = [
  path.join(publicDir, 'sitemap.xml'),
  path.join(__dirname, 'dist', 'sitemap.xml'),
];

outputPaths.forEach(outputPath => {
  const dir = path.dirname(outputPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(outputPath, sitemap);
});

console.log(`✅ Sitemap generado exitosamente con ${urls.length} URLs!`);
console.log(`   - ${staticPages.length} paginas estaticas escaneadas de public/`);
console.log(`   - ${cards.length * cities.length} paginas PSEO dinamicas`);
