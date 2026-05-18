#!/usr/bin/env python3
"""
Generate missing static HTML pages for dolarexpress.cl
Reads slugs from /tmp/missing_slugs.txt and generates HTML files in /public/
"""

import os
import re
import json

# Paths
MISSING_SLUGS_FILE = '/tmp/missing_slugs.txt'
PUBLIC_DIR = '/home/user/dolarexpress-final/public'
PSEO_DATA_FILE = '/home/user/dolarexpress-final/src/data/pseo-data.ts'

# ─── CARD NAME MAP ─────────────────────────────────────────────────────────────
CARD_NAMES = {
    'cmr': 'CMR Falabella',
    'falabella': 'CMR Falabella',
    'ripley': 'Ripley',
    'lider': 'Líder BCI',
    'líder': 'Líder BCI',
    'paris': 'París Cencosud',
    'parís': 'París Cencosud',
    'hites': 'Hites',
    'la-polar': 'La Polar',
    'lapolar': 'La Polar',
    'abcdin': 'ABCDin',
    'abc': 'ABCDin',
    'cencosud': 'Cencosud',
    'jumbo': 'Jumbo Cencosud',
    'easy': 'Easy Cencosud',
    'johnson': 'Johnson',
    'family-shop': 'Family Shop',
    'corona': 'Corona',
    'banco-chile': 'Banco de Chile',
    'bancochile': 'Banco de Chile',
    'banco-estado': 'BancoEstado',
    'bancoestado': 'BancoEstado',
    'bci': 'BCI',
    'itau': 'Itaú',
    'santander': 'Santander',
    'security': 'Banco Security',
    'scotiabank': 'Scotiabank',
    'bice': 'BICE',
    'amex': 'American Express',
    'american-express': 'American Express',
}

# ─── ACTION MAP ────────────────────────────────────────────────────────────────
ACTION_KEYWORDS = {
    'avance': 'avance en efectivo',
    'cupo-compras': 'cupo de compras a efectivo',
    'pasar-cupo': 'pasar cupo a efectivo',
    'convertir-cupo': 'convertir cupo a efectivo',
    'prestamo': 'préstamo con tarjeta',
    'liquidar': 'liquidar cupo',
    'sacar-plata': 'sacar plata con tarjeta',
    'necesito-plata': 'obtener plata urgente',
    'plata-rapida': 'plata rápida',
    'efectivo': 'obtener efectivo',
    'transferir-cupo': 'transferir cupo a cuenta',
    'vender-cupo': 'vender cupo',
    'comprar-cupo': 'comprar cupo',
    'compro-cupo': 'compro cupo',
    'cambiar-cupo': 'cambiar cupo',
    'cambio-cupo': 'cambio cupo',
    'alternativa': 'alternativa',
}

# ─── PARSE PSEO DATA ───────────────────────────────────────────────────────────
def parse_pseo_data(filepath):
    """Parse pseo-data.ts and return {slug: {title, description}}"""
    data = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find all slug/title/description blocks
        blocks = re.findall(
            r"\{\s*slug:\s*'([^']+)'.*?title:\s*'([^']+)'.*?description:\s*'([^']+)'",
            content, re.DOTALL
        )
        for slug, title, description in blocks:
            data[slug.strip()] = {
                'title': title.strip(),
                'description': description.strip()
            }
        # Also handle double-quoted descriptions
        blocks2 = re.findall(
            r'\{\s*slug:\s*\'([^\']+)\'.*?title:\s*\'([^\']+)\'.*?description:\s*"([^"]+)"',
            content, re.DOTALL
        )
        for slug, title, description in blocks2:
            if slug.strip() not in data:
                data[slug.strip()] = {
                    'title': title.strip(),
                    'description': description.strip()
                }
    except Exception as e:
        print(f"Warning: Could not parse pseo-data.ts: {e}")
    return data


# ─── DETECT CARD FROM SLUG ─────────────────────────────────────────────────────
def detect_card(slug):
    """Return (card_key, card_name) or (None, None)"""
    parts = slug.split('-')
    # Try multi-word keys first
    for key, name in CARD_NAMES.items():
        if key in slug:
            return key, name
    return None, None


def detect_action(slug):
    """Return the action label"""
    for key, label in ACTION_KEYWORDS.items():
        if key in slug:
            return label
    return 'convertir cupo a efectivo'


