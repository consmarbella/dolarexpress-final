import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { SignJWT, importPKCS8 } from 'jose';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SA_FILE = resolve(__dirname, 'gsc-service-account.json');

async function getAccessToken() {
  const sa = JSON.parse(readFileSync(SA_FILE, 'utf-8'));
  
  // Import the private key
  const privateKey = await importPKCS8(sa.private_key, 'RS256');
  
  const now = Math.floor(Date.now() / 1000);
  
  // Create JWT
  const jwt = await new SignJWT({
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/webmasters.readonly',
    aud: sa.token_uri,
    iat: now,
    exp: now + 3600
  })
    .setProtectedHeader({ alg: 'RS256' })
    .sign(privateKey);
  
  // Exchange for access token
  const res = await fetch(sa.token_uri, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: jwt
    })
  });
  
  const data = await res.json();
  if (!res.ok) throw new Error('Token error: ' + (data.error_description || data.error));
  return data.access_token;
}

async function queryGSC(accessToken, siteUrl, payload) {
  const res = await fetch(`https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/searchAnalytics/query`, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + accessToken, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error('GSC error: ' + JSON.stringify(data.error || data));
  return data;
}

async function main() {
  console.log('Obteniendo token de acceso...');
  const accessToken = await getAccessToken();
  console.log('Token OK\n');

  const siteUrl = 'https://dolarexpress.cl';
  
  // 1. Traffic by month
  console.log('=== TRÁFICO MENSUAL (últimos 3 meses) ===\n');
  
  const months = [
    { start: '2026-06-01', end: '2026-06-30', label: 'Junio 2026' },
    { start: '2026-07-01', end: '2026-07-31', label: 'Julio 2026' },
    { start: '2026-08-01', end: '2026-08-27', label: 'Agosto 2026 (parcial)' }
  ];
  
  for (const m of months) {
    try {
      const data = await queryGSC(accessToken, siteUrl, {
        startDate: m.start,
        endDate: m.end,
        dimensions: [],
        rowLimit: 1
      });
      const row = data.rows?.[0];
      if (row) {
        console.log(`${m.label}:`);
        console.log(`  Clicks:    ${row.clicks}`);
        console.log(`  Impressions: ${row.impressions}`);
        console.log(`  CTR:       ${(row.ctr * 100).toFixed(2)}%`);
        console.log(`  Posición:  ${row.position?.toFixed(1)}`);
        console.log('');
      } else {
        console.log(`${m.label}: Sin datos\n`);
      }
    } catch (e) {
      console.log(`${m.label}: Error - ${e.message}\n`);
    }
    await new Promise(r => setTimeout(r, 500));
  }

  // 2. Top pages
  console.log('=== TOP 15 PÁGINAS POR CLICKS (últimos 28 días) ===\n');
  try {
    const data = await queryGSC(accessToken, siteUrl, {
      startDate: '2026-07-31',
      endDate: '2026-08-27',
      dimensions: ['page'],
      rowLimit: 15
    });
    if (data.rows) {
      data.rows.sort((a, b) => b.clicks - a.clicks);
      data.rows.forEach((r, i) => {
        const page = r.keys[0].replace('https://dolarexpress.cl', '');
        console.log(`${i+1}. ${page || '/'}`);
        console.log(`   Clicks: ${r.clicks} | Imp: ${r.impressions} | CTR: ${(r.ctr*100).toFixed(1)}% | Pos: ${r.position?.toFixed(1)}`);
      });
    }
  } catch (e) {
    console.log('Error:', e.message);
  }
  console.log('');

  // 3. Top queries
  console.log('=== TOP 15 QUERIES (últimos 28 días) ===\n');
  try {
    const data = await queryGSC(accessToken, siteUrl, {
      startDate: '2026-07-31',
      endDate: '2026-08-27',
      dimensions: ['query'],
      rowLimit: 15
    });
    if (data.rows) {
      data.rows.sort((a, b) => b.impressions - a.impressions);
      data.rows.forEach((r, i) => {
        console.log(`${i+1}. "${r.keys[0]}"`);
        console.log(`   Clicks: ${r.clicks} | Imp: ${r.impressions} | CTR: ${(r.ctr*100).toFixed(1)}% | Pos: ${r.position?.toFixed(1)}`);
      });
    }
  } catch (e) {
    console.log('Error:', e.message);
  }
  console.log('');

  // 4. Comparison
  console.log('=== COMPARACIÓN: AGOSTO vs JULIO ===\n');
  try {
    const julio = await queryGSC(accessToken, siteUrl, {
      startDate: '2026-07-01',
      endDate: '2026-07-31',
      dimensions: [],
      rowLimit: 1
    });
    const agosto = await queryGSC(accessToken, siteUrl, {
      startDate: '2026-08-01',
      endDate: '2026-08-27',
      dimensions: [],
      rowLimit: 1
    });
    const j = julio.rows?.[0] || { clicks: 0, impressions: 0, ctr: 0, position: 0 };
    const a = agosto.rows?.[0] || { clicks: 0, impressions: 0, ctr: 0, position: 0 };
    
    const clicksDiff = a.clicks - j.clicks;
    const clicksPct = j.clicks ? ((a.clicks / j.clicks - 1) * 100).toFixed(1) : 'N/A';
    const impDiff = a.impressions - j.impressions;
    const impPct = j.impressions ? ((a.impressions / j.impressions - 1) * 100).toFixed(1) : 'N/A';
    const posDiff = (a.position - j.position).toFixed(1);
    
    console.log(`Julio 2026:     ${j.clicks} clicks | ${j.impressions} imp | CTR ${(j.ctr*100).toFixed(2)}% | Pos ${j.position?.toFixed(1)}`);
    console.log(`Agosto 2026:    ${a.clicks} clicks | ${a.impressions} imp | CTR ${(a.ctr*100).toFixed(2)}% | Pos ${a.position?.toFixed(1)}`);
    console.log('');
    console.log(`Clicks:     ${clicksDiff >= 0 ? '+' : ''}${clicksDiff} (${clicksPct}%)`);
    console.log(`Impresiones: ${impDiff >= 0 ? '+' : ''}${impDiff} (${impPct}%)`);
    console.log(`Posición:    ${posDiff > 0 ? '+' : ''}${posDiff} ${posDiff < 0 ? '↑ MEJOR' : posDiff > 0 ? '↓ PEOR' : '='}`);
  } catch (e) {
    console.log('Error:', e.message);
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });
