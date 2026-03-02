export interface PSEOPageData {
  slug: string;
  card: string;
  city: string;
  title: string;
  description: string;
}

const cards = ["CMR Falabella", "Cencosud", "Ripley", "Lider Bci"];
const cities = [
  "Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", 
  "Temuco", "Iquique", "Rancagua", "Puerto Montt", "Talca", 
  "Arica", "Chillán", "Copiapó", "Quillota", "Valdivia", 
  "Osorno", "Los Ángeles", "Calama", "Punta Arenas", "Viña del Mar"
];

export const pseoPages: PSEOPageData[] = [];

cards.forEach(card => {
  cities.forEach(city => {
    const cardSlug = card.toLowerCase().replace(/\s+/g, '-');
    const citySlug = city.toLowerCase().replace(/\s+/g, '-');
    const slug = `vender-cupo-${cardSlug}-${citySlug}`;
    
    pseoPages.push({
      slug,
      card,
      city,
      title: `Vender Cupo ${card} en ${city} | Efectivo al Instante`,
      description: `¿Necesitas liquidez en ${city}? Compramos tu cupo en dólares de tarjeta ${card}. Transferencia inmediata en 15 minutos. Seguro y rápido.`
    });
  });
});
