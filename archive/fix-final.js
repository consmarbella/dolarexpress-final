import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dir = path.join(__dirname, 'public');

// ── VENDER CUPO BANCO CHILE ──
let html = fs.readFileSync(path.join(dir, 'vender-cupo-banco-chile.html'), 'utf-8');
html = html.replace(/<title>.*?<\/title>/, '<title>Vender Cupo Dolar Banco de Chile: Proceso y Pago | DolarExpress</title>');
html = html.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="Vende tu cupo en dolares del Banco de Chile. Tarjetas Visa Signature, Mastercard Black, Amex. Transferencia inmediata, sin tramites.">');
html = html.replace(/<meta property="og:description" content="[^"]*">/, '<meta property="og:description" content="Vende tu cupo en dolares del Banco de Chile. Tarjetas Visa Signature, Mastercard Black, Amex.">');
html = html.replace(/<p class="lead">.*?<\/p>/, '<p class="lead">Banco de Chile ofrece tarjetas de credito con cupo internacional en Visa, Mastercard y American Express. Converti tu cupo a pesos chilenos con DolarExpress: proceso 100% online, pago en 15 minutos.</p>');
html = html.replace(/<div class="tip"><strong>.*?<br>.*?<\/div>/, '<div class="tip"><strong>Dato clave</strong><br>Las tarjetas premium de Banco de Chile (Visa Signature, Mastercard Black) suelen tener los cupos internacionales mas altos del mercado chileno, superando los USD 2.000.</div>');
html = html.replace(/BancoEstado/g, 'Banco de Chile');
const bcFaq = '<p><strong>Puedo vender el cupo de cualquier tarjeta del Banco de Chile?</strong><br>Si. Visa, Mastercard y American Express de Banco de Chile. Todas son compatibles con nuestro servicio.</p><p><strong>Afecta mi historial crediticio?</strong><br>No. La operacion usa tu cupo internacional de compras, no afecta tu scoring.</p><p><strong>Cuanto recibo por mi cupo del Banco de Chile?</strong><br>Depende del monto y la tasa del dia. Te cotizamos sin compromiso por WhatsApp.</p>';
html = html.replace(/(Cotizar por WhatsApp<\/a>)\s*(<\/div>\s*<\/main>)/, '$1\n<h2>Preguntas Frecuentes</h2>\n' + bcFaq + '\n$2');
fs.writeFileSync(path.join(dir, 'vender-cupo-banco-chile.html'), html);
console.log('[OK] vender-cupo-banco-chile');

// ── VISA GOLD ──
html = fs.readFileSync(path.join(dir, 'cupo-dolar-visa-gold.html'), 'utf-8');
html = html.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="Cupo Dolar Visa Gold Chile: cambia tu cupo a pesos. Tarjeta de entrada con cupo internacional. Transferencia en 15 min.">');
html = html.replace(/<meta property="og:description" content="[^"]*">/, '<meta property="og:description" content="Cupo Dolar Visa Gold Chile: cambia tu cupo a pesos. Tarjeta de entrada con cupo internacional.">');
html = html.replace(/<p class="lead">.*?<\/p>/, '<p class="lead">La Visa Gold es la tarjeta de entrada al mundo de los cupos internacionales. Ideal si tenes tu primera tarjeta de credito. Los cupos suelen ir desde USD 300 a USD 1.000, perfectos para una primera operacion de venta de cupo.</p>');
html = html.replace(/<div class="tip"><strong>.*?<br>.*?<\/div>/, '<div class="tip"><strong>Dato clave</strong><br>Las Visa Gold son las tarjetas mas comunes en Chile. Si la tenes hace mas de 6 meses, es muy probable que ya tengas cupo internacional acumulado sin usar.</div>');
const vgFaq = '<p><strong>Cuanto cupo tiene una Visa Gold tipica?</strong><br>Generalmente entre USD 300 y USD 1.000, dependiendo del banco y tu historial crediticio.</p><p><strong>Puedo vender el cupo si es mi primera vez?</strong><br>Si. Te guiamos paso a paso. El proceso es el mismo para cualquier tipo de Visa.</p><p><strong>Necesito un minimo de antiguedad?</strong><br>No. Mientras tengas cupo internacional disponible, podes operar sin importar hace cuanto tenes la tarjeta.</p>';
html = html.replace(/(Cotizar por WhatsApp<\/a>)\s*(<\/div>\s*<\/main>)/, '$1\n<h2>Preguntas Frecuentes</h2>\n' + vgFaq + '\n$2');
fs.writeFileSync(path.join(dir, 'cupo-dolar-visa-gold.html'), html);
console.log('[OK] cupo-dolar-visa-gold');

