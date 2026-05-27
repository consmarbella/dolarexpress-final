const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Servir archivos estáticos
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// ============================================================
// SERVIR WIDGET GUARD
// ============================================================
app.get('/guard', (req, res) => {
    res.sendFile(path.join(__dirname, 'guard.html'));
});

// ============================================================
// PROXY: Obtener tasa de cambio USD → CLP desde Guardarian
// ============================================================
app.get('/api/rate-clp', async (req, res) => {
    try {
        const response = await fetch(
            'https://api-payments.guardarian.com/v1/estimate?from_currency=USD&to_currency=CLP&from_network=USD&to_network=CLP&from_amount=100',
            {
                headers: {
                    'Accept': 'application/json',
                    'x-api-key': 'aba29bc3-2e85-481c-8e62-f409d0561684'
                }
            }
        );
        const data = await response.json();
        res.json({
            rate: data.estimated_exchange_rate || '930',
            service_fee: data.service_fees?.[0]?.amount || '0.5'
        });
    } catch (error) {
        res.json({ rate: '930', service_fee: '0.5' });
    }
});

// ============================================================
// PROXY: Crear transacción USD → CLP en Guardarian (Vender USD)
// ============================================================
app.post('/api/create-sell-clp', async (req, res) => {
    const { from_amount, email } = req.body;
    const WALLET = '15FxSPQd3t8JZ8TYuCb3rQJt2WfgaZFfN9';

    try {
        const response = await fetch('https://api-payments.guardarian.com/v1/transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'x-api-key': 'aba29bc3-2e85-481c-8e62-f409d0561684'
            },
            body: JSON.stringify({
                from_amount: from_amount,
                from_currency: 'USD',
                to_currency: 'CLP',
                from_network: 'USD',
                to_network: 'CLP',
                payout_info: {
                    payout_address: WALLET,
                    skip_choose_payout_address: false
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
                    successful: 'https://dolarexpress.cl/',
                    cancelled: 'https://dolarexpress.cl/',
                    failed: 'https://dolarexpress.cl/'
                },
                locale: 'es'
            })
        });

        const data = await response.json();

        if (!response.ok) {
            return res.status(400).json({ error: data.message || data.error || 'Error al crear transacción' });
        }

        res.json({
            redirect_url: data.redirect_url || `https://payments.guardarian.com/checkout?tid=${data.id}&auth_token=${data.preauth_token}`
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================================
// PROXY: Crear transacción USD → BTC en Guardarian
// ============================================================
app.post('/api/create-btc', async (req, res) => {

    const { from_amount, email } = req.body;
    const WALLET = '14GjaVeCyQwXLxSmVhMi9tbmXDCFt1G2Zd';

    try {
        const response = await fetch('https://api-payments.guardarian.com/v1/transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'x-api-key': 'aba29bc3-2e85-481c-8e62-f409d0561684'
            },
            body: JSON.stringify({
                from_amount: from_amount,
                from_currency: 'USD',
                to_currency: 'BTC',
                from_network: 'USD',
                to_network: 'BTC',
                payout_info: {
                    payout_address: WALLET,
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
                    successful: 'https://dolarexpress.cl/',
                    cancelled: 'https://dolarexpress.cl/',
                    failed: 'https://dolarexpress.cl/'
                },
                locale: 'es'
            })
        });

        const data = await response.json();

        if (!response.ok) {
            return res.status(400).json({ error: data.message || data.error || 'Error al crear transacción' });
        }

        res.json({
            redirect_url: data.redirect_url || `https://payments.guardarian.com/checkout?tid=${data.id}&auth_token=${data.preauth_token}`
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


// ============================================================
// INICIAR SERVIDOR
// ============================================================
app.listen(PORT, () => {
    console.log(`🚀 Servidor DolarExpress corriendo en http://localhost:${PORT}`);
    console.log(`📤 Los BTC se envían a la wallet: 14GjaVeCyQwXLxSmVhMi9tbmXDCFt1G2Zd`);

});


