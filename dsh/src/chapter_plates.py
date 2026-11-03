# -*- coding: utf-8 -*-
import os, math
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(BASE, 'site', 'assets', 'images')

CHAPTERS = [
    ('ch0', '序章', '物是人非', '序', '先學會站著，再學會殺人。', (150, 120, 80)),
    ('ch5', '正道大營', '崑崙支柱', '伍', '記憶之花藏在箭塔、墳場與一句不能殺的人身上。', (120, 60, 45)),
    ('ch6', '梅谷湖', '殺氣驅動船', '陸', '湖面很大，但真正要緊的只有一條船與一把琵琶。', (40, 75, 85)),
    ('ch7', '枷籠山', '哭泣之源', '柒', '霧散之後，山裡只剩兩種人：獄卒與囚徒。', (55, 60, 55)),
    ('ch8', '戲夢山莊', '前進之路', '捌', '走進這道門之前，先把整個江湖的事了結。', (90, 55, 65)),
    ('ch9', '斷魂山', '魂的價值', '終', '走到這裡，已經沒有回頭路；但結局還有兩種。', (110, 45, 40)),
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
    for k in range(26):
        pts = []
        for x in range(-40, w + 40, 18):
            y = h * (0.18 + 0.03 * k) + math.sin(x / (120 + k * 3) + k) * (16 + k * 1.2)
            pts.append((x, y))
        d.line(pts, fill=(26 + k, 24 + k, 27 + k), width=1)
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for r in range(700, 0, -8):
        a = int(26 * (1 - r / 700) ** 2)
        od.ellipse([w * 0.78 - r, -r * 0.5, w * 0.78 + r, r * 0.9],
                   fill=(color[0], color[1], color[2], a))
    im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for y in range(h):
        a = int(180 * (y / h) ** 1.7)
        od.line([(0, y), (w, y)], fill=(8, 8, 10, a))
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')

W, H = 1920, 1080
for cid, name, sub, num, tagline, color in CHAPTERS:
    # 章節頁主視覺：有名稱
    im = ink_bg(W, H, color)
    d = ImageDraw.Draw(im)
    d.text((W - 520, H - 620), num, font=font(560), fill=(30, 29, 32))
    d.line([(110, 300), (430, 300)], fill=(170, 145, 95), width=2)
    d.text((110, 250), '章節', font=font(30), fill=(190, 170, 130))
    fs = 150 if len(name) <= 4 else 120
    d.text((104, H - 620), name, font=font(fs), fill=(238, 231, 216), stroke_width=2, stroke_fill=(18, 16, 14))
    d.text((110, H - 430), sub, font=font(48), fill=(200, 190, 170))
    d.text((110, H - 330), tagline, font=font(30), fill=(150, 143, 130))
    d.rectangle([W - 220, 90, W - 110, 200], outline=(160, 60, 50), width=3)
    d.text((W - 196, 108), num, font=font(60), fill=(205, 120, 105))
    d.text((110, H - 120), '影之刃零・中文版攻略', font=font(26), fill=(120, 115, 105))
    im.save(os.path.join(IMGDIR, f'chapter-{cid}.jpg'), 'JPEG', quality=90, optimize=True)

    # 首頁卡片：只留背景與印章，避免與卡片標題重複
    card = ink_bg(1200, 760, color)
    cd = ImageDraw.Draw(card)
    cd.text((760, 220), num, font=font(360), fill=(32, 31, 34))
    cd.rectangle([1060, 52, 1148, 140], outline=(150, 55, 46), width=2)
    cd.text((1088, 66), num, font=font(42), fill=(200, 120, 105))
    cd.line([(64, 120), (520, 120)], fill=(170, 145, 95), width=1)
    card.save(os.path.join(IMGDIR, f'chapter-card-{cid}.jpg'), 'JPEG', quality=90, optimize=True)

    # 章節頁主視覺：無文字，只留背景與印章，讓 HTML 標題疊上去
    bg = ink_bg(1920, 1080, color)
    bd = ImageDraw.Draw(bg)
    bd.text((1180, 260), num, font=font(620), fill=(32, 31, 34))
    bd.rectangle([1700, 90, 1810, 200], outline=(150, 55, 46), width=3)
    bd.text((1734, 108), num, font=font(64), fill=(200, 120, 105))
    bg.save(os.path.join(IMGDIR, f'chapter-bg-{cid}.jpg'), 'JPEG', quality=90, optimize=True)
    print('chapter', cid, name)
