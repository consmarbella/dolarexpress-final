import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { createInterface } from 'readline';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = resolve(__dirname, '..', 'dist');
const TOKEN_FILE = resolve(__dirname, 'gsc-token.json');
const ENV_FILE = resolve(__dirname, '..', '.env.gsc');
if (!existsSync(OUTPUT_DIR)) mkdirSync(OUTPUT_DIR, { recursive: true });

function loadEnv() {
  if (!existsSync(ENV_FILE)) {
    console.error('Falta .env.gsc. Debe tener:');
    console.error('GSC_CLIENT_ID=...');
    console.error('GSC_CLIENT_SECRET=...');
    process.exit(1);
  }
  const env = {};
  for (const line of readFileSync(ENV_FILE, 'utf-8').split('\n').filter(Boolean)) {
    const [k, ...v] = line.split('=');
    env[k.trim()] = v.join('=').trim();
  }
  return env;
}

async function oauthFlow() {
  const env = loadEnv();
  const redirect = 'urn:ietf:wg:oauth:2.0:oob';

  const authUrl = 'https://accounts.google.com/o/oauth2/v2/auth?' +
    'client_id=' + env.GSC_CLIENT_ID +
    '&redirect_uri=' + redirect +
    '&response_type=code' +
    '&scope=https://www.googleapis.com/auth/webmasters.readonly' +
    '&access_type=offline' +
    '&prompt=consent';

  console.log('\n1) Abre este link en tu navegador:');
  console.log(authUrl);
  console.log('\n2) Inicia sesion con xaos27@gmail.com');
  console.log('3) Acepta los permisos');
  console.log('4) Copia el CODIGO que te muestra Google');
  console.log('5) Pegalo abajo y presiona Enter\n');

  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const code = await new Promise(r => rl.question('Codigo: ', r));
  rl.close();

  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code, client_id: env.GSC_CLIENT_ID, client_secret: env.GSC_CLIENT_SECRET,
      redirect_uri: redirect, grant_type: 'authorization_code'
    })
  });
  const tokens = await tokenRes.json();
  if (!tokenRes.ok) {
    console.error('Error OAuth:', tokens.error_description || tokens.error);
    process.exit(1);
  }
  writeFileSync(TOKEN_FILE, JSON.stringify(tokens, null, 2));
  console.log('Token guardado\n');
  return tokens.access_token;
}

async function refreshToken(refreshToken) {
  const env = loadEnv();
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      refresh_token: refreshToken, client_id: env.GSC_CLIENT_ID,
      client_secret: env.GSC_CLIENT_SECRET, grant_type: 'refresh_token'
    })
  });
  const json = await res.json();
  if (json.access_token) return json.access_token;
  throw new Error(json.error_description);
}

async function getToken() {
  if (existsSync(TOKEN_FILE)) {
    try {
      const tokens = JSON.parse(readFileSync(TOKEN_FILE, 'utf-8'));
      if (tokens.refresh_token) return await refreshToken(tokens.refresh_token);
      if (tokens.access_token) return tokens.access_token;
    } catch { }
  }
  return await oauthFlow();
}

async function inspectAll() {
  const token = await getToken();
  const siteUrl = 'https://dolarexpress.cl/';

  const data = readFileSync(resolve(__dirname, '..', 'src', 'data', 'pseo-data.ts'), 'utf-8');
  const slugs = [...new Set([...data.matchAll(/slug:\s*'([^']+)'/g)].map(m => m[1]))].filter(s => s !== 'index');

  console.log('Inspeccionando ' + slugs.length + ' URLs...\n');
  const results = [];

  for (let i = 0; i < slugs.length; i++) {
    process.stdout.write('[' + (i + 1) + '/' + slugs.length + '] ' + slugs[i].padEnd(50) + ' ');
    try {
      const res = await fetch('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', {
        method: 'POST',
        headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
        body: JSON.stringify({ siteUrl, inspectionUrl: siteUrl + slugs[i], languageCode: 'es-CL' })
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error?.message || 'HTTP ' + res.status);
      const s = json.inspectionResult?.indexStatusResult;
      const coverage = s?.coverageState || 'UNKNOWN';
      const verdict = s?.verdict || 'UNKNOWN';
      results.push({ slug: slugs[i], verdict, coverage });
      const label = verdict === 'PASS' ? 'INDEXADO' : coverage === 'ALTERNATE_PAGE_WITH_CANONICAL' ? 'ALT_CANONICA' : coverage === 'CRAWLED_NOT_INDEXED' ? 'NO_INDEXADO' : coverage;
      console.log(label);
    } catch (e) {
      results.push({ slug: slugs[i], verdict: 'ERROR', coverage: e.message });
      console.log('ERROR: ' + e.message.slice(0, 80));
    }
    if (i < slugs.length - 1) await new Promise(r => setTimeout(r, 1100));
  }

  const counts = {};
  for (const r of results) counts[r.coverage] = (counts[r.coverage] || 0) + 1;

  console.log('\n=== RESULTADOS ===');
  for (const [k, v] of Object.entries(counts).sort((a, b) => b[1] - a[1]))
    console.log('  ' + (k === 'PASS' ? 'INDEXADAS' : k) + ': ' + v);

  for (const key of ['ALTERNATE_PAGE_WITH_CANONICAL', 'CRAWLED_NOT_INDEXED', 'NOT_FOUND']) {
    const items = results.filter(r => r.coverage === key);
    if (items.length) {
      console.log('\n' + key + ' (' + items.length + '):');
      items.forEach(r => console.log('  ' + siteUrl + r.slug));
    }
  }

  writeFileSync(resolve(OUTPUT_DIR, 'gsc-inspection.csv'),
    'slug,verdict,coverage\n' + results.map(r => '"' + r.slug + '","' + r.verdict + '","' + r.coverage.replace(/"/g, '""') + '"').join('\n'), 'utf-8');
  console.log('\nCSV: ' + resolve(OUTPUT_DIR, 'gsc-inspection.csv'));
}

inspectAll().catch(e => { console.error(e.message); process.exit(1); });
