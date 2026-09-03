const fs = require('fs');
const sa = JSON.parse(fs.readFileSync('scripts/gsc-service-account.json', 'utf-8'));
const pk = sa.private_key;
console.log('Key type:', pk.includes('PRIVATE KEY') ? 'PKCS#8' : 'unknown');
console.log('Lines count:', pk.split('\n').length);
console.log('First line:', pk.split('\n')[0]);
console.log('Last line:', pk.split('\n').slice(-2)[0]);

// Try importing the key
const { createSign } = require('crypto');
try {
  const sign = createSign('RSA-SHA256');
  sign.update('test');
  const sig = sign.sign({ key: pk, format: 'pkcs8', type: 'pkcs8' });
  console.log('Key works with pkcs8 format, sig length:', sig.length);
} catch(e) {
  console.log('pkcs8 error:', e.message);
  try {
    const sign2 = createSign('RSA-SHA256');
    sign2.update('test');
    const sig2 = sign2.sign(pk);
    console.log('Key works with raw key, sig length:', sig2.length);
  } catch(e2) {
    console.log('raw error:', e2.message);
  }
}
