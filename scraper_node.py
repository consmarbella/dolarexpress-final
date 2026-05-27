"""
agents/scraper_node.py — Nodo A: Extracción de Datos Crudos
Con retry logic automático y rotación de headers.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import random
import time
from urllib.parse import urlparse, urljoin
from collections import Counter
from state import PSEOState

# ── POOL DE HEADERS (simula navegadores reales) ────────────────────────────────
HEADERS_POOL = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-CL,es;q=0.9,en-US;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Cache-Control": "max-age=0",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-419,es;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
]

NOISE_TAGS = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript', 'iframe', 'svg', 'form']
MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]  # segundos entre intentos


def scraper_node(state: PSEOState) -> PSEOState:
    """
    Nodo A: Descarga y extrae datos crudos de la URL objetivo.
    Reintenta automáticamente con headers diferentes si falla.
    """
    url = state["target_url"]
    attempt = state["scrape_attempts"]
    
    print(f"\n[Nodo A — Scraper] Intento {attempt + 1}/{MAX_RETRIES}: {url}")
    
    if attempt >= MAX_RETRIES:
        state["errors"].append(f"Scraper: máximo de reintentos alcanzado para {url}")
        state["scrape_success"] = False
        return state

    try:
        # Delay con jitter para no parecer bot
        if attempt > 0:
            delay = RETRY_DELAYS[attempt - 1] + random.uniform(0.5, 1.5)
            print(f"  Esperando {delay:.1f}s antes del reintento...")
            time.sleep(delay)
        else:
            time.sleep(random.uniform(1.0, 2.5))

        headers = random.choice(HEADERS_POOL)
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()

        print(f"  [OK] HTTP {response.status_code} | {len(response.content):,} bytes")

        soup = BeautifulSoup(response.content, 'html.parser')

        state["raw_html"] = response.text[:50000]  # Cap para no explotar memoria
        state["meta_tags"] = _extract_meta(soup)
        state["heading_structure"] = _extract_headings(soup)
        state["internal_links"] = _extract_links(soup, url)
        state["clean_text"] = _extract_clean_text(BeautifulSoup(response.content, 'html.parser'))
        state["keyword_analysis"] = _analyze_keywords(state["clean_text"])
        state["transactional_patterns"] = _detect_transactional(state["clean_text"])
        state["scrape_success"] = True
        state["scrape_attempts"] = attempt + 1
        state["current_node"] = "scraper_done"

        print(f"  [OK] Extraccion completa: {len(state['clean_text'])} chars de senal pura")

    except requests.exceptions.HTTPError as e:
        state["errors"].append(f"HTTP {e.response.status_code}: {url}")
        state["scrape_attempts"] = attempt + 1
        state["scrape_success"] = False
        print(f"  [FAIL] Error HTTP {e.response.status_code}")

    except Exception as e:
        state["errors"].append(f"Scraper error: {str(e)}")
        state["scrape_attempts"] = attempt + 1
        state["scrape_success"] = False
        print(f"  [FAIL] Error: {e}")

    return state


# ── FUNCIONES DE EXTRACCIÓN ────────────────────────────────────────────────────

def _extract_meta(soup) -> dict:
    meta = {"title": "", "description": "", "keywords": "", "og_title": "",
            "og_description": "", "canonical": "", "robots": "", "schema_types": []}
    
    title = soup.find('title')
    if title:
        meta["title"] = title.get_text(strip=True)
    
    for tag in soup.find_all('meta'):
        name = tag.get('name', '').lower()
        prop = tag.get('property', '').lower()
        content = tag.get('content', '')
        if name == 'description': meta["description"] = content
        elif name == 'keywords': meta["keywords"] = content
        elif name == 'robots': meta["robots"] = content
        elif prop == 'og:title': meta["og_title"] = content
        elif prop == 'og:description': meta["og_description"] = content
    
    canonical = soup.find('link', rel='canonical')
    if canonical:
        meta["canonical"] = canonical.get('href', '')
    
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            schema = json.loads(script.string or '{}')
            t = schema.get('@type', '')
            if t: meta["schema_types"].append(t)
        except: pass
    
    return meta


def _extract_headings(soup) -> dict:
    headings = {f"h{i}": [] for i in range(1, 7)}
    for level in range(1, 7):
        for tag in soup.find_all(f'h{level}'):
            text = tag.get_text(strip=True)
            if text and len(text) > 2:
                headings[f"h{level}"].append(text)
    return headings


def _extract_links(soup, base_url: str) -> list:
    domain = urlparse(base_url).netloc
    seen, links = set(), []
    for a in soup.find_all('a', href=True):
        full = urljoin(base_url, a['href'])
        text = a.get_text(strip=True)
        if urlparse(full).netloc == domain and text and full not in seen:
            seen.add(full)
            links.append({"url": full, "anchor": text[:100]})
    return links[:60]


def _extract_clean_text(soup) -> str:
    for tag in soup.find_all(NOISE_TAGS):
        tag.decompose()
    for cls in ['cookie', 'popup', 'modal', 'banner', 'ad']:
        for tag in soup.find_all(class_=re.compile(cls, re.I)):
            tag.decompose()
    lines = [l.strip() for l in soup.get_text(separator='\n').split('\n') if l.strip() and len(l.strip()) > 3]
    return '\n'.join(lines)


STOPWORDS_ES = {
    'de','la','el','en','y','a','los','del','se','las','un','por','con','una',
    'su','para','es','al','lo','como','más','o','pero','sus','le','ya','fue',
    'ha','que','no','te','me','si','todo','toda','todos','muy','bien','también',
    'hay','ser','estar','hacer','tener','poder','haber','este','esta','estos',
    'aquí','cuando','donde','cómo','qué','quién','cuál','entre','sobre','cada'
}

def _analyze_keywords(text: str) -> dict:
    words = [w for w in re.findall(r'\b[a-záéíóúñü]{3,}\b', text.lower()) if w not in STOPWORDS_ES]
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
    return {
        "unigrams": dict(Counter(words).most_common(30)),
        "bigrams": dict(Counter(bigrams).most_common(20)),
        "trigrams": dict(Counter(trigrams).most_common(15)),
        "total_words": len(words),
        "unique_words": len(set(words))
    }


def _detect_transactional(text: str) -> dict:
    t = text.lower()
    return {
        "cta_phrases": list(set(re.findall(r'\b(solicitar|cotizar|contratar|comprar|vender|cambiar|transferir|enviar|obtener|registrarse|depositar)\b', t))),
        "price_mentions": re.findall(r'\$[\d.,]+|[\d.,]+\s*(?:pesos|dólares|clp|usd)', t)[:10],
        "bank_mentions": list(set(re.findall(r'\b(banco\s+\w+|santander|bci|falabella|ripley|scotiabank|itaú|bbva|estado)\b', t))),
        "service_patterns": list(set(re.findall(r'\b(cupo\s+\w+|línea\s+\w+|tarjeta\s+\w+|crédito\s+\w+|remesa\s+\w+)\b', t)))[:15],
        "urgency_triggers": list(set(re.findall(r'\b(hoy|inmediato|rápido|ahora|express|urgente|instante|sin espera)\b', t))),
    }