def detect_city(slug):
    """Return city name if slug ends with -en-{city} or detectable city suffix"""
    m = re.search(r'-en-([a-z-]+)$', slug)
    if m:
        city_raw = m.group(1)
        return city_raw.replace('-', ' ').title()
    # Also cities at end without -en-
    city_suffixes = [
        'santiago', 'antofagasta', 'concepcion', 'valparaiso', 'vina-del-mar',
        'iquique', 'temuco', 'rancagua', 'la-serena', 'puerto-montt'
    ]
    for cs in city_suffixes:
        if slug.endswith('-' + cs):
            return cs.replace('-', ' ').title()
    return None


# ─── SLUG TO H1 ────────────────────────────────────────────────────────────────
def slug_to_h1(slug):
    """Convert slug to human-readable H1"""
    words = slug.replace('-', ' ').split()
    # Capitalize properly
    stop = {'y', 'de', 'del', 'la', 'el', 'en', 'a', 'con', 'sin', 'por', 'para', 'si', 'no'}
    result = []
    for i, w in enumerate(words):
        if i == 0 or w not in stop:
            result.append(w.capitalize())
        else:
            result.append(w)
    return ' '.join(result)


# ─── CONTENT GENERATOR ─────────────────────────────────────────────────────────
def generate_content(slug):
    """Generate lead_text, FAQs, related_slugs for a given slug"""
    card_key, card_name = detect_card(slug)
    action = detect_action(slug)
    city = detect_city(slug)
    h1 = slug_to_h1(slug)

    card_display = card_name if card_name else 'tu tarjeta'
    city_suffix = f" en {city}" if city else ""

    # ── LEAD TEXT ──
    if 'dolar' in slug or 'usd' in slug or 'usdc' in slug:
        lead = (
            f"DolarExpress convierte el cupo en dólares de tu tarjeta internacional en pesos chilenos directamente en tu cuenta bancaria{city_suffix}. "
            f"Operamos vía Transbank: autorizas una compra, procesamos la transacción y te transferimos los pesos al tipo de cambio acordado. "
            f"El proceso toma 15 minutos, sin trámites presenciales y sin importar si tienes DICOM. "
            f"Cotiza por WhatsApp ahora y recibe respuesta en menos de 2 minutos."
        )
    elif card_key in ('cmr', 'falabella'):
        lead = (
            f"DolarExpress opera como comercio afiliado a Transbank para convertir tu cupo de compras CMR Falabella en efectivo{city_suffix}. "
            f"Sin importar si tienes avance habilitado: usamos el cupo de compras, no el cupo de avance. "
            f"Autorizas una compra con tu tarjeta, procesamos vía Transbank y te transferimos el 85% a tu cuenta en 15 minutos. "
            f"El cargo aparece como compra en cuotas en tu estado Banco Falabella. Sin DICOM, sin papeleo."
        )
    elif card_key == 'ripley':
        lead = (
            f"Con DolarExpress puedes convertir el cupo de compras de tu Tarjeta Ripley en efectivo{city_suffix} en 15 minutos. "
            f"No necesitas tener avance en efectivo habilitado: trabajamos con el cupo de compras. "
            f"Transbank procesa la operación, tú recibes el 85% directo en tu cuenta bancaria. "
            f"El saldo queda en cuotas en tu Tarjeta Ripley. Sin DICOM, sin trámites."
        )
    elif card_key in ('lider', 'líder'):
        lead = (
            f"Convierte el cupo de tu Tarjeta Líder BCI en efectivo{city_suffix} con DolarExpress. "
            f"Operamos vía Transbank: la transacción queda registrada como compra en cuotas en tu tarjeta. "
            f"Recibes el 85% del monto en tu cuenta en 15 minutos. Sin avance necesario, sin DICOM. "
            f"Cotiza por WhatsApp para conocer el monto máximo disponible hoy."
        )
    elif card_key in ('paris', 'parís'):
        lead = (
            f"¿Tienes cupo disponible en tu Tarjeta París Cencosud y necesitas efectivo{city_suffix}? "
            f"DolarExpress convierte ese cupo en pesos en tu cuenta en 15 minutos. "
            f"Operamos con el cupo de compras vía Transbank, sin necesidad de avance habilitado. "
            f"El cargo se distribuye en cuotas en tu tarjeta. Sin DICOM, respuesta en 2 minutos por WhatsApp."
        )
    elif card_key == 'hites':
        lead = (
            f"Convierte el cupo de tu Tarjeta Hites en efectivo{city_suffix} con DolarExpress. "
            f"Sin avance habilitado: usamos el cupo de compras vía Transbank. "
            f"Recibes el 85% del monto en tu cuenta bancaria en 15 minutos. "
            f"Sin DICOM, sin trámites presenciales. Cotiza ahora por WhatsApp."
        )
    elif card_key in ('la-polar', 'lapolar'):
        lead = (
            f"Con DolarExpress conviertes el cupo de tu Tarjeta La Polar en efectivo{city_suffix} en minutos. "
            f"Operamos vía Transbank con el cupo de compras, sin necesitar avance en efectivo. "
            f"Transferencia directa a tu cuenta, el cargo en cuotas en tu tarjeta. "
            f"Sin DICOM, sin requisitos adicionales. Respuesta inmediata por WhatsApp."
        )
    elif card_key in ('abcdin', 'abc'):
        lead = (
            f"¿Necesitas efectivo y tienes cupo en tu Tarjeta ABCDin{city_suffix}? "
            f"DolarExpress convierte ese cupo en pesos vía Transbank en 15 minutos. "
            f"Sin avance habilitado necesario, sin DICOM. "
            f"Recibes el 85% en tu cuenta, el cargo en cuotas en tu tarjeta. Cotiza por WhatsApp."
        )
    elif card_key in ('banco-chile', 'bancochile'):
        lead = (
            f"DolarExpress convierte el cupo en dólares de tu tarjeta Banco de Chile en pesos chilenos{city_suffix}. "
            f"Operamos con tarjetas Visa, Mastercard y American Express del Banco de Chile. "
            f"Transferencia en 15 minutos al tipo de cambio acordado, sin DICOM. "
            f"Cotiza por WhatsApp para conocer la tasa del momento."
        )
    elif card_key in ('banco-estado', 'bancoestado'):
        lead = (
            f"Convierte el cupo en dólares de tu tarjeta BancoEstado en pesos chilenos{city_suffix} con DolarExpress. "
            f"Operamos con todas las tarjetas BancoEstado: Visa, Mastercard, American Express. "
            f"Proceso en 15 minutos, transferencia directa a tu cuenta. Sin DICOM. "
            f"Cotiza por WhatsApp para la tasa vigente."
        )
    elif card_key == 'bci':
        lead = (
            f"¿Tienes cupo en dólares en tu tarjeta BCI{city_suffix}? DolarExpress lo convierte en pesos chilenos en 15 minutos. "
            f"Operamos con Visa, Mastercard y Amex BCI. Tipo de cambio competitivo, transferencia inmediata. "
            f"Sin DICOM, sin trámites presenciales. Cotiza por WhatsApp ahora."
        )
    elif 'dicom' in slug:
        lead = (
            f"En DolarExpress trabajamos con personas en DICOM{city_suffix}. "
            f"Si tienes cupo disponible en tu tarjeta de crédito o tienda, podemos convertirlo en efectivo en 15 minutos, "
            f"sin importar tu historial crediticio. Solo necesitas tarjeta con cupo disponible. "
            f"Contáctanos por WhatsApp para verificar tu caso."
        )
    elif 'alternativa' in slug:
        lead = (
            f"¿Tu tarjeta no tiene avance habilitado? DolarExpress es la alternativa{city_suffix}: "
            f"convertimos el cupo de compras de tu tarjeta {card_display} en efectivo vía Transbank. "
            f"Sin necesitar avance, sin DICOM, en 15 minutos. "
            f"El proceso es 100% online, coordinas por WhatsApp."
        )
    elif 'transferir-cupo' in slug:
        lead = (
            f"Transfiere el cupo de tu tarjeta {card_display} directamente a tu cuenta bancaria{city_suffix} con DolarExpress. "
            f"Operamos vía Transbank: autorizas una compra, recibimos el pago y te transferimos el 85% del monto. "
            f"Proceso en 15 minutos, sin avance necesario, sin DICOM. "
            f"Cotiza el monto y condiciones ahora por WhatsApp."
        )
    else:
        lead = (
            f"DolarExpress ofrece el servicio de {action} con {card_display}{city_suffix}. "
            f"Operamos como comercio afiliado a Transbank: autorizas una compra con tu tarjeta, procesamos la transacción "
            f"y te transferimos el efectivo en 15 minutos a tu cuenta bancaria. "
            f"Sin avance habilitado necesario, sin DICOM, respuesta en 2 minutos por WhatsApp."
        )

    # ── FAQs ──
    if 'dolar' in slug or 'usd' in slug or 'usdc' in slug:
        faqs = [
            {
                'q': f'¿Cómo funciona la conversión de cupo en dólares con {card_display}?',
                'a': f'Coordinas el monto por WhatsApp, autorizas una compra con tu tarjeta {card_display} en nuestra terminal Transbank, y te transferimos los pesos al tipo de cambio acordado. El proceso toma 15 minutos.'
            },
            {
                'q': '¿Cuál es el tipo de cambio que aplican?',
                'a': 'Usamos el tipo de cambio del mercado al momento de la operación, con una pequeña comisión. Cotiza por WhatsApp para conocer la tasa exacta del día.'
            },
            {
                'q': '¿Puedo operar si tengo DICOM?',
                'a': 'Sí. No revisamos historial crediticio. Solo necesitas que tu tarjeta tenga cupo disponible en dólares. Contáctanos por WhatsApp para verificar.'
            }
        ]
    elif card_key in ('cmr', 'falabella'):
        faqs = [
            {
                'q': '¿Necesito tener el avance habilitado en CMR para usar este servicio?',
                'a': 'No. DolarExpress trabaja con el cupo de compras de tu tarjeta CMR, no con el cupo de avance. Aunque tengas el avance bloqueado, puedes convertir tu cupo de compras en efectivo.'
            },
            {
                'q': '¿Cuánto recibo y cuánto pago en cuotas en CMR?',
                'a': 'Recibes el 85% del monto en tu cuenta (comisión 15%). El total queda como una compra en tu tarjeta CMR Falabella que puedes pagar en cuotas. La tasa de interés la determina Banco Falabella.'
            },
            {
                'q': '¿Cuánto demora la transferencia?',
                'a': 'Una vez autorizada la transacción en Transbank, la transferencia a tu cuenta llega en menos de 15 minutos. Todo el proceso —desde el contacto inicial hasta que recibes el dinero— toma menos de 30 minutos.'
            }
        ]
    elif card_key == 'ripley':
        faqs = [
            {
                'q': '¿Puedo usar este servicio si no tengo avance habilitado en Ripley?',
                'a': 'Sí. Trabajamos con el cupo de compras de tu Tarjeta Ripley, no con el cupo de avance. No importa si el avance está bloqueado.'
            },
            {
                'q': '¿Cuánto cuesta convertir el cupo Ripley en efectivo?',
                'a': 'Cobramos una comisión del 15% sobre el monto. Por ejemplo, si conviertes $200.000, recibes $170.000 en tu cuenta. El cargo queda en cuotas en tu Tarjeta Ripley.'
            },
            {
                'q': '¿El servicio está disponible para todas las Tarjetas Ripley?',
                'a': 'Sí, operamos con todas las variantes de Tarjeta Ripley (Ripley Mastercard, Ripley clásica). Solo necesitas cupo de compras disponible.'
            }
        ]
    elif card_key in ('lider', 'líder'):
        faqs = [
            {
                'q': '¿Cómo convierto el cupo de mi Tarjeta Líder en efectivo?',
                'a': 'Cotizas el monto por WhatsApp, autorizas una compra con tu Tarjeta Líder BCI en nuestra terminal Transbank, y recibes el 85% del monto en tu cuenta en 15 minutos.'
            },
            {
                'q': '¿Necesito avance habilitado en la Tarjeta Líder?',
                'a': 'No. Usamos el cupo de compras de la Tarjeta Líder, que es independiente del avance en efectivo. Aunque no tengas avance, puedes operar.'
            },
            {
                'q': '¿Cuánto me cobran?',
                'a': 'La comisión es del 15%. Recibes el 85% del monto solicitado directo en tu cuenta bancaria. El resto queda como compra en cuotas en tu Tarjeta Líder BCI.'
            }
        ]
    elif card_key in ('paris', 'parís'):
        faqs = [
            {
                'q': '¿Cómo saco efectivo con mi Tarjeta París?',
                'a': 'Contactas a DolarExpress por WhatsApp, autorizas una compra en nuestra terminal Transbank con tu Tarjeta París, y recibimos el cupo y te transferimos el 85% a tu cuenta en minutos.'
            },
            {
                'q': '¿La Tarjeta París necesita avance habilitado?',
                'a': 'No. Operamos con el cupo de compras Cencosud, sin necesitar avance en efectivo. El cargo queda como compra en cuotas en tu estado de cuenta París.'
            },
            {
                'q': '¿Cuánto tiempo demora la operación con Tarjeta París?',
                'a': 'El proceso completo toma entre 15 y 30 minutos desde el primer mensaje de WhatsApp hasta que el dinero llega a tu cuenta.'
            }
        ]
    elif 'dicom' in slug:
        faqs = [
            {
                'q': '¿Pueden ayudarme aunque esté en DICOM?',
                'a': 'Sí. No consultamos historial en DICOM ni en ningún buró de crédito. Solo verificamos que tu tarjeta tenga cupo de compras disponible. Si tiene cupo, operamos.'
            },
            {
                'q': '¿Qué tarjetas aceptan para personas con DICOM?',
                'a': 'Cualquier tarjeta de tienda (CMR, Ripley, París, Líder, Hites, La Polar, ABCDin) o tarjeta bancaria con cupo disponible. La aprobación depende del cupo, no del historial.'
            },
            {
                'q': '¿Es seguro operar teniendo DICOM?',
                'a': 'Sí. Operamos vía Transbank, que es la red oficial de pagos en Chile. La transacción aparece como una compra normal en tu tarjeta, sin reportes adicionales al sistema financiero.'
            }
        ]
    elif 'transferir-cupo' in slug:
        faqs = [
            {
                'q': f'¿Cómo transfiero el cupo de mi tarjeta {card_display} a mi cuenta?',
                'a': f'Coordinas el monto por WhatsApp, autorizas una compra con tu tarjeta {card_display} en DolarExpress vía Transbank, y transferimos el 85% a tu cuenta bancaria en 15 minutos.'
            },
            {
                'q': '¿Cuánto de mi cupo puedo transferir?',
                'a': f'Puedes transferir desde $50.000 hasta el cupo de compras disponible en tu tarjeta. El máximo depende del cupo que tenga tu tarjeta {card_display} en ese momento.'
            },
            {
                'q': '¿Cuál es la comisión por transferir el cupo?',
                'a': 'Cobramos el 15% del monto total. Por ejemplo, si transfieres $300.000 de cupo, recibes $255.000 en tu cuenta. Sin costos ocultos.'
            }
        ]
    else:
        faqs = [
            {
                'q': f'¿Cómo funciona el servicio de {action} con {card_display}?',
                'a': f'Cotizas por WhatsApp el monto que necesitas, autorizas la compra con tu tarjeta {card_display} en nuestra terminal Transbank, y recibes el 85% del monto en tu cuenta bancaria en 15 minutos. El 15% restante es nuestra comisión.'
            },
            {
                'q': '¿Necesito tener avance habilitado en mi tarjeta?',
                'a': f'No. DolarExpress trabaja con el cupo de compras de tu tarjeta {card_display}, que es independiente del avance en efectivo. No importa si el avance está bloqueado.'
            },
            {
                'q': '¿Puedo operar si estoy en DICOM?',
                'a': 'Sí. No consultamos historial crediticio. Solo necesitas cupo de compras disponible en tu tarjeta. Contáctanos por WhatsApp para verificar.'
            }
        ]

    # ── RELATED SLUGS ──
    related = get_related_slugs(slug, card_key)

    return {
        'h1': h1,
        'lead': lead,
        'faqs': faqs,
        'related': related,
    }


