# -*- coding: utf-8 -*-
"""Anti-doorway patch 2026-10: inyecta contenido único (FAQ, particularidades, pasos, periexi)
en las páginas bancarias/retail de dolarexpress.cl y actualiza el JSON-LD FAQPage.
Uso: python patch.py [slug ...]     (sin args = todos)"""
import re, os, sys, json, io

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..', 'public'))
DATA = os.path.join(HERE, 'data')

RE_FAQ = re.compile(r'<dl class="faq">.*?</dl>', re.S)
RE_PART = re.compile(r'<h3[^>]*>Particularidades de [^<]*</h3>\s*<ul class="list">.*?</ul>', re.S)
RE_HOW = re.compile(r'<h3[^>]*>¿C&oacute;mo funciona con [^<]*\?|<h3[^>]*>¿Cómo funciona con [^<]*\?', re.I)
RE_LDX = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
RE_UPD = re.compile(r'Última actualización: [^<]*|&Uacute;ltima actualizaci&oacute;n: [^<]*')
RE_DID = re.compile(r'<div style="background:rgba\(212,175,55,0\.08\).*?</div>', re.S)

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def new_faq_dl(faqs):
    items = ''.join('<dt>%s</dt><dd>%s</dd>' % (esc(q), esc(a)) for q, a in faqs)
    return '<dl class="faq">%s</dl>' % items

def new_part_block(name, parts):
    lis = ''.join('<li><strong>%s:</strong> %s</li>' % (esc(t), esc(x)) for t, x in parts)
    return ('<h3 style="font-size:15px;margin-top:24px;margin-bottom:12px;">Particularidades de %s</h3>\n'
            '      <ul class="list">%s</ul>') % (esc(name), lis)

def new_how_block(name, steps):
    lis = ''.join('<li><strong>%d. %s</strong>&mdash; %s</li>' % (i + 1, esc(t), esc(x)) for i, (t, x) in enumerate(steps))
    return ('<h3 style="font-size:15px;margin-top:24px;margin-bottom:12px;">&iquest;C&oacute;mo funciona con %s?</h3>\n'
            '      <ul class="list">%s</ul>') % (esc(name), lis)

def new_did(text):
    return ('<div style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:14px;margin:20px 0;">\n'
            '        <p style="font-size:13px;color:var(--muted);margin:0;"><strong style="color:var(--accent);">&#128161; Sab&iacute;as que?</strong><br>%s</p>\n'
            '      </div>') % esc(text)

def patch_jsonld(html, faqs):
    m = RE_LDX.search(html)
    if not m:
        return None
    raw = m.group(1)
    try:
        data = json.loads(raw)
    except Exception as e:
        return None
    ents = data.get('@graph', [data])
    found = False
    for ent in ents:
        if isinstance(ent, dict) and ent.get('@type') == 'FAQPage':
            ent['mainEntity'] = [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ]
            found = True
    if not found:
        return None
    compact = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return html.replace(raw, compact, 1)

def process(slug, report):
    path = os.path.join(BASE, slug)
    with io.open(path, encoding='utf-8') as f:
        html = f.read()
    tree = json.load(io.open(os.path.join(DATA, slug + '.json'), encoding='utf-8'))
    name = tree['name']
    hits = []
    html, n = RE_FAQ.subn(new_faq_dl(tree['faqs']), html, count=1)
    hits.append('faq:' + str(n))
    html, n = RE_PART.subn(new_part_block(name, tree['particularidades']), html, count=1)
    hits.append('part:' + str(n))
    block_how = new_how_block(name, tree['steps'])
    mq = re.search(r'<h3[^>]*>(?:¿C&oacute;mo funciona con |¿Cómo funciona con )[^<]*\?</h3>\s*<ul class="list">.*?</ul>', html, re.S)
    if mq:
        html = html[:mq.start()] + block_how + html[mq.end():]
        hits.append('how:1')
    else:
        hits.append('how:MISS')
    html, n = RE_DID.subn(new_did(tree['did']), html, count=1)
    hits.append('did:' + str(n))
    j = patch_jsonld(html, tree['faqs'])
    if j:
        html = j
        hits.append('ld:1')
    else:
        hits.append('ld:MISS')
    html = RE_UPD.sub('Última actualización: Octubre 2026', html)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    report[slug] = hits

if __name__ == '__main__':
    slugs = sys.argv[1:] or sorted(os.listdir(DATA))
    report = {}
    for s in slugs:
        if s.endswith('.json'):
            s = s[:-5]
        try:
            process(s, report)
            print(s, '=>', report[s])
        except Exception as e:
            print('ERROR', s, repr(e))
