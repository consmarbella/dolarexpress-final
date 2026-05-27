const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// ============================================================
// CONFIGURACIÓN
// ============================================================
const GUARDARIAN_API_KEY = process.env.GUARDARIAN_API_KEY || 'aba29bc3-2e85-481c-8e62-f409d0561684';
const GUARDARIAN_API = 'https://api-payments.guardarian.com/v1';

// Wallet de DolarExpress para recibir los USD
const WALLET_USD = '15FxSPQd3t8JZ8TYuCb3rQJt2WfgaZFfN9';

// ============================================================
// MIDDLEWARE
// ============================================================
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// ============================================================
// API: Obtener tasa USD → CLP
// ============================================================
app.get('/api/rate', async (req, res) => {
    try {
        const amount = req.query.amount || 100;
        const response = await fetch(
            `${GUARDARIAN_API}/estimate?from_currency=USD&to_currency=CLP&from_network=USD&to_network=CLP&from_amount=${amount}`,
            {
                headers: {
                    'Accept': 'application/json',
                    'x-api-key': GUARDARIAN_API_KEY
                }
            }
        );
        const data = await response.json();

        if (!response.ok) {
            return res.status(400).json({ error: data.message || 'Error al obtener tasa' });
        }

        res.json({
            rate: data.estimated_exchange_rate || '930',
            service_fee: data.service_fees?.[0]?.amount || '0.5',
            min_amount: data.min_amount || '20',
            max_amount: data.max_amount || '10000'
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================================
// API: Crear transacción USD → CLP
// El cliente paga USD con tarjeta, recibe CLP en su cuenta
// ============================================================
app.post('/api/create-transaction', async (req, res) => {
    const { from_amount, email } = req.body;

    if (!from_amount || from_amount < 20) {
        return res.status(400).json({ error: 'El monto mínimo es 20 USD' });
    }

    try {
        const response = await fetch(`${GUARDARIAN_API}/transaction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'x-api-key': GUARDARIAN_API_KEY
            },
            body: JSON.stringify({
                from_amount: parseFloat(from_amount),
                from_currency: 'USD',
                to_currency: 'CLP',
                from_network: 'USD',
                to_network: 'CLP',
                payout_info: {
                    payout_address: WALLET_USD,
                    skip_choose_payout_address: true
                },
                customer: {
                    contact_info: {
                        email: email || 'cliente@dolarexpress.cl'
                    }
                },
                deposit: {
                    skip_choose_payment_category: false
                },
                redirects: {
                    successful: `${req.protocol}://${req.get('host')}/success.html`,
                    cancelled: `${req.protocol}://${req.get('host')}/cancel.html`,
                    failed: `${req.protocol}://${req.get('host')}/error.html`
                },
                locale: 'es'
            })
        });

        const data = await response.json();

        if (!response.ok) {
            return res.status(400).json({ error: data.message || data.error || 'Error al crear transacción' });
        }

        res.json({
            transaction_id: data.id,
            redirect_url: data.redirect_url || `https://payments.guardarian.com/checkout?tid=${data.id}&auth_token=${data.preauth_token}`,
            status: data.status
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================================
// API: Verificar estado de transacción
// ============================================================
app.get('/api/transaction/:id', async (req, res) => {
    try {
        const response = await fetch(`${GUARDARIAN_API}/transaction/${req.params.id}`, {
            headers: {
                'Accept': 'application/json',
                'x-api-key': GUARDARIAN_API_KEY
            }
        });
        const data = await response.json();

        if (!response.ok) {
            return res.status(400).json({ error: data.message || 'Error al obtener transacción' });
        }

        res.json({
            id: data.id,
            status: data.status,
            from_amount: data.from_amount,
            from_currency: data.from_currency,
            to_amount: data.to_amount,
            to_currency: data.to_currency,
            created_at: data.created_at
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================================
// SERVIR PÁGINAS
// ============================================================
app.get('/pagar', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'pagar.html'));
});

app.get('/success', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'success.html'));
});

app.get('/cancel', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'cancel.html'));
});

app.get('/error', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'error.html'));
});

// ============================================================
// INICIAR SERVIDOR
// ============================================================
app.listen(PORT, () => {
    console.log(`🚀 DolarExpress corriendo en http://localhost:${PORT}`);
    console.log(`💰 Sistema de pago USD → CLP vía API Guardarian`);
    console.log(`📤 Wallet destino: ${WALLET_USD}`);
});
