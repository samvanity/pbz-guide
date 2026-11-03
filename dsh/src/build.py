# -*- coding: utf-8 -*-
import os, shutil, html, math, sys
from opencc import OpenCC

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_part1 import CH0, CH1, CH2
from content_part2 import CH3, CH4, CH5
from content_part3 import CH6, CH7, CH8, CH9
import assets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
IMG = os.path.join(SITE, "assets", "images")
CC = OpenCC("s2tw")

CHAPTERS = [CH0, CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9]
SPOILER_KEYS = ("spoiler",)

def tr(s):
    if isinstance(s, str):
        return CC.convert(s)
    if isinstance(s, list):
        return [tr(x) for x in s]
    if isinstance(s, dict):
        return {k: tr(v) for k, v in s.items()}
    return s

CHAPTERS = tr(CHAPTERS)

def e(s):
    return html.escape(s, quote=True)

def exists_img(name):
    return name and os.path.exists(os.path.join(IMG, name))

def img(name, fallback="hero-creek.jpg", alt="", cls=""):
    if not exists_img(name):
        name = fallback
    if not exists_img(name):
        return ""
    return f'<img src="assets/images/{name}" alt="{e(alt)}" class="{cls}">'

def head(title, desc, extra=""):
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#08080a">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="assets/style.css">
<script defer src="assets/app.js"></script>
{extra}
</head>
<body>
<div class="readbar"></div>
<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="brand" href="index.html">
      <span class="brand-seal">刃</span>
      <span class="brand-text"><b>影之刃零 · 江湖行止錄</b><span>影之刃零 · 中文版錯過攻略</span></span>
    </a>
    <nav class="nav" aria-label="主選單">
      <a href="index.html">章節</a>
      <a href="bosses.html">頭目</a>
      <a href="missables.html">錯過清單</a>
      <a href="ending.html">真結局</a>
      <span class="sep"></span>
      <button class="spoiler-toggle" aria-pressed="false" type="button"><span class="dot"></span><span>開啟劇透</span></button>
    </nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-label="開啟選單">☰</button>
  </div>
</header>
"""

def foot():
    return """
<footer class="footer">
  <div class="wrap footer-top">
    <div>
      <a class="brand" href="index.html">
        <span class="brand-seal">刃</span>
        <span class="brand-text"><b>影之刃零 · 江湖行止錄</b><span>影之刃零 · 中文版錯過攻略</span></span>
      </a>
      <p>非官方中文攻略。以主機／電腦 中文版名稱為準，所有條目依遊玩時間順序排列；只寫容易錯過、錯過就拿不到的東西，盡量不碰劇情。遊戲畫面與資料版權屬 靈遊坊 與原權利人所有。</p>
    </div>
    <div class="footer-links">
      <a href="index.html">章節索引</a>
      <a href="bosses.html">頭目攻略</a>
      <a href="missables.html">錯過清單</a>
      <a href="ending.html">真結局</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>攻略整理：2026</span>
    <span>建議搭配中文版遊玩；劇透預設關閉</span>
  </div>
</footer>
</body>
</html>"""

TYPE_CLASS = {
    "飾品": "item", "武器": "weapon", "支線": "quest", "紫色任務": "purple",
    "道具": "item", "頭目": "boss", "系統": "", "地圖": "",
}

def badge(t, miss=False):
    cls = TYPE_CLASS.get(t, "")
    return f'<span class="badge {cls}">{e(t)}</span>' + ('<span class="badge miss">錯過不再</span>' if miss else "")

def stop_html(i, s, chapter):
    miss = bool(s.get("miss"))
    img_html = ""
    if s.get("img") and s["img"] in SAFE_STOP_IMAGES:
        alt = s["title"]
        img_html = f'<figure class="stop-img">{img(s["img"], chapter["hero"], alt)}<figcaption><span>{e(alt)}</span><span>取得位置實景</span></figcaption></figure>'
    gains = "".join(f"<span>{e(g)}</span>" for g in s.get("gain", []))
    return f"""
