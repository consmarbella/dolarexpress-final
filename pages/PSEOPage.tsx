import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { pseoPages, PSEOPageData } from '../src/data/pseo-data.ts';
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

function detectBank(slug: string): { key: string; name: string; desc: string; fact: string; offices: string } | null {
  for (const [key, data] of Object.entries(BANK_DATA)) {
    if (slug.includes(key)) return { key, ...data };
  }
  return null;
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
  'las-condes': 'Las Condes', 'providencia': 'Providencia', 'maipu': 'Maipú',
  'la-florida': 'La Florida', 'penalolen': 'Peñalolén', 'nunoa': 'Ñuñoa',
  'vitacura': 'Vitacura', 'lo-barnechea': 'Lo Barnechea', 'recoleta': 'Recoleta',
  'independencia': 'Independencia', 'san-miguel': 'San Miguel', 'el-bosque': 'El Bosque',
  'quilicura': 'Quilicura', 'cerro-navia': 'Cerro Navia', 'renca': 'Renca',
  'quinta-normal': 'Quinta Normal', 'estacion-central': 'Estación Central',
  'linares': 'Linares', 'san-fernando': 'San Fernando', 'san-antonio': 'San Antonio',
  'santa-cruz': 'Santa Cruz', 'pichilemu': 'Pichilemu', 'villaricca': 'Villarrica',
  'pucon': 'Pucón', 'castro': 'Castro', 'ancud': 'Ancud', 'quellon': 'Quellón',
  'la-union': 'La Unión', 'rio-bueno': 'Río Bueno', 'frutillar': 'Frutillar',
  'puerto-varas': 'Puerto Varas', 'llanquihue': 'Llanquihue', 'los-angeles': 'Los Ángeles',
};