def get_related_slugs(slug, card_key):
    """Return 5 related slugs for interlinking"""
    # Card-specific clusters
    card_clusters = {
        'cmr': [
            'avance-efectivo-tarjeta-cmr',
            'cupo-compras-a-efectivo-cmr',
            'cmr-efectivo-rapido',
            'convertir-cupo-cmr-pesos-hoy',
            'avance-cmr-sin-avance-habilitado',
        ],
        'falabella': [
            'avance-efectivo-tarjeta-cmr',
            'cupo-compras-a-efectivo-cmr',
            'cmr-efectivo-rapido',
            'convertir-cupo-cmr-pesos-hoy',
            'avance-cmr-sin-avance-habilitado',
        ],
        'ripley': [
            'avance-efectivo-tarjeta-ripley',
            'cupo-compras-a-efectivo-ripley',
            'avance-ripley-cuotas',
            'avance-ripley-sin-tener-avance',
            'convertir-cupo-ripley-efectivo-rapido',
        ],
        'lider': [
            'avance-efectivo-tarjeta-lider',
            'cupo-compras-a-efectivo-lider',
            'avance-lider-bci-online',
            'cuanto-me-dan-de-avance-tarjeta-lider',
            'avance-cupo-dolares',
        ],
        'paris': [
            'avance-efectivo-tarjeta-paris',
            'cupo-compras-efectivo-paris',
            'cuanto-presta-tarjeta-paris',
            'cupo-compras-a-efectivo-ripley',
            'cupo-compras-a-efectivo-cmr',
        ],
        'hites': [
            'avance-efectivo-tarjeta-hites',
            'cupo-compras-efectivo-hites',
            'vender-cupo-hites',
            'transferir-cupo-hites-a-cuenta',
            'avance-efectivo-tarjetas-grandes-tiendas-chile',
        ],
        'la-polar': [
            'avance-efectivo-tarjeta-la-polar',
            'cupo-compras-efectivo-la-polar',
            'alternativa-avance-la-polar',
            'transferir-cupo-la-polar-a-cuenta',
            'avance-la-polar-cuotas',
        ],
        'lapolar': [
            'avance-efectivo-tarjeta-la-polar',
            'cupo-compras-efectivo-la-polar',
            'alternativa-avance-la-polar',
            'transferir-cupo-la-polar-a-cuenta',
            'avance-la-polar-cuotas',
        ],
        'abcdin': [
            'avance-efectivo-tarjeta-abc',
            'cupo-compras-efectivo-abcdin',
            'vender-cupo-abcdin',
            'transferir-cupo-abcdin-a-cuenta',
            'avance-abc-visa',
        ],
        'abc': [
            'avance-efectivo-tarjeta-abc',
            'cupo-compras-efectivo-abcdin',
            'vender-cupo-abcdin',
            'transferir-cupo-abcdin-a-cuenta',
            'avance-abc-visa',
        ],
        'johnson': [
            'avance-tarjeta-johnson',
            'vender-cupo-johnson',
            'avance-efectivo-tarjetas-grandes-tiendas-chile',
            'cupo-compras-efectivo-hites',
            'avance-efectivo-tarjeta-abc',
        ],
        'banco-chile': [
            'cupo-dolar-banco-chile',
            'cupo-dolar-bancochile-pesos',
            'vender-cupo-dolar-banco-chile',
            'cupo-dolar-banco-chile-amex',
            'como-vender-cupo-dolar',
        ],
        'bancochile': [
            'cupo-dolar-banco-chile',
            'cupo-dolar-bancochile-pesos',
            'vender-cupo-dolar-banco-chile',
            'cupo-dolar-banco-chile-amex',
            'como-vender-cupo-dolar',
        ],
        'banco-estado': [
            'cupo-dolar-banco-estado',
            'cupo-dolar-bancoestado',
            'vender-cupo-dolar-banco-estado',
            'cupo-dolar-bancoestado-amex',
            'como-vender-cupo-dolar',
        ],
        'bancoestado': [
            'cupo-dolar-banco-estado',
            'cupo-dolar-bancoestado',
            'vender-cupo-dolar-banco-estado',
            'cupo-dolar-bancoestado-amex',
            'como-vender-cupo-dolar',
        ],
        'bci': [
            'cupo-dolar-bci',
            'avance-lider-bci-online',
            'vender-cupo-dolar-bci',
            'como-vender-cupo-dolar',
            'cupo-dolar-a-pesos',
        ],
    }

    # Generic fallback
    generic = [
        'avance-efectivo',
        'avance-efectivo-tarjeta-cmr',
        'avance-efectivo-tarjeta-ripley',
        'como-sacar-plata-si-no-tengo-avance',
        'como-obtener-liquidez-con-tarjeta-retail',
    ]

    if card_key and card_key in card_clusters:
        candidates = card_clusters[card_key]
    elif 'dolar' in slug or 'usd' in slug:
        candidates = [
            'como-vender-cupo-dolar',
            'cupo-dolar-a-pesos',
            'cupo-dolar-15-minutos',
            'vender-cupo-dolar-santiago',
            'cupo-dolar-banco-chile',
        ]
    elif 'dicom' in slug:
        candidates = [
            'tengo-dicom-y-necesito-efectivo',
            'tengo-dicom-y-tengo-cupo-disponible',
            'como-sacar-plata-si-no-tengo-avance',
            'avance-efectivo',
            'avance-efectivo-tarjeta-cmr',
        ]
    else:
        candidates = generic

    # Remove self
    candidates = [c for c in candidates if c != slug]
    # Fill to 5 with generics
    for g in generic:
        if g not in candidates and g != slug and len(candidates) < 5:
            candidates.append(g)
    return candidates[:5]