<article class="tl-item {'miss' if miss else ''}" id="s{i}">
  <span class="tl-node">{i:02d}</span>
  <div class="stop">
    <div class="stop-main">
      <div class="stop-top">{badge(s['type'], miss)}</div>
      <h3>{e(s['title'])}</h3>
      <div class="loc">{e(s['loc'])}</div>
      <div class="desc">{s['desc']}</div>
      {f'<div class="miss-box"><b>錯過條件</b>{s["miss"]}</div>' if miss else ''}
      {f'<div class="gain">{gains}</div>' if gains else ''}
    </div>
    {img_html}
  </div>
</article>"""

BOSS_PHOTOS = {"cangang", "pengmeng", "ahua", "zhuming"}
PLATE_KEYS = {"sanmian", "jinmianju", "muxiaokui", "xieqiudong", "guhe", "yuzan",
              "yumian", "zuoshang-true", "duanchang", "huangxing", "moyuan", "lizhe",
              "biyuan", "bifeng", "zuoshang", "yucong"}
SAFE_STOP_IMAGES = set()

def boss_html(i, b, chapter):
    miss = b.get("miss")
    tactics = "".join(f"<li>{x}</li>" for x in b["tactics"])
    lo = b["loadout"]
    key = os.path.splitext(b.get("img") or "")[0].replace("boss-", "")
    kind = "頭目實機" if key in BOSS_PHOTOS else "頭目名刺"
    tag = f'<span class="tag{" miss" if miss else ""}">{kind}{"・會錯過" if miss else ""}</span>'
    return f"""
<article class="boss-card" id="b{i}">
  <div class="boss-head">
    <div class="boss-portrait">
      {img(b['img'], chapter['hero'], b['name'] + ' 攻略畫面')}
      {tag}
    </div>
    <div class="boss-info">
      <div class="kicker">頭目攻略 · {e(chapter['name'])}</div>
      <h3>{e(b['name'])}</h3>
      <div class="sub">{e(b['title'])}</div>
      <div class="boss-loc"><span class="pin">◆</span><span>{e(b['loc'])}</span></div>
      <div class="boss-reward"><span>{e(b['phases'])}</span><span>獎勵：{e(b['reward'])}</span></div>
    </div>
  </div>
  <div class="boss-body">
    <ul class="boss-tactics">{tactics}</ul>
    <div class="boss-loadout">
      <div><div class="k">推薦武器</div><div class="v">{e(lo['weapon'])}</div></div>
      <div><div class="k">道具／藥瓶</div><div class="v">{e(lo['item'])}</div></div>
      <div><div class="k">飾品</div><div class="v">{e(lo['acc'])}</div></div>
      <div><div class="k">戰術核心</div><div class="v">{e(lo['tactic'])}</div></div>
    </div>
  </div>
</article>"""

def route_svg(ch):
    stops = ch["stops"][:7]
    n = len(stops)
    W, H = 1000, 300
    if n == 0:
        return ""
    pts = []
    for i in range(n):
        x = 80 + i * (W - 160) / max(1, n - 1)
        y = 150 + (36 if i % 2 == 0 else -36)
        pts.append((x, y))
    path = f"M {pts[0][0]} {pts[0][1]}"
    for i in range(1, n):
        x0, y0 = pts[i-1]; x1, y1 = pts[i]
        cx = (x0 + x1) / 2
        path += f" C {cx} {y0}, {cx} {y1}, {x1} {y1}"
    nodes = ""
    for i, (x, y) in enumerate(pts):
        label = stops[i]["title"]
        if len(label) > 9:
            label = label[:8] + "…"
        up = y < 150
        ly = y - 26 if up else y + 40
        nodes += f'<circle cx="{x}" cy="{y}" r="15" fill="#0b0b0d" stroke="#c9a96a" stroke-width="1.2"/>'
        nodes += f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="11" fill="#c9a96a" font-family="monospace">{i+1:02d}</text>'
        nodes += f'<text x="{x}" y="{ly}" text-anchor="middle" font-size="12.5" fill="#d8cfbd" font-family="Noto Serif TC, serif">{e(label)}</text>'
    return f"""<svg class="route-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{e(ch['name'])} 路線圖">
  <defs>
    <linearGradient id="g{ch['id']}" x1="0" x2="1"><stop offset="0" stop-color="#b23b30"/><stop offset="1" stop-color="#c9a96a"/></linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="none"/>
  <path d="{path}" fill="none" stroke="url(#g{ch['id']})" stroke-width="1.4" stroke-dasharray="5 7" opacity=".8"/>
  {nodes}
  <text x="{W-30}" y="{H-18}" text-anchor="end" font-size="11" fill="#6f6a61" font-family="monospace" letter-spacing="3">{e(ch['id'].upper())} · 路線</text>
