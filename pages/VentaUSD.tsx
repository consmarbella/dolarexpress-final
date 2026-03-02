import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';

const VentaUSD: React.FC = () => {
  useEffect(() => {
    document.title = "Procesa tu Venta de Cupo Dólar | DolarExpress";
    const metaDescription = document.querySelector('meta[name="description"]');
    const description = "Formulario seguro para procesar la venta de tu cupo en dólares. Transferencia inmediata a tu cuenta bancaria en Chile.";
    if (metaDescription) {
      metaDescription.setAttribute('content', description);
    } else {
      const meta = document.createElement('meta');
      meta.name = 'description';
      meta.content = description;
      document.head.appendChild(meta);
    }
  }, []);

  const widgetUrl = "https://widget.changelly.com?from=usd&to=btc&amount=500&address=&fromDefault=usd&toDefault=btc&merchant_id=O_zbRc229eHGJZj1&payment_id=&v=3&type=no-rev-share&color=5f41ff&headerId=1&logo=hide&buyButtonTextId=1";

  return (
    <div className="min-h-screen bg-[#1a1a1a] flex flex-col font-sans">
      {/* Navbar Minimal */}
      <nav className="p-6 text-center flex flex-col items-center gap-4">
        <div className="relative">
            <Logo className="h-16 w-auto object-contain brightness-0 invert" lightMode={false} />
        </div>
        <Link to="/" className="text-white font-bold text-sm opacity-80 hover:opacity-100 transition-opacity">
          ← Volver al Inicio
        </Link>
      </nav>
      
      <div className="flex-1 flex flex-col items-center justify-center p-4">
        <h1 className="text-white text-3xl font-bold mb-2 text-center">Procesa tu Venta</h1>
        <p className="text-gray-300 mb-8 text-center max-w-md">
          Completa los datos en el formulario seguro a continuación.
        </p>
        
        {/* Container for Widget */}
        <div className="w-full max-w-2xl bg-[#f4f7f6] rounded-xl shadow-2xl overflow-hidden border border-white/10">
          <div className="w-full h-[600px] relative bg-gray-50">
            <iframe
              width="100%"
              height="100%"
              style={{ border: 'none', display: 'block' }}
              allow="camera; payment; clipboard-write"
              referrerPolicy="origin"
              title="Transaction Widget"
              src={widgetUrl}
            >
              Can't load widget
            </iframe>
          </div>
        </div>
        
        {/* Fallback button */}
        <div className="mt-4 text-center">
             <a href={widgetUrl}
                target="_blank" 
                rel="noopener noreferrer"
                className="text-[#C8A045] hover:text-white text-sm underline opacity-80 hover:opacity-100 transition-all">
                ¿No ves el formulario? Haz clic aquí para abrirlo en una nueva ventana
             </a>
        </div>
        
        <div className="mt-8 text-white/50 text-sm flex items-center gap-2">
          <span>🔒</span> Conexión Encriptada 256-bit SSL
        </div>
      </div>
    </div>
  );
};

export default VentaUSD;