# ─── FAQ HTML BUILDER ──────────────────────────────────────────────────────────
def build_faq_html(faqs):
    parts = []
    for faq in faqs:
        parts.append(f'''        <details class="border border-gray-200 rounded-xl overflow-hidden group">
          <summary class="flex justify-between items-center px-5 py-4 cursor-pointer font-semibold text-[15px] hover:bg-gray-50 transition-colors list-none">
            {faq["q"]}
            <svg class="w-4 h-4 text-gray-400 transition-transform group-open:rotate-180 shrink-0 ml-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </summary>
          <div class="px-5 py-4 text-sm text-gray-600 leading-relaxed border-t border-gray-100">
            {faq["a"]}
          </div>
        </details>''')
    return '\n'.join(parts)


def build_faq_schema(faqs):
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }, ensure_ascii=False)


def build_breadcrumb_schema(slug, h1):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://dolarexpress.cl/"},
            {"@type": "ListItem", "position": 2, "name": h1, "item": f"https://dolarexpress.cl/{slug}"}
        ]
    }, ensure_ascii=False)


def build_related_links(related_slugs):
    parts = []
    for s in related_slugs:
        label = slug_to_h1(s)
        parts.append(
            f'        <li><a href="https://dolarexpress.cl/{s}" class="text-[#C8A045] hover:underline leading-snug block">{label}</a></li>'
        )
    return '\n'.join(parts)


