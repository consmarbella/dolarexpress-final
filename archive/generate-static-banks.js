import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, 'public');
const baseUrl = 'https://dolarexpress.cl';

// ─── BANK DATA ───
const BANKS = {
  'banco-chile': { name: 'Banco de Chile', color: '#003366', slug: 'banco-chile' },
  'banco-estado': { name: 'BancoEstado', color: '#E30613', slug: 'banco-estado' },
  'santander': { name: 'Santander', color: '#EC0000', slug: 'santander' },
  'bci': { name: 'BCI', color: '#003DA5', slug: 'bci' },
  'scotiabank': { name: 'Scotiabank', color: '#003399', slug: 'scotiabank' },
  'bbva': { name: 'BBVA', color: '#D52B1E', slug: 'bbva' },
  'itau': { name: 'Itaú', color: '#002F6C', slug: 'itau' },
  'internacional': { name: 'Internacional', color: '#004B87', slug: 'internacional' },
};

const RETAIL = {
  'cmr': { name: 'CMR Falabella', color: '#007F3E', slug: 'cmr' },
  'cencosud': { name: 'Cencosud', color: '#00519E', slug: 'cencosud' },
  'ripley': { name: 'Ripley', color: '#672C91', slug: 'ripley' },
  'lider': { name: 'Lider BCI', color: '#0A66C2', slug: 'lider' },
  'paris': { name: 'Paris', color: '#E31837', slug: 'paris' },
  'la-polar': { name: 'La Polar', color: '#003B71', slug: 'la-polar' },
  'hites': { name: 'Hites', color: '#DA291C', slug: 'hites' },
  'abcdin': { name: 'Abcdin', color: '#004B87', slug: 'abcdin' },
  'jumbo': { name: 'Jumbo', color: '#F48221', slug: 'jumbo' },
  'easy': { name: 'Easy', color: '#F5821F', slug: 'easy' },
};

function buildPage(title, description, h1, content, slug) {
  const today = new Date().toISOString().split('T')[0];
  return `<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
<meta name="description" content="${description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="${baseUrl}/${slug}">
<meta property="og:title" content="${title}">
<meta property="og:description" content="${description}">
<meta property="og:url" content="${baseUrl}/${slug}">
<meta property="og:type" content="website">
<meta property="og:image" content="${baseUrl}/og-image.svg">
<meta property="og:locale" content="es_CL">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FinancialService","name":"DolarExpress","description":"${description}","url":"${baseUrl}/${slug}","areaServed":{"@type":"Country","name":"Chile"},"currenciesAccepted":"CLP, USD","priceRange":"$$"}</script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;background:#f5f5f5;color:#1a1a1a;line-height:1.6}
.nav{background:#1a1a1a;padding:16px 24px;display:flex;justify-content:space-between;align-items:center}
.nav a{color:#C8A045;text-decoration:none;font-weight:bold;font-size:18px}
.nav .cta{background:#C8A045;color:#1a1a1a;padding:10px 20px;border-radius:8px;font-weight:bold;text-decoration:none;font-size:14px}
.hero{background:#1a1a1a;color:white;padding:60px 24px;text-align:center}
.hero h1{font-size:32px;margin-bottom:16px;max-width:700px;margin-left:auto;margin-right:auto}
.hero h1 span{color:#C8A045}
.hero p{color:#999;font-size:16px;max-width:500px;margin:0 auto 24px}
.hero .btn{display:inline-block;background:#C8A045;color:#1a1a1a;padding:14px 28px;border-radius:10px;font-weight:bold;text-decoration:none}
.content{max-width:800px;margin:0 auto;padding:40px 24px}
.content h2{font-size:24px;margin:32px 0 16px;color:#1a1a1a}
.content p{margin-bottom:16px;color:#555}
.content ul{margin:16px 0;padding-left:24px}
.content ul li{margin-bottom:8px;color:#555}
.cta-section{background:#1a1a1a;padding:60px 24px;text-align:center}
.cta-section h2{color:white;font-size:28px;margin-bottom:16px}
.cta-section .btn{display:inline-block;background:#C8A045;color:#1a1a1a;padding:14px 28px;border-radius:10px;font-weight:bold;text-decoration:none}
.footer{background:#1a1a1a;padding:32px 24px;text-align:center;border-top:1px solid #333}
.footer p{color:#666;font-size:12px}
.footer a{color:#C8A045;text-decoration:none;margin:0 8px}
.whatsapp{position:fixed;bottom:20px;right:20px;background:#25D366;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 15px rgba(37,211,102,0.3)}
</style>
</head>
<body>
<div class="nav">
  <a href="/">DolarExpress</a>
  <a href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo" class="cta">Vender Cupo →</a>
</div>
<div class="hero">
  <h1>${h1}</h1>
  <p>${description}</p>
  <a href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo" class="btn">Cotizar por WhatsApp</a>
</div>
<div class="content">
${content}
</div>
<div class="cta-section">
  <h2>¿Listo para vender tu cupo?</h2>
  <a href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo" class="btn">Cotizar por WhatsApp</a>
</div>
<div class="footer">
  <p>© ${new Date().getFullYear()} DolarExpress | <a href="/privacidad">Privacidad</a> | <a href="/contacto">Contacto</a></p>
</div>
<a href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo" class="whatsapp" aria-label="WhatsApp">
  <svg width="24" height="24" fill="white" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.414-.884-.74-1.48-1.764-1.656-2.058-.173-.298-.017-.456.132-.604.13-.13.296-.348.444-.52.149-.172.198-.298.296-.495.099-.198.051-.372-.022-.52-.074-.149-.668-1.614-.918-2.205-.24-.584-.485-.503-.668-.51-.173-.007-.371-.01-.57-.01-.198 0-.52.074-.793.372-.272.297-1.036 1.016-1.036 2.48s1.065 2.874 1.215 3.074c.148.2 2.09 3.198 5.073 4.489.704.307 1.26.49 1.694.627.71.227 1.356.193 1.87.119.574-.086 1.756-.718 2.007-1.414.248-.696.248-1.29.172-1.414-.074-.124-.273-.198-.57-.348z"/></svg>
</a>
</body>
</html>`;
}

