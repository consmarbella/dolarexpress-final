import { google } from 'googleapis';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { execSync } from 'child_process';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = resolve(__dirname, '..', 'dist');
if (!existsSync(OUTPUT_DIR)) mkdirSync(OUTPUT_DIR, { recursive: true });

async function getToken() {
  // Try gcloud auth print-access-token (user login, not ADC)
  try {
    const token = execSync('gcloud auth print-access-token 2>nul', { encoding: 'utf-8', timeout: 10000 }).trim();
    if (token && token.length > 20) {
      console.log('Token obtenido de gcloud');
      return token;
    }
  } catch { }
  // Fallback: ADC
  try {
    const auth = new google.auth.GoogleAuth({ scopes: ['https://www.googleapis.com/auth/webmasters.readonly'] });
    const client = await auth.getClient();
    const token = await client.getAccessToken();
    console.log('Token obtenido de ADC');
    return token.token;
  } catch { }
  console.error('\nNo hay credenciales. Corre:\n  gcloud auth login');
  process.exit(1);
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
        headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
        body: JSON.stringify({ siteUrl, inspectionUrl: siteUrl + slugs[i], languageCode: 'es-CL' })
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error?.message || 'HTTP ' + res.status);
      const s = json.inspectionResult?.indexStatusResult;
      const coverage = s?.coverageState || 'UNKNOWN';
      const verdict = s?.verdict || 'UNKNOWN';
      results.push({ slug: slugs[i], verdict, coverage });
      console.log(verdict === 'PASS' ? 'INDEXADO' : coverage);
    } catch (e) {
      results.push({ slug: slugs[i], verdict: 'ERROR', coverage: e.message });
      console.log(e.message);
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
      console.log('\n' + key + ':');
      items.forEach(r => console.log('  ' + siteUrl + r.slug));
    }
  }

  const csv = 'slug,verdict,coverage\n' + results.map(r => '"' + r.slug + '","' + r.verdict + '","' + r.coverage.replace(/"/g, '""') + '"').join('\n');
  writeFileSync(resolve(OUTPUT_DIR, 'gsc-inspection.csv'), csv, 'utf-8');
  console.log('\nCSV: ' + resolve(OUTPUT_DIR, 'gsc-inspection.csv'));
}

inspectAll().catch(e => { console.error('Error:', e.message); process.exit(1); });
