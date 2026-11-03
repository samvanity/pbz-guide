# -*- coding: utf-8 -*-
import os
base = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(base, 'content_part1.py')
s = open(p, encoding='utf-8').read()
s = s.replace('"map": None,', '"map": "map-ch1.jpg",', 1)
open(p, 'w', encoding='utf-8').write(s)

p = os.path.join(base, 'content_part2.py')
s = open(p, encoding='utf-8').read()
s = s.replace('收齊後到廟旁主屋盡頭驅散迷霧。這是<b>真結局前置</b>之一。',
              '收齊後到廟旁主屋盡頭驅散迷霧。這是<b>真結局前置</b>的起始；真正的湖心秘密要在梅谷湖湖心完成。')
s = s.replace('六朵螢火記憶之花全部拿到，湖心秘密完成',
              '六朵螢火記憶之花全部拿到（湖心秘密在梅谷湖收尾）')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
