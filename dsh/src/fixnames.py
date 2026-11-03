import re, glob
for p in glob.glob(r'dsh/src/content_part*.py'):
    s = open(p, encoding='utf-8').read()
    s = s.replace('三面魔偶', '三張臉的詭異魔偶')
    s = re.sub(r'金面具(?!黑衣人)', '金面具黑衣人', s)
    open(p, 'w', encoding='utf-8').write(s)
print('names fixed')
