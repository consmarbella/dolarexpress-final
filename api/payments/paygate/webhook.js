import { handleWebhook } from '../../../lib/paygate-gateway.js';

export default async function handler(req, res) {
  handleWebhook(req.query);
  res.status(200).send('*ok*');
}