def build_interlink_nav(related_slugs):
    parts = []
    for s in related_slugs:
        label = slug_to_h1(s)
        parts.append(f'    <a href="https://dolarexpress.cl/{s}" style="display:inline-block;margin:4px 8px 4px 0;">{label}</a>')
    return '\n'.join(parts)


# ─── HTML TEMPLATE ─────────────────────────────────────────────────────────────
def render_html(slug, title, description, content):
    h1 = content['h1']
    lead = content['lead']
    faqs = content['faqs']
    related = content['related']

    wa_text = slug.replace('-', ' ')
    wa_link = f"https://wa.me/56967658939?text=Hola,%20vengo%20de%20la%20web%20por%20{slug}"

    faq_html = build_faq_html(faqs)
    faq_schema = build_faq_schema(faqs)
    breadcrumb_schema = build_breadcrumb_schema(slug, h1)
    related_links = build_related_links(related)
    interlink_nav = build_interlink_nav(related)

    return f"""<!DOCTYPE html>
<html lang="es-CL">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <link rel="canonical" href="https://dolarexpress.cl/{slug}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="https://dolarexpress.cl/{slug}" />
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="es_CL" />
    <meta property="og:image" content="https://dolarexpress.cl/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary" />
    <meta name="robots" content="index, follow" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script defer src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={{theme:{{extend:{{fontFamily:{{sans:['Inter','-apple-system','sans-serif']}}}}}}}}</script>
    <script type="application/ld+json">{faq_schema}</script>
    <script type="application/ld+json">{breadcrumb_schema}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FinancialService","name":"DolarExpress","url":"https://dolarexpress.cl","telephone":"+56967658939","address":{{"@type":"PostalAddress","addressCountry":"CL"}},"openingHours":"Mo-Sa 09:00-21:00","description":"Servicio de conversión de cupo de tarjetas a efectivo vía Transbank."}}</script>
</head>
<body class="bg-white text-[#1a1a1a] font-sans antialiased">
<nav class="seo-home-link" style="padding:8px 12px;font-family:Arial,sans-serif"><a href="/">Inicio</a> · <a href="/directorio-general">Directorio</a></nav>

<header class="bg-[#1a1a1a] text-white sticky top-0 z-50 shadow-lg">
  <nav class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center" aria-label="Navegación principal">
    <a href="https://dolarexpress.cl/" class="font-black text-2xl tracking-tight text-white hover:text-[#C8A045] transition-colors">DolarExpress<span class="text-[#C8A045]">.cl</span></a>
    <a href="{wa_link}" target="_blank" rel="noopener noreferrer" class="bg-[#C8A045] hover:bg-[#a88434] text-white font-bold py-2.5 px-6 rounded-full text-sm shadow-md transition-all hover:shadow-lg">Cotizar</a>
  </nav>
</header>

<div class="max-w-6xl mx-auto px-4 py-3">
  <nav aria-label="Breadcrumb" class="text-sm text-gray-400">
    <a href="https://dolarexpress.cl/" class="hover:text-[#C8A045]">Inicio</a>
    <span class="mx-2">›</span>
    <span class="text-gray-600">{h1}</span>
  </nav>
</div>

<main class="max-w-6xl mx-auto px-4 py-8 flex flex-col md:flex-row gap-0">
  <article class="md:w-2/3">

    <header class="mb-10">
      <h1 class="text-3xl md:text-[2.5rem] font-extrabold leading-[1.15] tracking-tight mb-6">{h1}</h1>
      <p class="text-[15px] md:text-base text-gray-600 leading-relaxed max-w-prose">{lead}</p>
    </header>

    <div class="mb-10 flex flex-col sm:flex-row gap-4 items-start">
      <a href="{wa_link}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-3 bg-[#C8A045] hover:bg-[#a88434] text-white font-bold py-4 px-8 rounded-full text-lg shadow-xl hover:shadow-2xl transition-all transform hover:-translate-y-0.5">
        <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Cotizar por WhatsApp
      </a>
      <span class="text-xs text-gray-400 mt-3">Comisión: 15% · Respuesta: &lt;2 min</span>
    </div>

    <section class="mb-10">
      <h2 class="text-xl font-bold mb-6 text-[#1a1a1a]">Preguntas frecuentes</h2>
      <div class="space-y-3">
{faq_html}
      </div>
    </section>

    <div class="bg-[#1a1a1a] rounded-2xl p-8 text-center mb-10">
      <p class="text-white text-lg font-bold mb-2">¿Quieres cotizar tu operación?</p>
      <p class="text-gray-400 text-sm mb-5">Envíanos el monto y te respondemos en menos de 2 minutos.</p>
      <a href="{wa_link}" target="_blank" rel="noopener noreferrer" class="inline-block bg-[#C8A045] hover:bg-[#a88434] text-white font-bold py-3 px-8 rounded-full shadow-lg transition-all text-sm">Cotizar Ahora</a>
    </div>

  </article>

  <aside class="md:w-1/3 mt-12 md:mt-0 md:ml-10 space-y-8">
    <div class="bg-white rounded-2xl p-6 shadow-md border border-gray-100 sticky top-20">
      <h3 class="font-bold text-lg mb-4 text-[#1a1a1a] border-b border-gray-100 pb-3">Servicios relacionados</h3>
      <ul class="space-y-3 text-sm">
{related_links}
      </ul>
    </div>
  </aside>
</main>

<footer class="bg-[#1a1a1a] text-gray-400 py-10 mt-8">
  <div class="max-w-6xl mx-auto px-4 text-center text-xs space-y-2">
    <p class="font-semibold text-white text-sm">DolarExpress.cl</p>
    <p>&copy; 2026 DolarExpress. Chile. Este servicio no constituye una oferta de crédito. Las condiciones de pago en cuotas son determinadas por cada emisora de la tarjeta.</p>
    <div class="flex justify-center gap-4 mt-2">
      <a href="/privacidad" class="hover:text-white transition-colors">Privacidad</a>
      <a href="/terminos" class="hover:text-white transition-colors">Términos</a>
      <a href="/contacto" class="hover:text-white transition-colors">Contacto</a>
    </div>
  </div>
</footer>

<!-- Interlinking SEO -->
<div id="interlinking-seo" style="margin:2rem 0;padding:1rem;border-top:1px solid #eee;">
  <p><strong>Artículos relacionados:</strong></p>
  <nav>
{interlink_nav}
  </nav>
</div>
</body>
</html>"""


