import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { pseoPages } from '../src/data/pseo-data.ts';
import Logo from '../components/Logo';

// Bank-specific data for unique content generation
const BANK_DATA: Record<string, { name: string; desc: string; fact: string; offices: string }> = {
  'banco-chile': { name: 'Banco de Chile', desc: 'el banco más grande del país con más de 2 millones de clientes', fact: 'Fue fundado en 1893 y es uno de los bancos más antiguos de Chile', offices: 'más de 200 sucursales a lo largo de Chile' },
  'bancoestado': { name: 'BancoEstado', desc: 'el banco estatal más grande de Chile con más de 3 millones de clientes', fact: 'Tiene la red de cajeros automáticos más extensa del país', offices: 'más de 350 sucursales en todo Chile' },
  'bci': { name: 'BCI', desc: 'uno de los bancos más innovadores de Chile con más de 1.5 millones de clientes', fact: 'Fue pionero en Chile con la banca digital y la app móvil', offices: 'más de 150 sucursales en Chile' },
  'santander': { name: 'Santander', desc: 'un banco internacional con fuerte presencia en Chile y más de 1.3 millones de clientes', fact: 'Santander fue el primer banco en Chile en ofrecer transferencias internacionales desde su app', offices: 'más de 120 sucursales en Chile' },
  'scotiabank': { name: 'Scotiabank', desc: 'un banco canadiense con presencia en Chile y más de 800 mil clientes', fact: 'Scotiabank opera con presencia en más de 50 países a nivel global', offices: 'más de 60 sucursales en Chile' },
  'itau': { name: 'Itaú', desc: 'el banco más grande de América Latina con presencia en Chile', fact: 'Itaú fue pionero en Chile con su programa de puntos LATAM Pass', offices: 'más de 80 sucursales en Chile' },
  'bice': { name: 'BICE', desc: 'un banco chileno con más de 40 años de experiencia', fact: 'BICE se destaca por su atención personalizada a cada cliente', offices: '20 sucursales en las principales ciudades de Chile' },
  'security': { name: 'Security', desc: 'un banco chileno especializado en banca privada y empresas', fact: 'Security se enfoca en clientes de altos ingresos con cupos preferenciales', offices: '30 sucursales en Chile' },
  'bbva': { name: 'BBVA', desc: 'un banco español con presencia en Chile', fact: 'BBVA tiene alianza con las principales aerolíneas del mundo', offices: 'más de 70 sucursales en Chile' },
};

function detectBank(slug: string): { key: string; name: string; desc: string; fact: string; offices: string } | null {
  for (const [key, data] of Object.entries(BANK_DATA)) {
    if (slug.includes(key)) return { key, ...data };
  }
  return null;
}

function detectCity(slug: string): string | null {
  const cities = ['santiago','concepcion','valparaiso','vina-del-mar','temuco','rancagua','antofagasta',
    'la-serena','puerto-montt','iquique','arica','chillan','calama','copiapo','osorno','talca',
    'valdivia','punta-arenas','las-condes','providencia','maipu','la-florida','penalolen',
    'nunoa','vitacura','lo-barnechea','recoleta','independencia','san-miguel','el-bosque',
    'quilicura','cerro-navia','renca','quinta-normal','estacion-central','linares','san-fernando',
    'san-antonio','santa-cruz','pichilemu','villaricca','pucon','castro','ancud','quellon',
    'osorno','la-union','rio-bueno','frutillar','puerto-varas','llanquihue'];
  for (const c of cities) {
    if (slug.includes(c)) return c;
  }
  return null;
}

function detectCardType(slug: string): string | null {
  const cards: Record<string, string> = {
    'visa-gold': 'Visa Gold',
    'visa-platinum': 'Visa Platinum',
    'visa-signature': 'Visa Signature',
    'mastercard-gold': 'Mastercard Gold',
    'mastercard-black': 'Mastercard Black',
    'mastercard-platinum': 'Mastercard Platinum',
    'amex': 'American Express',
    'cmr': 'CMR Falabella',
    'ripley': 'Ripley',
    'falabella': 'Falabella',
    'lider': 'Líder BCI',
  };
  for (const [key, name] of Object.entries(cards)) {
    if (slug.includes(key)) return name;
  }
  return null;
}

