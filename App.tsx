import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home.tsx';
import VentaUSD from './pages/VentaUSD.tsx';
import PSEOPage from './pages/PSEOPage.tsx';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/venta-usd" element={<VentaUSD />} />
        {/* Redirects */}
        <Route path="/vender-cupo-internacional" element={<Navigate to="/cupo-internacional-a-pesos" replace />} />
        {/* Catch-all PSEO */}
        <Route path="/:slug" element={<PSEOPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;