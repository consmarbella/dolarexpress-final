const v=require('./vercel.json');
const vend=v.redirects.filter(r=>r.source && r.source.includes('vender-cupo-dolar'));
console.log('Total redirects vender-cupo-dolar:', vend.length);
console.log('Examples:', vend.slice(0,5).map(r=>r.source));
const exceptions = vend.filter(r=>r.source.includes('vitacura') || r.source.includes('recoleta') || r.source.includes('/vender-cupo-dolar-lider'));
console.log('Exceptions found:', exceptions.length);