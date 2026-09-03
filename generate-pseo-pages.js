import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── Data definitions ──────────────────────────────────────────
const BANKS = {
  'banco-chile': { name: 'Banco de Chile', clients: 'más de 2 millones', fact: 'Fue fundado en 1893 y es uno de los bancos más antiguos de Chile', offices: 'más de 200 sucursales' },
  'banco-estado': { name: 'BancoEstado', clients: 'más de 3 millones', fact: 'Tiene la red de cajeros automáticos más extensa del país', offices: 'más de 350 sucursales' },
  'bci': { name: 'BCI', clients: 'más de 1.5 millones', fact: 'Fue pionero en Chile con la banca digital y la app móvil', offices: 'más de 150 sucursales' },
  'santander': { name: 'Santander', clients: 'más de 1.3 millones', fact: 'Santander fue el primer banco en Chile en ofrecer transferencias internacionales desde su app', offices: 'más de 120 sucursales' },
  'scotiabank': { name: 'Scotiabank', clients: 'más de 800 mil', fact: 'Scotiabank opera con presencia en más de 50 países a nivel global', offices: 'más de 60 sucursales' },
  'itau': { name: 'Itaú', clients: 'más de 900 mil', fact: 'Itaú fue pionero en Chile con su programa de puntos LATAM Pass', offices: 'más de 80 sucursales' },
  'bice': { name: 'BICE', clients: 'más de 40 años', fact: 'BICE se destaca por su atención personalizada a cada cliente', offices: '20 sucursales' },
  'security': { name: 'Security', clients: 'banca privada', fact: 'Security se enfoca en clientes de altos ingresos con cupos preferenciales', offices: '30 sucursales' },
  'bbva': { name: 'BBVA', clients: 'más de 600 mil', fact: 'BBVA tiene alianza con las principales aerolíneas del mundo', offices: 'más de 70 sucursales' },
};

const RETAILS = {
  'cmr': { name: 'CMR Falabella', clients: 'más de 1.5 millones', fact: 'CMR es la tarjeta retail más grande de Chile, aceptada en más de 100 mil comercios', offices: 'tiendas Falabella en todo Chile' },
  'ripley': { name: 'Ripley', clients: 'más de 1.2 millones', fact: 'Ripley tiene programa de puntos Duoc que acumulan en cada compra', offices: 'tiendas Ripley en principales ciudades' },
  'paris': { name: 'Paris', clients: 'más de 900 mil', fact: 'Paris pertenece al grupo Falabella y tiene promociones exclusivas en tiendas', offices: 'tiendas Paris en centros comerciales' },
  'lider': { name: 'Líder BCI', clients: 'más de 700 mil', fact: 'Líder BCI es la tarjeta del supermercado más grande de Chile', offices: 'supermercados Líder en todo Chile' },
  'hites': { name: 'Hites', clients: 'más de 500 mil', fact: 'Hites se especializa en crédito accesible con aprobación rápida', offices: 'tiendas Hites en zonas céntricas' },
  'jumbo': { name: 'Jumbo', clients: 'más de 600 mil', fact: 'Jumbo es la cadena de supermercados premium de Falabella', offices: 'tiendas Jumbo en sectores premium' },
  'easy': { name: 'Easy', clients: 'más de 400 mil', fact: 'Easy se especializa en productos para mejoramiento del hogar', offices: 'tiendas Easy en principales ciudades' },
  'la-polar': { name: 'La Polar', clients: 'más de 450 mil', fact: 'La Polar tiene más de 80 años de historia en el retail chileno', offices: 'tiendas La Polar en Chile' },
  'abc-din': { name: 'ABC Din', clients: 'más de 300 mil', fact: 'ABC Din es conocida por su fácil aprobación de crédito', offices: 'tiendas ABC Din en zonas comerciales' },
};

const CARD_TYPES = [
  { slug: 'visa-classic', name: 'Visa Classic' },
  { slug: 'visa-gold', name: 'Visa Gold' },
  { slug: 'visa-platinum', name: 'Visa Platinum' },
  { slug: 'visa-signature', name: 'Visa Signature' },
  { slug: 'mastercard-gold', name: 'Mastercard Gold' },
  { slug: 'mastercard-black', name: 'Mastercard Black' },
  { slug: 'mastercard-platinum', name: 'Mastercard Platinum' },
  { slug: 'american-express', name: 'American Express' },
  { slug: 'amex', name: 'Amex' },
];

