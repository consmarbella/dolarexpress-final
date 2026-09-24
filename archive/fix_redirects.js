#!/usr/bin/env node
/**
 * Script para generar redirecciones 301 desde páginas 404 a páginas relevantes
 * Ejecutar: node fix_redirects.js
 */

const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, 'public');
const redirects = [];

// Mapeo de páginas 404 a páginas de destino relevantes
const redirectsMap = {
  // Bancos comunes
  'vender-cupo-banco-chile': 'vender-cupo-banco-chile.html',
  'vender-cupo-bci': 'vender-cupo-bci.html',
  'vender-cupo-santander': 'vender-cupo-santander.html',
  'vender-cupo-scotiabank': 'vender-cupo-scotiabank.html',
  'vender-cupo-bbva': 'vender-cupo-bbva.html',
  'vender-cupo-itau': 'vender-cupo-itau.html',
  'vender-cupo-banco-estado': 'vender-cupo-banco-estado.html',
  
  // Ciudades
  'cupo-dolar-santiago': 'cupo-dolar-banco-chile-santiago.html',
  'cupo-dolar-valparaiso': 'cupo-dolar-banco-chile-valparaiso.html',
  'cupo-dolar-concepcion': 'cupo-dolar-banco-chile-concepcion.html',
  
  // Montos
  'cupo-dolar-100-usd': 'cupo-dolar-100-usd.html',
  'cupo-dolar-500-usd': 'cupo-dolar-500-usd.html',
  'cupo-dolar-1000-usd': 'cupo-dolar-1000-usd.html',
  
  // Urgente
  'urgente/plata-rapida': 'urgente/plata-rapida-sin-banco/index.html',
  'urgente/necesito-plata': 'urgente/necesito-plata-urgente/index.html',
  'urgente/dinero-urgente': 'urgente/necesito-dinero-urgente-chile/index.html',
};

// Función para encontrar página más similar
function findSimilarPage(slug) {
  // Buscar en el mapa directo
  if (redirectsMap[slug]) {
    return redirectsMap[slug];
  }
  
  // Buscar por palabras clave
  const keywords = slug.split('-');
  const pages = getAllPages();
  
  for (const page of pages) {
    const pageName = page.toLowerCase().replace('.html', '');
    let matchCount = 0;
    for (const kw of keywords) {
      if (pageName.includes(kw) && kw.length > 2) {
        matchCount++;
      }
    }
    if (matchCount >= 2) {
      return page;
    }
  }
  
  // Default: homepage
  return 'venta-cupo-dolares.html';
}

function getAllPages() {
  const pages = [];
  
  function scanDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        scanDir(fullPath);
      } else if (entry.name.endsWith('.html')) {
        // Convertir a ruta relativa
        const relPath = path.relative(publicDir, fullPath).replace(/\\/g, '/');
        pages.push(relPath);
      }
    }
  }
  
  if (fs.existsSync(publicDir)) {
    scanDir(publicDir);
  }
  
  return pages;
}

// Generar archivo de redirecciones para Vercel (vercel.json)
const vercelRedirects = {
  "redirects": [
    { "source": "/vender-cupo-banco-chile", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/vender-cupo-bci", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/vender-cupo-santander", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/vender-cupo-scotiabank", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/vender-cupo-bbva", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/vender-cupo-itau", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/vender-cupo-banco-estado", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/cupo-dolar", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/avance-efectivo", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/convertir-cupo", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/comprar-cupo", "destination": "/venta-cupo-dolares", "statusCode": 301 },
    { "source": "/vender-usd", "destination": "/venta-cupo-dolares", "statusCode": 301 },
  ]
};

console.log('✅ Redirecciones generadas para Vercel');
console.log(JSON.stringify(vercelRedirects, null, 2));

// Guardar para referencia
fs.writeFileSync(
  path.join(__dirname, 'vercel-redirects.json'),
  JSON.stringify(vercelRedirects, null, 2)
);
console.log('✅ Guardado en vercel-redirects.json');