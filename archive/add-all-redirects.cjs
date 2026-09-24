const fs=require('fs');
const path=require('path');

const vercel=JSON.parse(fs.readFileSync('vercel.json','utf8'));

const exclude = new Set([
  'vender-cupo-dolar-vitacura',
  'vender-cupo-dolar-la-polar-recoleta',
  'vender-cupo-dolar-lider'
]);

const publicDir = path.join(__dirname, 'public');
const files = fs.readdirSync(publicDir);

const redirectUrls = files
  .filter(f => f.startsWith('vender-cupo-dolar-') && f.endsWith('.html'))
  .map(f => f.replace('.html', ''))
  .filter(s => !exclude.has(s))
  .filter(s => s !== 'vender-cupo-dolar');

console.log('Total a redirigir:', redirectUrls.length);

const newRedirects = redirectUrls.map(slug => ({
  source: '/' + slug,
  destination: '/vender-cupo-dolar',
  statusCode: 301
}));

vercel.redirects = [...vercel.redirects, ...newRedirects];

fs.writeFileSync('vercel.json', JSON.stringify(vercel, null, 2), 'utf8');
console.log('vercel.json actualizado con', newRedirects.length, 'redirects 301');
console.log('Ejemplos:', redirectUrls.slice(0, 10));