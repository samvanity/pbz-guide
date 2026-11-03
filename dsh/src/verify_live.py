import requests, re
base = 'https://samvanity.github.io/pbz-guide/pbz-dsh-guide/'
pages = ['index.html', 'bosses.html', 'missables.html', 'ending.html'] + [f'ch{i}.html' for i in range(10)]
bad = []
for p in pages:
    r = requests.get(base + p, timeout=30)
    print(p, r.status_code, len(r.content))
    for src in set(re.findall(r'src="([^"]+)"', r.text)):
        u = base + src if not src.startswith('http') else src
        h = requests.head(u, timeout=30)
        if h.status_code != 200:
            bad.append((p, src, h.status_code))
print('bad', len(bad))
print(bad[:5])
