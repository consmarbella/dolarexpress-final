import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';

const Home: React.FC = () => {
  useEffect(() => {
    document.title = "DolarExpress | Compra y Venta de Cupo en Dólares al Instante";
    const metaDescription = document.querySelector('meta[name="description"]');
    const description = "Servicio de compra y venta de cupo en dólares de tarjetas de crédito en Chile. Convertimos tu cupo internacional a pesos chilenos con transferencia inmediata.";
    if (metaDescription) {
      metaDescription.setAttribute('content', description);
    } else {
      const meta = document.createElement('meta');
      meta.name = 'description';
      meta.content = description;
      document.head.appendChild(meta);

                  const bingMeta = document.createElement('meta');
                  bingMeta.name = 'msvalidate.01';
                  bingMeta.content = '48D05AE35E1829A92FF3852D903F02A';
                  document.head.appendChild(bingMeta);
    }
  }, []);

  const structuredData = [
    {
      "@context": "https://schema.org",
      "@type": "FinancialService",
      "name": "DolarExpress",
      "description": "Servicio de compra y venta de cupo en dólares de tarjetas de crédito. Convertimos tu cupo internacional a pesos chilenos con transferencia inmediata.",
      "url": "https://dolarexpress.cl",
      "areaServed": {
        "@type": "Country",
        "name": "Chile"
      },
      "currenciesAccepted": "CLP, USD",
      "paymentAccepted": "Credit Card",
      "priceRange": "$$"
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "¿Es legal vender mi cupo en dólares?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sí, es completamente legal. La venta de cupo internacional es una operación de compraventa de servicios o productos digitales. Usted utiliza su cupo para realizar una compra y nosotros le pagamos por ello. Es una transacción privada y legítima bajo la legislación chilena."
          }
        },
        {
          "@type": "Question",
          "name": "¿Cuánto demora la transferencia a mi cuenta?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "El proceso es inmediato. Una vez validada la operación de compra de cupo, la transferencia se realiza en menos de 15 minutos a su Cuenta RUT, Cuenta Corriente o Vista de cualquier banco en Chile."
          }
        },
        {
          "@type": "Question",
          "name": "¿Qué tarjetas aceptan para comprar cupo?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Compramos cupo de todas las tarjetas de crédito con cupo internacional emitidas en Chile, incluyendo CMR Falabella, Cencosud Scotiabank, Ripley, Lider Bci, y tarjetas bancarias (Banco de Chile, Santander, Itaú, Bci, etc.)."
          }
        }
      ]
    }
  ];

  return (
    <div className="min-h-screen flex flex-col font-sans text-[#1a1a1a]">
      {/* Schema.org Injection */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      
      {/* Navbar */}
      <nav className="fixed w-full z-50 bg-[#1a1a1a] shadow-sm border-b border-[#333]">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center max-w-6xl">
          <Link to="/" className="flex items-center gap-2" aria-label="Volver al inicio">
            <Logo className="h-16 w-auto object-contain" />
          </Link>
          <div className="flex gap-4 items-center">
            <Link to="/" className="font-medium text-white hover:text-[#C8A045] transition-colors hidden md:block">
              Inicio
            </Link>
            <Link
              to="/venta-usd"
              className="bg-[#C8A045] text-white px-5 py-2 rounded-lg font-bold hover:brightness-105 hover:-translate-y-0.5 transition-all shadow-md"
            >
              Vender Cupo
            </Link>
          </div>
        </div>
      </nav>
      
      {/* Hero Section */}
      <header className="pt-36 pb-24 bg-[#1a1a1a] text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1a1a] via-[#2a2a2a] to-[#1a1a1a] z-0"></div>
        <div className="container mx-auto px-4 text-center z-10 relative max-w-4xl">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 leading-tight">
            Compra y Venta de Cupo en Dólares: <br />
            <span className="text-[#C8A045]">Transfiere a tu Cuenta al Instante</span>
          </h1>
          <p className="text-xl md:text-2xl mb-10 opacity-90 text-gray-200">
            ¿Necesitas efectivo? <strong>Compramos tu cupo dólar</strong> con la mejor tasa del mercado. Transferencias seguras en minutos a todo Chile.
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
      
      {/* Trust Section */}
      <section className="py-10 bg-white border-b border-gray-100" aria-label="Tarjetas aceptadas">
        <div className="container mx-auto px-4 max-w-6xl">
          <p className="text-center text-gray-400 text-sm font-semibold uppercase tracking-wider mb-8">Compramos cupo de todas estas tarjetas</p>
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-80 grayscale hover:grayscale-0 transition-all duration-500">
            <span className="text-2xl font-bold text-[#1A1F71]">VISA</span>
            <span className="text-2xl font-bold text-[#EB001B]">Mastercard</span>
            <span className="text-2xl font-bold text-[#007F3E]">CMR Falabella</span>
            <span className="text-2xl font-bold text-[#00519E]">Cencosud</span>
            <span className="text-2xl font-bold text-[#672C91]">Ripley</span>
          </div>
        </div>
      </section>
      
      {/* Main Content & SEO Strategy */}
      <main className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 max-w-4xl text-gray-700 leading-relaxed">
          <article>
            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6">¿Cómo cambiar cupo dólar a pesos chilenos?</h2>
            <p className="mb-6 text-lg">
              Si estás buscando <strong>dónde compran cupo en dólares</strong> de forma segura y rápida, DolarExpress es tu solución. Nos especializamos en la <strong>compra de cupo internacional</strong> de tarjetas de crédito, permitiéndote transformar ese saldo digital en dinero en efectivo (transferencia bancaria) sin los altos intereses de un avance en efectivo tradicional.
            </p>
            <p className="mb-6">
               Nuestro servicio es ideal para obtener liquidez inmediata utilizando el cupo disponible de tu tarjeta de crédito Visa o Mastercard emitida en Chile.
            </p>

            <div className="grid md:grid-cols-3 gap-6 my-12">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">1. Cotiza tu Cupo</h3>
                <p className="text-sm">Indícanos el monto en dólares que deseas vender. Te daremos una cotización transparente en pesos chilenos al instante.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">2. Verificación Segura</h3>
                <p className="text-sm">Validamos la operación mediante una pasarela segura para proteger tu identidad y prevenir fraudes.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">3. Recibe tus Pesos</h3>
                <p className="text-sm">Transferimos el dinero a tu cuenta bancaria (RUT, Corriente, Vista) en menos de 15 minutos.</p>
              </div>
            </div>

            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6 mt-16">Tarjetas de Crédito Compatibles</h2>
            <p className="mb-6">
              Aceptamos la mayoría de las tarjetas bancarias y del retail para la <strong>compra de cupo dólar</strong>. Las operaciones más frecuentes incluyen:
            </p>
            <ul className="list-disc pl-6 mb-8 space-y-2">
              <li><strong>Venta de cupo CMR Falabella:</strong> Convierte tu cupo internacional CMR en efectivo hoy.</li>
              <li><strong>Cambiar cupo Cencosud Scotiabank:</strong> Usa tu tarjeta Jumbo/Easy para obtener liquidez.</li>
              <li><strong>Banco Ripley y Lider Bci:</strong> También compramos cupo de estas tarjetas retail.</li>
              <li><strong>Bancos Tradicionales:</strong> Banco de Chile, Santander, Itaú, BancoEstado, Edwards, Security y Bice.</li>
            </ul>

            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6 mt-16">Seguridad en la Venta de Cupo</h2>
            <p className="mb-6">
              Entendemos que la seguridad es fundamental. Al realizar la <strong>venta de tu cupo en dólares</strong> con nosotros, operas bajo un modelo transparente y legal. Utilizamos tecnología SSL de 256 bits y nunca almacenamos los códigos de seguridad de tu tarjeta. Evita riesgos informales y opera con expertos en transacciones digitales.
            </p>
          </article>
        </div>
      </main>
      
      {/* FAQ Section */}
      <section className="py-16 bg-white border-t border-gray-100">
        <div className="container mx-auto px-4 max-w-3xl">
          <h2 className="text-3xl font-bold text-center text-[#1a1a1a] mb-12">Preguntas Frecuentes sobre Compra de Cupo</h2>
          <div className="space-y-6">
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿Es legal vender mi cupo en dólares?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>Sí, es completamente legal. Es una operación privada de compraventa de servicios digitales donde tú usas tu cupo internacional y nosotros te pagamos en pesos chilenos.</p>
              </div>
            </details>
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿Cuánto demora la transferencia?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>Generalmente menos de 15 minutos en horario hábil una vez validada la operación. Trabajamos con transferencia inmediata a la mayoría de bancos.</p>
              </div>
            </details>
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿Compran cupo de todas las tarjetas?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>Compramos cupo de tarjetas de crédito VISA y Mastercard emitidas en Chile que tengan cupo internacional disponible (cupo en dólares). Esto incluye CMR, Cencosud, Ripley y banca tradicional.</p>
              </div>
            </details>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="bg-[#1a1a1a] text-white py-12 mt-auto border-t border-[#333]">
        <div className="container mx-auto px-4 max-w-6xl text-center">
          <div className="relative w-40 h-16 mx-auto mb-6 opacity-90 flex justify-center items-center">
            <Logo className="h-full w-auto object-contain brightness-0 invert" lightMode={false} />
          </div>
          <div className="flex justify-center gap-6 mb-8 text-sm text-gray-400">
            <a href="#" className="hover:text-[#C8A045]">Términos y Condiciones</a>
            <a href="#" className="hover:text-[#C8A045]">Política de Privacidad</a>
            <a href="#" className="hover:text-[#C8A045]">Contacto</a>
          </div>
          <p className="text-xs text-gray-500 max-w-lg mx-auto leading-relaxed">
            © {new Date().getFullYear()} DolarExpress. Servicios financieros digitales líderes en Chile.
            <br />Especialistas en compra y venta de cupo dólar de manera segura.
          </p>
        </div>
      </footer>
      
      {/* WhatsApp Button Fixed */}
      <a
        href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo"
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 bg-[#25D366] w-14 h-14 rounded-full flex items-center justify-center text-white shadow-lg hover:bg-[#20ba5a] transition-colors md:hover:scale-110 md:animate-none animate-pulse-custom"
        aria-label="Contactar por WhatsApp para vender cupo"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" viewBox="0 0 16 16">
          <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z" />
        </svg>
      </a>
    </div>
  );
};

export default Home;
