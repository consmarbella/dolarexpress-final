# DolarExpress - Sistema de Pago con API Guardarian

Sistema de compra/venta de cupo en dólares usando la API de Guardarian.

## Stack
- **Backend**: Node.js + Express
- **Frontend**: HTML + Tailwind CSS
- **Pagos**: API Guardarian (sin widget iframe)

## Instalación

```bash
npm install
```

## Configuración

Copiar `.env.example` a `.env` y configurar:

```
GUARDARIAN_API_KEY=tu-api-key
PORT=3000
```

## Ejecutar

```bash
npm start
```

## Endpoints

- `GET /api/rate-btc` - Obtener tasa USD → BTC
- `POST /api/create-transaction` - Crear transacción de compra BTC
- `GET /api/rate-clp` - Obtener tasa USD → CLP
- `POST /api/create-sell-clp` - Crear transacción de venta USD → CLP
