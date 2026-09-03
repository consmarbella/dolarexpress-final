import React from 'react';

const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#1a1a2e] text-white p-4">
      <div className="text-center max-w-md">
        <h1 className="text-4xl font-bold mb-4">Página no encontrada</h1>
        <p className="text-gray-400 mb-6">
          Lo sentimos, la pagina que buscas no existe o ha sido movida.
        </p>
        <a
          href="/"
          className="inline-block bg-[#00b159] text-white px-6 py-3 rounded-lg font-semibold hover:bg-[#007a3d] transition-colors"
        >
          Volver al inicio
        </a>
      </div>
    </div>
  );
};

export default NotFound;
