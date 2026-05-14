import { google } from 'googleapis';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = resolve(__dirname, '..', 'dist');

if (!existsSync(OUTPUT_DIR)) mkdirSync(OUTPUT_DIR, { recursive: true });

async function getAuthClient() {
  const jsonPaths = [
    resolve(__dirname, '..', 'gsc-credentials.json'),
    resolve(__dirname, '..', 'dolarexpress-seo-7f49ec49eb3c.json'),
  ];

  for (const jsonPath of jsonPaths) {
    if (existsSync(jsonPath)) {
      const key = JSON.parse(readFileSync(jsonPath, 'utf-8'));
      const jwtClient = new google.auth.JWT(
        key.client_email,
        null,
        key.private_key,
        ['https://www.googleapis.com/auth/webmasters.readonly'],
        null
      );
      await jwtClient.authorize();
      console.log(`✅ Autenticado con service account: ${key.client_email}`);
      return jwtClient;
    }
  }

  console.error('\n❌ No se encontró archivo JSON de service account.');
  console.error('\nBusca el archivo .json que descargaste de Google Cloud');
  console.error('y cópialo a esta carpeta:');
  console.error(resolve(__dirname, '..'));
  console.error('\nCon nombre: gsc-credentials.json');
  process.exit(1);
}

async function inspectAll() {
  const auth = await getAuthClient();
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
  const csv = 'slug,url,verdict,coverage,canonical\n' +
    results.map(r => `"${r.slug}","${r.url}","${r.verdict}","${r.coverage.replace(/"/g, '""')}","${r.canonical}"`).join('\n');
  writeFileSync(csvPath, csv, 'utf-8');
  console.log(`\n✅ CSV guardado: ${csvPath}`);
}

inspectAll().catch(err => {
  console.error('\n💥 Error fatal:', err.message);
  if (err.message.includes('not authorized') || err.message.includes('not found')) {
    console.error('\n📌 El service account necesita acceso en GSC:');
    console.error('   1. https://search.google.com/search-console');
    console.error('   2. Settings → Users and permissions → Add user');
    console.error(`   3. Email: seo-236@dolarexpress-seo.iam.gserviceaccount.com`);
  }
  process.exit(1);
});
