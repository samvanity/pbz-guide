# -*- coding: utf-8 -*-
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
from opencc import OpenCC

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_part1 import CH0, CH1, CH2
from content_part2 import CH3, CH4, CH5
from content_part3 import CH6, CH7, CH8, CH9

CC = OpenCC('s2tw')
IMGDIR = os.path.join(BASE, 'site', 'assets', 'images')
PHOTOS = {'cangang', 'pengmeng', 'ahua', 'zhuming'}

CHAPTERS = [
    (CH0, '序', (150, 120, 80)), (CH1, '壹', (150, 70, 60)), (CH2, '貳', (120, 55, 50)),
    (CH3, '參', (120, 105, 80)), (CH4, '肆', (120, 60, 45)), (CH5, '伍', (120, 80, 55)),
    (CH6, '陸', (40, 75, 85)), (CH7, '柒', (55, 60, 55)), (CH8, '捌', (90, 55, 65)),
    (CH9, '終', (110, 45, 40)),
]

def font(size):
    for p in [r'C:\Windows\Fonts\msjh.ttc', r'C:\Windows\Fonts\msjhbd.ttc', r'C:\Windows\Fonts\simkai.ttf']:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def ink_bg(w, h, color):
    im = Image.new('RGB', (w, h), (10, 10, 12))
    d = ImageDraw.Draw(im)
    for k in range(22):
        pts = []
        for x in range(-40, w + 40, 16):
            y = h * (0.12 + 0.04 * k) + math.sin(x / (110 + k * 4) + k) * (12 + k)
            pts.append((x, y))
        d.line(pts, fill=(24 + k, 23 + k, 26 + k), width=1)
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for r in range(620, 0, -8):
        a = int(30 * (1 - r / 620) ** 2)
        od.ellipse([w * 0.82 - r, -r * 0.6, w * 0.82 + r, r * 0.85],
                   fill=(color[0], color[1], color[2], a))
    im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for y in range(h):
        a = int(190 * (y / h) ** 1.7)
        od.line([(0, y), (w, y)], fill=(8, 8, 10, a))
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')

W, H = 1200, 740
for ch, num, color in CHAPTERS:
    for b in ch['bosses']:
        key = os.path.splitext(b.get('img') or '')[0].replace('boss-', '')
        if key in PHOTOS:
            continue
        name = CC.convert(b['name'])
        title = CC.convert(b['title'])
        im = ink_bg(W, H, color)
        d = ImageDraw.Draw(im)
        d.text((W - 260, H - 520), num, font=font(300), fill=(27, 26, 29))
        d.line([(64, 120), (W - 64, 120)], fill=(175, 145, 95), width=1)
        d.text((66, 72), '頭目名刺', font=font(24), fill=(198, 178, 138))
        d.rectangle([W - 130, 58, W - 66, 122], outline=(150, 55, 46), width=2)
        d.text((W - 110, 70), num, font=font(38), fill=(200, 120, 105))
        fs = 118 if len(name) <= 4 else (92 if len(name) <= 6 else 74)
        d.text((62, H - 250), name, font=font(fs), fill=(238, 231, 216), stroke_width=1, stroke_fill=(18, 16, 14))
        d.text((68, H - 108), title, font=font(26), fill=(190, 180, 160))
        d.text((68, H - 62), '影之刃零・中文版攻略', font=font(20), fill=(130, 124, 112))
        im.save(os.path.join(IMGDIR, f'boss-{key}.jpg'), 'JPEG', quality=90, optimize=True)
        print('plate', key, name)
