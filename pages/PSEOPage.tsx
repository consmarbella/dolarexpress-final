import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { pseoPages } from '../src/data/pseo-data.ts';
import Logo from '../components/Logo';

// Bank-specific data for unique content generation
const BANK_DATA: Record<string, { name: string; desc: string; fact: string; offices: string }> = {
  'banco-chile': { name: 'Banco de Chile', desc: 'el banco más grande del país con más de 2 millones de clientes', fact: 'Fue fundado en 1893 y es uno de los bancos más antiguos de Chile', offices: 'más de 200 sucursales a lo largo de Chile' },
  'bancoestado': { name: 'BancoEstado', desc: 'el banco estatal más grande de Chile con más de 3 millones de clientes', fact: 'Tiene la red de cajeros automáticos más extensa del país', offices: 'más de 350 sucursales en todo Chile' },
  'bci': { name: 'BCI', desc: 'uno de los bancos más innovadores de Chile con más de 1.5 millones de clientes', fact: 'Fue pionero en Chile con la banca digital y la app móvil', offices: 'más de 150 sucursales en Chile' },
  'santander': { name: 'Santander', desc: 'un banco internacional con fuerte presencia en Chile y más de 1.3 millones de clientes', fact: 'Santander fue el primer banco en Chile en ofrecer transferencias internacionales desde su app', offices: 'más de 120 sucursales en Chile' },
  'scotiabank': { name: 'Scotiabank', desc: 'un banco canadiense con presencia en Chile y más de 800 mil clientes', fact: 'Scotiabank opera con presencia en más de 50 países a nivel global', offices: 'más de 60 sucursales en Chile' },
  'itau': { name: 'Itaú', desc: 'el banco más grande de América Latina con presencia en Chile', fact: 'Itaú fue pionero en Chile con su programa de puntos LATAM Pass', offices: 'más de 80 sucursales en Chile' },
  'bice': { name: 'BICE', desc: 'un banco chileno con más de 40 años de experiencia', fact: 'BICE se destaca por su atención personalizada a cada cliente', offices: '20 sucursales en las principales ciudades de Chile' },
  'security': { name: 'Security', desc: 'un banco chileno especializado en banca privada y empresas', fact: 'Security se enfoca en clientes de altos ingresos con cupos preferenciales', offices: '30 sucursales en Chile' },
  'bbva': { name: 'BBVA', desc: 'un banco español con presencia en Chile', fact: 'BBVA tiene alianza con las principales aerolíneas del mundo', offices: 'más de 70 sucursales en Chile' },
};

const RETAIL_CARD_DATA: Record<string, { name: string; fullName: string; group: string; desc: string; fact: string; cupoRange: string; noAvance: boolean }> = {
  'lider': { name: 'Líder', fullName: 'Tarjeta Líder BCI', group: 'Walmart Chile', desc: 'la tarjeta de la cadena de supermercados más grande de Chile, respaldada por BCI', fact: 'La Tarjeta Líder no tiene avance en efectivo habilitado por defecto, pero su cupo de compras se puede convertir en efectivo con DolarExpress', cupoRange: '$100.000 a $1.500.000', noAvance: true },
  'cmr': { name: 'CMR Falabella', fullName: 'Tarjeta CMR Falabella', group: 'Falabella', desc: 'la tarjeta de retail más utilizada en Chile, con millones de tarjetahabientes activos', fact: 'La CMR Falabella es la tarjeta de grandes tiendas con mayor base de clientes en Chile, aunque su avance en efectivo tiene restricciones importantes', cupoRange: '$100.000 a $3.000.000', noAvance: true },
  'ripley': { name: 'Ripley', fullName: 'Tarjeta Ripley', group: 'Ripley Corp', desc: 'una de las tarjetas retail más reconocidas de Chile y Latinoamérica', fact: 'La Tarjeta Ripley opera en Chile, Perú y Colombia; muchos clientes no saben que pueden usar su cupo de compras para obtener efectivo sin necesitar avance habilitado', cupoRange: '$100.000 a $2.500.000', noAvance: true },
  'paris': { name: 'Paris', fullName: 'Tarjeta Paris Cencosud', group: 'Cencosud', desc: 'la tarjeta del grupo Cencosud, uno de los retailers más grandes de Sudamérica', fact: 'Paris pertenece al grupo Cencosud, que también opera Jumbo, Santa Isabel y Easy; su tarjeta tiene cupo compartido entre todos los formatos del grupo', cupoRange: '$100.000 a $2.000.000', noAvance: false },
  'la-polar': { name: 'La Polar', fullName: 'Tarjeta La Polar', group: 'La Polar S.A.', desc: 'la tarjeta retail más popular en el segmento trabajador chileno con presencia nacional', fact: 'La Polar tiene una de las mayores tasas de aprobación entre tarjetas retail en Chile, lo que la hace muy accesible para personas con historial crediticio ajustado', cupoRange: '$50.000 a $800.000', noAvance: true },
  'hites': { name: 'Hites', fullName: 'Tarjeta Hites', group: 'Hites S.A.', desc: 'una tarjeta retail con fuerte presencia en Santiago y regiones del país', fact: 'Hites es conocida por aprobar tarjetas a clientes que otras tiendas rechazan, lo que la hace muy valorada por personas con restricciones financieras', cupoRange: '$50.000 a $600.000', noAvance: true },
  'abcdin': { name: 'ABCDin', fullName: 'Tarjeta ABCDin', group: 'ABCDin', desc: 'la tarjeta retail especializada en electrodomésticos y tecnología para el hogar chileno', fact: 'ABCDin es reconocida por financiar productos del hogar en cuotas sin interés; su cupo puede convertirse en efectivo a través de DolarExpress', cupoRange: '$50.000 a $700.000', noAvance: true },
  'cencosud': { name: 'Cencosud', fullName: 'Tarjeta Cencosud', group: 'Cencosud S.A.', desc: 'la tarjeta del conglomerado retail más grande de Chile con cobertura en todos los formatos Cencosud', fact: 'Con la Tarjeta Cencosud podés comprar en Jumbo, Santa Isabel, Paris, Easy y más; su cupo consolidado suele ser mayor al de tarjetas individuales', cupoRange: '$100.000 a $2.500.000', noAvance: false },
  'johnson': { name: 'Johnson', fullName: 'Tarjeta Johnson', group: 'Johnson S.A.', desc: 'una tarjeta retail chilena con fuerte presencia en regiones y sectores populares', fact: 'Johnson tiene tiendas en múltiples ciudades fuera de Santiago; muchos clientes del interior del país nos prefieren para obtener efectivo con su tarjeta', cupoRange: '$50.000 a $500.000', noAvance: true },
  'easy': { name: 'Easy', fullName: 'Tarjeta Easy Cencosud', group: 'Cencosud', desc: 'la tarjeta de la cadena líder en materiales de construcción y mejoramiento del hogar en Chile', fact: 'Easy Cencosud es el retailer de construcción más grande de Chile; su tarjeta tiene cupo compartido con otros formatos del grupo Cencosud', cupoRange: '$100.000 a $1.500.000', noAvance: false },
  'jumbo': { name: 'Jumbo', fullName: 'Tarjeta Jumbo Cencosud', group: 'Cencosud', desc: 'la tarjeta del supermercado premium del grupo Cencosud con amplia presencia nacional', fact: 'Jumbo es reconocido como el supermercado premium de Chile; su tarjeta tiene cupo compartido con el grupo Cencosud, lo que puede significar montos más altos', cupoRange: '$100.000 a $2.000.000', noAvance: false },
  'corona': { name: 'Corona', fullName: 'Tarjeta Corona', group: 'Corona S.A.', desc: 'una tarjeta retail enfocada en vestuario y hogar para el segmento popular urbano de Chile', fact: 'Corona tiene una extensa red de tiendas en Santiago y regiones con atención cercana al cliente del sector popular', cupoRange: '$50.000 a $600.000', noAvance: true },
};