// ── VISA PLATINUM ──
html = fs.readFileSync(path.join(dir, 'cupo-dolar-visa-platinum.html'), 'utf-8');
html = html.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="Cupo Dolar Visa Platinum: converti tu cupo premium a pesos. Mayores limites, beneficios de viaje. Transferencia inmediata.">');
html = html.replace(/<meta property="og:description" content="[^"]*">/, '<meta property="og:description" content="Cupo Dolar Visa Platinum: converti tu cupo premium a pesos. Mayores limites, beneficios de viaje.">');
html = html.replace(/<p class="lead">.*?<\/p>/, '<p class="lead">La Visa Platinum es un paso arriba de la Gold. Ofrece mayores limites de cupo internacional (USD 1.500 a USD 3.000 tipicamente) y beneficios adicionales como seguros de viaje y asistencia. Converti tu cupo Platinum a pesos con la mejor tasa.</p>');
html = html.replace(/<div class="tip"><strong>.*?<br>.*?<\/div>/, '<div class="tip"><strong>Dato clave</strong><br>Las tarjetas Visa Platinum suelen acumular mas cupo internacional que las Gold porque estan disenadas para viajeros frecuentes. Muchos clientes Platinum tienen cupos sin usar de meses anteriores.</div>');
const vpFaq = '<p><strong>Cual es el cupo tipico de una Visa Platinum?</strong><br>Entre USD 1.500 y USD 3.000, aunque puede ser mayor segun tu perfil crediticio y el banco emisor.</p><p><strong>Pierdo los beneficios de viaje al vender el cupo?</strong><br>No. Los seguros de viaje, asistencia y otros beneficios Visa Platinum no se ven afectados por la operacion.</p><p><strong>La tasa es mejor para tarjetas Platinum?</strong><br>La tasa depende del mercado, no del tipo de tarjeta. Pero al tener cupos mas altos, la operacion es mas eficiente.</p>';
html = html.replace(/(Cotizar por WhatsApp<\/a>)\s*(<\/div>\s*<\/main>)/, '$1\n<h2>Preguntas Frecuentes</h2>\n' + vpFaq + '\n$2');
fs.writeFileSync(path.join(dir, 'cupo-dolar-visa-platinum.html'), html);
console.log('[OK] cupo-dolar-visa-platinum');

// ── MASTERCARD BLACK ──
html = fs.readFileSync(path.join(dir, 'cupo-dolar-mastercard-black.html'), 'utf-8');
html = html.replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="Cupo Dolar Mastercard Black: converti tu cupo premium elite a pesos. Limites altos, beneficios exclusivos. Pago inmediato.">');
html = html.replace(/<meta property="og:description" content="[^"]*">/, '<meta property="og:description" content="Cupo Dolar Mastercard Black: converti tu cupo premium elite a pesos. Limites altos, beneficios exclusivos.">');
html = html.replace(/<p class="lead">.*?<\/p>/, '<p class="lead">La Mastercard Black es la categoria elite de Mastercard en Chile. Ofrece los cupos internacionales mas altos (desde USD 3.000), acceso a salas VIP en aeropuertos y servicio de concierge. Converti ese cupo elite a liquidez inmediata con DolarExpress.</p>');
html = html.replace(/<div class="tip"><strong>.*?<br>.*?<\/div>/, '<div class="tip"><strong>Dato clave</strong><br>Las Mastercard Black pueden tener cupos internacionales superiores a USD 5.000. Muchos tarjetahabientes Black no usan ni el 20% de su cupo en dolares, dejando miles de dolares sin utilizar.</div>');
const mbFaq = '<p><strong>Cual es el cupo tipico de una Mastercard Black?</strong><br>Desde USD 3.000, pudiendo superar los USD 10.000 en algunos casos. Es la categoria con los cupos mas altos del mercado chileno.</p><p><strong>Hay algun limite maximo para vender?</strong><br>No tenemos limite maximo. Mientras tengas cupo disponible, podemos operar. Los montos altos se procesan con la misma rapidez.</p><p><strong>Los beneficios Black se mantienen?</strong><br>Si. Acceso a salas VIP, concierge, seguros y todos los beneficios de tu Mastercard Black se mantienen intactos.</p>';
html = html.replace(/(Cotizar por WhatsApp<\/a>)\s*(<\/div>\s*<\/main>)/, '$1\n<h2>Preguntas Frecuentes</h2>\n' + mbFaq + '\n$2');
fs.writeFileSync(path.join(dir, 'cupo-dolar-mastercard-black.html'), html);
console.log('[OK] cupo-dolar-mastercard-black');

console.log('\nListo: 1 legacy + 3 visa tiers diferenciados.');
