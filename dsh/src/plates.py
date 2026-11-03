# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(BASE, 'site', 'assets', 'images')

PLATES = {
    'sanmian': ('三面魔偶', 'hero-creek.jpg', '壹'),
    'jinmianju': ('金面具', 'hero-creek.jpg', '壹'),
    'muxiaokui': ('沐小葵', 'hero-lu.jpg', '參'),
    'xieqiudong': ('謝秋冬', 'hero-pang.jpg', '肆'),
    'guhe': ('古鶴', 'hero-lake.jpg', '陸'),
    'yuzan': ('玉瓚', 'hero-lu.jpg', '參'),
    'yumian': ('玉面郎君', 'hero-jail.jpg', '柒'),
    'zuoshang-true': ('左殤', 'hero-soul.jpg', '終'),
    'duanchang': ('斷腸', 'hero-lake.jpg', '陸'),
    'huangxing': ('黃行', 'hero-jail.jpg', '柒'),
    'moyuan': ('魔淵', 'hero-soul.jpg', '終'),
    'lizhe': ('力者與鋸者', 'hero-soul.jpg', '終'),
    'biyuan': ('畢遠', 'hero-lu.jpg', '參'),
    'bifeng': ('橫刀畢峰', 'hero-prologue.jpg', '柒'),
}

def font(size):
    for p in [r'C:\Windows\Fonts\msjh.ttc', r'C:\Windows\Fonts\msjhbd.ttc', r'C:\Windows\Fonts\simkai.ttf']:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

W, H = 1200, 740
for key, (name, bgname, num) in PLATES.items():
    bgp = os.path.join(IMGDIR, bgname)
    if not os.path.exists(bgp):
        bgp = os.path.join(IMGDIR, 'hero-creek.jpg')
    im = Image.open(bgp).convert('RGB')
    # 去掉畫面上方的頭目血條與名稱，避免名刺背景出現別的頭目
    im = im.crop((0, int(im.height * 0.17), im.width, im.height))
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(2))
    im = ImageEnhance.Brightness(im).enhance(0.62)
    im = ImageEnhance.Color(im).enhance(0.72)
    im = im.convert('RGBA')
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for yy in range(H):
        a = int(200 * (yy / H) ** 1.45)
        od.line([(0, yy), (W, yy)], fill=(8, 8, 10, a))
    im = Image.alpha_composite(im, ov).convert('RGB')
    d = ImageDraw.Draw(im)
    d.line([(64, 120), (W - 64, 120)], fill=(180, 150, 95), width=1)
    d.text((66, 72), '頭目名刺', font=font(24), fill=(198, 178, 138))
    d.rectangle([W - 130, 58, W - 66, 122], outline=(150, 55, 46), width=2)
    d.text((W - 112, 70), num, font=font(38), fill=(200, 120, 105))
    fs = 120 if len(name) <= 4 else 92
    d.text((62, H - 230), name, font=font(fs), fill=(238, 231, 216), stroke_width=1, stroke_fill=(20, 18, 16))
    d.text((68, H - 78), '影之刃零・中文版攻略', font=font(24), fill=(170, 160, 142))
    im.save(os.path.join(IMGDIR, f'boss-{key}.jpg'), 'JPEG', quality=88, optimize=True)
    print('plate', key, name)
