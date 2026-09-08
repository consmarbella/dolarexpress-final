const fs = require('fs');
const path = require('path');

const pubDir = path.join(__dirname, '..', 'public');

// PAGES TO KEEP - quality content with real value
const KEEP = new Set([
  // Core pages
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
  // Bank-specific (one per bank)
  'vender-cupo-banco-chile',
  'vender-cupo-banco-estado',
  'vender-cupo-bci',
  'vender-cupo-santander',
  'vender-cupo-scotiabank',
  'vender-cupo-itau',
  'vender-cupo-cmr-falabella',
  // Card-specific (retail, one per card)
  'vender-cupo-ripley-rapido',
  'vender-cupo-lider-santiago',
  'vender-cupo-paris-efectivo',
  'vender-cupo-hites-ahora',
  'vender-cupo-abcdin-urgente',
  'vender-cupo-easy-mismo-dia',
  // guia subdirectory
  'vender-cupo-dolares',
  // prestamos-santiago subdirectory
  'sacar-dinero-hites',
]);

// Patterns that are DEFINITELY doorway pages
const DOORWAY_PATTERNS = [
  /^avance-cupo-en-dolares-en-/,  // city pages
  /^cupo-en-dolares-en-/,         // city pages
  /^cupo-dolar-banco-chile-/,     // bank-city-card combos
  /^cupo-dolar-bancoestado-/,
  /^cupo-dolar-bbva-/,
  /^cupo-dolar-bci-/,
  /^cupo-dolar-bice-/,
  /^cupo-dolar-itau-/,
  /^cupo-dolar-santander-/,
  /^cupo-dolar-scotiabank-/,
  /^cupo-dolar-security-/,
  /^cupo-dolar-\d+/,              // amount pages (100, 200, 500, etc.)
  /^vender-cupo-dolar-[a-z]/,     // city-specific vender pages
];

// Synonym/thin pages that say the same thing
const THIN_SYNONYMS = [
  'cambiar-cupo-dolar',
  'cambiar-cupo-dolares-chile',
  'cambiar-cupo-tarjeta-efectivo',
  'cambiar-dolares-tarjeta',
  'cambio-cupo-dolar',
  'cambio-dolar-tarjeta',
  'cambio-dolares-tarjeta-credito',
  'compra-cupo-dolares',
  'comprar-cupo-dolar',
  'compro-cupo-dolar',
  'convertir-cupo-cmr-pesos-hoy',
  'convertir-cupo-dolar-pesos',
  'convertir-cupo-en-efectivo-chile',
  'convertir-cupo-internacional-pesos',
  'convertir-cupo-ripley-efectivo-rapido',
  'cupo-dolar-a-pesos',
  'cupo-dolar-disponible',
  'cupo-dolar-hoy-chile',
  'cupo-dolar-online',
  'cupo-dolar-rapido',
  'cupo-dolar-recomendado',
  'cupo-dolar-tiempo',
  'cupo-dolar-transferencia-inmediata',
  'cupo-dolar-urgente',
  'cupo-dolar-whatsapp',
  'cupo-dolares-tarjeta-credito',
  'cupo-internacional-pesos',
  'cupo-internacional-tarjeta-credito',
  'cupo-mastercard-pesos',
  'cupo-para-compras-a-efectivo-chile',
  'cupo-tarjeta-a-transferencia',
  'cupo-usd-a-clp',
  'dolar-tarjeta-pesos',
  'efectivo-cupo-dolar',
  'efectivo-rapido-cupo-cmr',
  'efectivo-rapido-cupo-ripley',
  'girar-cupo-dolares',
  'girar-dolares-tarjeta',
  'liquidez-cupo-dolar',
  'mejor-tasa-cupo-dolar',
  'necesito-pesos-tengo-dolares',
  'necesito-plata-tengo-cupo-cmr',
  'necesito-plata-tengo-cupo-ripley',
  'necesito-plata-y-tengo-cupo-en-tarjeta',
  'pagar-con-cupo-dolar',
  'pasar-cupo-de-compras-a-efectivo',
  'pasar-cupo-dolar-cuenta',
  'plata-rapida-con-tarjeta-retail-chile',
  'ripley-plata-al-tiro',
  'sacar-cupo-dolares',
  'servicios-cupo-dolar',
  'tarjeta-credito-cupo-dolar',
  'tarjeta-retail-efectivo-mismo-dia',
  'transferir-cupo-cmr-a-cuenta',
  'urgente-cupo-lider-efectivo',
  'urgente-cupo-paris-hoy',
  'venta-cupo-dolares',
  'vender-dolares-tarjeta-credito',
  'vender-dolares-tarjeta-visa',
  'vender-usd-chile',
];

