import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pubDir = path.join(__dirname, '..', 'public');

// ONLY these files stay
const KEEP = new Set([
  'index.html',
  'avance-cupo-dolares.html',
  'cupo-dolares-por-banco.html',
  'cuanto-pagan-por-cupo-dolar.html',
  'que-es-cupo-en-dolares.html',
  'preguntas-frecuentes.html',
  'directorio-general.html',
  'contacto.html',
  'privacidad.html',
  'terminos.html',
  'nosotros.html',
  'testimonios.html',
  'seguridad.html',
  'vender-cupo-banco-chile.html',
  'vender-cupo-banco-estado.html',
  'vender-cupo-bci.html',
  'vender-cupo-santander.html',
  'vender-cupo-scotiabank.html',
  'vender-cupo-itau.html',
  'vender-cupo-cmr-falabella.html',
  'vender-cupo-ripley-rapido.html',
  'vender-cupo-lider-santiago.html',
  'vender-cupo-paris-efectivo.html',
  'vender-cupo-hites-ahora.html',
  'vender-cupo-abcdin-urgente.html',
  'vender-cupo-easy-mismo-dia.html',
  'vender-cupo-dolar.html',
  'vender-cupo-tarjeta-credito.html',
  'vender-usd.html',
  'sitemap.xml',
  'llms.txt',
  'llms-full.txt',
  'robots.txt',
]);

const KEEP_DIRS = new Set(['guia']);

let deleted = 0;
const entries = fs.readdirSync(pubDir, { withFileTypes: true });

for (const entry of entries) {
  const fullPath = path.join(pubDir, entry.name);

  if (entry.isDirectory()) {
    if (KEEP_DIRS.has(entry.name)) {
      // Clean guia - only keep vender-cupo-dolares.html
      const guiaFiles = fs.readdirSync(fullPath);
      for (const f of guiaFiles) {
        if (f !== 'vender-cupo-dolares.html') {
          fs.unlinkSync(path.join(fullPath, f));
          deleted++;
        }
      }
    } else {
      fs.rmSync(fullPath, { recursive: true, force: true });
      deleted++;
    }
  } else if (entry.name.endsWith('.html') || entry.name.endsWith('.txt') || entry.name.endsWith('.xml')) {
    if (!KEEP.has(entry.name)) {
      fs.unlinkSync(fullPath);
      deleted++;
    }
  } else {
    // Delete non-essential files (CSS, JS, images that aren't needed)
    if (!entry.name.startsWith('.')) {
      // Keep robots.txt, sitemap.xml, llms.txt etc
    }
  }
}

// Count what's left
const remaining = fs.readdirSync(pubDir, { withFileTypes: true });
let count = 0;
for (const e of remaining) {
  if (e.isFile()) count++;
  if (e.isDirectory()) {
    count += fs.readdirSync(path.join(pubDir, e.name)).length;
  }
}

console.log(`Deleted: ${deleted} items`);
console.log(`Remaining in public/: ${count} items`);

// List remaining
const final = fs.readdirSync(pubDir);
console.log('Files:', final.join(', '));
