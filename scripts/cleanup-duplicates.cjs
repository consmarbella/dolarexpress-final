const fs = require('fs');
const path = require('path');

const pubDir = path.join(__dirname, '..', 'public');

// Pages to keep (only root .html, no directory duplicate)
const KEEP_ROOT = new Set([
  'index',
  'avance-cupo-dolares',
  'cupo-dolares-por-banco',
  'cuanto-pagan-por-cupo-dolar',
  'que-es-cupo-en-dolares',
  'preguntas-frecuentes',
  'directorio-general',
  'contacto',
  'privacidad',
  'terminos',
  'nosotros',
  'testimonios',
  'seguridad',
  'comisiones',
  'vender-usd',
  'vender-cupo-dolar',
  'vender-cupo-tarjeta-credito',
  'cupo-en-dolares',
  'cupo-internacional-a-pesos',
  'cupo-dolar-como-funciona',
  'cupo-dolar-requisitos',
  'cupo-dolar-primera-vez',
  'cupo-dolar-seguro',
  'cupo-dolar-confiable',
  'cupo-dolar-conviene',
  'es-legal-vender-cupo-dolar',
  'riesgos-vender-cupo-dolar',
  'cupo-dolar-empresas',
  'cupo-dolar-persona-natural',
  'vender-cupo-banco-chile',
  'vender-cupo-banco-estado',
  'vender-cupo-bci',
  'vender-cupo-santander',
  'vender-cupo-scotiabank',
  'vender-cupo-itau',
  'vender-cupo-cmr-falabella',
  'vender-cupo-ripley-rapido',
  'vender-cupo-lider-santiago',
  'vender-cupo-paris-efectivo',
  'vender-cupo-hites-ahora',
  'vender-cupo-abcdin-urgente',
  'vender-cupo-easy-mismo-dia',
  'que-es-cupo-dolar',
]);

// Everything else - delete both .html and directory
let deletedFiles = 0;
let deletedDirs = 0;

// First pass: delete all non-keep files
const allEntries = fs.readdirSync(pubDir, { withFileTypes: true });
for (const entry of allEntries) {
  if (entry.isDirectory()) {
    if (entry.name === 'guia' || entry.name === 'prestamos-santiago') continue;
    const baseName = entry.name;
    if (!KEEP_ROOT.has(baseName)) {
      const dirPath = path.join(pubDir, entry.name);
      fs.rmSync(dirPath, { recursive: true, force: true });
      deletedDirs++;
    }
  } else if (entry.name.endsWith('.html')) {
    const baseName = entry.name.replace('.html', '');
    if (!KEEP_ROOT.has(baseName) && baseName !== 'index') {
      fs.unlinkSync(path.join(pubDir, entry.name));
      deletedFiles++;
    }
  }
}

// Clean prestamos-santiago - keep only sacar-dinero-hites
const prestDir = path.join(pubDir, 'prestamos-santiago');
if (fs.existsSync(prestDir)) {
  const entries = fs.readdirSync(prestDir, { withFileTypes: true });
  for (const entry of entries) {
    const baseName = entry.name.replace('.html', '');
    if (baseName !== 'sacar-dinero-hites') {
      const fullPath = path.join(prestDir, entry.name);
      if (entry.isDirectory()) {
        fs.rmSync(fullPath, { recursive: true, force: true });
        deletedDirs++;
      } else {
        fs.unlinkSync(fullPath);
        deletedFiles++;
      }
    }
  }
}

// Count remaining
const remaining = fs.readdirSync(pubDir, { withFileTypes: true });
let htmlCount = 0;
for (const e of remaining) {
  if (e.isFile() && e.name.endsWith('.html')) htmlCount++;
  if (e.isDirectory()) {
    const sub = fs.readdirSync(path.join(pubDir, e.name));
    htmlCount += sub.filter(f => f.endsWith('.html')).length;
  }
}

console.log(`Deleted: ${deletedFiles} files, ${deletedDirs} directories`);
console.log(`Remaining: ${htmlCount} HTML pages`);