// City-specific data for rich unique content generation
interface CityData {
  name: string; region: string; poblacion: string; bancos: string; sucursales: number; fact: string;
}
const CITY_DATA: Record<string, CityData> = {"santiago":{"name":"Santiago","region":"RM","poblacion":"6.2M","bancos":"Banco de Chile, Santander, BCI, Scotiabank, Itaú, BancoEstado, Security, BBVA, BICE","sucursales":582,"fact":"Concentra más del 40% del PIB nacional y alberga las casas matrices de todos los bancos del país"},"concepcion":{"name":"Concepción","region":"Biobío","poblacion":"1M","bancos":"BancoEstado, Santander, BCI, Banco de Chile, Scotiabank","sucursales":98,"fact":"Es la segunda área metropolitana más grande de Chile"},"valparaiso":{"name":"Valparaíso","region":"Valparaíso","poblacion":"900K","bancos":"Banco de Chile, Santander, BCI, BancoEstado, Scotiabank","sucursales":76,"fact":"Alberga el Congreso Nacional y es el principal puerto comercial"},"vina-del-mar":{"name":"Viña del Mar","region":"Valparaíso","poblacion":"330K","bancos":"Banco de Chile, Santander, BCI, BancoEstado, Itaú","sucursales":45,"fact":"Es la capital turística de Chile"},"temuco":{"name":"Temuco","region":"La Araucanía","poblacion":"280K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":35,"fact":"Es el centro financiero y comercial de la Araucanía"},"rancagua":{"name":"Rancagua","region":"O'Higgins","poblacion":"240K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":30,"fact":"Es la puerta de entrada a la Región del Vino"},"antofagasta":{"name":"Antofagasta","region":"Antofagasta","poblacion":"360K","bancos":"Banco de Chile, Santander, BCI, Scotiabank, BancoEstado, Itaú","sucursales":42,"fact":"Es la capital minera de Chile"},"la-serena":{"name":"La Serena","region":"Coquimbo","poblacion":"250K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":28,"fact":"Es una de las ciudades más antiguas de Chile, fundada en 1544"},"puerto-montt":{"name":"Puerto Montt","region":"Los Lagos","poblacion":"200K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":25,"fact":"Es el centro financiero del sur de Chile, puerta a la Patagonia"},"iquique":{"name":"Iquique","region":"Tarapacá","poblacion":"190K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank, Itaú","sucursales":22,"fact":"Es la capital de la Zona Franca ZOFRI"},"arica":{"name":"Arica","region":"Arica y Parinacota","poblacion":"170K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":18,"fact":"Es la puerta de entrada a Chile desde Perú y Bolivia"},"chillan":{"name":"Chillán","region":"Ñuble","poblacion":"180K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":20,"fact":"Es la capital de la Región de Ñuble"},"calama":{"name":"Calama","region":"Antofagasta","poblacion":"160K","bancos":"Banco de Chile, Santander, BCI, Scotiabank, BancoEstado","sucursales":15,"fact":"Ciudad más cercana a Chuquicamata, la mina de cobre más grande del mundo"},"copiapo":{"name":"Copiapo","region":"Atacama","poblacion":"150K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":16,"fact":"Fue el centro del rescate de los 33 mineros en 2010"},"osorno":{"name":"Osorno","region":"Los Lagos","poblacion":"150K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":14,"fact":"Corazón de la industria lechera de Chile"},"talca":{"name":"Talca","region":"Maule","poblacion":"220K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank, Itaú","sucursales":24,"fact":"Es la capital de la Región del Maule, el granero de Chile"},"valdivia":{"name":"Valdivia","region":"Los Ríos","poblacion":"160K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":16,"fact":"Famosa por su cerveza artesanal y la Feria Fluvial"},"punta-arenas":{"name":"Punta Arenas","region":"Magallanes","poblacion":"130K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":12,"fact":"Es la ciudad más austral del mundo continental chileno"},"las-condes":{"name":"Las Condes","region":"RM","poblacion":"300K","bancos":"Banco de Chile, Santander, BCI, Scotiabank, Itaú, Security, BBVA, BICE","sucursales":80,"fact":"Es el barrio financiero de Santiago"},"providencia":{"name":"Providencia","region":"RM","poblacion":"140K","bancos":"Banco de Chile, Santander, BCI, Scotiabank, Itaú, Security","sucursales":55,"fact":"Centro corporativo y comercial del sector oriente"},"maipu":{"name":"Maipú","region":"RM","poblacion":"520K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":25,"fact":"Es la comuna más poblada de Chile"},"la-florida":{"name":"La Florida","region":"RM","poblacion":"360K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":20,"fact":"Segunda comuna más poblada de Santiago"},"penalolen":{"name":"Peñalolén","region":"RM","poblacion":"240K","bancos":"BancoEstado, Santander, Banco de Chile, BCI","sucursales":12,"fact":"Mayor crecimiento inmobiliario de Santiago"},"nunoa":{"name":"Ñuñoa","region":"RM","poblacion":"210K","bancos":"Banco de Chile, Santander, BCI, Scotiabank, Itaú","sucursales":30,"fact":"Comuna residencial con el Estadio Nacional"},"vitacura":{"name":"Vitacura","region":"RM","poblacion":"85K","bancos":"Banco de Chile, Santander, BCI, Itaú, Security, BBVA","sucursales":35,"fact":"Comuna con mayor renta per cápita de Chile"},"lo-barnechea":{"name":"Lo Barnechea","region":"RM","poblacion":"100K","bancos":"Banco de Chile, Santander, BCI, Itaú, Security","sucursales":18,"fact":"Incluye el exclusivo sector de La Dehesa"},"recoleta":{"name":"Recoleta","region":"RM","poblacion":"160K","bancos":"BancoEstado, Santander, Banco de Chile, BCI","sucursales":10,"fact":"Comuna comercial con ferias libres y emprendedores"},"independencia":{"name":"Independencia","region":"RM","poblacion":"130K","bancos":"BancoEstado, Santander, Banco de Chile","sucursales":8,"fact":"Comuna universitaria con la Facultad de Medicina UChile"},"san-miguel":{"name":"San Miguel","region":"RM","poblacion":"100K","bancos":"BancoEstado, Santander, Banco de Chile, BCI, Scotiabank","sucursales":14,"fact":"Comuna tradicional del sur de Santiago"},"el-bosque":{"name":"El Bosque","region":"RM","poblacion":"180K","bancos":"BancoEstado, Santander, Banco de Chile","sucursales":6,"fact":"Muchas personas usan tarjeta retail"},"quilicura":{"name":"Quilicura","region":"RM","poblacion":"210K","bancos":"BancoEstado, Santander, BCI","sucursales":8,"fact":"Rápido crecimiento industrial y poblacional"},"cerro-navia":{"name":"Cerro Navia","region":"RM","poblacion":"130K","bancos":"BancoEstado, Santander","sucursales":4,"fact":"Familias venden su cupo para cubrir gastos"},"renca":{"name":"Renca","region":"RM","poblacion":"150K","bancos":"BancoEstado, Santander, Banco de Chile","sucursales":6,"fact":"Alberga el Parque Industrial de Renca"},"quinta-normal":{"name":"Quinta Normal","region":"RM","poblacion":"100K","bancos":"BancoEstado, Santander","sucursales":5,"fact":"Alberga el Museo Nacional de Historia Natural"},"estacion-central":{"name":"Estación Central","region":"RM","poblacion":"140K","bancos":"BancoEstado, Santander, Banco de Chile, BCI","sucursales":10,"fact":"Centro de transporte más importante de Chile"},"linares":{"name":"Linares","region":"Maule","poblacion":"90K","bancos":"BancoEstado, Santander, Banco de Chile, BCI","sucursales":10,"fact":"Capital de la Huasa"},"san-fernando":{"name":"San Fernando","region":"O'Higgins","poblacion":"70K","bancos":"BancoEstado, Santander, Banco de Chile","sucursales":8,"fact":"Capital de Colchagua, corazón de la Ruta del Vino"},"san-antonio":{"name":"San Antonio","region":"Valparaíso","poblacion":"90K","bancos":"BancoEstado, Santander, Banco de Chile, BCI","sucursales":10,"fact":"Puerto más grande de Chile en movimiento de carga"},"santa-cruz":{"name":"Santa Cruz","region":"O'Higgins","poblacion":"35K","bancos":"BancoEstado, Santander","sucursales":4,"fact":"Corazón del Valle de Colchagua"},"pichilemu":{"name":"Pichilemu","region":"O'Higgins","poblacion":"15K","bancos":"BancoEstado","sucursales":2,"fact":"Capital mundial del surf en Chile"},"villaricca":{"name":"Villarrica","region":"La Araucanía","poblacion":"55K","bancos":"BancoEstado, Santander, Banco de Chile","sucursales":5,"fact":"A los pies del Volcán Villarrica"},"pucon":{"name":"Pucón","region":"La Araucanía","poblacion":"28K","bancos":"BancoEstado, Santander","sucursales":3,"fact":"Destino de turismo aventura más importante de Chile"},"castro":{"name":"Castro","region":"Los Lagos","poblacion":"45K","bancos":"BancoEstado, Santander","sucursales":5,"fact":"Capital de Chiloé, famosa por sus palafitos"},"ancud":{"name":"Ancud","region":"Los Lagos","poblacion":"42K","bancos":"BancoEstado","sucursales":4,"fact":"Puerta de entrada a la Isla de Chiloé"},"quellon":{"name":"Quellón","region":"Los Lagos","poblacion":"30K","bancos":"BancoEstado","sucursales":3,"fact":"Ultimo puerto de la Carretera Austral en Chiloé"},"la-union":{"name":"La Unión","region":"Los Ríos","poblacion":"40K","bancos":"BancoEstado","sucursales":3,"fact":"Centro agropecuario del sur de Chile"},"rio-bueno":{"name":"Río Bueno","region":"Los Ríos","poblacion":"32K","bancos":"BancoEstado","sucursales":3,"fact":"Producción agrícola y lechera"},"frutillar":{"name":"Frutillar","region":"Los Lagos","poblacion":"18K","bancos":"BancoEstado","sucursales":2,"fact":"Semanas Musicales y arquitectura alemana"},"puerto-varas":{"name":"Puerto Varas","region":"Los Lagos","poblacion":"45K","bancos":"BancoEstado, Santander, Banco de Chile","sucursales":6,"fact":"Capital del turismo de Los Lagos"},"llanquihue":{"name":"Llanquihue","region":"Los Lagos","poblacion":"18K","bancos":"BancoEstado","sucursales":2,"fact":"Actividad agropecuaria y pesquera"}};