function detectBank(slug: string): { key: string; name: string; desc: string; fact: string; offices: string } | null {
  for (const [key, data] of Object.entries(BANK_DATA)) {
    if (slug.includes(key)) return { key, ...data };
  }
  return null;
}

function detectRetailCard(slug: string): { key: string; name: string; fullName: string; group: string; desc: string; fact: string; cupoRange: string; noAvance: boolean } | null {
  // Order matters: check more specific first
  const order = ['la-polar', 'abcdin', 'cencosud', 'johnson', 'corona', 'ripley', 'paris', 'hites', 'jumbo', 'easy', 'lider', 'cmr'];
  for (const key of order) {
    if (slug.includes(key)) return { key, ...RETAIL_CARD_DATA[key] };
  }
  return null;
}

function detectIntent(slug: string): string {
  if (slug.startsWith('como-')) return 'como';
  if (slug.includes('sin-dicom')) return 'sin-dicom';
  if (slug.includes('con-dicom') || slug.includes('estoy-en-dicom') || slug.includes('tengo-dicom')) return 'con-dicom';
  if (slug.includes('urgente') || slug.includes('rapida') || slug.includes('mismo-dia') || slug.includes('al-instante') || slug.includes('inmediata')) return 'urgente';
  if (slug.includes('online')) return 'online';
  if (slug.startsWith('vender-cupo') || slug.startsWith('liquidar-cupo')) return 'vender';
  if (slug.includes('transferir') || slug.includes('pasar-cupo') || slug.includes('convertir')) return 'convertir';
  if (slug.startsWith('plata-rapida') || slug.startsWith('efectivo-urgente') || slug.startsWith('efectivo-hoy') || slug.startsWith('efectivo-mismo-dia')) return 'efectivo-rapido';
  if (slug.startsWith('credito')) return 'credito';
  if (slug.includes('cupo-de-compras')) return 'cupo-compras';
  if (slug.includes('avance')) return 'avance';
  if (slug.includes('sin-liquidaciones') || slug.includes('sin-cotizaciones') || slug.includes('sin-cuenta') || slug.includes('sin-aval') || slug.includes('sin-garante') || slug.includes('sin-boleta') || slug.includes('sin-acreditar') || slug.includes('sin-papeles') || slug.includes('sin-banco') || slug.includes('solo-con-rut') || slug.includes('sin-requisitos')) return 'sin-requisitos';
  if (slug.includes('necesito-plata') || slug.includes('necesito-prestamo') || slug.includes('tengo-cupo') || slug.includes('no-me-dan') || slug.includes('no-me-aprueban')) return 'necesidad';
  return 'prestamo';
}

function detectCity(slug: string): string | null {
  const cities = ['santiago','concepcion','valparaiso','vina-del-mar','temuco','rancagua','antofagasta',
    'la-serena','puerto-montt','iquique','arica','chillan','calama','copiapo','osorno','talca',
    'valdivia','punta-arenas','las-condes','providencia','maipu','la-florida','penalolen',
    'nunoa','vitacura','lo-barnechea','recoleta','independencia','san-miguel','el-bosque',
    'quilicura','cerro-navia','renca','quinta-normal','estacion-central','linares','san-fernando',
    'san-antonio','santa-cruz','pichilemu','villaricca','pucon','castro','ancud','quellon',
    'osorno','la-union','rio-bueno','frutillar','puerto-varas','llanquihue'];
  for (const c of cities) {
    if (slug.includes(c)) return c;
  }
  return null;
}

function detectCardType(slug: string): string | null {
  const cards: Record<string, string> = {
    'visa-gold': 'Visa Gold',
    'visa-platinum': 'Visa Platinum',
    'visa-signature': 'Visa Signature',
    'mastercard-gold': 'Mastercard Gold',
    'mastercard-black': 'Mastercard Black',
    'mastercard-platinum': 'Mastercard Platinum',
    'amex': 'American Express',
    'cmr': 'CMR Falabella',
    'ripley': 'Ripley',
    'falabella': 'Falabella',
    'lider': 'Líder BCI',
  };
  for (const [key, name] of Object.entries(cards)) {
    if (slug.includes(key)) return name;
  }
  return null;
}

