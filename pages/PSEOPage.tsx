import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { pseoPages } from '../src/data/pseo-data.ts';
import Logo from '../components/Logo';

const PSEOPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const pageData = pseoPages.find(p => p.slug === slug);

  useEffect(() => {
    if (pageData) {
      document.title = pageData.title;
      const metaDescription = document.querySelector('meta[name="description"]');
      if (metaDescription) {
        metaDescription.setAttribute('content', pageData.description);
      } else {
        const meta = document.createElement('meta');
        meta.name = 'description';
        meta.content = pageData.description;
        document.head.appendChild(meta);
      }
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

  // Use generic content if card/city not provided
  const title = pageData.card && pageData.city 
    ? `Vende tu Cupo ${pageData.card} en ${pageData.city}`
    : 'Servicio de DolarExpress';
  
  const description = pageData.card && pageData.city
    ? `En DolarExpress facilitamos la compra de cupo en dólares para residentes de ${pageData.city}. Si tienes una tarjeta ${pageData.card} con cupo internacional, puedes convertirlo en pesos chilenos de forma inmediata y segura.`
    : 'Compramos tu cupo en dólares de tarjetas de crédito. Transferencia inmediata, segura y rápida.';

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": `DolarExpress`,
    "description": pageData.description,
    "url": `https://dolarexpress.cl/${pageData.slug}`,
    ...(pageData.city && {
      "areaServed": {
        "@type": "City",
        "name": pageData.city
      }
    })
  };

  return (
    <div className="min-h-screen flex flex-col font-sans text-[#1a1a1a]">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
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
            <li className="text-white truncate max-w-[300px]" aria-current="page">
              {pageData ? pageData.title.replace(' | DolarExpress', '') : 'Pagina'}
            </li>
          </ol>
        </div>
      </nav>
      
      {/* Schema.org BreadcrumbList */}
      {pageData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "BreadcrumbList",
              "itemListElement": [
                { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://dolarexpress.cl/" },
                { "@type": "ListItem", "position": 2, "name": pageData.title.replace(' | DolarExpress', ''), "item": `https://dolarexpress.cl/${pageData.slug}` }
              ]
            })
          }}
        />
      )}
      
      {/* Hero Section */}
      <header className="pt-36 pb-24 bg-[#1a1a1a] text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1a1a] via-[#2a2a2a] to-[#1a1a1a] z-0"></div>
        <div className="container mx-auto px-4 text-center z-10 relative max-w-4xl">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 leading-tight">
            {title}
          </h1>
          <p className="text-xl md:text-2xl mb-10 opacity-90 text-gray-200">
            {pageData.description}
          </p>
          <div className="flex justify-center gap-4">
            <a
              href={`https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20${encodeURIComponent(pageData.title.replace(' | DolarExpress', ''))}`}
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
            <p className="mb-6 text-lg">{description}</p>
            <p className="mb-6">
              Nuestro proceso está diseñado para ser rápido y confiable, permitiéndote obtener liquidez sin las complicaciones de un avance en efectivo bancario tradicional.
            </p>

            <div className="grid md:grid-cols-3 gap-6 my-12">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">1. Cotiza Ahora</h3>
                <p className="text-sm">Contáctanos para recibir la mejor tasa del mercado para tu cupo en dólares.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">2. Validación</h3>
                <p className="text-sm">Procesamos tu solicitud de forma segura a través de nuestra plataforma verificada.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">3. Pago Inmediato</h3>
                <p className="text-sm">Recibe tu transferencia en menos de 15 minutos en cualquier banco de Chile.</p>
              </div>
            </div>
          </article>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-[#1a1a1a] text-white py-12 mt-auto">
        <div className="container mx-auto px-4 max-w-6xl text-center">
          <p className="text-xs text-gray-500">
            © {new Date().getFullYear()} DolarExpress. Especialistas en compra de cupo en dólares.
          </p>
        </div>
      </footer>

      {/* WhatsApp Button Fixed */}
      <a
        href={`https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20${encodeURIComponent(pageData.title.replace(' | DolarExpress', ''))}`}
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
