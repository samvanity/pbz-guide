p = 'dsh/src/style.css'
s = open(p, encoding='utf-8-sig').read()
s = s.replace('\u00e2\u20ac\u201d', '\u2014')
s = s.replace('\u00e2\u20ac\u2039', '')
open(p, 'w', encoding='utf-8').write(s)
print('remaining a-circumflex:', s.count('\u00e2'))
