import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';

const Home: React.FC = () => {
  useEffect(() => {
    document.title = "DolarExpress | Compramos tu Cupo en Dólares | Efectivo al Instante";

    // Canonical de la home
    let canonical = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.rel = 'canonical';
      document.head.appendChild(canonical);
    }
    canonical.href = 'https://dolarexpress.cl/';

    const metaDescription = document.querySelector('meta[name="description"]');
    const description = "Servicio de compra de cupo en dólares de tarjetas de crédito en Chile. Te compramos tu cupo internacional y te transferimos a pesos chilenos al instante.";
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
      "@type": "LocalBusiness",
      "name": "DolarExpress",
      "url": "https://dolarexpress.cl",
      "telephone": "+56967658939",
      "email": "contacto@dolarexpress.cl",
      "areaServed": { "@type": "Country", "name": "Chile" },
      "currenciesAccepted": "CLP, USD",
      "paymentAccepted": "Transferencia bancaria",
      "priceRange": "$$",
      "openingHours": "Mo-Fr 09:00-18:30"
    },
    {
      "@context": "https://schema.org",
      "@type": "FinancialService",
      "name": "DolarExpress",
      "description": "Servicio de compra de cupo en dólares de tarjetas de crédito. Te compramos tu cupo internacional y te transferimos a pesos chilenos al instante.",
      "url": "https://dolarexpress.cl",
      "areaServed": { "@type": "Country", "name": "Chile" },
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
          "acceptedAnswer": { "@type": "Answer", "text": "Sí, es completamente legal. Es una operación privada de compraventa regulada por el Código Civil chileno. No hay ninguna ley que lo prohíba." }
        },
        {
          "@type": "Question",
          "name": "¿Cuánto demora la transferencia?",
          "acceptedAnswer": { "@type": "Answer", "text": "El proceso completo toma aproximadamente 15-20 minutos. Una vez confirmada, la transferencia a tu cuenta es inmediata en horario hábil." }
        },
        {
          "@type": "Question",
          "name": "¿Qué necesito para vender mi cupo?",
          "acceptedAnswer": { "@type": "Answer", "text": "Solo necesitás tu cédula de identidad, una cuenta bancaria y cupo internacional disponible en tu tarjeta. No necesitás avance habilitado." }
        },
        {
          "@type": "Question",
          "name": "¿Aceptan tarjetas sin avance en efectivo?",
          "acceptedAnswer": { "@type": "Answer", "text": "Sí. Usamos tu cupo de compras internacional, no el avance. Funciona con CMR, Ripley, Líder y todas las tarjetas retail." }
        },
        {
          "@type": "Question",
          "name": "¿Cuánto puedo recibir por mi cupo?",
          "acceptedAnswer": { "@type": "Answer", "text": "Con comisión del 15%, por USD 100 de cupo recibís ~USD 85 en CLP. Un cupo de USD 1.000 puede darte más de $750.000. Cotizá sin compromiso." }
        },
        {
          "@type": "Question",
          "name": "¿En qué ciudades de Chile operan?",
          "acceptedAnswer": { "@type": "Answer", "text": "En todo Chile. Proceso 100% online por WhatsApp. Atendemos Santiago, regiones y todas las ciudades del país." }
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
            <Logo className="h-20 w-auto object-contain" lightMode={true} />
          </Link>
          <div className="flex gap-4 items-center">
            <Link to="/" className="font-medium text-white hover:text-[#C8A045] transition-colors hidden md:block">
              Inicio
            </Link>
            <a
              href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#C8A045] text-white px-5 py-2 rounded-lg font-bold hover:brightness-105 hover:-translate-y-0.5 transition-all shadow-md"
            >
              Vender Cupo
            </a>
          </div>
        </div>
      </nav>
      
      {/* Hero Section */}
      <header className="pt-36 pb-24 bg-[#1a1a1a] text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1a1a] via-[#2a2a2a] to-[#1a1a1a] z-0"></div>
        <div className="container mx-auto px-4 text-center z-10 relative max-w-4xl">
          <div className="inline-block bg-white/5 border border-[#C8A045]/30 rounded-xl px-8 py-4 mb-8">
            <span className="text-white text-2xl md:text-3xl font-bold">Comisión <span className="text-[#C8A045]">15%</span></span>
            <span className="text-gray-500 text-2xl md:text-3xl mx-3">·</span>
            <span className="text-white text-2xl md:text-3xl font-bold"><span className="text-[#C8A045]">+7 años</span> en el mercado</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 leading-tight">
            Compramos tu <span className="text-[#C8A045]">Cupo en Dólares</span>
          </h1>
          <p className="text-xl md:text-2xl mb-10 opacity-90 text-gray-200">
            ¿Necesitas efectivo? <strong>Compramos tu cupo dólar</strong>. Sin avance, sin papeleos. 100% online por WhatsApp.
          </p>
          <div className="flex justify-center gap-4">
            <a
              href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#C8A045] text-white text-lg px-10 py-4 rounded-xl font-bold hover:shadow-[0_0_25px_rgba(200,160,69,0.5)] transition-all transform hover:scale-105"
            >
              Quiero Vender mi Cupo
            </a>
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
              Con <strong>más de 7 años en el mercado chileno</strong>, somos uno de los servicios más confiables para convertir tu cupo en dólares a pesos. Nuestra comisión es de solo <strong>15%</strong> — una de las más competitivas del país. Sin costos ocultos, sin letra chica.
            </p>

            <div className="grid md:grid-cols-3 gap-6 my-12">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">1. Cotiza tu Cupo</h3>
                <p className="text-sm">Indícanos el monto en dólares que deseas vender. Te daremos una cotización transparente en pesos chilenos al instante, sin compromiso.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">2. Verificación Segura</h3>
                <p className="text-sm">Validamos la operación mediante una pasarela segura para proteger tu identidad y prevenir fraudes. Nunca te pedimos claves bancarias ni datos sensibles.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">3. Recibe tus Pesos</h3>
                <p className="text-sm">Transferimos el dinero a tu cuenta bancaria (RUT, Corriente, Vista). Proceso 100% online desde tu celular, sin moverte de tu casa.</p>
              </div>
            </div>

            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6 mt-16">¿Qué es el cupo en dólares y cómo funciona?</h2>
            <p className="mb-6">
              El <strong>cupo en dólares</strong> —también conocido como cupo internacional— es una línea de crédito adicional que viene incluida en la mayoría de las tarjetas Visa y Mastercard emitidas en Chile. Está diseñado para compras en el extranjero o en sitios internacionales como Amazon, AliExpress, Netflix o Spotify.
            </p>
            <p className="mb-6">
              Muchas personas no saben que tienen este cupo disponible. Si tenés una tarjeta de crédito hace más de 6 meses, es muy probable que tengas cientos o miles de dólares acumulados sin usar. Ese dinero puede convertirse a pesos chilenos hoy mismo.
            </p>

            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6 mt-16">¿Por qué elegir DolarExpress?</h2>
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#1a1a1a] mb-2">💰 Comisión 15% fija</h3>
                <p className="text-sm text-gray-600">Sin costos ocultos. Sabés exactamente cuánto recibís antes de aceptar. Una de las más bajas del mercado chileno.</p>
              </div>
              <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#1a1a1a] mb-2">🏆 +7 años de experiencia</h3>
                <p className="text-sm text-gray-600">Años en el mercado nos respaldan. Miles de operaciones realizadas con clientes en todo Chile.</p>
              </div>
              <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#1a1a1a] mb-2">🔒 100% seguro y transparente</h3>
                <p className="text-sm text-gray-600">No pedimos claves bancarias ni datos sensibles. Operás desde tu propia app. Transferencia trazable.</p>
              </div>
              <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#1a1a1a] mb-2">📱 Sin DICOM ni aval</h3>
                <p className="text-sm text-gray-600">No consultamos antecedentes comerciales. Solo necesitás tu cédula de identidad y cupo disponible en tu tarjeta.</p>
              </div>
            </div>

            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6 mt-16">Tarjetas de Crédito Compatibles</h2>
            <p className="mb-6">
              Trabajamos con <strong>todas las tarjetas de crédito Visa y Mastercard emitidas en Chile</strong> que tengan cupo internacional disponible. Esto incluye tarjetas bancarias y del retail.
            </p>
            <h3 className="font-bold text-lg mb-3 text-[#1a1a1a]">Tarjetas bancarias:</h3>
            <ul className="list-disc pl-6 mb-6 space-y-1 text-sm">
              <li><strong>Banco de Chile:</strong> Visa Signature, Mastercard Black, American Express — <Link to="/cupo-dolar-banco-chile" className="text-[#C8A045] hover:underline">ver más</Link></li>
              <li><strong>BancoEstado:</strong> Visa y Mastercard de crédito (no CuentaRUT) — <Link to="/cupo-dolar-banco-estado" className="text-[#C8A045] hover:underline">ver más</Link></li>
              <li><strong>Santander:</strong> WorldMember, LATAM Pass — <Link to="/cupo-dolar-santander" className="text-[#C8A045] hover:underline">ver más</Link></li>
              <li><strong>BCI:</strong> Visa Infinite, Mastercard Black — <Link to="/cupo-dolar-bci" className="text-[#C8A045] hover:underline">ver más</Link></li>
              <li><strong>Scotiabank, Itaú, BBVA, BICE, Security:</strong> todas las tarjetas de crédito con cupo internacional.</li>
            </ul>
            <h3 className="font-bold text-lg mb-3 text-[#1a1a1a]">Tarjetas retail:</h3>
            <ul className="list-disc pl-6 mb-8 space-y-1 text-sm">
              <li><strong>CMR Falabella:</strong> la tarjeta retail más grande de Chile — <Link to="/cupo-dolar-cmr" className="text-[#C8A045] hover:underline">ver más</Link></li>
              <li><strong>Ripley:</strong> con programa RipleyPuntos GO — <Link to="/cupo-dolar-ripley" className="text-[#C8A045] hover:underline">ver más</Link></li>
              <li><strong>Líder BCI, Cencosud, Paris, La Polar, Hites, ABCDin, Jumbo, Easy:</strong> todas aceptadas.</li>
            </ul>

            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6 mt-16">Vender cupo en dólares vs Avance en efectivo</h2>
            <p className="mb-6">
              Muchas personas confunden la <strong>venta de cupo en dólares</strong> con un avance en efectivo tradicional. Son cosas muy diferentes y conviene entenderlas:
            </p>
            <div className="overflow-x-auto mb-8">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-[#1a1a1a] text-white">
                    <th className="p-3 text-left rounded-tl-lg">Característica</th>
                    <th className="p-3 text-left">Vender cupo dólar</th>
                    <th className="p-3 text-left rounded-tr-lg">Avance en efectivo</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-200">
                    <td className="p-3 font-medium">Comisión / Interés</td>
                    <td className="p-3"><strong className="text-[#C8A045]">15% fijo</strong></td>
                    <td className="p-3">30% a 60% anual + comisión</td>
                  </tr>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <td className="p-3 font-medium">¿Necesito avance habilitado?</td>
                    <td className="p-3"><strong>No</strong></td>
                    <td className="p-3">Sí, hay que solicitarlo al banco</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-3 font-medium">¿Afecta historial crediticio?</td>
                    <td className="p-3"><strong>No directamente</strong></td>
                    <td className="p-3">Aparece como deuda en tu informe</td>
                  </tr>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <td className="p-3 font-medium">¿Piden DICOM?</td>
                    <td className="p-3"><strong>No</strong></td>
                    <td className="p-3">Sí, el banco evalúa tu historial</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-3 font-medium">Tiempo del proceso</td>
                    <td className="p-3"><strong>Mismo día</strong></td>
                    <td className="p-3">Puede tardar días hábiles</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-medium">¿Presencial?</td>
                    <td className="p-3"><strong>100% online</strong></td>
                    <td className="p-3">Requiere ir al banco o cajero</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6 mt-16">Seguridad en la Venta de Cupo</h2>
            <p className="mb-6">
              Entendemos que la seguridad es fundamental. Al realizar la <strong>venta de tu cupo en dólares</strong> con nosotros, operas bajo un modelo transparente y legal. Utilizamos tecnología de encriptación y nunca almacenamos los códigos de seguridad de tu tarjeta.
            </p>
            <p className="mb-6">
              La operación es una compraventa entre privados regulada por el Código Civil chileno. No hay intermediarios bancarios, no hay letra chica. Todo el proceso es trazable: recibís un comprobante y la transferencia queda registrada en tu cuenta bancaria. <Link to="/es-legal-vender-cupo-dolar" className="text-[#C8A045] hover:underline">Conocé más sobre la legalidad del proceso</Link>.
            </p>
            <p className="mb-6">
              <strong>Consejos de seguridad:</strong> Nunca compartas tus claves bancarias, CVV o contraseñas con nadie. En DolarExpress no te las pedimos. La operación la realizás vos mismo desde tu app o home banking. Nosotros solo te guiamos paso a paso.
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
                <p>Sí, es completamente legal. Es una operación privada de compraventa de servicios digitales regulada por el Código Civil chileno. No hay ninguna ley que prohíba vender el cupo internacional de tu tarjeta de crédito.</p>
              </div>
            </details>
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿Cuánto demora la transferencia?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>El proceso completo toma aproximadamente 15-20 minutos. Una vez confirmada la operación, la transferencia a tu cuenta bancaria es inmediata en horario hábil.</p>
              </div>
            </details>
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿Qué necesito para vender mi cupo?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>Solo necesitás tres cosas: tu cédula de identidad chilena vigente, una cuenta bancaria donde recibir la transferencia (CuentaRUT, corriente o vista), y cupo internacional disponible en tu tarjeta de crédito. No necesitás avance habilitado ni ir al banco.</p>
              </div>
            </details>
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿Aceptan tarjetas sin avance en efectivo?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>Sí. Muchas tarjetas retail como CMR, Ripley o Líder no tienen avance en efectivo. Nosotros usamos tu cupo de compras internacional, no el avance. Funciona con prácticamente todas las tarjetas.</p>
              </div>
            </details>
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿Cuánto puedo recibir por mi cupo?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>Depende del monto de tu cupo disponible y el tipo de cambio del día. Con nuestra comisión del 15%, por cada USD 100 de cupo recibís aproximadamente USD 85 convertidos a pesos chilenos. Por ejemplo, con un cupo de USD 1.000 podés recibir más de $750.000 CLP. Te cotizamos sin compromiso por WhatsApp.</p>
              </div>
            </details>
            <details className="group bg-gray-50 rounded-xl p-6 cursor-pointer">
              <summary className="font-bold text-lg text-[#1a1a1a] list-none flex justify-between items-center">
                ¿En qué ciudades de Chile operan?
                <span className="text-[#C8A045] transform group-open:rotate-180 transition-transform">▼</span>
              </summary>
              <div className="text-gray-600 mt-4 leading-relaxed">
                <p>Operamos en todo Chile. Como el proceso es 100% online por WhatsApp, no necesitás estar en una ciudad específica. Atendemos clientes en Santiago, regiones y ciudades de todo el país. Revisá nuestro <Link to="/directorio-general" className="text-[#C8A045] hover:underline">directorio de ciudades</Link>.</p>
              </div>
            </details>
          </div>
        </div>
      </section>
      
      {/* City Coverage Section - SEO interlinking */}
      <section className="py-16 bg-gray-50 border-t border-gray-100">
        <div className="container mx-auto px-4 max-w-6xl">
          <h2 className="text-3xl font-bold text-center text-[#1a1a1a] mb-4">Cobertura en Todo Chile</h2>
          <p className="text-center text-gray-500 mb-12 max-w-2xl mx-auto">
            Operamos en ciudades y comunas de todo Chile. Hac clic en tu ciudad y vende tu cupo en d lares desde donde est s.
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-[#C8A045] mb-3 uppercase text-sm tracking-wider">RM</h3>
              <ul className="space-y-2 text-sm">
                <li><Link to="/vender-cupo-dolar-santiago" className="text-gray-600 hover:text-[#C8A045]">Santiago</Link></li>
                <li><Link to="/vender-cupo-dolar-las-condes" className="text-gray-600 hover:text-[#C8A045]">Las Condes</Link></li>
                <li><Link to="/vender-cupo-dolar-providencia" className="text-gray-600 hover:text-[#C8A045]">Providencia</Link></li>
                <li><Link to="/vender-cupo-dolar-nunoa" className="text-gray-600 hover:text-[#C8A045]"> u oa</Link></li>
                <li><Link to="/vender-cupo-dolar-maipu" className="text-gray-600 hover:text-[#C8A045]">Maip </Link></li>
                <li><Link to="/vender-cupo-dolar-la-florida" className="text-gray-600 hover:text-[#C8A045]">La Florida</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-[#C8A045] mb-3 uppercase text-sm tracking-wider">Norte</h3>
              <ul className="space-y-2 text-sm">
                <li><Link to="/vender-cupo-dolar-antofagasta" className="text-gray-600 hover:text-[#C8A045]">Antofagasta</Link></li>
                <li><Link to="/vender-cupo-dolar-iquique" className="text-gray-600 hover:text-[#C8A045]">Iquique</Link></li>
                <li><Link to="/vender-cupo-dolar-arica" className="text-gray-600 hover:text-[#C8A045]">Arica</Link></li>
                <li><Link to="/vender-cupo-dolar-calama" className="text-gray-600 hover:text-[#C8A045]">Calama</Link></li>
                <li><Link to="/vender-cupo-dolar-la-serena" className="text-gray-600 hover:text-[#C8A045]">La Serena</Link></li>
                <li><Link to="/vender-cupo-dolar-copiapo" className="text-gray-600 hover:text-[#C8A045]">Copiapo</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-[#C8A045] mb-3 uppercase text-sm tracking-wider">Centro</h3>
              <ul className="space-y-2 text-sm">
                <li><Link to="/vender-cupo-dolar-valparaiso" className="text-gray-600 hover:text-[#C8A045]">Valpara so</Link></li>
                <li><Link to="/vender-cupo-dolar-vina-del-mar" className="text-gray-600 hover:text-[#C8A045]">Vi a del Mar</Link></li>
                <li><Link to="/vender-cupo-dolar-rancagua" className="text-gray-600 hover:text-[#C8A045]">Rancagua</Link></li>
                <li><Link to="/vender-cupo-dolar-talca" className="text-gray-600 hover:text-[#C8A045]">Talca</Link></li>
                <li><Link to="/vender-cupo-dolar-concepcion" className="text-gray-600 hover:text-[#C8A045]">Concepci n</Link></li>
                <li><Link to="/vender-cupo-dolar-temuco" className="text-gray-600 hover:text-[#C8A045]">Temuco</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-[#C8A045] mb-3 uppercase text-sm tracking-wider">Sur</h3>
              <ul className="space-y-2 text-sm">
                <li><Link to="/vender-cupo-dolar-valdivia" className="text-gray-600 hover:text-[#C8A045]">Valdivia</Link></li>
                <li><Link to="/vender-cupo-dolar-osorno" className="text-gray-600 hover:text-[#C8A045]">Osorno</Link></li>
                <li><Link to="/vender-cupo-dolar-puerto-montt" className="text-gray-600 hover:text-[#C8A045]">Puerto Montt</Link></li>
                <li><Link to="/vender-cupo-dolar-punta-arenas" className="text-gray-600 hover:text-[#C8A045]">Punta Arenas</Link></li>
                <li><Link to="/vender-cupo-dolar-castro" className="text-gray-600 hover:text-[#C8A045]">Castro</Link></li>
                <li><Link to="/vender-cupo-dolar-pucon" className="text-gray-600 hover:text-[#C8A045]">Puc n</Link></li>
              </ul>
            </div>
          </div>
          <div className="text-center mt-10">
            <Link to="/directorio-general" className="text-[#C8A045] font-semibold hover:underline">
              Ver todas las ciudades &rarr;</Link>
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
            <br />Especialistas en compra de cupo dólar de manera segura.
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
