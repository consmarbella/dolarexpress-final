const v=require('./vercel.json');
const vend=v.redirects.filter(r=>r.source && r.source.includes('vender-cupo-dolar'));

// Check specific URLs we want to KEEP (not redirect)
const keep = [
  '/vender-cupo-dolar-vitacura',
  '/vender-cupo-dolar-la-polar-recoleta',
  '/vender-cupo-dolar-lider'
];

keep.forEach(k => {
  const found = vend.find(r => r.source === k);
  console.log(`${k}: ${found ? 'REDIRECTED (BAD)' : 'NOT redirected (GOOD)'}`);
});

// Also check bank-specific vitacura pages
const bankVitacura = vend.filter(r => r.source.includes('vitacura'));
console.log('\nAll vitacura redirects:', bankVitacura.length);
bankVitacura.forEach(r => console.log('  ', r.source));