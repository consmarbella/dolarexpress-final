const API_BASE = 'https://api.paygate.to';
const CHECKOUT_BASE = 'https://checkout.paygate.to';

function getConfig() {
  return {
    wallet: process.env.PAYGATE_USDC_WALLET || process.env.WALLET_ADDRESS,
    mode: process.env.PAYGATE_MODE || 'redirect',
    successUrl: process.env.PAYGATE_SUCCESS_URL || '/billing?status=success',
    cancelUrl: process.env.PAYGATE_CANCEL_URL || '/billing?status=cancel',
  };
}

function log(event, data) {
  console.log(JSON.stringify({ t: new Date().toISOString(), gw: 'paygate', event, ...data }));
}

async function createPaymentSession({ amount, currency = 'USD', orderId, baseUrl }) {
  const config = getConfig();

  if (!config.wallet) {
    throw new Error('PAYGATE_USDC_WALLET not configured');
  }

  log('create_session', { orderId, amount, currency, wallet: config.wallet });

  const callbackUrl = `${baseUrl}/api/payments/paygate/webhook`;

  const res = await fetch(
    `${API_BASE}/control/wallet.php?address=${config.wallet}&callback=${encodeURIComponent(callbackUrl)}`
  );

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`PayGate API error ${res.status}: ${text}`);
  }

  const data = await res.json();

  if (!data.address_in) {
    throw new Error('PayGate: no address_in in response');
  }

  log('session_created', { orderId, address_in: data.address_in });

  const email = 'pago@dolarexpress.cl';

  const checkoutUrl = `${CHECKOUT_BASE}/pay.php?address=${data.address_in}&amount=${amount}&email=${encodeURIComponent(email)}&currency=${currency}`;

  return { sessionId: data.address_in, checkoutUrl, amount, currency, orderId };
}

function getCheckoutUrl(session) {
  return session.checkoutUrl;
}

function handleWebhook(params) {
  const { invoice_id, value_coin, coin, txid_out, sig } = params;

  log('webhook', { invoice_id, value_coin, coin, txid_out, sig });

  if (txid_out) {
    log('payment_confirmed', { invoice_id, txid_out, value_coin, coin });
    return { status: 'confirmed', txid_out, value_coin, coin };
  }

  return { status: 'pending' };
}

export { createPaymentSession, getCheckoutUrl, handleWebhook, getConfig, log };
