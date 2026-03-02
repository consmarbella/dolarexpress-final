import fs from 'fs';

const cards = ["CMR Falabella", "Cencosud", "Ripley", "Lider Bci"];
const cities = [
  "Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", 
  "Temuco", "Iquique", "Rancagua", "Puerto Montt", "Talca", 
  "Arica", "Chillán", "Copiapó", "Quillota", "Valdivia", 
  "Osorno", "Los Ángeles", "Calama", "Punta Arenas", "Viña del Mar"
];

const baseUrl = 'https://dolarexpress.cl';
const urls = [
  `${baseUrl}/`,
  `${baseUrl}/venta-usd`
];

cards.forEach(card => {
  cities.forEach(city => {
    const cardSlug = card.toLowerCase().replace(/\s+/g, '-');
    const citySlug = city.toLowerCase().replace(/\s+/g, '-');
    urls.push(`${baseUrl}/vender-cupo-${cardSlug}-${citySlug}`);
  });
});

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(url => `  <url>
    <loc>${url}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${url === `${baseUrl}/` ? '1.0' : '0.8'}</priority>
  </url>`).join('\n')}
</urlset>`;

fs.writeFileSync('public/sitemap.xml', sitemap);
console.log('Sitemap generated successfully!');