</svg>"""

def chapter_page(ch, idx):
    stops_html = "".join(stop_html(i+1, s, ch) for i, s in enumerate(ch["stops"]))
    bosses_html = "".join(boss_html(i+1, b, ch) for i, b in enumerate(ch["bosses"]))
    checks = "".join(
        f'<div class="check"><label><input type="checkbox" value="c{i}"><span class="txt">{e(x)}</span></label></div>'
        for i, x in enumerate(ch["checklist"])
    )
    miss_count = sum(1 for s in ch["stops"] if s.get("miss"))
    boss_count = len(ch["bosses"])
    facts = []
    for k, v in ch["facts"]:
        if k == "易錯過":
            v = str(miss_count)
        elif k == "頭目":
            v = str(boss_count)
        facts.append((k, v))
    prev_ch = CHAPTERS[idx-1] if idx > 0 else None
    next_ch = CHAPTERS[idx+1] if idx < len(CHAPTERS)-1 else None
    nav = '<div class="chapter-nav">'
    nav += (f'<a href="{prev_ch["id"]}.html"><span class="dir">← 上一章</span><span class="name">{e(prev_ch["name"])}</span></a>' if prev_ch else '<span></span>')
    nav += (f'<a href="{next_ch["id"]}.html"><span class="dir">下一章 →</span><span class="name">{e(next_ch["name"])}</span></a>' if next_ch else '<span></span>')
    nav += '</div>'
    map_block = ""
    if ch.get("map"):
        map_block = f'<figure class="chapter-map">{img(ch["map"], ch["hero"], ch["name"] + " 地圖")}<figcaption><span>{e(ch["name"])}・遊戲內地圖</span><span>可搭配下方路線圖閱讀</span></figcaption></figure>'
    notice = ch.get("notice")
    notice_html = ""
    if notice:
        notice_html = f"""<div class="notice {notice.get('kind','red')}">
  <div class="seal">{e(notice['seal'])}</div>
  <div><h3>{e(notice['title'])}</h3><p>{notice['text']}</p></div>
</div>"""
    hero_class = "chapter-hero plate-hero" if ch["hero"].startswith("chapter-bg-") else "chapter-hero"
    return head(f"{ch['name']}｜影之刃零 攻略", ch["tagline"]) + f"""
<section class="{hero_class}">
  <div class="bg">{img(ch['hero'], 'hero-creek.jpg', ch['name'])}</div>
  <div class="wrap inner">
    <div class="chapter-kicker"><span class="n">{e(ch['num'])}</span><span>{e(ch['sub'])}</span></div>
    <h1 class="chapter-title">{e(ch['name'])}<small>{e(ch['tagline'])}</small></h1>
    <p class="chapter-lead">{ch['intro']}</p>
    <div class="chapter-facts">
      {''.join(f'<div class="f"><b>{e(v)}</b><span>{e(k)}</span></div>' for k, v in facts)}
    </div>
  </div>