function slugToTitle(slug: string): string {
  return slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

const cityNames: Record<string, string> = {
  'santiago': 'Santiago', 'concepcion': 'Concepción', 'valparaiso': 'Valparaíso',
  'vina-del-mar': 'Viña del Mar', 'temuco': 'Temuco', 'rancagua': 'Rancagua',
  'antofagasta': 'Antofagasta', 'la-serena': 'La Serena', 'puerto-montt': 'Puerto Montt',
  'iquique': 'Iquique', 'arica': 'Arica', 'chillan': 'Chillán', 'calama': 'Calama',
  'copiapo': 'Copiapo', 'osorno': 'Osorno', 'talca': 'Talca', 'valdivia': 'Valdivia',
  'punta-arenas': 'Punta Arenas',
};

function generateUniqueMeta(page: { slug: string; title: string; card?: string; city?: string }): { title: string; description: string } {
  const parts = page.slug.split('/');
  const lastPart = parts[parts.length - 1] || page.slug;
  const bank = detectBank(lastPart);
  const retailCard = detectRetailCard(lastPart);
  const cardType = detectCardType(lastPart);
  const intent = detectIntent(lastPart);

  if (retailCard) {
    const intents: Record<string, { title: string; description: string }> = {
      'como': {
        title: lastPart.includes('liquidez') ? `Cómo Obtener Liquidez con Tarjeta ${retailCard.name} | DolarExpress` :
               lastPart.includes('plata-si-no-tengo-avance') ? `Cómo Sacar Plata sin Avance Habilitado | DolarExpress` :
               lastPart.includes('cupo-de-mi-tarjeta-sin-avance') ? `Cómo Usar el Cupo de tu Tarjeta ${retailCard.name} sin Avance | DolarExpress` :
               lastPart.includes('vender-cupo-dolar') ? `Cómo Vender tu Cupo Dólar Hoy | DolarExpress` :
               `Cómo Obtener Efectivo con Tarjeta ${retailCard.name} | DolarExpress`,
        description: lastPart.includes('liquidez') ? `Aprende cómo obtener liquidez con tu tarjeta ${retailCard.name}. Te explicamos el proceso paso a paso para convertir tu cupo en efectivo en 15 minutos sin avance habilitado.` :
                   lastPart.includes('plata-si-no-tengo-avance') ? `¿No tenés avance habilitado? Descubre cómo sacar plata con tu tarjeta de tienda usando el cupo de compras. DolarExpress te lo explica paso a paso.` :
                   lastPart.includes('cupo-de-mi-tarjeta-sin-avance') ? `Guía completa: cómo usar el cupo de tu tarjeta ${retailCard.name} sin avance habilitado. Conoce las opciones para convertir tu cupo en efectivo hoy.` :
                   lastPart.includes('vender-cupo-dolar') ? `Aprende cómo vender tu cupo en dólares de forma segura. DolarExpress te explica el proceso, tasas y cómo recibir tu dinero en minutos.` :
                   `Cómo obtener efectivo de tu tarjeta ${retailCard.name}. Guía paso a paso para usar tu cupo de compras sin avance.`
      },
      'sin-dicom': {
        title: `Préstamo Tarjeta ${retailCard.name} Sin Dicom | DolarExpress`,
        description: `¿Tenés tarjeta ${retailCard.name} y estás en DICOM? No importa tu historial. Solo necesitás cupo disponible. Recibís efectivo en 15 minutos.`
      },
      'con-dicom': {
        title: `Préstamo con Tarjeta ${retailCard.name} Estando en DICOM | DolarExpress`,
        description: `Estás en DICOM y tenés tarjeta ${retailCard.name} con cupo. Te damos efectivo igual. Sin revisión de historial. Transferencia en 15 minutos.`
      },
      'urgente': {
        title: `Efectivo Urgente Tarjeta ${retailCard.name} | DolarExpress`,
        description: `Necesitás plata urgente y tenés tarjeta ${retailCard.name}? Te transferimos en 15 minutos. Proceso express por WhatsApp, sin filas ni trámites.`
      },
      'online': {
        title: `Préstamo Online Tarjeta ${retailCard.name} | DolarExpress`,
        description: `Convertí tu cupo ${retailCard.name} en efectivo 100% online. Sin ir a sucursales, sin papeleos. Transferencia a tu cuenta en minutos.`
      },
      'vender': {
        title: `Vender Cupo ${retailCard.name} en Efectivo | DolarExpress`,
        description: `Vendé tu cupo de la tarjeta ${retailCard.name} y recibí efectivo hoy. Proceso simple por WhatsApp. Pagamos al instante vía transferencia bancaria.`
      },
      'convertir': {
        title: `Convertir Cupo ${retailCard.name} a Efectivo | DolarExpress`,
        description: `Convertí el cupo de tu tarjeta ${retailCard.name} en pesos chilenos hoy. Sin avance habilitado. Operación en 15 minutos por WhatsApp.`
      },
      'efectivo-rapido': {
        title: `Plata Rápida con Tarjeta ${retailCard.name} | DolarExpress`,
        description: `Obtenés plata rápida usando el cupo de tu tarjeta ${retailCard.name}. Transferencia en 15 minutos. Sin requisitos bancarios ni revisión de historial.`
      },
      'credito': {
        title: `Crédito con Tarjeta ${retailCard.name} | DolarExpress`,
        description: `Obtén crédito usando tu tarjeta ${retailCard.name} sin pasar por el banco. Usamos tu cupo de compras para darte efectivo en minutos.`
      },
      'cupo-compras': {
        title: `Préstamo con Cupo de Compras ${retailCard.name} | DolarExpress`,
        description: `Usá el cupo de compras de tu tarjeta ${retailCard.name} para obtener efectivo. No es avance, es diferente. Transferencia en 15 minutos.`
      },
      'avance': {
        title: `Alternativa al Avance Tarjeta ${retailCard.name} | DolarExpress`,
        description: `¿No tenés avance habilitado en tu tarjeta ${retailCard.name}? Usamos tu cupo de compras para darte efectivo igual. En 15 minutos.`
      },
      'sin-requisitos': {
        title: `Efectivo con Tarjeta ${retailCard.name} Sin Requisitos | DolarExpress`,
        description: `Sin liquidaciones, sin boletas, sin garante. Solo necesitás tu tarjeta ${retailCard.name} con cupo disponible. Recibís efectivo en 15 minutos.`
      },
      'necesidad': {
        title: `Tenés Cupo ${retailCard.name} y Necesitás Plata | DolarExpress`,
        description: `Si tenés cupo disponible en tu tarjeta ${retailCard.name}, te damos el efectivo que necesitás hoy. Sin banco, sin DICOM. Solo WhatsApp.`
      },
      'prestamo': {
        title: `Préstamo con Tarjeta ${retailCard.name} | DolarExpress`,
        description: `Obtén efectivo usando el cupo de compras de tu tarjeta ${retailCard.name}. Sin avance bancario, sin revisar DICOM. Transferencia en 15 minutos.`
      },
    };
    return intents[intent] || intents['prestamo'];
  }

  if (bank) {
    const citySlug = detectCity(lastPart);
    const cityName = citySlug ? (cityNames[citySlug] || slugToTitle(citySlug)) : '';
    const base = cityName ? ` en ${cityName}` : '';
    return {
      title: `Cupo Dólar ${bank.name}${base} | DolarExpress`,
      description: cityName
        ? `¿Tenés tarjeta ${bank.name} en ${cityName} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.fact}.`
        : `¿Tenés tarjeta ${bank.name} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos. ${bank.fact}.`,
    };
  }

  // Generic DICOM pages
  if (lastPart.includes('con-dicom') || lastPart.includes('estoy-en-dicom') || lastPart.includes('tengo-dicom')) {
    return {
      title: `Préstamo con DICOM usando Tarjeta de Tienda | DolarExpress`,
      description: `Estás en DICOM pero tenés tarjeta de tienda con cupo. Te damos efectivo igual. No revisamos historial crediticio. Transferencia en 15 minutos.`
    };
  }

  if (lastPart.includes('sin-dicom')) {
    return {
      title: `Préstamo Sin DICOM con Tarjeta de Tienda | DolarExpress`,
      description: `Obtenés efectivo sin que te revisen el DICOM. Solo necesitás cupo en tu tarjeta de tienda. Proceso 100% online, transferencia en 15 minutos.`
    };
  }

  if (cardType) return { title: `Cupo Dólar ${cardType} a Pesos | DolarExpress`, description: `¿Tenés tarjeta ${cardType} con cupo en dólares? Te lo compramos al instante. Transferencia en 15 minutos.` };
  if (lastPart.startsWith('avance')) return { title: slugToTitle(lastPart) + ' | DolarExpress', description: `¿Necesitás ${slugToTitle(lastPart).toLowerCase()}? Te compramos tu cupo en dólares y te transferimos al instante.` };
  const citySlugGen = detectCity(lastPart);
  const cityNameGen = citySlugGen ? (cityNames[citySlugGen] || slugToTitle(citySlugGen)) : '';
  if (citySlugGen && lastPart.startsWith('vender-cupo-dolar')) return { title: `Vender Cupo Dólar en ${cityNameGen} | DolarExpress`, description: `¿Necesitás vender tu cupo en dólares en ${cityNameGen}? Te lo compramos al instante. Transferencia en 15 minutos a tu cuenta bancaria. Seguro y 100% online.` };
  if (citySlugGen) return { title: page.title, description: `¿Tenés cupo en dólares en ${cityNameGen}? Te lo compramos al instante. Transferencia en 15 minutos. Proceso 100% online.` };
  return { title: page.title, description: `Compramos tu cupo en dólares en Chile. Transferencia inmediata y segura.` };
}

function generateUniqueContent(slug: string): { paragraph1: string; paragraph2: string; tip: string } {
  const bank = detectBank(slug);
  const retailCard = detectRetailCard(slug);
  const citySlug = detectCity(slug);
  const cityName = citySlug ? (cityNames[citySlug] || slugToTitle(citySlug)) : 'Chile';
  const cardType = detectCardType(slug);
  const intent = detectIntent(slug);

  if (retailCard) {
    const rc = retailCard;

    const contentByIntent: Record<string, { paragraph1: string; paragraph2: string; tip: string }> = {
      'como': {
        paragraph1: slug.includes('liquidez') ? `Obtener liquidez con tu tarjeta ${rc.fullName} es más simple de lo que pensás. ${rc.desc.charAt(0).toUpperCase() + rc.desc.slice(1)}. Si tenés cupo de compras disponible, podés convertirlo en efectivo hoy sin necesidad de tener avance habilitado. En DolarExpress somos especialistas en esto: hemos realizado miles de operaciones transformando cupo retail en pesos que llegan directamente a tu cuenta bancaria en menos de 15 minutos.` :
                 slug.includes('plata-si-no-tengo-avance') ? `La mayoría de las tarjetas retail en Chile, como la ${rc.fullName}, no tienen avance en efectivo disponible para todos los clientes. Esto deja a miles de personas sin opciones para acceder a liquidez cuando la necesitan. Pero existe una solución: tu cupo de compras. DolarExpress convierte ese cupo en pesos chilenos sin que necesites tener avance habilitado.` :
                 slug.includes('cupo-de-mi-tarjeta-sin-avance') ? `Tu tarjeta ${rc.fullName} tiene un cupo de compras entre ${rc.cupoRange} que podés usar normalmente en tiendas. Pero sabías que podés convertir ese mismo cupo en efectivo sin necesitar avance? En DolarExpress realizamos exactamente eso: usamos tu cupo de compras y te transferimos el equivalente en pesos a tu cuenta bancaria.` :
                 slug.includes('vender-cupo-dolar') ? `Vender tu cupo en dólares nunca fue tan fácil. Si tenés una tarjeta con cupo internacional (Visa, Mastercard, Amex), ese cupo en dólares tiene valor real. En DolarExpress lo compramos todos los días a las mejores tasas del mercado. El proceso es simple: nos muestras tu saldo en dólares, acordamos la tasa, y recibes la transferencia en pesos en tu cuenta bancaria.` :
                 `Tu tarjeta ${rc.fullName} es una herramienta financiera más poderosa de lo que creés. El cupo de compras entre ${rc.cupoRange} que tenés disponible puede convertirse en efectivo inmediato sin necesidad de avance bancario tradicional. DolarExpress es el especialista en Chile en esta operación.`,
        paragraph2: slug.includes('liquidez') ? `El proceso es directo y seguro: (1) Contactanos por WhatsApp. (2) Nos mostrás el cupo disponible en tu app ${rc.name}. (3) Te damos la mejor tasa del mercado sin comisiones ocultas. (4) Ejecutamos la operación. (5) Recibís la transferencia en tu CuentaRUT o cuenta corriente en menos de 15 minutos. No pedimos liquidaciones, boletas ni aval. Solo cupo disponible y tus datos bancarios para transferencia.` :
                 slug.includes('plata-si-no-tengo-avance') ? `Si no tenés avance habilitado en tu tarjeta ${rc.name}, el sistema bancario te dice que no podés sacar efectivo. Pero DolarExpress ofrece una alternativa real. Tu cupo de compras funciona diferente: lo usamos para efectuar una operación de compra y te transferimos el equivalente en pesos. El resultado es el mismo para vos: tenés efectivo en tu cuenta, sin pasar por el banco.` :
                 slug.includes('cupo-de-mi-tarjeta-sin-avance') ? `El cupo de compras es diferente del avance en efectivo. El avance es una función bancaria que requiere habilitar, mientras que el cupo de compras ya está activo en tu tarjeta ${rc.name}. Con DolarExpress usamos ese cupo de compras para darte efectivo. No es transferencias ni movimientos normales de tu tarjeta: es una operación directa entre nosotros y vos. Transferencia en 15 minutos.` :
                 slug.includes('vender-cupo-dolar') ? `Vender cupo dólar en DolarExpress es diferente a otras opciones. No necesitás ir a ningún lado ni compliar con requisitos bancarios complicados. Todo se maneja por WhatsApp: verificas tu saldo en dólares en tu app, nos dices qué monto querés vender, te mostramos la tasa, aceptás, ejecutamos y listo. La transferencia en pesos llega a tu cuenta en minutos. Operamos los 7 días de la semana, incluyendo feriados.` :
                 `El cupo de tu tarjeta ${rc.name} no es solo para comprar: puede convertirse en efectivo inmediato. El proceso es completamente diferente a un préstamo bancario. No evaluamos historial, no pedimos documentos, no hacemos consultas a registros de deudores. Solo verificamos que tengas cupo disponible y ejecutamos la operación en minutos.`,
        tip: slug.includes('liquidez') ? `${rc.fact}. La liquidez es crítica en situaciones inesperadas. Tener una tarjeta ${rc.name} con cupo disponible es como tener un fondo de emergencia instantáneo. Contacta a DolarExpress cualquier momento.` :
             slug.includes('plata-si-no-tengo-avance') ? `Dato importante: no todos los bancos habilitaban avance para todos los clientes. Muchas personas con tarjetas retail en Chile no tienen acceso a avance. ${rc.fact}. Con DolarExpress, eso no es un problema porque trabajamos con el cupo de compras.` :
             slug.includes('cupo-de-mi-tarjeta-sin-avance') ? `${rc.fact}. Tu tarjeta ${rc.name} es uno de tus activos financieros más valiosos. El cupo que te aprobaron está ahí para usarlo. Con DolarExpress lo convertís en efectivo cuando lo necesites.` :
             slug.includes('vender-cupo-dolar') ? `Los tipos de cambio varían constantemente. Cuando tenés cupo en dólares y necesitas pesos, el tiempo es importante. DolarExpress te da la mejor cotización al momento de la operación, sin retrasos ni esperas. Recibís tu dinero en minutos.` :
             `${rc.fact}. Muchos chilenos descubren DolarExpress cuando necesitan efectivo urgente y se dan cuenta de que su tarjeta ${rc.name} puede ser la solución.`
      },
      'sin-dicom': {
        paragraph1: `La tarjeta ${rc.fullName} es ${rc.desc}. Muchas personas en DICOM tienen esta tarjeta con cupo disponible pero creen que no pueden acceder a efectivo. En DolarExpress rompemos ese mito: no revisamos tu historial crediticio ni tu situación en DICOM. Lo único que necesitás es tener cupo de compras disponible en tu tarjeta ${rc.name}.`,
        paragraph2: `El proceso es completamente diferente a un préstamo bancario. No hacemos consultas al DICOM, no pedimos liquidaciones de sueldo ni boletas de honorarios. Coordinamos todo por WhatsApp: vos nos mostrás el cupo disponible en tu app, nosotros usamos ese cupo y te transferimos el efectivo equivalente a tu CuentaRUT o cuenta corriente en menos de 15 minutos.`,
        tip: `${rc.fact}. Muchos clientes con tarjeta ${rc.name} que estaban en DICOM ya recibieron efectivo con nosotros. El cupo de compras es tuyo y podés usarlo como quieras.`
      },
      'con-dicom': {
        paragraph1: `Si estás en DICOM y tenés una tarjeta ${rc.fullName} con cupo disponible, tenés una solución real hoy mismo. En DolarExpress trabajamos con personas que los bancos y financieras rechazan. Tu situación en el registro de deudores no nos afecta, porque no prestamos dinero: compramos tu cupo de compras y te pagamos en efectivo.`,
        paragraph2: `La lógica es simple: vos tenés cupo en tu tarjeta ${rc.name} que no podés convertir en efectivo por los canales normales. Nosotros te damos ese efectivo hoy, usando ese cupo. No hay evaluación crediticia, no hay score, no hay DICOM. Solo necesitás tener cupo disponible y seguir el proceso por WhatsApp. La transferencia llega en 15 minutos.`,
        tip: `Estar en DICOM no te impide usar tu tarjeta ${rc.name} para compras. Y si podés comprar, DolarExpress puede convertir ese cupo en efectivo para vos. ${rc.fact}.`
      },
      'urgente': {
        paragraph1: `Cuando necesitás plata urgente y tenés una tarjeta ${rc.fullName} con cupo disponible, DolarExpress es tu solución más rápida. Desde que nos escribís por WhatsApp hasta que el dinero llega a tu cuenta, el proceso completo tarda menos de 15 minutos. Sin filas, sin citas, sin papeleos.`,
        paragraph2: `El proceso express de DolarExpress funciona así: nos contactás por WhatsApp, nos mostrás el cupo disponible en tu app ${rc.name}, acordamos el monto y la tasa, ejecutamos la operación, y en menos de 15 minutos tenés la transferencia en tu cuenta. No importa si es de noche, un fin de semana o un festivo: operamos todos los días.`,
        tip: `${rc.fact}. Para emergencias financieras, tener una tarjeta ${rc.name} con cupo es como tener un respaldo de efectivo disponible las 24 horas.`
      },
      'online': {
        paragraph1: `Convertí el cupo de tu tarjeta ${rc.fullName} en efectivo sin salir de tu casa. En DolarExpress todo el proceso es 100% online: no necesitás ir a sucursales de la tienda, ni a un banco, ni a ningún lado. Solo necesitás tu celular y la app de tu tarjeta ${rc.name}.`,
        paragraph2: `Así funciona nuestro proceso online: (1) Abrís WhatsApp y nos contactás. (2) Verificás el cupo disponible en tu app ${rc.name}. (3) Acordamos monto y tasa. (4) Ejecutamos la operación desde la comodidad de tu hogar. (5) Recibís la transferencia en tu cuenta. Todo desde el sofá, en menos de 15 minutos.`,
        tip: `${rc.fact}. El proceso online de DolarExpress elimina las filas y los horarios de atención. Podés gestionar tu operación con tarjeta ${rc.name} en cualquier momento del día.`
      },
      'vender': {
        paragraph1: `Vender el cupo de tu tarjeta ${rc.fullName} en DolarExpress es el proceso más directo para convertir plástico en efectivo. Tu tarjeta ${rc.name} tiene un cupo de compras entre ${rc.cupoRange}. Ese cupo se puede liquidar hoy en efectivo sin necesitar avance habilitado, sin banco y sin burocracia.`,
        paragraph2: `El proceso de venta de cupo es seguro y transparente: te mostramos la tasa antes de aceptar, sin comisiones ocultas ni letras chicas. Una vez que acordás, la operación se ejecuta en minutos y la transferencia llega a tu CuentaRUT o cuenta corriente el mismo día. Pagamos los 7 días de la semana, incluyendo feriados.`,
        tip: `${rc.fact}. Muchos clientes venden su cupo ${rc.name} cuando necesitan liquidez inmediata para gastos imprevistos, cuentas médicas o aprovechar oportunidades de negocio.`
      },
      'convertir': {
        paragraph1: `Convertir el cupo de compras de tu tarjeta ${rc.fullName} en efectivo es el servicio central de DolarExpress. ${rc.desc.charAt(0).toUpperCase() + rc.desc.slice(1)}. Muchos holders de esta tarjeta no saben que su cupo de compras puede transformarse en pesos chilenos hoy mismo, sin avance habilitado y sin requisitos bancarios.`,
        paragraph2: `La conversión funciona de manera diferente al avance en efectivo tradicional. En lugar de cargar un avance a tu tarjeta, DolarExpress realiza una operación de compra usando tu cupo, y te transfiere el equivalente en pesos a tu cuenta bancaria. El resultado es el mismo para vos: recibís efectivo en minutos. La diferencia: lo podés hacer sin tener avance habilitado.`,
        tip: `${rc.fact}. El cupo de compras de tu tarjeta ${rc.name} es un activo que podés liquidar cuando lo necesitás. DolarExpress hace esa conversión de forma rápida y segura.`
      },
      'efectivo-rapido': {
        paragraph1: `Si necesitás plata rápida y tenés una tarjeta ${rc.fullName}, llegaste al lugar correcto. DolarExpress es especialista en convertir cupo de tarjetas de grandes tiendas en efectivo en el menor tiempo posible. Con tu tarjeta ${rc.name}, el proceso desde que nos contactás hasta que tenés el dinero en tu cuenta puede completarse en menos de 15 minutos.`,
        paragraph2: `¿Por qué somos tan rápidos? Porque hemos optimizado cada paso del proceso. No pedimos documentos, no hacemos evaluaciones crediticias, no esperamos aprobaciones. Si tenés cupo disponible en tu tarjeta ${rc.name}, el proceso es inmediato. Operamos de lunes a domingo, feriados incluidos, para que puedas acceder a tu efectivo cuando lo necesitás.`,
        tip: `${rc.fact}. La velocidad es nuestra ventaja principal. Mientras un banco puede demorar días en aprobar un crédito, DolarExpress convierte tu cupo ${rc.name} en efectivo en minutos.`
      },
      'credito': {
        paragraph1: `Obtener crédito en el sistema bancario chileno se ha vuelto difícil: piden liquidaciones, contratos de trabajo, revisión de DICOM y otros requisitos que muchos no cumplen. Si tenés una tarjeta ${rc.fullName}, tenés una alternativa real de crédito sin pasar por el banco. DolarExpress usa tu cupo de compras para darte efectivo, sin los requisitos del sistema financiero formal.`,
        paragraph2: `No es exactamente un crédito en el sentido tradicional: es la liquidación de tu cupo de compras. Vos tenés un cupo en tu tarjeta ${rc.name} que podés usar para compras. DolarExpress convierte ese cupo en pesos chilenos que van directamente a tu cuenta. El resultado para vos es el mismo que un crédito rápido: tenés el efectivo disponible hoy.`,
        tip: `${rc.fact}. Para muchos chilenos, su tarjeta ${rc.name} es su principal fuente de acceso al crédito informal. DolarExpress maximiza esa herramienta convirtiéndola en efectivo cuando lo necesitás.`
      },
      'cupo-compras': {
        paragraph1: `El cupo de compras de tu tarjeta ${rc.fullName} es más valioso de lo que pensás. Ese cupo, que normalmente usás para comprar en tiendas del grupo ${rc.group}, puede convertirse en efectivo directo a tu cuenta bancaria. DolarExpress es el especialista en Chile en esta operación: tomamos tu cupo de compras y te pagamos el equivalente en pesos, de forma inmediata.`,
        paragraph2: `La diferencia clave entre el cupo de compras y el avance en efectivo es que el cupo de compras es más fácil de activar y no requiere habilitar funciones especiales en tu tarjeta. ${rc.noAvance ? `La tarjeta ${rc.name} no tiene avance en efectivo disponible para todos los clientes, pero sí tiene cupo de compras que podés liquidar con DolarExpress.` : `Incluso si tenés avance habilitado en tu tarjeta ${rc.name}, usar el cupo de compras con DolarExpress puede ser una alternativa más conveniente.`}`,
        tip: `${rc.fact}. El cupo de compras entre ${rc.cupoRange} que tiene tu tarjeta ${rc.name} puede convertirse en efectivo hoy con DolarExpress. Consultá por WhatsApp sin compromiso.`
      },
      'avance': {
        paragraph1: `${rc.noAvance ? `La tarjeta ${rc.fullName} no tiene avance en efectivo disponible para la mayoría de los clientes. Este es un limitante real que afecta a miles de personas que necesitan liquidez urgente. DolarExpress ofrece la alternativa: usamos tu cupo de compras para darte efectivo, sin necesitar que el avance esté habilitado.` : `Aunque la tarjeta ${rc.fullName} tiene avance habilitado para algunos clientes, no todos lo tienen disponible o el monto puede ser insuficiente. DolarExpress complementa ese servicio usando tu cupo de compras para darte efectivo adicional.`}`,
        paragraph2: `El mecanismo es diferente al avance tradicional pero el resultado es el mismo: recibís efectivo en tu cuenta bancaria. No cargamos un "avance" a tu tarjeta, sino que realizamos una operación de compra usando tu cupo. Esto significa que el proceso está disponible incluso si tu tarjeta ${rc.name} no tiene avance habilitado. Todo por WhatsApp en menos de 15 minutos.`,
        tip: `${rc.fact}. Muchos clientes de tarjeta ${rc.name} descubren DolarExpress cuando se dan cuenta de que no tienen avance disponible pero necesitan efectivo urgente. Somos la alternativa que buscaban.`
      },
      'sin-requisitos': {
        paragraph1: `¿Cansado de que te pidan liquidaciones, boletas, contrato de trabajo o un garante para acceder a un préstamo? Con tu tarjeta ${rc.fullName}, DolarExpress te ofrece efectivo sin ninguno de esos requisitos. No importa si sos trabajador informal, independiente, o si tenés deudas: solo necesitás cupo disponible en tu tarjeta ${rc.name}.`,
        paragraph2: `La operación con DolarExpress no requiere documentación: sin liquidaciones de sueldo, sin boletas de honorarios, sin contrato de trabajo, sin cuenta corriente, sin garante y sin aval. El único requisito es tener cupo de compras disponible en tu tarjeta ${rc.name}. El resto lo manejamos nosotros por WhatsApp en menos de 15 minutos.`,
        tip: `${rc.fact}. El sistema financiero formal tiene barreras de entrada altas. Tu tarjeta ${rc.name} es la llave para acceder a efectivo sin esas barreras. DolarExpress hace el resto.`
      },
      'necesidad': {
        paragraph1: `Si tenés cupo disponible en tu tarjeta ${rc.fullName} y necesitás plata hoy, la solución está más cerca de lo que pensás. Miles de chilenos se encuentran en esa situación exacta: tienen cupo en su tarjeta ${rc.name} pero no saben cómo convertirlo en efectivo sin avance habilitado. DolarExpress es la respuesta.`,
        paragraph2: `El proceso es directo: nos escribís por WhatsApp, nos mostrás el cupo disponible en tu app ${rc.name}, te decimos exactamente cuánto te podemos transferir y a qué tasa, vos aceptás y en menos de 15 minutos el dinero está en tu cuenta. Sin burocracia, sin filas, sin requisitos. Solo tu tarjeta con cupo y tus ganas de resolver.`,
        tip: `${rc.fact}. Si estás viendo esta página es porque necesitás una solución financiera hoy. Tu tarjeta ${rc.name} con cupo disponible ES esa solución. Contactanos por WhatsApp ahora.`
      },
      'prestamo': {
        paragraph1: `Obtener un préstamo usando tu tarjeta ${rc.fullName} es posible y más simple de lo que creés. ${rc.desc.charAt(0).toUpperCase() + rc.desc.slice(1)}. DolarExpress opera con este tipo de tarjeta comprando tu cupo de compras y transfiriéndote el equivalente en pesos directamente a tu cuenta bancaria, en menos de 15 minutos.`,
        paragraph2: `No se trata de un préstamo en el sentido tradicional: no cargamos intereses al estilo bancario ni requiere aprobación crediticia. Usamos el cupo que ya tenés disponible en tu tarjeta ${rc.name}. El cupo de compras entre ${rc.cupoRange} que tiene tu tarjeta puede convertirse en efectivo hoy. Sin Dicom, sin garante, sin papeleos.`,
        tip: `${rc.fact}. La tarjeta ${rc.name} tiene cupo de compras que podés usar de muchas formas. Con DolarExpress, ese cupo se transforma en efectivo en minutos.`
      }
    };

    return contentByIntent[intent] || contentByIntent['prestamo'];
  }

  if (bank) {
    return {
      paragraph1: `${bank.name} es ${bank.desc}. ${bank.fact}. Si tenés una tarjeta de crédito de ${bank.name} con cupo internacional disponible en ${cityName}, nosotros te lo compramos al instante. El proceso es 100% online y no requiere que vayas a ninguna sucursal.`,
      paragraph2: `${bank.name} cuenta con ${bank.offices}. Si estás en ${cityName}, podés coordinar la operación completamente por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta en menos de 15 minutos.`,
      tip: `Dato de ${bank.name}: ${bank.fact}. Muchos clientes nos prefieren porque no necesitan ir al banco ni hacer filas.`,
    };
  }

  // Generic DICOM content
  if (slug.includes('con-dicom') || slug.includes('estoy-en-dicom') || slug.includes('tengo-dicom')) {
    return {
      paragraph1: `Estar en DICOM en Chile es una barrera real para acceder al sistema financiero formal. Los bancos y financieras rechazan automáticamente a las personas con registro en DICOM. Pero si tenés una tarjeta de tienda (CMR Falabella, Ripley, Paris, La Polar, Hites, Líder, Cencosud, ABCDin, Johnson, Corona) con cupo disponible, tenés una alternativa concreta con DolarExpress.`,
      paragraph2: `DolarExpress no revisa el DICOM. No nos interesa tu historial crediticio. Lo que nos importa es que tengas cupo disponible en tu tarjeta de grandes tiendas. Si lo tenés, podemos darte efectivo en 15 minutos. El proceso es por WhatsApp, sin documentos, sin evaluación y sin rechazo por deudas pasadas.`,
      tip: `En Chile, más del 20% de la población adulta tiene algún tipo de registro en DICOM. Si estás en ese grupo y tenés una tarjeta retail con cupo, DolarExpress tiene la solución. Contactanos hoy.`
    };
  }

  if (cardType) {
    return {
      paragraph1: `¿Tenés una tarjeta ${cardType} en ${cityName}? Nosotros te compramos el cupo en dólares al mejor tipo de cambio. El proceso es simple y rápido, sin papeleos ni trámites complicados.`,
      paragraph2: `Las tarjetas ${cardType} tienen cupo internacional disponible para compras en el extranjero. Ese mismo cupo podés convertirlo a pesos chilenos con nosotros. Te transferimos a tu cuenta en minutos.`,
      tip: `¿Sabías que muchas tarjetas como ${cardType} permiten usar el cupo internacional sin tener que activarlo? Verificá en tu app bancaria si tenés cupo disponible.`,
    };
  }

  if (citySlug) {
    return {
      paragraph1: `¿Estás en ${cityName} y querés vender tu cupo en dólares? En DolarExpress te compramos el cupo internacional de tu tarjeta de crédito al mejor tipo de cambio. El proceso es 100% online desde ${cityName}, sin moverte de tu casa.`,
      paragraph2: `Coordinamos todo por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta bancaria en menos de 15 minutos. No importa si estás en el centro de ${cityName} o en cualquier otra comuna, el proceso es el mismo: rápido, seguro y sin papeleos.`,
      tip: `En ${cityName}, muchas personas ya vendieron su cupo en dólares con nosotros. La mayoría de las tarjetas Visa y Mastercard emitidas en Chile tienen cupo internacional disponible sin necesidad de activación. Verificá en tu app bancaria.`,
    };
  }

  return {
    paragraph1: 'En DolarExpress te ofrecemos la solución más rápida y segura para convertir tu cupo en pesos chilenos. Olvidate de los trámites bancarios tradicionales, las filas y los papeleos.',
    paragraph2: 'Trabajamos con todas las tarjetas de grandes tiendas: CMR Falabella, Ripley, Paris, La Polar, Hites, Líder, Cencosud, ABCDin, Johnson, Easy, Jumbo y Corona. También con tarjetas bancarias con cupo en dólares.',
    tip: 'Muchas tarjetas retail como CMR, Ripley o Líder NO tienen avance en efectivo disponible. Nosotros usamos tu cupo de compras para darte efectivo al instante.',
  };
}

const PSEOPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const pageData = pseoPages.find(p => p.slug === slug);

  useEffect(() => {
    if (pageData) {
      const meta = generateUniqueMeta(pageData);
      document.title = meta.title;

      const metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) {
        metaDesc.setAttribute('content', meta.description);
      } else {
        const m = document.createElement('meta');
        m.name = 'description';
        m.content = meta.description;
        document.head.appendChild(m);
      }

      // Canonical
      let canonical = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
      if (!canonical) {
        canonical = document.createElement('link');
        canonical.rel = 'canonical';
        document.head.appendChild(canonical);
      }
      canonical.href = `https://dolarexpress.cl/${pageData.slug}`;
    }
  }, [pageData]);

  if (!pageData) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#1a1a1a] text-white">
        <h1 className="text-2xl font-bold">Página no encontrada</h1>
        <p className="text-gray-400 mt-2">La página que buscas no existe</p>
        <Link to="/" className="text-[#C8A045] mt-4 hover:underline">Volver al inicio</Link>
      </div>
    );
  }

  const meta = generateUniqueMeta(pageData);
  const title = meta.title.replace(' | DolarExpress', '');
  const whatsappText = `Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20${encodeURIComponent(title)}`;
  const uniqueContent = generateUniqueContent(pageData.slug);
  const retailCard = detectRetailCard(pageData.slug);

  // Generate interlinking URLs from same category
  const slugLower = slug?.toLowerCase() || '';
  const related = pseoPages
    .filter(p => {
      if (p.slug === slug) return false;
      // Bank pages: link to other bank pages
      if (slugLower.includes('banco') || slugLower.includes('bci') || slugLower.includes('santander') || slugLower.includes('scotiabank') || slugLower.includes('itau')) {
        return p.slug.includes('cupo-dolar-') && !p.slug.includes('/');
      }
      // Retail card pages: link to same brand or same intent
      if (retailCard) {
        const sameCard = p.slug.includes(retailCard.key) && p.slug !== slug;
        const sameIntent = detectIntent(p.slug) === detectIntent(slugLower) && detectRetailCard(p.slug) !== null;
        return sameCard || sameIntent;
      }
      // DICOM pages: link to other DICOM pages
      if (slugLower.includes('dicom')) {
        return p.slug.includes('dicom') && p.slug !== slug;
      }
      return false;
    })
    .slice(0, 8);

  return (
    <div className="min-h-screen flex flex-col font-sans text-[#1a1a1a]">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "FinancialService",
            name: title,
            description: meta.description,
            url: `https://dolarexpress.cl/${pageData.slug}`,
            provider: { "@type": "Organization", name: "DolarExpress", url: "https://dolarexpress.cl" },
            areaServed: { "@type": "Country", name: "Chile" },
          }),
        }}
      />

      {/* Navbar */}
      <nav className="fixed w-full z-50 bg-[#1a1a1a] shadow-sm border-b border-[#333]">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center max-w-6xl">
          <Link to="/" className="flex items-center gap-2">
            <Logo className="h-16 w-auto object-contain" />
          </Link>
          <div className="flex gap-4 items-center">
            <Link to="/" className="font-medium text-white hover:text-[#C8A045] hidden md:block">Inicio</Link>
            <Link to="/directorio-general" className="font-medium text-white hover:text-[#C8A045] hidden md:block">Directorio</Link>
            <a
              href="https://wa.me/56967658939?text=Hola%20DolarExpress%2C%20vengo%20de%20la%20web%20por%20Vender%20Cupo"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#C8A045] text-white px-5 py-2 rounded-lg font-bold"
            >
              Vender Cupo
            </a>
          </div>
        </div>
      </nav>

      {/* Breadcrumbs */}
      <nav className="pt-24 pb-2 bg-[#1a1a1a] text-gray-400 text-sm" aria-label="Breadcrumb">
        <div className="container mx-auto px-4 max-w-6xl">
          <ol className="flex flex-wrap gap-1">
            <li><Link to="/" className="hover:text-[#C8A045]">Inicio</Link></li>
            <li className="mx-1">/</li>
            <li className="text-white truncate max-w-[300px]" aria-current="page">{title}</li>
          </ol>
        </div>
      </nav>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            itemListElement: [
              { "@type": "ListItem", position: 1, name: "Inicio", item: "https://dolarexpress.cl/" },
              { "@type": "ListItem", position: 2, name: title, item: `https://dolarexpress.cl/${pageData.slug}` },
            ],
          }),
        }}
      />

      {/* Hero Section */}
      <header className="pt-36 pb-24 bg-[#1a1a1a] text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1a1a] via-[#2a2a2a] to-[#1a1a1a] z-0"></div>
        <div className="container mx-auto px-4 text-center z-10 relative max-w-4xl">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-6 leading-tight">
            {title}
          </h1>
          <p className="text-xl md:text-2xl mb-10 opacity-90 text-gray-200">
            {meta.description}
          </p>
          <div className="flex justify-center gap-4">
            <a
              href={`https://wa.me/56967658939?text=${whatsappText}`}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-[#C8A045] text-white text-lg px-10 py-4 rounded-xl font-bold hover:shadow-[0_0_25px_rgba(200,160,69,0.5)] transition-all transform hover:scale-105"
            >
              Cotizar por WhatsApp
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="py-20 bg-gray-50">
        <div className="container mx-auto px-4 max-w-4xl text-gray-700 leading-relaxed">
          <article>
            <h2 className="text-3xl font-bold text-[#1a1a1a] mb-6">{title}</h2>
            <p className="mb-6 text-lg">{meta.description}</p>
            <p className="mb-6">{uniqueContent.paragraph1}</p>
            <p className="mb-6">{uniqueContent.paragraph2}</p>

            <div className="grid md:grid-cols-3 gap-6 my-12">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">1. Cotizá Ahora</h3>
                <p className="text-sm">Contactanos por WhatsApp y te mostramos la mejor tasa del mercado para tu cupo en dólares.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">2. Validación</h3>
                <p className="text-sm">Procesamos tu solicitud de forma segura. Sin compartir claves bancarias ni datos sensibles.</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                <h3 className="font-bold text-[#C8A045] text-lg mb-2">3. Pago Inmediato</h3>
                <p className="text-sm">Recibís la transferencia en tu cuenta bancaria en menos de 15 minutos. Rápido, seguro y sin complicaciones.</p>
              </div>
            </div>

            <h3 className="text-2xl font-bold text-[#1a1a1a] mb-4">¿Por qué elegir DolarExpress?</h3>
            <ul className="list-disc pl-6 mb-8 space-y-2">
              <li><strong>Transferencia en 15 minutos:</strong> Coordinamos todo por WhatsApp y el dinero llega al instante a tu CuentaRUT o cuenta corriente.</li>
              <li><strong>Sin Dicom ni aval:</strong> No revisamos tu historial crediticio. Solo necesitás tener cupo disponible en tu tarjeta.</li>
              <li><strong>100% online:</strong> Todo desde tu celular, sin ir a sucursales, sin filas, sin papeleos.</li>
              <li><strong>Mejor tasa del mercado:</strong> Te mostramos la tasa antes de aceptar. Sin sorpresas, sin comisiones ocultas.</li>
              <li><strong>Seguro y transparente:</strong> Operamos con años de experiencia en el mercado chileno. Miles de operaciones realizadas.</li>
            </ul>

            <div className="bg-[#C8A045]/10 p-6 rounded-xl border border-[#C8A045]/30 my-8">
              <p className="text-lg font-semibold text-[#1a1a1a] mb-2">💡 ¿Sabías que...?</p>
              <p>{uniqueContent.tip}</p>
            </div>

            {retailCard && (
              <div className="mt-10">
                <h3 className="text-2xl font-bold text-[#1a1a1a] mb-6">Preguntas frecuentes sobre tarjeta {retailCard.name}</h3>
                <div className="space-y-4">
                  <details className="bg-white rounded-xl border border-gray-100 p-5">
                    <summary className="font-semibold text-[#C8A045] cursor-pointer">¿Necesito tener avance habilitado en mi tarjeta {retailCard.name}?</summary>
                    <p className="mt-3 text-gray-600">{retailCard.noAvance ? `No. La mayoría de los clientes con tarjeta ${retailCard.name} no tienen avance habilitado, y aun así pueden usar DolarExpress. Trabajamos con el cupo de compras, no con el avance en efectivo.` : `No es necesario. Aunque tu tarjeta ${retailCard.name} puede tener avance disponible, DolarExpress usa el cupo de compras para darte efectivo, lo que puede ser más conveniente y rápido.`}</p>
                  </details>
                  <details className="bg-white rounded-xl border border-gray-100 p-5">
                    <summary className="font-semibold text-[#C8A045] cursor-pointer">¿Cuánto efectivo puedo obtener con mi tarjeta {retailCard.name}?</summary>
                    <p className="mt-3 text-gray-600">Depende del cupo disponible en tu tarjeta. Las tarjetas {retailCard.name} suelen tener cupos entre {retailCard.cupoRange}. El monto que te transferimos corresponde al cupo que uses, menos nuestra comisión por el servicio.</p>
                  </details>
                  <details className="bg-white rounded-xl border border-gray-100 p-5">
                    <summary className="font-semibold text-[#C8A045] cursor-pointer">¿Me revisan el DICOM para operar con tarjeta {retailCard.name}?</summary>
                    <p className="mt-3 text-gray-600">No revisamos el DICOM ni ningún registro de deudas. Solo nos importa que tengas cupo disponible en tu tarjeta {retailCard.name}. Si tenés cupo, podemos operar.</p>
                  </details>
                  <details className="bg-white rounded-xl border border-gray-100 p-5">
                    <summary className="font-semibold text-[#C8A045] cursor-pointer">¿Cuánto tiempo tarda la transferencia?</summary>
                    <p className="mt-3 text-gray-600">Una vez que acordamos los términos y ejecutamos la operación, la transferencia llega a tu CuentaRUT o cuenta corriente en menos de 15 minutos. Operamos de lunes a domingo, incluyendo feriados.</p>
                  </details>
                </div>
              </div>
            )}
          </article>
        </div>
      </main>

      {/* Related Services */}
      {related.length > 0 && (
        <section className="py-12 bg-white border-t border-gray-100">
          <div className="container mx-auto px-4 max-w-4xl">
            <h3 className="text-xl font-bold text-[#1a1a1a] mb-6">Servicios relacionados</h3>
            <div className="flex flex-wrap gap-3">
              {related.map(r => (
                <Link
                  key={r.slug}
                  to={`/${r.slug}`}
                  className="text-sm text-[#C8A045] bg-gray-50 border border-[#C8A045]/20 px-4 py-2 rounded-full hover:bg-[#C8A045] hover:text-white transition"
                >
                  {generateUniqueMeta(r).title.replace(' | DolarExpress', '')}
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="bg-[#1a1a1a] text-white py-12 mt-auto">
        <div className="container mx-auto px-4 max-w-6xl text-center">
          <div className="flex justify-center gap-6 mb-6 text-sm text-gray-400">
            <Link to="/" className="hover:text-[#C8A045]">Inicio</Link>
            <Link to="/directorio-general" className="hover:text-[#C8A045]">Directorio</Link>
            <Link to="/testimonios" className="hover:text-[#C8A045]">Testimonios</Link>
            <Link to="/preguntas-frecuentes" className="hover:text-[#C8A045]">FAQ</Link>
            <Link to="/privacidad" className="hover:text-[#C8A045]">Privacidad</Link>
            <Link to="/contacto" className="hover:text-[#C8A045]">Contacto</Link>
          </div>
          <p className="text-xs text-gray-500">
            © {new Date().getFullYear()} DolarExpress. Especialistas en compra de cupo en dólares.
          </p>
        </div>
      </footer>

      {/* WhatsApp Button Fixed */}
      <a
        href={`https://wa.me/56967658939?text=${whatsappText}`}
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 bg-[#25D366] w-14 h-14 rounded-full flex items-center justify-center text-white shadow-lg hover:bg-[#20ba5a] transition-colors md:hover:scale-110 md:animate-none animate-pulse-custom"
        aria-label="Contactar por WhatsApp"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" viewBox="0 0 16 16">
          <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z" />
        </svg>
      </a>
    </div>
  );
};

export default PSEOPage;
