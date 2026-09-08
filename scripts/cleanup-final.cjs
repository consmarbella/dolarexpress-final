const fs = require('fs');
const path = require('path');

const pubDir = path.join(__dirname, '..', 'public');

// FINAL KEEP LIST - ~35 pages max
const KEEP = new Set([
  // Core
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
  // Bank vender pages
  'vender-cupo-banco-chile',
  'vender-cupo-banco-estado',
  'vender-cupo-bci',
  'vender-cupo-santander',
  'vender-cupo-scotiabank',
  'vender-cupo-itau',
  // Card vender pages
  'vender-cupo-cmr-falabella',
  'vender-cupo-ripley-rapido',
  'vender-cupo-lider-santiago',
  'vender-cupo-paris-efectivo',
  'vender-cupo-hites-ahora',
  'vender-cupo-abcdin-urgente',
  'vender-cupo-easy-mismo-dia',
  // Core vender
  'vender-cupo-dolar',
  'vender-cupo-tarjeta-credito',
  'vender-usd',
  // Guide
  'guia/vender-cupo-dolares',
]);

let deleted = 0;

// Delete everything that's not in KEEP
function clean(dir, prefix) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relPath = prefix ? `${prefix}/${entry.name}` : entry.name;

    if (entry.isDirectory()) {
      if (entry.name === 'guia') {
        // Clean guia directory
        const guiaFiles = fs.readdirSync(fullPath);
        for (const f of guiaFiles) {
          const base = f.replace('.html', '');
          if (!KEEP.has(`guia/${base}`)) {
            fs.unlinkSync(path.join(fullPath, f));
            deleted++;
          }
        }
        continue;
      }
      // Delete all other directories
      fs.rmSync(fullPath, { recursive: true, force: true });
      deleted++;
    } else if (entry.name.endsWith('.html')) {
      const base = entry.name.replace('.html', '');
      if (!KEEP.has(base) && base !== 'index') {
        fs.unlinkSync(fullPath);
        deleted++;
      }
    }
  }
}

clean(pubDir, '');

// Also clean prestamos-santiago completely
const prestDir = path.join(pubDir, 'prestamos-santiago');
if (fs.existsSync(prestDir)) {
  fs.rmSync(prestDir, { recursive: true, force: true });
  deleted++;
}

// Count remaining
const remaining = fs.readdirSync(pubDir, { withFileTypes: true });
let count = 0;
for (const e of remaining) {
  if (e.isFile() && e.name.endsWith('.html')) count++;
  if (e.isDirectory() && e.name === 'guia') {
    const sub = fs.readdirSync(path.join(pubDir, e.name));
    count += sub.filter(f => f.endsWith('.html')).length;
  }
}

console.log(`Deleted: ${deleted} items`);
console.log(`Remaining: ${count} pages`);