</section>
<div class="wrap chapter-layout">
  <aside class="toc">
    <div class="toc-title">本章目錄</div>
    <a href="#route"><span class="i">00</span>路線圖</a>
    <a href="#timeline"><span class="i">01</span>時間軸・易錯過</a>
    {''.join(f'<a class="toc-sub" href="#s{i+1}">{i+1:02d}　{e(s["title"])}</a>' for i, s in enumerate(ch['stops']))}
    <a href="#bosses"><span class="i">02</span>頭目攻略</a>
    {''.join(f'<a class="toc-sub" href="#b{i+1}">{i+1:02d}　{e(b["name"])}</a>' for i, b in enumerate(ch['bosses']))}
    <a href="#checklist"><span class="i">03</span>離開前檢查</a>
    <div class="back"><a href="index.html">← 回到章節索引</a></div>
  </aside>
  <main class="chapter-content">
    {notice_html}
    <section id="route">
      <div class="content-head"><h2><small>路線</small>本章路線</h2><span class="count">{miss_count} 個易錯過・{boss_count} 個頭目</span></div>
      {map_block}
      <div class="route-wrap">
        <div class="route-head"><span>依遊玩順序</span><span>點擊右側時間軸看詳細</span></div>
        {route_svg(ch)}
      </div>
    </section>
    <section id="timeline">
      <div class="content-head"><h2><small>時間軸</small>時間軸・容易錯過的東西</h2><span class="count">{len(ch['stops'])} 個節點</span></div>
      <div class="timeline">{stops_html}</div>
    </section>
    <section id="bosses">
      <div class="content-head"><h2><small>頭目</small>頭目攻略</h2><span class="count">{boss_count} 個</span></div>
      <p class="small muted" style="margin:-8px 0 20px">只保留確認對應的頭目實機畫面；其餘一律用名刺卡，避免圖不對題。</p>
      {bosses_html}
    </section>
    <section id="checklist">
      <div class="content-head"><h2><small>檢查</small>離開本章前檢查</h2><span class="count">勾選會自動保存</span></div>
      <div class="check-progress"><div class="bar"><i></i></div><div class="txt">0 / {len(ch['checklist'])} 已完成</div></div>
      <div class="checklist" data-key="{ch['id']}" id="checklist-{ch['id']}">{checks}</div>
      <p class="small muted" style="margin-top:12px">完成度只存在你的瀏覽器；換裝置不會同步。</p>
    </section>
    {nav}
  </main>
</div>
""" + foot()

def index_page():
    cards = ""
    for ch in CHAPTERS:
        miss = sum(1 for s in ch["stops"] if s.get("miss"))
        if ch["hero"].startswith("chapter-bg-"):
            card_img = ch["hero"].replace("chapter-bg-", "chapter-card-", 1)
        elif ch["hero"].startswith("chapter-card-"):
            card_img = ch["hero"]
        elif ch["hero"].startswith("chapter-"):
            card_img = ch["hero"].replace("chapter-", "chapter-card-", 1)
        else:
            card_img = ch["hero"]
        card_cls = "chapter-card plate-card reveal" if ch["hero"].startswith("chapter-") else "chapter-card reveal"
        cards += f"""
<a class="{card_cls}" href="{ch['id']}.html">
  {img(card_img, 'hero-creek.jpg', ch['name'])}
  <div class="cc-top"><span class="cc-num">章節 {e(ch['num'])}</span><span class="cc-tag">{e(ch['sub'])}</span></div>
  <div class="cc-body">
    <h3>{e(ch['name'])}</h3>
    <div class="sub">{e(ch['tagline'])}</div>
    <div class="cc-stats"><span><b>{miss}</b> 錯過不再</span><span><b>{len(ch['bosses'])}</b> 頭目</span><span><b>{len(ch['stops'])}</b> 節點</span></div>
  </div>
  <span class="cc-arrow">→</span>
</a>"""
    total_miss = sum(1 for ch in CHAPTERS for s in ch["stops"] if s.get("miss"))
    total_boss = sum(len(ch["bosses"]) for ch in CHAPTERS)
    total_stop = sum(len(ch["stops"]) for ch in CHAPTERS)
    return head("影之刃零 攻略｜錯過不再的道具、支線與頭目打法", "以中文版名稱為準的《影之刃零》攻略：依遊玩順序整理每章容易錯過的道具、支線、武器與頭目打法。") + f"""
