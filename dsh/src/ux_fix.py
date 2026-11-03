# -*- coding: utf-8 -*-
import re
p = 'dsh/src/style.css'
s = open(p, encoding='utf-8').read()

repl = [
    ('  font-size:16px;\n  line-height:1.85;', '  font-size:17px;\n  line-height:1.9;'),
    ('.nav a{\n  font-family:var(--sans);font-size:12.5px;', '.nav a{\n  font-family:var(--sans);font-size:13.5px;'),
    ('.legend p{font-size:12.5px;line-height:1.8;color:var(--muted)}', '.legend p{font-size:14px;line-height:1.8;color:var(--muted)}'),
    ('.chapter-lead{max-width:660px;margin-top:22px;color:#d5ccba;font-size:15px;line-height:2}', '.chapter-lead{max-width:680px;margin-top:22px;color:#d5ccba;font-size:16.5px;line-height:2}'),
    ('.toc{position:sticky;top:104px}', '''.toc{
  position:sticky;top:96px;
  max-height:calc(100vh - 120px);
  max-height:calc(100dvh - 120px);
  overflow-y:auto;
  overscroll-behavior:contain;
  -webkit-overflow-scrolling:touch;
  padding-right:10px;
  scrollbar-width:thin;
  scrollbar-color:#3a3831 transparent;
}
.toc::-webkit-scrollbar{width:5px}
.toc::-webkit-scrollbar-track{background:transparent}
.toc::-webkit-scrollbar-thumb{background:#34322c;border-radius:4px}'''),
    ('.toc-title{font-family:var(--sans);font-size:10px;letter-spacing:.26em;color:var(--muted);padding-bottom:14px;border-bottom:1px solid var(--line);margin-bottom:14px}',
     '.toc-title{position:sticky;top:0;z-index:2;background:var(--ink);font-family:var(--sans);font-size:11.5px;letter-spacing:.26em;color:var(--muted);padding:2px 0 14px;border-bottom:1px solid var(--line);margin-bottom:14px}'),
    ('.toc a{display:flex;align-items:baseline;gap:10px;padding:8px 0;font-size:13px;', '.toc a{display:flex;align-items:baseline;gap:10px;padding:9px 0;font-size:14.5px;'),
    ('.toc a .i{font-family:var(--mono);font-size:10px;', '.toc a .i{font-family:var(--mono);font-size:11px;'),
    ('.toc .toc-sub{margin-left:32px;font-family:var(--sans);font-size:10.5px;', '.toc .toc-sub{margin-left:32px;font-family:var(--sans);font-size:12.5px;'),
    ('.toc .back{margin-top:22px;border-top:1px solid var(--line);padding-top:14px;font-family:var(--sans);font-size:11px;', '.toc .back{margin-top:22px;border-top:1px solid var(--line);padding-top:14px;font-family:var(--sans);font-size:12px;'),
    ('.stop .desc{margin-top:12px;font-size:14px;line-height:1.95;color:var(--paper-dim)}', '.stop .desc{margin-top:12px;font-size:15.5px;line-height:1.95;color:var(--paper-dim)}'),
    ('.stop h3{font-size:21px;', '.stop h3{font-size:22px;'),
    ('.stop .loc{font-family:var(--sans);font-size:11px;', '.stop .loc{font-family:var(--sans);font-size:12px;'),
    ('.miss-box{\n  margin-top:14px;padding:12px 14px;border-left:2px solid var(--red);background:rgba(178,59,48,.07);\n  font-size:12.5px;', '.miss-box{\n  margin-top:14px;padding:12px 14px;border-left:2px solid var(--red);background:rgba(178,59,48,.07);\n  font-size:13.5px;'),
    ('.boss-tactics li{position:relative;padding-left:18px;font-size:13.5px;', '.boss-tactics li{position:relative;padding-left:18px;font-size:15px;'),
    ('.boss-loadout .k{font-family:var(--sans);font-size:9px;', '.boss-loadout .k{font-family:var(--sans);font-size:10px;'),
    ('.boss-loadout .v{font-size:12.5px;', '.boss-loadout .v{font-size:14px;'),
    ('.boss-loadout .v small{display:block;color:var(--muted);font-size:11px;', '.boss-loadout .v small{display:block;color:var(--muted);font-size:12px;'),
    ('.check .txt{font-size:13.5px;', '.check .txt{font-size:14.5px;'),
    ('.check .txt small{display:block;font-family:var(--sans);font-size:10.5px;', '.check .txt small{display:block;font-family:var(--sans);font-size:11.5px;'),
    ('.notice p{font-size:13px;', '.notice p{font-size:14px;'),
    ('.content-head .count{font-family:var(--mono);font-size:11px;', '.content-head .count{font-family:var(--mono);font-size:12px;'),
    ('.footer p{font-size:12px;', '.footer p{font-size:13px;'),
    ('.boss-tile p{font-family:var(--sans);font-size:10.5px;', '.boss-tile p{font-family:var(--sans);font-size:11.5px;'),
    ('.page-hero p{max-width:640px;color:var(--muted);font-size:14.5px;', '.page-hero p{max-width:660px;color:var(--muted);font-size:16px;'),
    ('.deadline p{font-size:12.5px;', '.deadline p{font-size:13.5px;'),
    ('.miss-summary span{font-family:var(--sans);font-size:10px;', '.miss-summary span{font-family:var(--sans);font-size:11px;'),
    ('.small{font-size:13px}', '.small{font-size:14px}'),
    ('.gain span{font-family:var(--sans);font-size:10.5px;', '.gain span{font-family:var(--sans);font-size:11.5px;'),
    ('.chapter-facts span{font-family:var(--sans);font-size:10px;', '.chapter-facts span{font-family:var(--sans);font-size:11px;'),
    ('.chapter-facts b{font-family:var(--mono);font-size:22px;', '.chapter-facts b{font-family:var(--mono);font-size:24px;'),
    ('.content-head{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:26px;padding-bottom:16px;border-bottom:1px solid var(--line)}',
     '.content-head{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:26px;padding-bottom:16px;border-bottom:1px solid var(--line);scroll-margin-top:112px}'),
]
for a, b in repl:
    if a not in s:
        print('MISS:', a[:70])
    s = s.replace(a, b)