const CITIES = [
  { slug: 'santiago', name: 'Santiago', region: 'Metropolitana' },
  { slug: 'concepcion', name: 'Concepción', region: 'Biobío' },
  { slug: 'valparaiso', name: 'Valparaíso', region: 'Valparaíso' },
  { slug: 'vina-del-mar', name: 'Viña del Mar', region: 'Valparaíso' },
  { slug: 'temuco', name: 'Temuco', region: 'La Araucanía' },
  { slug: 'rancagua', name: 'Rancagua', region: "O'Higgins" },
  { slug: 'antofagasta', name: 'Antofagasta', region: 'Antofagasta' },
  { slug: 'la-serena', name: 'La Serena', region: 'Coquimbo' },
  { slug: 'puerto-montt', name: 'Puerto Montt', region: 'Los Lagos' },
  { slug: 'iquique', name: 'Iquique', region: 'Tarapacá' },
  { slug: 'arica', name: 'Arica', region: 'Arica y Parinacota' },
  { slug: 'chillan', name: 'Chillán', region: 'Ñuble' },
  { slug: 'calama', name: 'Calama', region: 'Antofagasta' },
  { slug: 'copiapo', name: 'Copiapó', region: 'Atacama' },
  { slug: 'osorno', name: 'Osorno', region: 'Los Lagos' },
  { slug: 'talca', name: 'Talca', region: 'Maule' },
  { slug: 'valdivia', name: 'Valdivia', region: 'Los Ríos' },
  { slug: 'punta-arenas', name: 'Punta Arenas', region: 'Magallanes' },
  { slug: 'las-condes', name: 'Las Condes', region: 'Metropolitana' },
  { slug: 'providencia', name: 'Providencia', region: 'Metropolitana' },
  { slug: 'nunoa', name: 'Ñuñoa', region: 'Metropolitana' },
  { slug: 'vitacura', name: 'Vitacura', region: 'Metropolitana' },
  { slug: 'lo-barnechea', name: 'Lo Barnechea', region: 'Metropolitana' },
  { slug: 'maipu', name: 'Maipú', region: 'Metropolitana' },
  { slug: 'la-florida', name: 'La Florida', region: 'Metropolitana' },
  { slug: 'penalolen', name: 'Peñalolén', region: 'Metropolitana' },
  { slug: 'san-miguel', name: 'San Miguel', region: 'Metropolitana' },
  { slug: 'quilicura', name: 'Quilicura', region: 'Metropolitana' },
  { slug: 'recoleta', name: 'Recoleta', region: 'Metropolitana' },
  { slug: 'independencia', name: 'Independencia', region: 'Metropolitana' },
  { slug: 'el-bosque', name: 'El Bosque', region: 'Metropolitana' },
  { slug: 'cerro-navia', name: 'Cerro Navia', region: 'Metropolitana' },
  { slug: 'renca', name: 'Renca', region: 'Metropolitana' },
  { slug: 'quinta-normal', name: 'Quinta Normal', region: 'Metropolitana' },
  { slug: 'estacion-central', name: 'Estación Central', region: 'Metropolitana' },
  { slug: 'linares', name: 'Linares', region: 'Maule' },
  { slug: 'san-fernando', name: 'San Fernando', region: "O'Higgins" },
  { slug: 'san-antonio', name: 'San Antonio', region: 'Valparaíso' },
  { slug: 'santa-cruz', name: 'Santa Cruz', region: "O'Higgins" },
  { slug: 'pichilemu', name: 'Pichilemu', region: "O'Higgins" },
  { slug: 'villaricca', name: 'Villarrica', region: 'La Araucanía' },
  { slug: 'pucon', name: 'Pucón', region: 'La Araucanía' },
  { slug: 'castro', name: 'Castro', region: 'Los Lagos' },
  { slug: 'ancud', name: 'Ancud', region: 'Los Lagos' },
  { slug: 'quellon', name: 'Quellón', region: 'Los Lagos' },
  { slug: 'la-union', name: 'La Unión', region: 'Los Ríos' },
  { slug: 'rio-bueno', name: 'Río Bueno', region: 'Los Ríos' },
  { slug: 'frutillar', name: 'Frutillar', region: 'Los Lagos' },
  { slug: 'puerto-varas', name: 'Puerto Varas', region: 'Los Lagos' },
  { slug: 'llanquihue', name: 'Llanquihue', region: 'Los Lagos' },
  { slug: 'curico', name: 'Curicó', region: 'Maule' },
  { slug: 'coquimbo', name: 'Coquimbo', region: 'Coquimbo' },
  { slug: 'los-angeles', name: 'Los Ángeles', region: 'Biobío' },
];

