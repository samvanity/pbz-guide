# -*- coding: utf-8 -*-
import re, io, os
base = os.path.dirname(os.path.abspath(__file__))

p = os.path.join(base, 'build.py')
s = open(p, encoding='utf-8').read()
repl = {
    'PHANTOM BLADE ZERO · 錯過不再的攻略': '影之刃零 · 中文版錯過攻略',
    'PHANTOM BLADE ZERO · 中文版攻略': '中文版 · 錯過不再的攻略',
    '<small>CHAPTERS</small>': '<small>章節</small>',
    '<small>HOW TO USE</small>': '<small>使用方式</small>',
    '<small>BEFORE YOU GO</small>': '<small>出發前</small>',
    '<small>ROUTE</small>': '<small>路線</small>',
    '<small>TIMELINE</small>': '<small>時間軸</small>',
    '<small>BOSSES</small>': '<small>頭目</small>',
    '<small>CHECKLIST</small>': '<small>檢查</small>',
    'BOSS COMPENDIUM': '頭目圖鑑',
    'MISSABLE CHECKLIST': '錯過清單',
    'TRUE ENDING · 內含劇透': '真結局 · 內含劇透',
    '<small>PURPLE TASKS</small>': '<small>紫色任務</small>',
    '<small>DRAGON PILLARS</small>': '<small>龍柱</small>',
    '<small>FINAL CHOICE</small>': '<small>最終分歧</small>',
    'DEADLINE': '期限',
    "CH. {e(ch['num'])}": "章節 {e(ch['num'])}",
    'cc-tag">CHECKLIST': 'cc-tag">錯過清單',
    'cc-tag">TRUE ENDING': 'cc-tag">真結局',
    'cc-tag">BOSSES': 'cc-tag">頭目',
    '· ROUTE': '· 路線',
    '攻略整理：DeepSeek Harness · 2026': '攻略整理：2026',
}
for a, b in repl.items():
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)

# map keys
for fn in ('content_part1.py', 'content_part2.py', 'content_part3.py'):
    q = os.path.join(base, fn)
    t = open(q, encoding='utf-8').read()
    if fn in ('content_part1.py', 'content_part2.py'):
        t = re.sub(r'"map": "map-ch[0-9]\.jpg"', '"map": None', t)
    if fn == 'content_part3.py':
        t = t.replace('"map": None,', '"map": "map-ch6.jpg",', 1)
    open(q, 'w', encoding='utf-8').write(t)
print('localized')