# 手機／平板目錄
s += '''

/* ============ 目錄：小螢幕與縮放 ============ */
.toc-mobile{display:none;margin:0 0 26px}
.toc-mobile summary{
  list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;
  padding:14px 16px;border:1px solid var(--line-strong);background:var(--panel);
  font-family:var(--sans);font-size:13px;letter-spacing:.08em;color:var(--gold);
}
.toc-mobile summary::-webkit-details-marker{display:none}
.toc-mobile summary::after{content:"＋";font-family:var(--mono);color:var(--gold)}
.toc-mobile[open] summary::after{content:"－"}
.toc-mobile-links{border:1px solid var(--line);border-top:0;background:var(--panel);padding:6px 16px 14px}
.toc-mobile-links a{display:flex;align-items:baseline;gap:10px;padding:9px 0;font-size:14px;line-height:1.6;color:var(--paper-dim);border-bottom:1px solid rgba(255,255,255,.05)}
.toc-mobile-links a:last-child{border-bottom:0}
.toc-mobile-links a .i{font-family:var(--mono);font-size:10.5px;color:var(--muted);min-width:18px}
.toc-mobile-links a.toc-sub{padding-left:24px;font-family:var(--sans);font-size:12.5px;color:var(--muted)}
.toc-mobile-links a:hover{color:var(--gold)}

@media (max-width:1080px){
  .toc-mobile{display:block}
  body{font-size:17.5px}
  .toc-mobile-links a{font-size:15px}
  .toc-mobile-links a.toc-sub{font-size:13.5px}
}

@media (max-width:860px){
  .toc-mobile{margin-bottom:22px}
  .toc-mobile summary{font-size:14px}
}
'''
open(p, 'w', encoding='utf-8').write(s)
print('done')
