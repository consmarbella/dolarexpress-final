#!/usr/bin/env node
/**
 * Regenera el sitemap.xml solo con páginas HTML válidas del directorio public
 */

const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, 'public');
const sitemapPath = path.join(publicDir, 'sitemap.xml');

const urls = [];

function scanDir(dir, prefix = '') {
  if (!fs.existsSync(dir)) return;
  
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relPath = path.relative(publicDir, fullPath).replace(/\\/g, '/');
    
    if (entry.isDirectory()) {
      // Buscar index.html dentro de la carpeta
      const indexPath = path.join(fullPath, 'index.html');
      if (fs.existsSync(indexPath)) {
        const urlPath = '/' + relPath.replace('/index.html', '').replace('.html', '');
        urls.push(urlPath);
      }
      scanDir(fullPath);
    } else if (entry.name.endsWith('.html') && !entry.name.startsWith('.')) {
      // Archivos HTML en la raíz
      const urlPath = '/' + entry.name.replace('.html', '');
      if (!entry.name.includes('index')) {
        urls.push(urlPath);
      }
    }
  }
}

console.log('Escaneando directorio public...');
scanDir(publicDir);

// Eliminar duplicados
const uniqueUrls = [...new Set(urls)];

// Ordenar
uniqueUrls.sort();

// Generar XML
let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
`;

// Homepage
xml += `  <url>
    <loc>https://dolarexpress.cl/</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
`;

// Páginas principales
const importantPages = [
  '/venta-usd',
  '/directorio-general', 
  '/contacto',
  '/venta-cupo-dolares',
  '/vender-usd',
  '/vender-usd-chile'
];

for (const page of importantPages) {
  if (uniqueUrls.includes(page)) {
    xml += `  <url>
    <loc>https://dolarexpress.cl${page}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
`;
  }
}

// Resto de páginas
for (const url of uniqueUrls) {
  if (!importantPages.includes(url) && url !== '/') {
    xml += `  <url>
    <loc>https://dolarexpress.cl${url}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
`;
  }
}

xml += '</urlset>';

// Guardar
fs.writeFileSync(sitemapPath, xml);

console.log(`✅ Sitemap actualizado con ${uniqueUrls.length} URLs`);
console.log(`📄 Guardado en: ${sitemapPath}`);