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
      <div className="min-h-screen flex flex-col items-center justify-center">
        <h1 className="text-2xl font-bold">Página no encontrada</h1>
        <Link to="/" className="text-[#C8A045] mt-4">Volver al inicio</Link>
      </div>
    );
  }

  const structuredData = {
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "name": `DolarExpress ${pageData.city}`,
    "description": pageData.description,
    "url": `https://dolarexpress.cl/${pageData.slug}`,
    "areaServed": {
      "@type": "City",
      "name": pageData.city
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans text-[#1a1a1a]">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      
      {/* Navbar */}
      <nav className="fixed w-full z-50 bg-white/95 backdrop-blur-md shadow-sm border-b border-gray-100">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center max-w-6xl">
          <Link to="/" className="flex items-center gap-2">
            <Logo className="h-16 w-auto object-contain" />
          </Link>
          <div className="flex gap-4 items-center">
            <Link to="/" className="font-medium text-gray-600 hover:text-[#C8A045] hidden md:block">Inicio</Link>
            <Link to="/venta-usd" className="bg-[#C8A045] text-white px-5 py-2 rounded-lg font-bold">Vender Cupo</Link>
          </div>
        </div>
      </nav>
      
      {/* Hero Section */}
      <header className="pt-36 pb-24 bg-[#1a1a1a] text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1a1a] via-[#2a2a2a] to-[#1a1a1a] z-0"></div>
        <div className="container mx-auto px-4 text-center z-10 relative max-w-4xl">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 leading-tight">
            Vende tu Cupo <span className="text-[#C8A045]">{pageData.card}</span> en {pageData.city}
          </h1>
          <p className="text-xl md:text-2xl mb-10 opacity-90 text-gray-200">
            {pageData.description}
          </p>
          <div className="flex justify-center gap-4">
            <Link
              to="/venta-usd"
              className="bg-[#C8A045] text-white text-lg px-10 py-4 rounded-xl font-bold hover:shadow-[0_0_25px_rgba(200,160,69,0.5)] transition-all transform hover:scale-105"
            >
              Quiero Vender mi Cupo
            </Link>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 max-w-4xl text-gray-700 leading-relaxed">
          <article>
            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6">¿Cómo vender cupo {pageData.card} en {pageData.city}?</h2>
            <p className="mb-6 text-lg">
              En DolarExpress facilitamos la <strong>compra de cupo en dólares</strong> para residentes de {pageData.city}. Si tienes una tarjeta {pageData.card} con cupo internacional, puedes convertirlo en pesos chilenos de forma inmediata y segura.
            </p>
            <p className="mb-6">
              Nuestro proceso está diseñado para ser rápido y confiable, permitiéndote obtener liquidez sin las complicaciones de un avance en efectivo bancario tradicional.
            </p>

            <div className="grid md:grid-cols-3 gap-6 my-12">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">1. Cotiza en {pageData.city}</h3>
                <p className="text-sm">Contáctanos para recibir la mejor tasa del mercado para tu cupo {pageData.card}.</p>
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
            © {new Date().getFullYear()} DolarExpress. Especialistas en compra de cupo {pageData.card} en {pageData.city}.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default PSEOPage;
