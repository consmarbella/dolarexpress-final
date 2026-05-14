import { google } from 'googleapis';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { createInterface } from 'readline';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TOKEN_PATH = resolve(__dirname, 'gsc-token.json');
const OUTPUT_DIR = resolve(__dirname, '..', 'dist');

if (!existsSync(OUTPUT_DIR)) mkdirSync(OUTPUT_DIR, { recursive: true });

function loadCredentials() {
  const envPath = resolve(__dirname, '..', '.env.gsc');
  if (!existsSync(envPath)) {
    console.error('\n❌ No se encuentra .env.gsc');
    console.error('\nCrea el archivo en: ' + envPath);
    console.error('Con este contenido:');
    console.error('\nGSC_CLIENT_ID=tu-client-id.apps.googleusercontent.com');
    console.error('GSC_CLIENT_SECRET=tu-client-secret');
    console.error('\nPara obtenerlos:');
    console.error('1. https://console.cloud.google.com/apis/credentials');
    console.error('2. Crear credenciales → ID de cliente OAuth 2.0');
    console.error('3. Tipo: Aplicación de escritorio');
    console.error('4. Copiar Client ID y Client Secret al .env.gsc');
    process.exit(1);
  }
  const lines = readFileSync(envPath, 'utf-8').split('\n').filter(Boolean);
  const env = {};
  for (const line of lines) {
    const [key, ...rest] = line.split('=');
    env[key.trim()] = rest.join('=').trim();
  }
  if (!env.GSC_CLIENT_ID || !env.GSC_CLIENT_SECRET) {
    console.error('❌ .env.gsc debe contener GSC_CLIENT_ID y GSC_CLIENT_SECRET');
    process.exit(1);
  }
  return env;
}

async function getAuthenticatedClient() {
  const env = loadCredentials();
  const redirectUri = 'urn:ietf:wg:oauth:2.0:oob';

  if (existsSync(TOKEN_PATH)) {
    const token = JSON.parse(readFileSync(TOKEN_PATH, 'utf-8'));
    const oauth2Client = new google.auth.OAuth2(env.GSC_CLIENT_ID, env.GSC_CLIENT_SECRET, redirectUri);
    oauth2Client.setCredentials(token);
    return oauth2Client;
  }

  const oauth2Client = new google.auth.OAuth2(env.GSC_CLIENT_ID, env.GSC_CLIENT_SECRET, redirectUri);

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/webmasters.readonly'],
  });

  console.log('\n🔗 Abre este link en tu navegador:');
  console.log(authUrl);
  console.log('\nInicia sesión con tu cuenta de GSC, acepta los permisos');
  console.log('Google te mostrará un código. Cópialo y pégalo abajo.\n');

  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const code = await new Promise(resolve => rl.question('Código: ', resolve));
  rl.close();

  const { tokens } = await oauth2Client.getToken(code);
  oauth2Client.setCredentials(tokens);
  writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
  console.log('✅ Token guardado (no hace falta autenticarse de nuevo)');
  return oauth2Client;
}

