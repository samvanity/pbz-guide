# -*- coding: utf-8 -*-
import os, math
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(BASE, 'site', 'assets', 'images')

PLATES = {
    'sanmian': ('三張臉的詭異魔偶', '聖母像裂縫・隱藏頭目', '壹', (150, 70, 60)),
    'jinmianju': ('金面具黑衣人', '龍柱挑戰', '壹', (150, 120, 80)),
    'muxiaokui': ('沐小葵', '組織少主', '參', (110, 80, 120)),
    'xieqiudong': ('謝秋冬', '神醫', '肆', (70, 110, 100)),
    'guhe': ('古鶴', '枯葉寺僧人', '陸', (90, 110, 90)),
    'yuzan': ('玉瓚', '三號樂偶師', '參', (130, 90, 110)),
    'yumian': ('玉面郎君', '獄方高手', '柒', (110, 90, 70)),
    'zuoshang-true': ('左殤', '真龍・真最終頭目', '終', (150, 60, 50)),
    'duanchang': ('斷腸', '鬼差高手', '陸', (90, 100, 110)),
    'huangxing': ('黃行', '崑崙叛徒', '柒', (100, 90, 70)),
    'moyuan': ('魔淵', '隱藏頭目', '終', (80, 80, 90)),
    'lizhe': ('力者與鋸者', '雙人組', '終', (120, 80, 60)),
    'biyuan': ('畢遠', '天玄派掌門殘軀', '參', (120, 110, 80)),
    'bifeng': ('橫刀畢峰', '精英劍客', '柒', (90, 95, 105)),
    'zuoshang': ('左殤', '序幕・練武場切磋', '序', (150, 120, 80)),
    'yucong': ('玉琮', '三十四號扭曲傀儡', '貳', (90, 100, 120)),
}

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
for key, (name, title, num, color) in PLATES.items():
    im = ink_bg(W, H, color)
    d = ImageDraw.Draw(im)
    # 巨大印章數字浮水印
    d.text((W - 260, H - 520), num, font=font(300), fill=(27, 26, 29))
    # 標頭
    d.line([(64, 120), (W - 64, 120)], fill=(175, 145, 95), width=1)
    d.text((66, 72), '頭目名刺', font=font(24), fill=(198, 178, 138))
    d.rectangle([W - 130, 58, W - 66, 122], outline=(150, 55, 46), width=2)
    d.text((W - 110, 70), num, font=font(38), fill=(200, 120, 105))
    # 名與稱號
    fs = 118 if len(name) <= 4 else 92
    d.text((62, H - 250), name, font=font(fs), fill=(238, 231, 216), stroke_width=1, stroke_fill=(18, 16, 14))
    d.text((68, H - 108), title, font=font(28), fill=(190, 180, 160))
    d.text((68, H - 62), '影之刃零・中文版攻略', font=font(20), fill=(130, 124, 112))
    im.save(os.path.join(IMGDIR, f'boss-{key}.jpg'), 'JPEG', quality=90, optimize=True)
    print('plate', key, name)
