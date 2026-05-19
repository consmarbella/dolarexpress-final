import React from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import Logo from '../components/Logo';

const Home: React.FC = () => {
  const pageTitle = "DolarExpress | Compramos tu Cupo en Dólares | Efectivo al Instante";
  const pageDescription = "Compramos tu cupo en dólares de tarjetas de crédito CMR, Ripley, Cencosud y bancos. Te transferimos a pesos en menos de 15 minutos. 100% online, sin filas.";

  const structuredData = [
    {
      "@context": "https://schema.org",
      "@type": "FinancialService",
      "name": "DolarExpress",
      "description": pageDescription,
      "url": "https://dolarexpress.cl",
      "telephone": "+56967658939",
      "areaServed": { "@type": "Country", "name": "Chile" },
      "currenciesAccepted": "CLP, USD",
      "openingHours": "Mo-Su 09:00-21:00",
      "sameAs": ["https://wa.me/56967658939"]
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "¿Es legal vender mi cupo en dólares?",
          "acceptedAnswer": { "@type": "Answer", "text": "Sí, es completamente legal. Usas tu cupo para comprar en un comercio internacional y nosotros te pagamos en pesos chilenos. Es una operación privada legítima." }
        },
        {
          "@type": "Question",
          "name": "¿Cuánto demora la transferencia?",
          "acceptedAnswer": { "@type": "Answer", "text": "Menos de 15 minutos desde que confirmas la operación. Trabajamos con transferencia inmediata a cualquier banco en Chile." }
        },
        {
          "@type": "Question",
          "name": "¿Qué tarjetas aceptan?",
          "acceptedAnswer": { "@type": "Answer", "text": "CMR Falabella, Cencosud, Ripley, Líder BCI, La Polar, Hites, ABCDin y tarjetas bancarias (Banco de Chile, Santander, BCI, BancoEstado, Itaú, Scotiabank)." }
        },
        {
          "@type": "Question",
          "name": "¿Revisan DICOM?",
          "acceptedAnswer": { "@type": "Answer", "text": "No. Solo necesitas cupo disponible en tu tarjeta. No revisamos historial crediticio ni DICOM." }
        }
      ]
    }
  ];

  const WA_URL = "https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20quiero%20vender%20mi%20cupo";

  return (
    <div className="min-h-screen flex flex-col font-sans bg-white text-[#1a1a1a]">
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <link rel="canonical" href="https://dolarexpress.cl/" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://dolarexpress.cl/" />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        <meta property="og:image" content="https://dolarexpress.cl/og-image.svg" />
        <meta property="og:site_name" content="DolarExpress" />
        <meta name="twitter:card" content="summary_large_image" />
      </Helmet>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />

      {/* Navbar */}
      <nav className="fixed w-full z-50 bg-[#1a1a1a] shadow-lg">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center max-w-6xl">
          <Link to="/" aria-label="DolarExpress inicio">
            <Logo className="h-14 w-auto object-contain" />
          </Link>
          <a
            href={WA_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-[#C8A045] text-white px-6 py-2.5 rounded-lg font-bold text-sm hover:brightness-110 transition-all shadow-md"
          >
            Cotizar Ahora
          </a>
        </div>
      </nav>

      {/* Hero */}
      <header className="pt-28 pb-20 bg-[#1a1a1a] text-white">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="flex flex-col md:flex-row items-center gap-12">
            <div className="flex-1 text-center md:text-left">
              <div className="inline-block bg-[#C8A045]/20 text-[#C8A045] text-sm font-semibold px-4 py-1.5 rounded-full mb-6">
                Servicio 100% online · Lunes a domingo
              </div>
              <h1 className="text-4xl md:text-5xl font-extrabold leading-tight mb-6">
                Compramos tu Cupo en Dólares.<br />
                <span className="text-[#C8A045]">Te transferimos en 15 min.</span>
              </h1>
              <p className="text-gray-300 text-lg mb-8 max-w-xl">
                Tienes cupo en dólares en tu tarjeta CMR, Ripley, Cencosud o bancaria y necesitas efectivo. Coordinamos todo por WhatsApp y el dinero llega a tu cuenta al instante.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
                <a
                  href={WA_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center gap-3 bg-[#25D366] text-white text-lg px-8 py-4 rounded-xl font-bold hover:bg-[#20ba5a] transition-all shadow-lg"
                >
                  <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                  </svg>
                  Cotizar por WhatsApp
                </a>
              </div>
              <p className="text-gray-500 text-sm mt-4">Respuesta en menos de 2 minutos · Comisión 15%</p>
            </div>

            {/* Info Box */}
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6 md:w-72 w-full">
              <div className="space-y-4">
                {[
                  { label: "Tiempo de transferencia", value: "< 15 minutos" },
                  { label: "Comisión", value: "15% del monto" },
                  { label: "Monto mínimo", value: "USD 200" },
                  { label: "Revisan DICOM", value: "No" },
                  { label: "Horario", value: "Lun–Dom 9–21h" },
                ].map(({ label, value }) => (
                  <div key={label} className="flex justify-between items-center border-b border-white/10 pb-3 last:border-0 last:pb-0">
                    <span className="text-gray-400 text-sm">{label}</span>
                    <span className="text-white font-semibold text-sm">{value}</span>
                  </div>
                ))}
              </div>
              <a href={WA_URL} target="_blank" rel="noopener noreferrer"
                className="mt-6 w-full block text-center bg-[#C8A045] text-white font-bold py-3 rounded-xl hover:brightness-110 transition-all text-sm">
                Iniciar operación →
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Cómo funciona */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4 max-w-5xl">
          <h2 className="text-2xl font-bold text-center mb-12">¿Cómo funciona?</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { n: "1", title: "Escríbenos", desc: "Contáctanos por WhatsApp con el monto en dólares que tienes disponible." },
              { n: "2", title: "Cotización al instante", desc: "Te enviamos cuánto recibirás en pesos chilenos. Tasa clara, sin sorpresas." },
              { n: "3", title: "Autorizas la operación", desc: "Usas tu tarjeta para procesar la compra. Tú controlas todo el proceso." },
              { n: "4", title: "Recibes tu dinero", desc: "Transferimos a tu cuenta bancaria en menos de 15 minutos." },
            ].map(({ n, title, desc }) => (
              <div key={n} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center">
                <div className="w-10 h-10 bg-[#C8A045] text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-4">{n}</div>
                <h3 className="font-bold mb-2">{title}</h3>
                <p className="text-sm text-gray-600">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tarjetas aceptadas */}
      <section className="py-14 bg-white border-y border-gray-100">
        <div className="container mx-auto px-4 max-w-5xl">
          <h2 className="text-2xl font-bold text-center mb-10">Tarjetas que compramos</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { name: "CMR Falabella", color: "bg-green-50 text-green-800 border-green-200" },
              { name: "Ripley", color: "bg-purple-50 text-purple-800 border-purple-200" },
              { name: "Cencosud", color: "bg-blue-50 text-blue-800 border-blue-200" },
              { name: "Líder BCI", color: "bg-yellow-50 text-yellow-800 border-yellow-200" },
              { name: "La Polar", color: "bg-red-50 text-red-800 border-red-200" },
              { name: "Hites", color: "bg-orange-50 text-orange-800 border-orange-200" },
              { name: "Banco de Chile", color: "bg-sky-50 text-sky-800 border-sky-200" },
              { name: "Santander", color: "bg-red-50 text-red-800 border-red-200" },
              { name: "BCI", color: "bg-blue-50 text-blue-800 border-blue-200" },
              { name: "BancoEstado", color: "bg-green-50 text-green-800 border-green-200" },
              { name: "Itaú", color: "bg-orange-50 text-orange-800 border-orange-200" },
              { name: "Scotiabank", color: "bg-red-50 text-red-800 border-red-200" },
            ].map(({ name, color }) => (
              <div key={name} className={`border rounded-lg px-4 py-3 text-center text-sm font-semibold ${color}`}>
                {name}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4 max-w-3xl">
          <h2 className="text-2xl font-bold text-center mb-10">Preguntas frecuentes</h2>
          <div className="space-y-3">
            {[
              { q: "¿Es legal vender mi cupo en dólares?", a: "Sí, es completamente legal. Usas tu cupo para comprar en un comercio y nosotros te pagamos en pesos. Es una operación privada entre particulares." },
              { q: "¿Revisan mi DICOM o historial?", a: "No revisamos DICOM ni historial crediticio. Solo necesitas tener cupo disponible en tu tarjeta." },
              { q: "¿Cuánto demora la transferencia?", a: "Menos de 15 minutos desde que confirmas la operación. En horario bancario puede ser incluso más rápido." },
              { q: "¿Cuál es la comisión?", a: "15% del monto. Si tienes USD 1.000 de cupo, recibes el equivalente a USD 850 en pesos chilenos al tipo de cambio del día." },
              { q: "¿Necesito ir a alguna sucursal?", a: "No. Todo el proceso es 100% online coordinado por WhatsApp. Puedes hacerlo desde tu casa o desde cualquier lugar de Chile." },
            ].map(({ q, a }) => (
              <details key={q} className="bg-white border border-gray-200 rounded-xl group">
                <summary className="px-6 py-4 font-semibold cursor-pointer list-none flex justify-between items-center hover:bg-gray-50 transition-colors">
                  {q}
                  <span className="text-[#C8A045] text-lg transition-transform group-open:rotate-180 shrink-0 ml-4">▼</span>
                </summary>
                <div className="px-6 pb-4 text-gray-600 text-sm leading-relaxed">{a}</div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-16 bg-[#1a1a1a] text-white text-center">
        <div className="container mx-auto px-4 max-w-2xl">
          <h2 className="text-3xl font-bold mb-4">¿Listo para cotizar?</h2>
          <p className="text-gray-400 mb-8">Escríbenos ahora. Te respondemos en menos de 2 minutos con el monto exacto que recibirás.</p>
          <a href={WA_URL} target="_blank" rel="noopener noreferrer"
            className="inline-flex items-center gap-3 bg-[#25D366] text-white text-lg px-10 py-4 rounded-xl font-bold hover:bg-[#20ba5a] transition-all shadow-lg">
            <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
            </svg>
            Cotizar por WhatsApp
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#111] text-gray-500 py-8 text-center text-sm">
        <div className="container mx-auto px-4 max-w-4xl">
          <Logo className="h-10 w-auto object-contain mx-auto mb-4 opacity-60 brightness-0 invert" lightMode={false} />
          <p>© {new Date().getFullYear()} DolarExpress.cl — Servicio de compra de cupo en dólares.</p>
          <p className="mt-1">
            <a href="https://wa.me/56967658939" className="hover:text-[#C8A045] transition-colors">WhatsApp</a>
            {" · "}
            <a href="/directorio-general" className="hover:text-[#C8A045] transition-colors">Directorio</a>
          </p>
        </div>
      </footer>

      {/* WhatsApp flotante */}
      <a href={WA_URL} target="_blank" rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 bg-[#25D366] w-14 h-14 rounded-full flex items-center justify-center text-white shadow-xl hover:bg-[#20ba5a] transition-colors"
        aria-label="Contactar por WhatsApp">
        <svg width="28" height="28" fill="currentColor" viewBox="0 0 24 24">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
        </svg>
      </a>
    </div>
  );
};

export default Home;
