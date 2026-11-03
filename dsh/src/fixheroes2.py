import os
base = os.path.dirname(os.path.abspath(__file__))
for fn, ids in [('content_part1.py', ['ch0']), ('content_part2.py', ['ch5']),
                ('content_part3.py', ['ch6', 'ch7', 'ch8', 'ch9'])]:
    p = os.path.join(base, fn)
    s = open(p, encoding='utf-8').read()
    for cid in ids:
        s = s.replace(f'"hero": "chapter-{cid}.jpg"', f'"hero": "chapter-card-{cid}.jpg"')
    open(p, 'w', encoding='utf-8').write(s)
print('ok')
