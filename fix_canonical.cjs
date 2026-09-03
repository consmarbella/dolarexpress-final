#!/usr/bin/env node
/**
 * Arregla canonical tags en todas las páginas HTML
 * y genera archivo _redirects para backup
 */

const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, 'public');
const redirects = [];

function getCanonicalUrl(filePath) {
  // Convertir ruta de archivo a URL
  let url = filePath.replace(publicDir, '').replace(/\\/g, '/');
  
  // Si es index.html en carpeta, usar la carpeta como ruta
  if (url.endsWith('/index.html')) {
    url = url.replace('/index.html', '');
  } else if (url.endsWith('.html')) {
    url = url.replace('.html', '');
  }
  
  // Quitar barra inicial si existe
  if (url.startsWith('/')) url = url.substring(1);
  
  return 'https://dolarexpress.cl/' + url;
}

function processFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  
  const canonicalUrl = getCanonicalUrl(filePath);
  
  // Verificar si tiene canonical tag
  if (!content.includes('rel="canonical"')) {
    // Agregar canonical después del title
    const titleMatch = content.match(/<title>(.*?)<\/title>/i);
    if (titleMatch) {
      const canonicalTag = `<link rel="canonical" href="${canonicalUrl}/" />`;
      content = content.replace(
        '</title>',
        '</title>' + '\n' + canonicalTag
      );
      modified = true;
    }
  } else {
    // Verificar si el canonical es correcto
    const canonicalMatch = content.match(/<link rel="canonical" href="([^"]+)" \/>/i);
    if (canonicalMatch && canonicalMatch[1] !== canonicalUrl + '/') {
      // Corregir canonical
      content = content.replace(
        canonicalMatch[0],
        `<link rel="canonical" href="${canonicalUrl}/" />`
      );
      modified = true;
    }
  }
  
  // Agregar noindex si es soft 404 o página no deseada
  const fileName = path.basename(filePath).toLowerCase();
  if (fileName.includes('404') || fileName.includes('error') || fileName.startsWith('.')) {
    if (!content.includes('noindex')) {
      content = content.replace('<head>', '<head>\n<meta name="robots" content="noindex, follow">');
      modified = true;
    }
  }
  
  if (modified) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('  ✅ Corregido:', filePath.replace(publicDir, ''));
  }
  
  // Agregar a redirects si es página válida
  if (!fileName.includes('404') && !fileName.startsWith('.')) {
    const url = getCanonicalUrl(filePath);
    redirects.push(url);
  }
}

function scanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    
    if (entry.isDirectory()) {
      scanDir(fullPath);
    } else if (entry.name.endsWith('.html')) {
      processFile(fullPath);
    }
  }
}

console.log('🔧 Arreglando canonicals en todas las páginas...\n');
scanDir(publicDir);

// Generar archivo _redirects para respaldo
console.log('\n📄 Generando archivo _redirects...');
let redirectContent = `# Redirects de respaldo para Vercel
# Generated automatically

/                   301!    /
/index.html         301!    /
/home               301!    /

# Pages without trailing slash redirect
`;

for (const url of redirects) {
  const cleanUrl = url.replace('https://dolarexpress.cl/', '').replace(/\/$/, '');
  if (cleanUrl && cleanUrl !== 'index.html') {
    redirectContent += `/${cleanUrl}   301!    /\n`;
  }
}

fs.writeFileSync(path.join(publicDir, '_redirects'), redirectContent);
console.log('✅ _redirects generado');

console.log('\n✅ Proceso completado');