// Generate bank pages
const allEntities = { ...BANKS, ...RETAIL };
let sitemapUrls = [];

for (const [key, entity] of Object.entries(allEntities)) {
  const title = `Vender cupo ${entity.name} | DolarExpress`;
  const desc = `Vende tu cupo en dólares de ${entity.name}. Te compramos tu cupo internacional al instante. Transferencia en 15 minutos.`;
  const h1 = `Vende tu cupo <span>${entity.name}</span> al instante`;
  const content = `
    <h2>Vender cupo ${entity.name}</h2>
    <p>En DolarExpress te compramos el cupo internacional de tu tarjeta ${entity.name}. Transforma ese cupo en dólares en pesos chilenos y recibe el dinero en tu cuenta bancaria en menos de 15 minutos.</p>
    <p>No necesitas tener avance en efectivo habilitado. Usamos tu cupo de compras internacional para darte liquidez inmediata.</p>
    
    <h2>¿Cómo funciona?</h2>
    <ol>
      <li><strong>Cotiza:</strong> Contáctanos por WhatsApp y dime el monto que quieres vender.</li>
      <li><strong>Validamos:</strong> Verificamos tu identidad mediante un proceso seguro.</li>
      <li><strong>Recibe:</strong> Transferencia bancaria a tu cuenta en menos de 15 minutos.</li>
    </ol>
    
    <h2>Beneficios de vender con nosotros</h2>
    <ul>
      <li>Tasa del 85% (comisión solo 15%)</li>
      <li>Transferencia en 15 minutos</li>
      <li>Sin avance habilitado</li>
      <li>Sin papeleos ni filas</li>
      <li>100% online por WhatsApp</li>
    </ul>
    
    <h2>¿Por qué ${entity.name}?</h2>
    <p>Si tienes una tarjeta ${entity.name} con cupo internacional disponible, puedes venderlo hoy mismo. Trabajamos con todas las tarjetas bancarias y retail de Chile.</p>
  `;
  
  const html = buildPage(title, desc, h1, content, key);
  const filePath = path.join(publicDir, `${key}.html`);
  fs.writeFileSync(filePath, html);
  console.log(`  ✅ ${key}.html (${entity.name})`);
  sitemapUrls.push(`    <loc>${baseUrl}/${key}</loc>`);
}

console.log(`\n✅ Generadas ${Object.keys(allEntities).length} páginas de banco/tarjeta`);

// ─── CONTENT PAGES ───
const contentPages = {
  'prestamo-rapido': { t: 'Préstamo Rápido Online', h: 'Préstamo rápido online sin dicom', kw: 'préstamo rápido' },
  'necesito-plata-hoy': { t: 'Necesito Plata Hoy', h: 'Necesito plata hoy: soluciones al instante', kw: 'necesito plata' },
  'dinero-urgente': { t: 'Dinero Urgente', h: 'Dinero urgente: obtén efectivo hoy mismo', kw: 'dinero urgente' },
  'liquidez-inmediata': { t: 'Liquidez Inmediata', h: 'Liquidez inmediata con tu tarjeta de crédito', kw: 'liquidez' },
  'efectivo-inmediato': { t: 'Efectivo Inmediato', h: 'Efectivo inmediato: vende tu cupo en dólares', kw: 'efectivo inmediato' },
  'prestamo-online': { t: 'Préstamo Online | Sin Dicom', h: 'Préstamo online sin dicom ni aval', kw: 'préstamo online' },
  'sacar-plata-tarjeta': { t: 'Sacar Plata de Tarjeta de Crédito', h: 'Sacar plata de tarjeta de crédito al instante', kw: 'sacar plata tarjeta' },
  'cupo-dolar-a-pesos': { t: 'Cupo Dólar a Pesos Chilenos', h: 'Convierte tu cupo dólar a pesos chilenos', kw: 'cupo dolar a pesos' },
  'cupo-dolar-urgente': { t: 'Cupo Dólar Urgente', h: 'Vende tu cupo dólar urgente: recibe plata hoy', kw: 'cupo dolar urgente' },
  'cupo-dolar-transferencia-inmediata': { t: 'Cupo Dólar Transferencia Inmediata', h: 'Cupo dólar con transferencia inmediata a tu cuenta', kw: 'cupo dolar transferencia inmediata' },
  'cupo-dolar-whatsapp': { t: 'Vender Cupo Dólar por WhatsApp', h: 'Vende tu cupo dólar por WhatsApp de forma segura', kw: 'cupo dolar whatsapp' },
  'cupo-dolar-sin-avance': { t: 'Cupo Dólar Sin Avance Habilitado', h: 'Vende tu cupo dólar sin tener avance habilitado', kw: 'cupo dolar sin avance' },
};

for (const [key, page] of Object.entries(contentPages)) {
  const title = `${page.t} | DolarExpress`;
  const desc = `¿${page.t}? En DolarExpress te ayudamos. ${page.h.replace(/<[^>]+>/g,'')}. Transferencia en 15 minutos.`;
  const content = `
    <h2>${page.t}</h2>
    <p>En DolarExpress te ofrecemos la solución más rápida para obtener liquidez. Vendemos tu cupo en dólares y te transferimos el dinero a tu cuenta bancaria en menos de 15 minutos.</p>
    <p>No necesitas avance habilitado, no hay papeleos ni filas. Todo se hace por WhatsApp, desde donde estés.</p>
    <h2>¿Por qué elegir DolarExpress?</h2>
    <ul>
      <li>Tasa del 85% (comisión solo 15%)</li>
      <li>Transferencia en 15 minutos</li>
      <li>Sin avance habilitado</li>
      <li>Sin dicom ni aval</li>
      <li>Aceptamos todas las tarjetas: CMR, Cencosud, Ripley, Lider BCI, y bancarias</li>
    </ul>
    <h2>¿Cómo funciona?</h2>
    <ol>
      <li><strong>Cotiza:</strong> Contáctanos por WhatsApp y dime cuánto necesitas.</li>
      <li><strong>Validamos:</strong> Verificamos tu identidad mediante un proceso seguro.</li>
      <li><strong>Recibe:</strong> Transferencia bancaria a tu cuenta en minutos.</li>
    </ol>
  `;
  const html = buildPage(title, desc, `<span>${page.h}</span>`, content, key);
  fs.writeFileSync(path.join(publicDir, `${key}.html`), html);
  console.log(`  ✅ ${key}.html`);
  sitemapUrls.push(`    <loc>${baseUrl}/${key}</loc>`);
}

// Regenerate sitemap with all URLs
const today = new Date().toISOString().split('T')[0];
const flatPages = [...Object.keys(allEntities), ...Object.keys(contentPages)];
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>${baseUrl}/</loc><lastmod>${today}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
${flatPages.map(k => `  <url><loc>${baseUrl}/${k}</loc><lastmod>${today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>`).join('\n')}
</urlset>`;
fs.writeFileSync(path.join(publicDir, 'sitemap.xml'), sitemap);

console.log(`\n✅ Total: ${Object.keys(allEntities).length + Object.keys(contentPages).length} páginas generadas`);
console.log(`✅ Sitemap regenerado`);
