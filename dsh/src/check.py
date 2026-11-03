import os, re, glob
site = r'dsh/site'
htmls = glob.glob(site + '/*.html')
missing = []
for f in htmls:
    s = open(f, encoding='utf-8').read()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
        u = m.group(1)
        if u.startswith(('http', '#', 'mailto', 'javascript')):
            continue
        p = os.path.normpath(os.path.join(os.path.dirname(f), u.split('#')[0]))
        if not os.path.exists(p):
            missing.append((os.path.basename(f), u))
print('pages', len(htmls), 'missing', len(missing))
for x in missing[:30]:
    print(x)
total = sum(os.path.getsize(p) for p in glob.glob(site + '/**/*', recursive=True) if os.path.isfile(p))
print('total MB', round(total / 1048576, 2))