# ─── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    # Load existing HTMLs
    existing = set()
    for fname in os.listdir(PUBLIC_DIR):
        if fname.endswith('.html'):
            existing.add(fname[:-5])  # strip .html

    print(f"Existing HTML files: {len(existing)}")

    # Load missing slugs
    with open(MISSING_SLUGS_FILE, 'r', encoding='utf-8') as f:
        missing_slugs = [line.strip() for line in f if line.strip()]

    print(f"Missing slugs listed: {len(missing_slugs)}")

    # Filter out slugs with "/" and already-existing ones
    to_generate = []
    for slug in missing_slugs:
        if '/' in slug:
            print(f"  SKIP (contains /): {slug}")
            continue
        if slug in existing:
            print(f"  SKIP (already exists): {slug}")
            continue
        to_generate.append(slug)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for s in to_generate:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    to_generate = deduped

    print(f"To generate: {len(to_generate)}")

    # Load pseo data
    pseo_data = parse_pseo_data(PSEO_DATA_FILE)
    print(f"Loaded pseo data entries: {len(pseo_data)}")

    created = 0
    skipped = 0

    for slug in to_generate:
        # Get title/description from pseo data or generate fallback
        if slug in pseo_data:
            title = pseo_data[slug]['title']
            description = pseo_data[slug]['description']
        else:
            h1_fallback = slug_to_h1(slug)
            title = f"{h1_fallback} | DolarExpress"
            description = f"{h1_fallback}: convierte tu cupo en efectivo en 15 minutos vía Transbank. Sin avance necesario, sin DICOM. DolarExpress.cl"

        # Generate content
        content = generate_content(slug)

        # Render HTML
        html = render_html(slug, title, description, content)

        # Write file
        out_path = os.path.join(PUBLIC_DIR, f"{slug}.html")
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            created += 1
            if created % 50 == 0:
                print(f"  Progress: {created} files created...")
        except Exception as e:
            print(f"  ERROR writing {slug}: {e}")
            skipped += 1

    print(f"\n=== DONE ===")
    print(f"Files created: {created}")
    print(f"Files skipped (errors): {skipped}")
    total_after = len([f for f in os.listdir(PUBLIC_DIR) if f.endswith('.html')])
    print(f"Total HTML files in /public/ now: {total_after}")


if __name__ == '__main__':
    main()
