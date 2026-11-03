p = r'dsh/src/content_part1.py'
s = open(p, encoding='utf-8').read()
s = s.replace('"map": "map-ch1.jpg",', '"map": None,', 1)
i = s.find('"id": "ch1"')
j = s.find('"map": None,', i)
s = s[:j] + '"map": "map-ch1.jpg",' + s[j + len('"map": None,'):]
open(p, 'w', encoding='utf-8').write(s)
print('ok')