const AVANCE_TYPES = [
  { slug: 'avance-en-efectivo', name: 'Avance en Efectivo' },
  { slug: 'avance-de-cupo-dolar', name: 'Avance de Cupo Dólar' },
  { slug: 'avance-internacional', name: 'Avance Internacional' },
  { slug: 'avance-rapido', name: 'Avance Rápido' },
  { slug: 'avance-urgente', name: 'Avance Urgente' },
  { slug: 'avance-sin-avance-habilitado', name: 'Avance Sin Avance Habilitado' },
  { slug: 'avance-con-tarjeta-de-credito', name: 'Avance con Tarjeta de Crédito' },
  { slug: 'avance-online', name: 'Avance Online' },
];

const VENDER_TYPES = [
  { slug: 'vender-cupo-dolar', name: 'Vender Cupo Dólar' },
  { slug: 'vender-cupo-internacional', name: 'Vender Cupo Internacional' },
  { slug: 'vender-dolares-tarjeta', name: 'Vender Dólares Tarjeta' },
];

// ── Helper ─────────────────────────────────────────────────────
function titleCase(s) {
  return s.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

// ── Generate entries ───────────────────────────────────────────
const entries = [];
const seen = new Set();

function esc(s) {
  return s.replace(/'/g, "\\'");
}

function add(slug, title, description) {
  if (seen.has(slug)) return;
  seen.add(slug);
  entries.push({ slug, title: esc(title), description: esc(description) });
}

// Bank pages
for (const [bk, bd] of Object.entries(BANKS)) {
  add(
    `cupo-dolar-${bk}`,
    `Cupo Dólar ${bd.name} | DolarExpress`,
    `¿Tenés tarjeta ${bd.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bd.fact}.`,
  );
  add(
    `vender-cupo-dolar-${bk}`,
    `Vender Cupo Dólar ${bd.name} | DolarExpress`,
    `Vendé tu cupo en dólares de ${bd.name}. Transferencia inmediata y segura. ${bd.fact}.`,
  );
}

// Retail pages
for (const [rk, rd] of Object.entries(RETAILS)) {
  add(
    `cupo-dolar-${rk}`,
    `Cupo Dólar ${rd.name} | DolarExpress`,
    `¿Tenés tarjeta ${rd.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.`,
  );
  add(
    `vender-cupo-dolar-${rk}`,
    `Vender Cupo Dólar ${rd.name} | DolarExpress`,
    `Vendé tu cupo en dólares de ${rd.name}. Transferencia inmediata y segura.`,
  );
}

// City pages
for (const c of CITIES) {
  add(
    `cupo-dolar-${c.slug}`,
    `Cupo Dólar en ${c.name} | DolarExpress`,
    `¿Tenés cupo en dólares en ${c.name}? Te lo compramos al instante. Transferencia en 15 minutos. Proceso 100% online.`,
  );
  add(
    `vender-cupo-dolar-${c.slug}`,
    `Vender Cupo Dólar en ${c.name} | DolarExpress`,
    `Vendé tu cupo en dólares en ${c.name}. Transferencia inmediata a tu cuenta. Seguro y 100% online.`,
  );
}

// Bank × City pages
for (const [bk, bd] of Object.entries(BANKS)) {
  for (const c of CITIES) {
    add(
      `cupo-dolar-${bk}-${c.slug}`,
      `Cupo Dólar ${bd.name} en ${c.name} | DolarExpress`,
      `¿Tenés tarjeta ${bd.name} en ${c.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bd.fact}.`,
    );
    add(
      `vender-cupo-dolar-${bk}-${c.slug}`,
      `Vender Cupo Dólar ${bd.name} en ${c.name} | DolarExpress`,
      `Vendé tu cupo en dólares de ${bd.name} en ${c.name}. Transferencia inmediata. ${bd.fact}.`,
    );
  }
}

// Retail × City pages
for (const [rk, rd] of Object.entries(RETAILS)) {
  for (const c of CITIES) {
    add(
      `cupo-dolar-${rk}-${c.slug}`,
      `Cupo Dólar ${rd.name} en ${c.name} | DolarExpress`,
      `¿Tenés tarjeta ${rd.name} en ${c.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.`,
    );
  }
}

// Card type pages
for (const ct of CARD_TYPES) {
  add(
    `cupo-dolar-${ct.slug}`,
    `Cupo Dólar ${ct.name} a Pesos | DolarExpress`,
    `¿Tenés tarjeta ${ct.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.`,
  );
}

// Bank × Card pages
for (const [bk, bd] of Object.entries(BANKS)) {
  for (const ct of CARD_TYPES) {
    add(
      `cupo-dolar-${bk}-${ct.slug}`,
      `Cupo Dólar ${bd.name} ${ct.name} | DolarExpress`,
      `¿Tenés tarjeta ${bd.name} ${ct.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bd.fact}.`,
    );
  }
}

// Bank × Card × City pages
for (const [bk, bd] of Object.entries(BANKS)) {
  for (const ct of CARD_TYPES) {
    for (const c of CITIES) {
      add(
        `cupo-dolar-${bk}-${ct.slug}-${c.slug}`,
        `Cupo Dólar ${bd.name} ${ct.name} en ${c.name} | DolarExpress`,
        `¿Tenés tarjeta ${bd.name} ${ct.name} en ${c.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bd.fact}.`,
      );
    }
  }
}

// Card × City pages
for (const ct of CARD_TYPES) {
  for (const c of CITIES) {
    add(
      `cupo-dolar-${ct.slug}-${c.slug}`,
      `Cupo Dólar ${ct.name} en ${c.name} | DolarExpress`,
      `¿Tenés tarjeta ${ct.name} en ${c.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.`,
    );
  }
}

// Avance pages
for (const at of AVANCE_TYPES) {
  add(
    at.slug,
    `${at.name} | DolarExpress`,
    `¿Necesitás ${at.name.toLowerCase()}? Te compramos tu cupo en dólares y te transferimos al instante.`,
  );
  for (const c of CITIES) {
    add(
      `${at.slug}-${c.slug}`,
      `${at.name} en ${c.name} | DolarExpress`,
      `¿Necesitás ${at.name.toLowerCase()} en ${c.name}? Te compramos tu cupo en dólares al instante.`,
    );
  }
  for (const [bk, bd] of Object.entries(BANKS)) {
    add(
      `${at.slug}-${bk}`,
      `${at.name} ${bd.name} | DolarExpress`,
      `¿Necesitás ${at.name.toLowerCase()} con ${bd.name}? Te compramos tu cupo en dólares al instante. ${bd.fact}.`,
    );
  }
}

// Existing entries to keep (read from current file)
const currentPath = path.join(__dirname, 'src', 'data', 'pseo-data.ts');
const currentContent = fs.readFileSync(currentPath, 'utf8');
const existingMatches = currentContent.matchAll(/slug: '([^']+)',\s*\n\s*title: '([^']+)',\s*\n\s*description: '([^']+)'/g);
for (const m of existingMatches) {
  add(m[1], m[2], m[3]);
}

// ── Write output ───────────────────────────────────────────────
const lines = [
  'export interface PSEOPageData {',
  '  slug: string;',
  '  card?: string;',
  '  city?: string;',
  '  title: string;',
  '  description: string;',
  '}',
  '',
  'export const pseoPages: PSEOPageData[] = [',
];

for (const e of entries) {
  lines.push('  {');
  lines.push(`    slug: '${e.slug}',`);
  lines.push(`    title: '${e.title}',`);
  lines.push(`    description: '${e.description}'`);
  lines.push('  },');
}

lines.push('];');
lines.push('');

const output = lines.join('\n');
fs.writeFileSync(currentPath, output, 'utf8');

console.log(`✅ Generated ${entries.length} PSEO entries`);
console.log(`📁 File: src/data/pseo-data.ts (${(Buffer.byteLength(output) / 1024).toFixed(0)} KB)`);