// City-to-region mapping for interlinking
const CITY_REGIONS: Record<string, string> = {
  'santiago': 'rm', 'las-condes': 'rm', 'providencia': 'rm', 'nunoa': 'rm', 'vitacura': 'rm',
  'lo-barnechea': 'rm', 'maipu': 'rm', 'la-florida': 'rm', 'penalolen': 'rm', 'recoleta': 'rm',
  'independencia': 'rm', 'san-miguel': 'rm', 'el-bosque': 'rm', 'quilicura': 'rm', 'cerro-navia': 'rm',
  'renca': 'rm', 'quinta-normal': 'rm', 'estacion-central': 'rm',
  'antofagasta': 'norte', 'iquique': 'norte', 'arica': 'norte', 'calama': 'norte', 'copiapo': 'norte', 'la-serena': 'norte',
  'valparaiso': 'centro', 'vina-del-mar': 'centro', 'rancagua': 'centro', 'san-antonio': 'centro',
  'talca': 'centro', 'linares': 'centro', 'san-fernando': 'centro', 'santa-cruz': 'centro', 'pichilemu': 'centro',
  'concepcion': 'sur', 'temuco': 'sur', 'chillan': 'sur', 'valdivia': 'sur', 'osorno': 'sur',
  'puerto-montt': 'sur', 'punta-arenas': 'sur', 'castro': 'sur', 'ancud': 'sur', 'quellon': 'sur',
  'la-union': 'sur', 'rio-bueno': 'sur', 'frutillar': 'sur', 'puerto-varas': 'sur', 'llanquihue': 'sur',
  'pucon': 'sur', 'villaricca': 'sur', 'los-angeles': 'sur',
};

