import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import Home from './pages/Home.tsx';
import VentaUSD from './pages/VentaUSD.tsx';
import PSEOPage from './pages/PSEOPage.tsx';

const App: React.FC = () => {
  return (
    <HelmetProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/venta-usd" element={<VentaUSD />} />
          <Route path="/:slug" element={<PSEOPage />} />
        </Routes>
      </BrowserRouter>
    </HelmetProvider>
  );
};

export default App;