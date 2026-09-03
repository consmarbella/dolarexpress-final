import { createPaymentSession, getCheckoutUrl, log } from '../../../lib/paygate-gateway.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { amount } = req.body;

  if (!amount || amount <= 0) {
    return res.status(400).json({ error: 'Invalid amount' });
  }

  try {
    const orderId = `ord_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const baseUrl = process.env.PAYGATE_BASE_URL || `https://${req.headers.host}`;

    log('create_request', { orderId, amount });

    const session = await createPaymentSession({ amount, orderId, baseUrl });
    const url = getCheckoutUrl(session);

    res.json({ url, sessionId: session.sessionId, orderId });
  } catch (err) {
    log('create_error', { error: err.message });
    res.status(502).json({ error: err.message });
  }
}