function generateUniqueMeta(page: { slug: string; title: string; card?: string; city?: string }): { title: string; description: string } {
  const parts = page.slug.split('/');
  const lastPart = parts[parts.length - 1] || page.slug;
  const bank = detectBank(lastPart);
  const cardType = detectCardType(lastPart);

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
  const citySlug = detectCity(slug);
  const cityName = citySlug ? (cityNames[citySlug] || slugToTitle(citySlug)) : 'tu ciudad';
  const cardType = detectCardType(slug);

  if (bank) {
    return {
      paragraph1: `${bank.name} es ${bank.desc}. ${bank.fact}. Si tenés una tarjeta de crédito de ${bank.name} con cupo internacional disponible en ${cityName}, nosotros te lo compramos al instante. El proceso es 100% online y no requiere que vayas a ninguna sucursal.`,
      paragraph2: `${bank.name} cuenta con ${bank.offices}. Si estás en ${cityName}, podés coordinar la operación completamente por WhatsApp. Te mostramos la tasa antes de aceptar y la transferencia llega a tu cuenta en menos de 15 minutos.`,
      tip: `Dato de ${bank.name}: ${bank.fact}. Muchos clientes nos prefieren porque no necesitan ir al banzo ni hacer filas.`,
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
    paragraph1: 'En DolarExpress te ofrecemos la solución más rápida y segura para convertir tu cupo en dólares a pesos chilenos. Olvidate de los trámites bancarios tradicionales, las filas y los papeleos.',
    paragraph2: 'Trabajamos con todas las tarjetas de crédito chilenas: bancarias (Banco Chile, Santander, BCI, Scotiabank, Itaú, Security, BICE, BancoEstado) y retail (CMR Falabella, Ripley, Líder BCI, Cencosud, Paris, Jumbo, Easy, Hites, La Polar, ABC Din, Johnson).',
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

  // Generate interlinking URLs from same category
  const slugLower = slug?.toLowerCase() || '';
  const detectedCity = detectCity(slugLower);
  
  // Same-region cities for interlinking
  let sameRegionSlugs: string[] = [];
  if (detectedCity && CITY_REGIONS[detectedCity]) {
    const region = CITY_REGIONS[detectedCity];
    sameRegionSlugs = Object.entries(CITY_REGIONS)
      .filter(([c, r]) => r === region && c !== detectedCity)
      .map(([c]) => c);
  }

  const related = sameRegionSlugs.length > 0
    ? pseoPages.filter(p => {
        const c = detectCity(p.slug);
        return c && sameRegionSlugs.includes(c);
      }).slice(0, 6)
    : pseoPages
    .filter(p => {
      if (p.slug === slug) return false;
      if (slugLower.includes('banco') || slugLower.includes('bci') || slugLower.includes('santander') || slugLower.includes('scotiabank') || slugLower.includes('itau')) {
        return p.slug.includes('cupo-dolar-') && !p.slug.includes('/');
      }
      return false;
    })
    .slice(0, 6);

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