<section class="hero">
  <div class="hero-bg">{img('hero-creek.jpg', 'hero-creek.jpg', '影之刃零')}</div>
  <div class="hero-inner">
    <div class="hero-kicker"><span class="line"></span><span>中文版 · 錯過不再的攻略</span></div>
    <h1>影之刃零<span class="thin">江湖行止錄</span></h1>
    <p class="hero-sub">只寫<b>容易忘記、忽略、錯過就再也拿不到</b>的東西。每一章依遊玩時間順序排列，附章節路線、實機截圖與頭目配裝；劇情能避就避。</p>
    <div class="hero-meta">
      <div class="item"><span class="num">{total_miss}</span><span class="lbl">錯過不再</span></div>
      <div class="item"><span class="num">{total_boss}</span><span class="lbl">頭目攻略</span></div>
      <div class="item"><span class="num">{total_stop}</span><span class="lbl">時間軸節點</span></div>
      <div class="item"><span class="num">10</span><span class="lbl">章節頁</span></div>
    </div>
    <div class="hero-cta">
      <a class="btn btn-primary" href="#chapters">選擇章節 <span class="arrow">→</span></a>
      <a class="btn" href="missables.html">先看錯過清單</a>
    </div>
  </div>
  <div class="scroll-cue">往下</div>
</section>

<section class="section" id="chapters">
  <div class="wrap">
    <div class="section-head">
      <h2><small>章節</small>選擇章節</h2>
      <p>依主線順序排列。卡片上的「錯過不再」是本章會永久消失的條目數量，不是收集品總數。圖片只放確認對題的實機畫面，其餘以章節圖與名刺呈現。</p>
    </div>
    <div class="chapter-grid">{cards}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head">
      <h2><small>使用方式</small>使用方式</h2>
      <p>先看紅框，再看路線。真的卡住時，再打開頭目卡。</p>
    </div>
    <div class="legend reveal">
      <div><h3><span class="k">斷</span>紅框＝錯過不再</h3><p>標了「錯過不再」的條目，都有明確的斷點：推進主線、擊敗某個頭目、或進入下一張地圖後永久失效。</p></div>
      <div><h3><span class="k">光</span>藍光、紅光、黑光</h3><p>藍光要完美格擋，紅光要完美閃避，黑光只能閃避。格擋黑光會清空自己的殺氣，這是前期最常死的理由。</p></div>
      <div><h3><span class="k">序</span>時間軸順序</h3><p>每章的節點都照實際遊玩順序編號；不是地圖分區，也不是收集品分類。照著走就不會來回繞。</p></div>
      <div><h3><span class="k">劇</span>劇透預設關閉</h3><p>牽涉劇情的地方會模糊處理；按右上角「開啟劇透」才會顯示。真結局頁另有一次確認。</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><h2><small>出發前</small>先看這三件事</h2><p>如果你只讀一頁，讀這一頁。</p></div>
    <div class="chapter-grid" style="grid-template-columns:repeat(3,1fr)">
      <a class="chapter-card reveal" href="missables.html" style="min-height:260px">
        {img('item-jianyan.jpg', 'hero-creek.jpg', '堅巖護腕')}
        <div class="cc-top"><span class="cc-num">01</span><span class="cc-tag">錯過清單</span></div>
        <div class="cc-body"><h3 style="font-size:24px">所有錯過清單</h3><div class="sub">依章節與期限排列，適合出發前掃一眼</div></div>
      </a>
      <a class="chapter-card reveal" href="ending.html" style="min-height:260px">
        {img('hero-soul.jpg', 'hero-creek.jpg', '真結局')}
        <div class="cc-top"><span class="cc-num">02</span><span class="cc-tag">真結局</span></div>
        <div class="cc-body"><h3 style="font-size:24px">真結局期限</h3><div class="sub">十個紫色任務與五根龍柱，進戲夢山莊前要完成</div></div>
      </a>
      <a class="chapter-card reveal" href="bosses.html" style="min-height:260px">
        {img('boss-baichilian.jpg', 'hero-forest.jpg', '頭目')}
        <div class="cc-top"><span class="cc-num">03</span><span class="cc-tag">頭目</span></div>
        <div class="cc-body"><h3 style="font-size:24px">頭目索引</h3><div class="sub">依章節與「會錯過」篩選，直接跳到打法</div></div>
      </a>
    </div>
  </div>
</section>
""" + foot()

def bosses_page():
    tiles = ""
    for ch in CHAPTERS:
        for b in ch["bosses"]:
            key = os.path.splitext(b.get("img") or "")[0].replace("boss-", "")
            kind = "頭目實機" if key in BOSS_PHOTOS else "名刺"
            tiles += f"""