async function inspectAll() {
  const auth = await getAuthenticatedClient();
  const urlInspection = google.searchconsole('v1');
  const siteUrl = 'https://dolarexpress.cl/';

  const pseoPath = resolve(__dirname, '..', 'src', 'data', 'pseo-data.ts');
  const pseoContent = readFileSync(pseoPath, 'utf-8');
  const slugs = [...pseoContent.matchAll(/slug:\s*'([^']+)'/g)].map(m => m[1]);
  const uniqueSlugs = [...new Set(slugs)].filter(s => s !== 'index');

  console.log(`\n🔍 Inspeccionando ${uniqueSlugs.length} URLs...\n`);

  const results = [];

  for (let i = 0; i < uniqueSlugs.length; i++) {
    const slug = uniqueSlugs[i];
    const url = `https://dolarexpress.cl/${slug}`;
    process.stdout.write(`[${i + 1}/${uniqueSlugs.length}] ${slug.padEnd(50)} `);

    try {
      const res = await urlInspection.urlInspection.index.inspect({
        requestBody: {
          siteUrl,
          inspectionUrl: url,
          languageCode: 'es-CL'
        }
      });

      const indexStatus = res.data.inspectionResult?.indexStatusResult;
      const verdict = indexStatus?.verdict || 'UNKNOWN';
      const coverage = indexStatus?.coverageState || 'UNKNOWN';
      const canonical = indexStatus?.canonical || '-';

      results.push({ slug, url, verdict, coverage, canonical });

      if (verdict === 'PASS') {
        console.log('✅ INDEXADO');
      } else if (coverage === 'ALTERNATE_PAGE_WITH_CANONICAL') {
        console.log('❌ Alternativa canónica');
      } else if (coverage === 'CRAWLED_NOT_INDEXED') {
        console.log('⏳ Crawleado no indexado');
      } else if (coverage === 'NOT_FOUND') {
        console.log('🚫 404');
      } else {
        console.log(`❌ ${coverage}`);
      }

      if (i < uniqueSlugs.length - 1) await new Promise(r => setTimeout(r, 1100));
    } catch (err) {
      results.push({ slug, url, verdict: 'ERROR', coverage: err.message, canonical: '-' });
      console.log(`💥 Error: ${err.message.slice(0, 60)}`);
      await new Promise(r => setTimeout(r, 5000));
    }
  }

  const indexed = results.filter(r => r.verdict === 'PASS').length;
  const alternate = results.filter(r => r.coverage === 'ALTERNATE_PAGE_WITH_CANONICAL').length;
  const crawledNotIndexed = results.filter(r => r.coverage === 'CRAWLED_NOT_INDEXED').length;
  const errors = results.filter(r => r.verdict === 'ERROR').length;
  const notFound = results.filter(r => r.coverage === 'NOT_FOUND').length;
  const others = results.length - indexed - alternate - crawledNotIndexed - errors - notFound;

  console.log('\n═══════════════════════════════════════');
  console.log('            RESULTADOS');
  console.log('═══════════════════════════════════════');
  console.log(`  Total:                  ${results.length}`);
  console.log(`  ✅ INDEXADAS:           ${indexed}`);
  console.log(`  ❌ Alternativa canónica: ${alternate}`);
  console.log(`  ⏳ Crawleado no indexado: ${crawledNotIndexed}`);
  console.log(`  🚫 404:                 ${notFound}`);
  console.log(`  💥 Error:               ${errors}`);
  console.log(`  Otros:                  ${others}`);
  console.log('');

  if (alternate > 0) {
    console.log('\nPÁGINAS CON ALTERNATE PAGE WITH CANONICAL:');
    results.filter(r => r.coverage === 'ALTERNATE_PAGE_WITH_CANONICAL').forEach(r =>
      console.log(`  https://dolarexpress.cl/${r.slug}`)
    );
  }

  if (crawledNotIndexed > 0) {
    console.log('\nPÁGINAS CRAWLEADAS NO INDEXADAS:');
    results.filter(r => r.coverage === 'CRAWLED_NOT_INDEXED').forEach(r =>
      console.log(`  https://dolarexpress.cl/${r.slug}`)
    );
  }

  if (notFound > 0) {
    console.log('\nPÁGINAS 404:');
    results.filter(r => r.coverage === 'NOT_FOUND').forEach(r =>
      console.log(`  https://dolarexpress.cl/${r.slug}`)
    );
  }

  const csvPath = resolve(OUTPUT_DIR, 'gsc-inspection.csv');
  const csv = 'slug,url,verdict,coverage\n' +
    results.map(r => `"${r.slug}","${r.url}","${r.verdict}","${r.coverage.replace(/"/g, '""')}"`).join('\n');
  writeFileSync(csvPath, csv, 'utf-8');
  console.log(`\n✅ CSV guardado: ${csvPath}`);
}

inspectAll().catch(err => {
  console.error('\n💥 Error fatal:', err.message);
  process.exit(1);
});
