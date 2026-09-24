const fs=require('fs');
const vercel=JSON.parse(fs.readFileSync('vercel.json','utf8'));

const exclude = new Set([
  'vender-cupo-dolar-vitacura',
  'vender-cupo-dolar-la-polar-recoleta',
  'vender-cupo-dolar-lider'
]);

const xml=fs.readFileSync('public/sitemap.xml','utf8');
const urls=xml.match(/<loc>([^<]+)<\/loc>/g).map(u=>u.replace('<loc>','').replace('</loc>',''));

const redirectUrls = urls
  .filter(u => u.includes('vender-cupo-dolar') && !u.endsWith('/vender-cupo-dolar'))
  .map(u => u.replace('https://dolarexpress.cl/',''))
  .filter(s => !exclude.has(s))
  .filter(s => s.startsWith('vender-cupo-dolar-') && s !== 'vender-cupo-dolar');

console.log('Total a redirigir:', redirectUrls.length);

const newRedirects = redirectUrls.map(slug => ({
  source: '/' + slug,
  destination: '/vender-cupo-dolar',
  statusCode: 301
}));

vercel.redirects = [...vercel.redirects, ...newRedirects];

fs.writeFileSync('vercel.json', JSON.stringify(vercel, null, 2), 'utf8');
console.log('vercel.json actualizado con', newRedirects.length, 'redirects 301');