<a class="boss-tile" href="{ch['id']}.html#b{ch['bosses'].index(b)+1}" data-chapter="{ch['id']}" data-miss="{1 if b.get('miss') else 0}">
  <div class="ph">{img(b['img'], ch['hero'], b['name'])}<span class="tile-tag">{kind}</span></div>
  <div class="bd"><div class="ch">{e(ch['name'])} · {e(b['title'])}</div><h3>{e(b['name'])}</h3><p>{e(b['loc'])}</p></div>
  <span class="go">→</span>
</a>"""
    filters = '<button class="filter active" data-filter="all">全部</button>'
    for ch in CHAPTERS:
        filters += f'<button class="filter" data-filter="{ch["id"]}">{e(ch["name"])}</button>'
    filters += '<button class="filter" data-filter="miss">只看會錯過</button>'
    return head("頭目索引｜影之刃零 攻略", "依章節整理《影之刃零》頭目位置、推薦武器、道具、飾品與戰術。") + f"""
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">頭目圖鑑</div>
  <h1>頭目索引</h1>
  <p>每一張卡都附位置、階段、推薦武器／道具／飾品與戰術核心。點擊直接跳到該章對應段落；「會錯過」表示該頭目有期間限定的獎勵或支線。</p>
  <div class="filters">{filters}</div>
</div></section>
<div class="wrap"><div class="boss-grid">{tiles}</div><div class="empty" style="display:none">這個分類目前沒有頭目。</div></div>
""" + foot()

def missables_page():
    rows = ""
    deadlines = ""
    total = 0
    for ch in CHAPTERS:
        items = [s for s in ch["stops"] if s.get("miss")]
        total += len(items)
        if not items:
            continue
        items_html = "".join(
            f'<div class="check"><label><input type="checkbox" value="{ch["id"]}-{i}"><span class="txt"><b>{e(s["title"])}</b><small>{e(s["loc"])}　—　{s["miss"]}</small></span></label></div>'
            for i, s in enumerate(items)
        )
        rows += f"""
<section style="margin-bottom:44px">
  <div class="content-head"><h2><small>{e(ch['sub'])}</small>{e(ch['name'])}</h2><span class="count">{len(items)} 項</span></div>
  <div class="checklist" data-key="miss-{ch['id']}">{items_html}</div>
</section>"""
    deadline_list = [
        ("進入血色森林前", "溪谷的【見習醫師】【清理門戶】【堅巖護腕】；驛站眾人在血色森林後全滅。"),
        ("擊敗白赤練前", "溪谷與飛賊營地的所有人員支線；她死後兩地全滅。"),
        ("打開飛賊通道／前往龐鎮前", "陸家村的【蘭家大少】與【歸途】第二步。"),
        ("進入戲夢山莊前", "十個真結局紫色任務：溪谷深處、虛空幻象、機關船、浮華引、幻術琵琶、崑崙三傑、泣聲何來、夢差的幻象、紅房子、湖心秘密。"),
        ("進入斷魂山最終區域前", "五根龍柱與血脈覺醒；斷魂山【最後的挽回之地】是最後警告。"),
    ]
    for d, txt in deadline_list:
        deadlines += f'<div class="deadline"><div class="day">期限</div><h3>{e(d)}</h3><p>{e(txt)}</p></div>'
    return head("錯過清單｜影之刃零 攻略", "《影之刃零》所有容易錯過、錯過就永久失效的道具、支線、武器與飾品，依章節與期限整理。") + f"""
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">錯過清單</div>
  <h1>錯過清單</h1>
  <p>只列會永久消失的東西。每一項都標了位置與斷點；勾選會存在瀏覽器，出發前掃一遍就夠。</p>
  <div class="miss-summary">
    <div><b>{total}</b><span>期限定條目</span></div>
    <div><b>5</b><span>關鍵斷點</span></div>
    <div><b>0</b><span>劇透（預設關閉）</span></div>
  </div>
</div></section>
<div class="wrap" style="padding:64px 0 100px">
  <div class="section-head"><h2><small>期限</small>五個斷點</h2><p>先記這五個時間，比記一百個道具位置有用。</p></div>
  {deadlines}
  <div style="height:40px"></div>
  {rows}
