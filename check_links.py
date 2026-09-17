import re, os

public_dir = 'public'
results = {}
for f in sorted(os.listdir(public_dir)):
    if f.endswith('.html'):
        with open(os.path.join(public_dir, f), 'r') as fh:
            content = fh.read()
        links = re.findall(r'<a href="(/[^"]+)"', content)
        internal = [l for l in links if not l.startswith('http')]
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content)
        # Count words in body
        body_match = re.search(r'<body.*?>(.*?)</body>', content, re.DOTALL)
        if body_match:
            text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
            words = len(text.split())
        else:
            words = 0
        results[f] = {'words': words, 'h2s': len(h2s), 'links': len(internal), 'link_list': internal[:5]}

for f, data in results.items():
    print(f"{f}: {data['words']}w, {data['h2s']}h2, {data['links']}links -> {data['link_list']}")

# Find pages with no internal links
print("\n--- Pages with few internal links ---")
for f, data in results.items():
    if data['links'] < 3:
        print(f"{f}: only {data['links']} internal links")
