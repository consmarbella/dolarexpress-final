export default async function handler(req, res) {
  const { invoice_id, value_coin, coin, txid_out } = req.query;
  const sig = req.query.sig;

  if (sig === '*ok*') {
    return res.status(200).send('*ok*');
  }

  if (txid_out) {
    console.log('[PayGate Callback]', JSON.stringify({ invoice_id, value_coin, coin, txid_out }));
  }

  res.status(200).send('*ok*');
}
