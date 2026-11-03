import glob, re
for p in glob.glob('dsh/src/content_part*.py'):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'"hero": "chapter-card-(ch[0-9])\.jpg"', r'"hero": "chapter-bg-\1.jpg"', s)
    open(p, 'w', encoding='utf-8').write(s)
print('ok')