// Pages about cards without avance - thin
const THIN_CARDS = [
  'avance-efectivo',
  'avance-efectivo-dolares',
  'avance-efectivo-sin-avance-habilitado',
  'avance-efectivo-tarjeta-abc',
  'avance-efectivo-tarjeta-cmr',
  'avance-efectivo-tarjeta-hites',
  'avance-efectivo-tarjeta-la-polar',
  'avance-efectivo-tarjeta-lider',
  'avance-efectivo-tarjeta-paris',
  'avance-efectivo-tarjeta-ripley',
  'avance-efectivo-tarjetas-grandes-tiendas-chile',
  'avance-la-polar-cuotas',
  'avance-lider-bci-online',
  'avance-ripley-cuotas',
  'avance-ripley-sin-tener-avance',
  'avance-tarjeta-dolares',
  'avance-tarjeta-easy',
  'avance-tarjeta-johnson',
  'avance-abc-visa',
  'avance-cmr-sin-avance-habilitado',
  'cupo-compras-a-efectivo-cmr',
  'cupo-compras-a-efectivo-lider',
  'cupo-compras-a-efectivo-ripley',
  'cupo-compras-efectivo-abcdin',
  'cupo-compras-efectivo-hites',
  'cupo-compras-efectivo-la-polar',
  'cupo-compras-efectivo-paris',
  'cupo-disponible-tarjeta-a-pesos',
  'cupo-dolar-american-express',
  'cupo-dolar-amex',
  'cupo-dolar-antofagasta',
  'cupo-dolar-arica',
  'cupo-dolar-calama',
  'cupo-dolar-cencosud-pesos',
  'cupo-dolar-chillan',
  'cupo-dolar-cmr-pesos',
  'cupo-dolar-cmr',
  'cupo-dolar-concepcion',
  'cupo-dolar-coopeuch',
  'cupo-dolar-copiapo',
  'cupo-dolar-cruz-verde',
  'cupo-dolar-iquique',
  'cupo-dolar-la-serena',
  'cupo-dolar-las-condes',
  'cupo-dolar-mastercard',
  'cupo-dolar-monto-minimo',
  'cupo-dolar-osorno',
  'cupo-dolar-providencia',
  'cupo-dolar-puerto-montt',
  'cupo-dolar-punta-arenas',
  'cupo-dolar-rancagua',
  'cupo-dolar-regiones-chile',
  'cupo-dolar-ripley-pesos',
  'cupo-dolar-ripley',
  'cupo-dolar-santiago',
  'cupo-dolar-sin-claves-bancarias',
  'cupo-dolar-sin-complicaciones',
  'cupo-dolar-sin-cuenta-bancaria',
  'cupo-dolar-sin-cuotas-internacionales',
  'cupo-dolar-sin-estafa',
  'cupo-dolar-sin-monto-minimo',
  'cupo-dolar-sin-usar',
  'cupo-dolar-talca',
  'cupo-dolar-tarjeta-bloqueada',
  'cupo-dolar-tarjeta-empresas',
  'cupo-dolar-temuco',
  'cupo-dolar-valdivia',
  'cupo-dolar-valparaiso',
  'cupo-dolar-vina-del-mar',
  'cupo-dolar-visa-gold',
  'cupo-dolar-visa-platinum',
  'cupo-dolar-visa-signature',
  'cupo-dolar-visa',
  'cupo-internacional-banco-chile',
  'cupo-internacional-bancoestado',
  'cupo-internacional-bci',
  'cupo-internacional-entel',
  'cupo-internacional-santander',
  'cupo-internacional-tarjeta',
  'como-obtener-liquidez-con-tarjeta-retail',
  'como-sacar-plata-si-no-tengo-avance',
  'como-usar-el-cupo-de-mi-tarjeta-sin-avance',
  'como-vender-cupo-dolar',
  'como-vender-cupo-tarjeta-credito',
  'comparador-tasas-cupo-dolar',
  'cuanto-me-dan-de-avance-tarjeta-lider',
  'cuanto-presta-la-cmr',
  'cuanto-presta-tarjeta-paris',
  'cuanto-presta-tarjeta-ripley',
  'hites-plata-rapido',
  'liquidar-cupo-abcdin-online',
  'liquidar-cupo-casa-comercial',
  'liquidar-cupo-cmr-efectivo',
  'liquidar-cupo-dolar',
  'liquidar-cupo-hites-transferencia',
  'liquidar-cupo-internacional',
  'liquidar-cupo-lider-hoy',
  'liquidar-cupo-paris-pesos',
  'liquidar-cupo-ripley-rapido',
  'liquidar-cupo-tarjeta-retail',
  'sacar-dinero-tarjeta-abc-din',
  'sacar-dinero-tarjeta-casa-comercial',
  'sacar-dinero-tarjeta-cmr-falabella',
  'sacar-dinero-tarjeta-hites',
  'sacar-dinero-tarjeta-jumbo',
  'sacar-dinero-tarjeta-la-polar',
  'sacar-dinero-tarjeta-lider',
  'sacar-dinero-tarjeta-paris',
  'sacar-dinero-tarjeta-ripley',
  'sacar-plata-cmr',
  'sacar-plata-de-tarjeta-de-tienda',
  'sacar-plata-ripley',
  'sacar-plata-tarjeta-abcdin',
  'sacar-plata-tarjeta-cencosud',
  'sacar-plata-tarjeta-hites',
  'sacar-plata-tarjeta-lider',
  'sacar-plata-tarjeta-polar',
  'superavance-cmr-falabella',
  'superavance-tarjeta-lider',
  'superavance-tarjeta-paris-cencosud',
  'tarjeta-abc-din-efectivo-rapido',
  'tarjeta-abc-sin-avance',
  'tarjeta-cmr-sin-avance',
  'tarjeta-hites-sin-avance',
  'tarjeta-la-polar-sin-avance',
  'tarjeta-lider-bci-efectivo-rapido',
  'tarjeta-lider-con-cupo-y-sin-avance',
  'tarjeta-lider-sin-avance',
  'tarjeta-paris-plata-rapido',
  'tarjeta-paris-sin-avance',
  'tarjeta-ripley-efectivo-inmediato',
  'tarjeta-ripley-sin-avance',
  'tarjeta-sin-avance-habilitado-chile',
  'cmr-efectivo-rapido',
  'banco-chile',
  'banco-estado',
  'bbva',
  'bci',
  'cencosud',
  'cmr',
  'easy',
  'hites',
  'internacional',
  'itau',
  'jumbo',
  'la-polar',
  'lider',
  'page1',
  'paris',
  'ripley',
  'santander',
  'scotiabank',
  'compra-usdc',
];

