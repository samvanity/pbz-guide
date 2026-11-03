import os
base = os.path.dirname(os.path.abspath(__file__))

p = os.path.join(base, 'content_part1.py')
s = open(p, encoding='utf-8').read()
s = s.replace('"hero": "hero-prologue.jpg"', '"hero": "chapter-ch0.jpg"', 1)
open(p, 'w', encoding='utf-8').write(s)

p = os.path.join(base, 'content_part2.py')
s = open(p, encoding='utf-8').read()
s = s.replace('"hero": "hero-camp.jpg"', '"hero": "chapter-ch5.jpg"')
open(p, 'w', encoding='utf-8').write(s)

p = os.path.join(base, 'content_part3.py')
s = open(p, encoding='utf-8').read()
s = s.replace('"hero": "hero-lake.jpg"', '"hero": "chapter-ch6.jpg"')
s = s.replace('"hero": "hero-prologue.jpg"', '"hero": "chapter-ch7.jpg"')
s = s.replace('"hero": "hero-lu.jpg"', '"hero": "chapter-ch8.jpg"')
s = s.replace('"hero": "hero-soul.jpg"', '"hero": "chapter-ch9.jpg"')
open(p, 'w', encoding='utf-8').write(s)
print('heroes fixed')