</div>
""" + foot()

def ending_page():
    tasks = ["溪谷深處", "虛空幻象", "機關船", "浮華引", "幻術琵琶", "崑崙三傑", "泣聲何來", "夢差的幻象", "紅房子", "湖心秘密"]
    checks = "".join(f'<div class="check"><label><input type="checkbox" value="t{i}"><span class="txt"><b>{e(t)}</b><small>紫色任務</small></span></label></div>' for i, t in enumerate(tasks))
    return head("真結局｜影之刃零 攻略", "《影之刃零》真結局條件：十個紫色任務、五根龍柱與斷魂山分歧，含劇透開關。") + f"""
<section class="page-hero"><div class="wrap">
  <div class="eyebrow">真結局 · 內含劇透</div>
  <h1>真結局</h1>
  <p>這一頁會提到後期任務與最終頭目，預設以模糊處理。按右上角「開啟劇透」才會顯示完整條件。</p>
</div></section>
<div class="wrap-narrow" style="padding:64px 0 100px">
  <div class="notice red"><div class="seal">劇</div><div><h3>先說結論</h3><p>真結局＝十個紫色任務全部完成＋五根龍柱（血脈覺醒）全部完成。兩者都要在進入斷魂山最終區域前收尾；進入戲夢山莊是第一個硬期限。</p></div></div>
  <div class="content-head" style="margin-top:48px"><h2><small>紫色任務</small>十個紫色任務</h2><span class="count">進戲夢山莊前</span></div>
  <div class="checklist" data-key="ending-tasks">{checks}</div>
  <div class="content-head" style="margin-top:48px"><h2><small>龍柱</small>五根龍柱</h2><span class="count">進斷魂山前</span></div>
  <div class="notice gold"><div class="seal">龍</div><div><h3>血脈覺醒</h3><p>五根龍柱分別在悲泣溪谷、血色森林、陸家村（或周邊）、梅谷湖與後段區域；每根都要完成挑戰。第五根完成後，血脈覺醒才算完成。龍柱旁的金面具與魔淵都屬於這條線。</p></div></div>
  <div class="content-head" style="margin-top:48px"><h2><small>最終分歧</small>斷魂山分歧</h2><span class="count">最終區域</span></div>
  <div class="spoiler">
    <div class="notice jade"><div class="seal">終</div><div><h3>擊敗夢華之後</h3><p>完成全部真結局條件，左殤會現身，帶你進入金色光柱，挑戰真最終頭目「左殤（真龍）」，觸發真結局與獎盃「昭昭心與血」。若條件不足，夢華死後直接播放普通結局，沒有左殤戰。</p></div></div>
  </div>
  <p class="small muted" style="margin-top:18px">※ 本頁只整理條件，不展開劇情。需要看完整劇透時，再開啟右上角開關。</p>
</div>
""" + foot()

def main():
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    # 只清掉舊頁面，保留已下載圖片，避免每次重建都重新抓圖
    import glob
    for f in glob.glob(os.path.join(SITE, "*.html")):
        os.remove(f)
    # 9game 的湖區地圖偶爾連不上，使用已下載的備份
    lake_backup = os.path.join(ROOT, "research", "imgs", "lake2.jpg")
    if not os.path.exists(os.path.join(IMG, "map-ch6.jpg")) and os.path.exists(lake_backup):
        shutil.copy(lake_backup, os.path.join(IMG, "map-ch6.jpg"))

    # static
    for f in ("style.css", "app.js"):
        shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), os.path.join(SITE, "assets", f))

    assets.download_all(IMG)

    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(index_page())
    for i, ch in enumerate(CHAPTERS):
        open(os.path.join(SITE, ch["id"] + ".html"), "w", encoding="utf-8").write(chapter_page(ch, i))
    open(os.path.join(SITE, "bosses.html"), "w", encoding="utf-8").write(bosses_page())
    open(os.path.join(SITE, "missables.html"), "w", encoding="utf-8").write(missables_page())
    open(os.path.join(SITE, "ending.html"), "w", encoding="utf-8").write(ending_page())

    # GitHub Pages
    open(os.path.join(SITE, ".nojekyll"), "w").write("")
    print("built", SITE)

if __name__ == "__main__":
    main()