// Pages that should be noindex'd (kept but not indexed)
const NOINDEX_PAGES = new Set([
  'page1',
  'compra-usdc',
]);

function shouldDelete(name) {
  if (KEEP.has(name)) return false;
  if (THIN_SYNONYMS.includes(name)) return true;
  if (THIN_CARDS.includes(name)) return true;
  for (const pattern of DOORWAY_PATTERNS) {
    if (pattern.test(name)) return true;
  }
  return false;
}

let deleted = 0;
let noindexed = 0;
let kept = 0;

// Delete files and directories
function cleanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'guia' || entry.name === 'prestamos-santiago') {
        // Clean subdirectories too
        cleanDir(fullPath);
        continue;
      }
      const baseName = entry.name;
      if (shouldDelete(baseName)) {
        fs.rmSync(fullPath, { recursive: true, force: true });
        deleted++;
      }
    } else if (entry.name.endsWith('.html')) {
      const baseName = entry.name.replace('.html', '');
      if (shouldDelete(baseName)) {
        fs.unlinkSync(fullPath);
        deleted++;
      } else if (NOINDEX_PAGES.has(baseName)) {
        // Add noindex to these pages
        let html = fs.readFileSync(fullPath, 'utf8');
        if (!html.includes('noindex')) {
          html = html.replace('<head>', '<head>\n<meta name="robots" content="noindex, follow">');
          fs.writeFileSync(fullPath, html, 'utf8');
          noindexed++;
        }
      } else {
        kept++;
      }
    }
  }
}

cleanDir(pubDir);

console.log(`Deleted: ${deleted} doorway/thin pages`);
console.log(`Noindexed: ${noindexed} pages`);
console.log(`Kept: ${kept} quality pages`);
