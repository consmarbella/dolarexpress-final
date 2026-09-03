export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { amount } = req.body;

  if (!amount || amount <= 0) {
    return res.status(400).json({ error: 'Invalid amount' });
  }

  const wallet = process.env.WALLET_ADDRESS;
  if (!wallet) {
    return res.status(500).json({ error: 'Wallet not configured' });
  }

  const callbackUrl = `https://${req.headers.host}/api/payment-callback`;

  try {
    const response = await fetch(
      `https://api.paygate.to/control/wallet.php?address=${wallet}&callback=${encodeURIComponent(callbackUrl)}`
    );
    const data = await response.json();

    if (!data.address_in) {
      return res.status(502).json({ error: 'Failed to get payment address' });
    }

    const checkoutUrl = `https://checkout.paygate.to/pay.php?address=${data.address_in}&amount=${amount}&currency=USD`;

    res.json({ url: checkoutUrl });
  } catch (err) {
    res.status(502).json({ error: err.message });
  }
}
