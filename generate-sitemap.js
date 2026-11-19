// Genera public/sitemap.xml (y dist/sitemap.xml) a partir de las páginas HTML de public/.
//
// Cambios respecto a la versión anterior:
//  - La lista de URLs se arma sola desde public/ (excluye páginas con noindex, como widget).
//  - lastmod NO usa `git log` (en el clon superficial de Vercel daba la misma fecha a todas las páginas).
//    Se toma, por página, la más reciente entre:
//      a) "dateModified" del JSON-LD de la propia página, y
//      b) la fecha registrada en sitemap-lastmod.json.
//    Si no hay ninguna fecha, se OMITE lastmod (es válido) en vez de inventar una.
//  - Se eliminan <changefreq> y <priority>: Google los ignora.
//
// Uso:
//   node generate-sitemap.js                         → genera el sitemap
//   node generate-sitemap.js --touch /vender-cupo-bci /nosotros
//                                                    → marca esas rutas como modificadas HOY y genera el sitemap
//   (usa "/" para la home)

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const baseUrl = 'https://www.dolarexpress.cl';
const publicDir = path.join(__dirname, 'public');
const lastmodFile = path.join(__dirname, 'sitemap-lastmod.json');

// ── fechas manuales ──
let manual = {};
try {
  manual = JSON.parse(fs.readFileSync(lastmodFile, 'utf8'));
} catch {
  manual = {};
}

const args = process.argv.slice(2);
const touchIdx = args.indexOf('--touch');
if (touchIdx !== -1) {
  const today = new Date().toISOString().split('T')[0];
  const routes = args.slice(touchIdx + 1).filter((a) => a.startsWith('/'));
  for (const r of routes) manual[r] = today;
  const sorted = Object.fromEntries(Object.entries(manual).sort(([a], [b]) => a.localeCompare(b)));
  fs.writeFileSync(lastmodFile, JSON.stringify(sorted, null, 2) + '\n');
  console.log(`🕒 Marcadas como modificadas hoy (${today}): ${routes.join(', ') || '(ninguna)'}`);
}

// ── descubrir páginas ──
function walk(dir, base = '') {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const rel = path.posix.join(base, entry.name);
    if (entry.isDirectory()) out.push(...walk(path.join(dir, entry.name), rel));
    else if (entry.name.endsWith('.html')) out.push(rel);
  }
  return out;
}

const routeFor = (rel) => {
  const noExt = rel.replace(/\.html$/, '');
  if (noExt === 'index') return '/';
  return '/' + noExt.replace(/\/index$/, '');
};

const isNoindex = (html) => /<meta\s+name="robots"\s+content="[^"]*noindex/i.test(html);

const pageDate = (html) => {
  const m = html.match(/"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})/);
  return m ? m[1] : null;
};

const entries = [];
const skipped = [];
const noDate = [];

for (const rel of walk(publicDir).sort()) {
  const html = fs.readFileSync(path.join(publicDir, rel), 'utf8');
  const route = routeFor(rel);
  if (isNoindex(html)) {
    skipped.push(route);
    continue;
  }
  const dates = [manual[route], pageDate(html)].filter(Boolean).sort();
  const lastmod = dates.length ? dates[dates.length - 1] : null;
  if (!lastmod) noDate.push(route);
  entries.push({ route, loc: baseUrl + (route === '/' ? '/' : route), lastmod });
}

// home primero, resto alfabético
entries.sort((a, b) => (a.route === '/' ? -1 : b.route === '/' ? 1 : a.route.localeCompare(b.route)));

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${entries
  .map(
    (e) => `  <url>
    <loc>${e.loc}</loc>${e.lastmod ? `\n    <lastmod>${e.lastmod}</lastmod>` : ''}
  </url>`
  )
  .join('\n')}
</urlset>
`;

for (const outputPath of [path.join(publicDir, 'sitemap.xml'), path.join(__dirname, 'dist', 'sitemap.xml')]) {
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, sitemap);
}

console.log(`✅ Sitemap generado con ${entries.length} URLs`);
if (skipped.length) console.log(`   (excluidas por noindex: ${skipped.join(', ')})`);
if (noDate.length) console.log(`⚠️  Sin fecha de modificación (lastmod omitido): ${noDate.join(', ')}`);