function slugToTitle(slug: string): string {
  return slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

const cityNames: Record<string, string> = {
  'santiago': 'Santiago', 'concepcion': 'Concepción', 'valparaiso': 'Valparaíso',
  'vina-del-mar': 'Viña del Mar', 'temuco': 'Temuco', 'rancagua': 'Rancagua',
  'antofagasta': 'Antofagasta', 'la-serena': 'La Serena', 'puerto-montt': 'Puerto Montt',
  'iquique': 'Iquique', 'arica': 'Arica', 'chillan': 'Chillán',
};

function generateUniqueMeta(page: { slug: string; title: string; card?: string; city?: string }): { title: string; description: string } {
  const parts = page.slug.split('/');
  const lastPart = parts[parts.length - 1] || page.slug;
  const bank = detectBank(lastPart);
  const cardType = detectCardType(lastPart);

  if (bank) {
    const citySlug = detectCity(lastPart);
    const cityName = citySlug ? (cityNames[citySlug] || slugToTitle(citySlug)) : '';
    const base = cityName ? ` en ${cityName}` : '';
    return {
      title: `Cupo Dólar ${bank.name}${base} | DolarExpress`,
      description: cityName
        ? `¿Tenés tarjeta ${bank.name} en ${cityName} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.fact}.`
        : `¿Tenés tarjeta ${bank.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.fact}.`,
    };
  }

  if (cardType) return { title: `Cupo Dólar ${cardType} a Pesos | DolarExpress`, description: `¿Tenés tarjeta ${cardType} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.` };
  if (lastPart.startsWith('avance')) return { title: slugToTitle(lastPart) + ' | DolarExpress', description: `¿Necesitás ${slugToTitle(lastPart).toLowerCase()}? Te compramos tu cupo en dólares y te transferimos al instante.` };
  return { title: page.title, description: `Compramos tu cupo en dólares en Chile. Transferencia inmediata y segura.` };
}

function generateUniqueContent(slug: string): { paragraph1: string; paragraph2: string; tip: string } {
  const bank = detectBank(slug);
  const citySlug = detectCity(slug);
  const cityName = citySlug ? (cityNames[citySlug] || slugToTitle(citySlug)) : 'tu ciudad';
  const cardType = detectCardType(slug);

  if (bank) {
    return {
      paragraph1: `${bank.name} es ${bank.desc}. ${bank.fact}. Si tenés una tarjeta de crédito de ${bank.name} con cupo internacional disponible en ${cityName}, nosotros te lo compramos al instante. El proceso es 100% online y no requiere que vayas a ninguna sucursal.`,
      paragraph2: `${bank.name} cuenta con ${bank.offices}. Si estás en ${cityName}, podés coordinar la operación completamente por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta en menos de 15 minutos.`,
      tip: `Dato de ${bank.name}: ${bank.fact}. Muchos clientes nos prefieren porque no necesitan ir al banzo ni hacer filas.`,
    };
  }

  if (cardType) {
    return {
      paragraph1: `¿Tenés una tarjeta ${cardType} en ${cityName}? Nosotros te compramos el cupo en dólares al mejor tipo de cambio. El proceso es simple y rápido, sin papeleos ni trámites complicados.`,
      paragraph2: `Las tarjetas ${cardType} tienen cupo internacional disponible para compras en el extranjero. Ese mismo cupo podés convertirlo a pesos chilenos con nosotros. Te transferimos a tu cuenta en minutos.`,
      tip: `¿Sabías que muchas tarjetas como ${cardType} permiten usar el cupo internacional sin tener que activarlo? Verificá en tu app bancaria si tenés cupo disponible.`,
    };
  }

  if (citySlug && bank) {
    return {
      paragraph1: `En ${cityName}, trabajamos con todas las tarjetas bancarias y del retail. ${bank ? `${bank.name} es uno de los bancos más usados en ${cityName}.` : ''}`,
      paragraph2: `No importa dónde estés en ${cityName}, el proceso es 100% online. Te contactamos por WhatsApp, coordinamos la operación y recibís la transferencia en tu cuenta.`,
      tip: `¿Sabías que en ${cityName} muchas personas ya usaron nuestro servicio? El proceso es simple y seguro.`,
    };
  }

  return {
    paragraph1: 'En DolarExpress te ofrecemos la solución más rápida y segura para convertir tu cupo en dólares a pesos chilenos. Olvidate de los trámites bancarios tradicionales, las filas y los papeleos.',
    paragraph2: 'Trabajamos con todas las tarjetas de crédito chilenas: bancarias (Banco Chile, Santander, BCI, Scotiabank, Itaú, Security, BICE, BancoEstado) y retail (CMR Falabella, Ripley, Líder BCI, Cencosud, Paris, Jumbo, Easy, Hites, La Polar, ABC Din, Johnson).',
    tip: 'Muchas tarjetas retail como CMR, Ripley o Líder NO tienen avance en efectivo disponible. Nosotros usamos tu cupo de compras para darte efectivo al instante.',
  };
}

const PSEOPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const pageData = pseoPages.find(p => p.slug === slug);

  useEffect(() => {
    if (pageData) {
      const meta = generateUniqueMeta(pageData);
      document.title = meta.title;

      const metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) {
        metaDesc.setAttribute('content', meta.description);
      } else {
        const m = document.createElement('meta');
        m.name = 'description';
        m.content = meta.description;
        document.head.appendChild(m);
      }

      // Canonical
      let canonical = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
      if (!canonical) {
        canonical = document.createElement('link');
        canonical.rel = 'canonical';
        document.head.appendChild(canonical);
      }
      canonical.href = `https://dolarexpress.cl/${pageData.slug}`;
    }
  }, [pageData]);

  if (!pageData) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#1a1a1a] text-white">
        <h1 className="text-2xl font-bold">Página no encontrada</h1>
        <p className="text-gray-400 mt-2">La página que buscas no existe</p>
        <Link to="/" className="text-[#C8A045] mt-4 hover:underline">Volver al inicio</Link>
      </div>
    );
  }

  const meta = generateUniqueMeta(pageData);
  const title = meta.title.replace(' | DolarExpress', '');
  const whatsappText = `Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20${encodeURIComponent(title)}`;
  const uniqueContent = generateUniqueContent(pageData.slug);

  // Generate interlinking URLs from same category
  const slugLower = slug?.toLowerCase() || '';
  const related = pseoPages
    .filter(p => {
      if (p.slug === slug) return false;
      if (slugLower.includes('banco') || slugLower.includes('bci') || slugLower.includes('santander') || slugLower.includes('scotiabank') || slugLower.includes('itau')) {
        return p.slug.includes('cupo-dolar-') && !p.slug.includes('/');
      }
      return false;
    })
    .slice(0, 6);

  return (
    <div className="min-h-screen flex flex-col font-sans text-[#1a1a1a]">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "FinancialService",
            name: title,
            description: meta.description,
            url: `https://dolarexpress.cl/${pageData.slug}`,
            provider: { "@type": "Organization", name: "DolarExpress", url: "https://dolarexpress.cl" },
            areaServed: { "@type": "Country", name: "Chile" },
          }),
        }}
      />

      {/* Navbar */}
      <nav className="fixed w-full z-50 bg-[#1a1a1a] shadow-sm border-b border-[#333]">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center max-w-6xl">
          <Link to="/" className="flex items-center gap-2">
            <Logo className="h-16 w-auto object-contain" />
          </Link>
          <div className="flex gap-4 items-center">
            <Link to="/" className="font-medium text-white hover:text-[#C8A045] hidden md:block">Inicio</Link>
            <Link to="/directorio-general" className="font-medium text-white hover:text-[#C8A045] hidden md:block">Directorio</Link>
            <a
              href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20Vender%20Cupo"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#C8A045] text-white px-5 py-2 rounded-lg font-bold"
            >
              Vender Cupo
            </a>
          </div>
        </div>
      </nav>

      {/* Breadcrumbs */}
      <nav className="pt-24 pb-2 bg-[#1a1a1a] text-gray-400 text-sm" aria-label="Breadcrumb">
        <div className="container mx-auto px-4 max-w-6xl">
          <ol className="flex flex-wrap gap-1">
            <li><Link to="/" className="hover:text-[#C8A045]">Inicio</Link></li>
            <li className="mx-1">/</li>
            <li className="text-white truncate max-w-[300px]" aria-current="page">{title}</li>
          </ol>
        </div>
      </nav>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            itemListElement: [
              { "@type": "ListItem", position: 1, name: "Inicio", item: "https://dolarexpress.cl/" },
              { "@type": "ListItem", position: 2, name: title, item: `https://dolarexpress.cl/${pageData.slug}` },
            ],
          }),
        }}
      />

      {/* Hero Section */}
      <header className="pt-36 pb-24 bg-[#1a1a1a] text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1a1a] via-[#2a2a2a] to-[#1a1a1a] z-0"></div>
        <div className="container mx-auto px-4 text-center z-10 relative max-w-4xl">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 leading-tight">
            {title}
          </h1>
          <p className="text-xl md:text-2xl mb-10 opacity-90 text-gray-200">
            {meta.description}
          </p>
          <div className="flex justify-center gap-4">
            <a
              href={`https://wa.me/56967658939?text=${whatsappText}`}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#C8A045] text-white text-lg px-10 py-4 rounded-xl font-bold hover:shadow-[0_0_25px_rgba(200,160,69,0.5)] transition-all transform hover:scale-105"
            >
              Cotizar por WhatsApp
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 max-w-4xl text-gray-700 leading-relaxed">
          <article>
            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6">{title}</h2>
            <p className="mb-6 text-lg">{meta.description}</p>
            <p className="mb-6">{uniqueContent.paragraph1}</p>
            <p className="mb-6">{uniqueContent.paragraph2}</p>

            <div className="grid md:grid-cols-3 gap-6 my-12">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">1. Cotizá Ahora</h3>
                <p className="text-sm">Contactanos por WhatsApp y te mostramos la mejor tasa del mercado para tu cupo en dólares.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">2. Validación</h3>
                <p className="text-sm">Procesamos tu solicitud de forma segura. Sin compartir claves bancarias ni datos sensibles.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">3. Pago Inmediato</h3>
                <p className="text-sm">Recibís la transferencia en tu cuenta bancaria en menos de 15 minutos. Rápido, seguro y sin complicaciones.</p>
              </div>
            </div>

            <h3 className="text-2xl font-bold text-[#1a1a1a] mb-4">¿Por qué elegir DolarExpress?</h3>
            <ul className="list-disc pl-6 mb-8 space-y-2">
              <li><strong>Transferencia en 15 minutos:</strong> Coordinamos todo por WhatsApp y el dinero llega al instante a tu CuentaRUT o cuenta corriente.</li>
              <li><strong>Sin Dicom ni aval:</strong> No revisamos tu historial crediticio. Solo necesitás tener cupo disponible en tu tarjeta.</li>
              <li><strong>100% online:</strong> Todo desde tu celular, sin ir a sucursales, sin filas, sin papeleos.</li>
              <li><strong>Mejor tasa del mercado:</strong> Te mostramos la tasa antes de aceptar. Sin sorpresas, sin comisiones ocultas.</li>
              <li><strong>Seguro y transparente:</strong> Operamos con años de experiencia en el mercado chileno. Miles de operaciones realizadas.</li>
            </ul>

            <div className="bg-[#C8A045]/10 p-6 rounded-xl border border-[#C8A045]/30 my-8">
              <p className="text-lg font-semibold text-[#1a1a1a] mb-2">💡 ¿Sabías que...?</p>
              <p>{uniqueContent.tip}</p>
            </div>
          </article>
        </div>
      </main>

      {/* Related Services */}
      {related.length > 0 && (
        <section className="py-12 bg-white border-t border-gray-100">
          <div className="container mx-auto px-4 max-w-4xl">
            <h3 className="text-xl font-bold text-[#1a1a1a] mb-6">Servicios relacionados</h3>
            <div className="flex flex-wrap gap-3">
              {related.map(r => (
                <Link
                  key={r.slug}
                  to={`/${r.slug}`}
                  className="text-sm text-[#C8A045] bg-gray-50 border border-[#C8A045]/20 px-4 py-2 rounded-full hover:bg-[#C8A045] hover:text-white transition"
                >
                  {generateUniqueMeta(r).title.replace(' | DolarExpress', '')}
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="bg-[#1a1a1a] text-white py-12 mt-auto">
        <div className="container mx-auto px-4 max-w-6xl text-center">
          <div className="flex justify-center gap-6 mb-6 text-sm text-gray-400">
            <Link to="/" className="hover:text-[#C8A045]">Inicio</Link>
            <Link to="/directorio-general" className="hover:text-[#C8A045]">Directorio</Link>
            <Link to="/testimonios" className="hover:text-[#C8A045]">Testimonios</Link>
            <Link to="/preguntas-frecuentes" className="hover:text-[#C8A045]">FAQ</Link>
            <Link to="/privacidad" className="hover:text-[#C8A045]">Privacidad</Link>
            <Link to="/contacto" className="hover:text-[#C8A045]">Contacto</Link>
          </div>
          <p className="text-xs text-gray-500">
            © {new Date().getFullYear()} DolarExpress. Especialistas en compra de cupo en dólares.
          </p>
        </div>
      </footer>

      {/* WhatsApp Button Fixed */}
      <a
        href={`https://wa.me/56967658939?text=${whatsappText}`}
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 bg-[#25D366] w-14 h-14 rounded-full flex items-center justify-center text-white shadow-lg hover:bg-[#20ba5a] transition-colors md:hover:scale-110 md:animate-none animate-pulse-custom"
        aria-label="Contactar por WhatsApp"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" viewBox="0 0 16 16">
          <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z" />
        </svg>
      </a>
    </div>
  );
};

export default PSEOPage;
