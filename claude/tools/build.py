# -*- coding: utf-8 -*-
"""Generate the static guide pages (index.html, ch1..ch9.html) from the data below.

Run:  python claude/tools/build.py
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- image sources ----------
PP = "https://www.powerpyx.com/wp-content/uploads/phantom-blade-zero-"
KG = "https://images.keengamer.com/wp-content/uploads/2026/10/"
PG = "https://www.pcgamesn.com/wp-content/sites/pcgamesn/2026/10/"


def pp(region, n, suffix=""):
    """PowerPyx screenshot pair: (-1 = in-game map with marker, -2 = in-world)."""
    return (f"{PP}{region}-{n}-1{suffix}.jpg", f"{PP}{region}-{n}-2{suffix}.jpg")


WCV, CF, VL, PZ, ME, ML, MI = (
    "weeping-creek-valley", "crimson-forest", "village-of-lu", "pangzhen",
    "mandate-encampment", "meigu-lake", "mountain-of-imprisonment",
)

TAGS = {
    "miss": ("錯過不再", "t-miss"),
    "weapon": ("武器", "t-weapon"),
    "edge": ("Phantom Edge", "t-edge"),
    "acc": ("飾品", "t-acc"),
    "tale": ("支線 Tale", "t-tale"),
    "key": ("關鍵道具", "t-key"),
    "pillar": ("長柱挑戰", "t-pillar"),
    "mask": ("Acolyte 面具", "t-mask"),
    "true": ("真結局必要", "t-true"),
    "opt": ("可選", "t-opt"),
}

# ---------- entry constructors ----------

def I(name, tags, where, note="", miss=None, img=None, zh=""):
    return dict(kind="item", name=name, tags=tags, where=where, note=note, miss=miss, img=img, zh=zh)


def B(name, sub, img, map=None, opt=False, reward="", weak="", resist="", gear=None,
      tips=None, note="", spoil=False, true=False, label=None):
    return dict(kind="boss", name=name, sub=sub, img=img, map=map, opt=opt, reward=reward,
                weak=weak, resist=resist, gear=gear or [], tips=tips or [], note=note,
                spoil=spoil, true=true, label=label)


def W(title, body, info=False):
    return dict(kind="banner", title=title, body=body, info=info)


R = '<span class="glint g-red">紅光</span>'
BL = '<span class="glint g-blue">藍光</span>'

# =====================================================================
#  CHAPTER DATA (each list is in play order)
# =====================================================================
CHAPTERS = []

# ---------------------------------------------------------------- 1
CHAPTERS.append(dict(
    id="ch1", num="序章・第一章", title="泣溪谷", en="Prologue & Weeping Creek Valley",
    cover=KG + "Fighting-The-Hunt-1.jpg",
    lead="序章兩場教學戰之後抵達第一個大區域。這裡的 Outpost（前哨站）支線全部會在第二章頭目戰後失效，"
         "而治療師 Yu'er 的藥草要越早交越好。",
    sections=[
        ("序章 Prologue", "兩場劇情教學戰", [
            B("Zuo Shang", "序章教學頭目 · Diverging Paths", KG + "Fighting-Zho-Shang.jpg",
              reward="無（劇情戰）",
              gear=[("提示", "此戰為教學，結果固定，專心熟悉格擋與彈反即可")],
              tips=["近戰連段時，他身後會飛來遠程攻擊——聽音效提示並舉盾格擋",
                    "彈指 = 遠程攻擊要來：先按住格擋，再閃避飛來的巨錘",
                    f"飛劍連段的第 7 擊是 {BL}，在此時彈反",
                    "迴旋劍斬接四連踢，之後是空中遠程與一記可閃避的重擊"]),
            B("The Hunt（第一戰）", "Hunter of the Order · Reckless Pursuit", KG + "Fighting-The-Hunt-1.jpg",
              reward="無（打到半血即過關）",
              gear=[("提示", "只需把他打到一半血量，不必擊殺")],
              tips=["開場五連擊的最後一下可彈反；彈反成功後會出現 Ghostep 提示，連按可白打",
                    f"他跳到空中時，按住格擋擋下四下鎖鏈揮擊，再彈反最後的 {BL} 突刺",
                    "空檔後他的下一擊同樣可以彈反"]),
        ]),
        ("泣溪谷 Weeping Creek Valley", "依遊玩順序", [
            I("Triple Threat", ["tale", "opt"], "The Lady's Rift Bell 旁的雕像，進入即可接取。",
              "此時實力不足以完成，留到遊戲後期（Mirage Estate 之後）回來處理。",
              img=pp(WCV, 3)),
            I("Hunter's Insight", ["acc"], "從 The Lady's Rift Bell 攀上鎖鏈後，前方敵人掉落。", img=pp(WCV, 4)),
            I("Flesh Lily（Yu'er）", ["tale", "true"], "與瀑布旁的 Yu'er 交談自動接取。",
              "這條線與後面的 Apprentice Healer、A Healer's Mercy 一起構成獎盃 The Healer's Legacy。",
              img=pp(WCV, 5)),
            I("Sanguine Twin", ["weapon"], "Yu'er 後方瀑布處的武器架上。", "速度快的雙刀，前期好用。", img=pp(WCV, 6)),
            I("Battle Wraps", ["acc"], "First Meeting Bell 的橋後，拿大劍的敵人掉落。", img=pp(WCV, 8)),
            I("Four Fierce Axes", ["tale"], "Broken Puppet Valley Bell 附近樹旁的書本。", img=pp(WCV, 11)),
            B("Jagged Steel", "The Frenzied Brute · 主線", KG + "Fighting-Jagged-Steel.jpg", map=pp(WCV, 13)[0],
              reward="Jagged Steel（主武器，出血）", weak="毒、雷",
              gear=[("武器", "初始武器即可"), ("提示", "這是彈反 / 完美閃避的教學頭目")],
              tips=[f"看到 {BL} 就彈反，看到 {R} 就閃避——之後所有頭目都遵循這個規則",
                    "完美閃避會觸發 Ghostep，趁機反擊",
                    "打完拿到的 Jagged Steel 出血效果強，可作為整個第一章的主力"]),
            I("Purge the Sect（Brooding Old Archer）", ["tale", "miss"], "Outpost 屋頂上的老弓手。",
              "需要去 Creek Valley Plains 的弓手營地擊敗所有弓手，取得 Broken-String Bow 交給他。",
              miss="第二章最終頭目 Bai Chilian 被擊敗後失效。", img=pp(WCV, 17)),
            I("Sanguine Reach", ["weapon"], "Outpost 鐵匠 Forge 正後方的武器架。",
              "後期可用 Scorching Flames 進行 Soul Tempering。", img=pp(WCV, 18)),
            I("Festering Secrets", ["tale", "miss"], "與 Forge 交談後走向守衛自動接取（Outpost 的鐵鍊封住院子）。",
              "需要 Peng Meng 給的 Dread Axe 斬斷鐵鍊。",
              miss="Bai Chilian 被擊敗後失效。", img=pp(WCV, 19)),
            B("Peng Meng", "The Axemaster · 主線", KG + "Peng-Meng-Boss.jpg", map=pp(WCV, 22)[0],
              reward="Dread Axe（Phantom Edge，可斬鐵鍊、破盾）", weak="毒、出血", resist="火 / 冰 / 雷，極抗水",
              gear=[("武器", "Jagged Steel（出血）"), ("飾品", "Battle Wraps、Hunter's Insight")],
              tips=["大多招式都能格擋或彈反，而且他常常不會接續會打空你 Sha-Chi 的攻擊",
                    f"上撈斧一定接 {BL} 重擊（兩種變化），等光再彈反",
                    "雙手扛斧上肩 → 轉身後有一記可完美彈反的大揮",
                    f"抓取是 {R} Killer Move，一定要閃",
                    "背摔若命中會清空全部 Sha-Chi，務必閃開"]),
            I("Apprentice Healer", ["tale", "miss"], "Outpost Bell 與 Yu'er 交談接取。",
              "收集三種藥草：Blood-Stopper Vine、Congealeaf、Blemish Goldweed（見下方），交給 Yu'er。",
              miss="第二章擊敗 Jing Ye 時自動失敗；另有攻略指出 Yu'er 移往 Crimson Forest 營地後就無法在 Outpost 交，最好一拿齊就交。",
              img=pp(WCV, 25)),
            I("Boulderguard", ["acc", "miss"], "先跟 Old Archer 右邊建築裡、躲在箱子後的人（Petrified Mandate Disciple）反覆對話直到他提到墳墓，"
              "再去 Axemaster's Holding Cell Bell 旁檢查墳墓。",
              "效果：未被破防時受到傷害 -15%。",
              miss="Bai Chilian 被擊敗後此 NPC 會變成敵人，無法再觸發。", img=pp(WCV, 27, "-")),
            I("Blood-Stopper Vine", ["key"], "Focus Pill 寶箱之後、橋下的小溪中。Apprentice Healer 藥草 1/3。",
              img=pp(WCV, "key-item-1")),
            I("Broken-String Bow", ["key"], "Creek Valley Plains Entrance Bell 上坡的弓手營地，打倒所有弓手。", img=pp(WCV, 29)),
            I("Token of Pursuit", ["acc"], "弓手營地附近的寶箱。", img=pp(WCV, 30)),
            I("Feather Bow", ["edge", "miss"], "把 Broken-String Bow 交給 Outpost 的 Brooding Old Archer 修好。",
              miss="Bai Chilian 被擊敗後此支線自動失敗。", img=pp(WCV, 32)),
            B("Hua, Deadly Betrothed", "可選頭目 · Flesh Lily Fields", KG + "Fighting-Hua-Deadly-Betrothed.jpg", map=pp(WCV, 34)[0],
              opt=True, reward="Scarlet Wraithblade（主武器）、Twin Flesh Lilies", weak="火，稍弱雷", resist="冰 / 水，免疫毒與出血",
              gear=[("武器", "火屬性或純物理；Jagged Steel 的出血對她無效"),
                    ("提示", "從 Valley Sha-Chi Tower 1F 後方的木橋滑下去，穿過開口")],
              tips=["地上的花叢會持續傷害，保持移動、不要站在花上",
                    "打贏後拿到的 Scarlet Wraithblade 被多家攻略評為前半段最強武器之一，削 Sha-Chi 極快",
                    "戰鬥場地祭壇旁的 Twin Flesh Lilies 記得撿"]),
            I("Twin Flesh Lilies", ["key", "miss"], "Hua 戰鬥場地的祭壇旁。交給 Yu'er 完成 Flesh Lily。",
              "之後 Pangzhen 的 Blessed Jade Pendant 也需要 Flesh Lily。",
              miss="各攻略說法不一：最晚在 Bai Chilian 之前、或進入 Village of Lu 之前交給 Yu'er。建議拿到就交。",
              img=pp(WCV, "key-item-2")),
            I("A Severed Mindseal（Shadow Warden）", ["tale", "miss"], "Valley Sha-Chi Tower Summit Bell 的 Shadow Warden。",
              "屋頂敵人掉落 Sha-Chi Furnace Inspection Crank → 到塔 1F 熔爐使用，取得 Primal Stone 交給他。",
              miss="第一次交付 Primal Stone 必須在離開泣溪谷前完成，否則失去獎盃 Spectral Blade。",
              img=pp(WCV, 37)),
            I("Primal Stone", ["key"], "用 Inspection Crank 打開 Tower 1F 的熔爐取得。", img=pp(WCV, "key-item-4")),
            B("The Hunt（第二戰）", "Hunter of the Order → Sixfold Scythe · 章節頭目", KG + "The-Hunt-Boss.jpg", map=pp(WCV, 40)[0],
              reward="Hunter's Chain Sickle（Phantom Edge，可鉤索移動）", weak="雷", resist="火 / 毒 / 出血",
              gear=[("武器", "Scarlet Wraithblade（快速削 Sha-Chi）＋ Jagged Steel 交替"),
                    ("Phantom Edge", "Dread Axe"),
                    ("飾品", "Battle Wraps、Hunter's Insight、Token of Pursuit"),
                    ("道具", "Healing Gourd、Focus Pill")],
              tips=["五連斬全部按住格擋，最後一下重擊彈反",
                    f"往側邊跳 → 雙斬突進，看到 {BL} 彈反",
                    "三道範圍斬會生成水龍捲：先避開（血少就先補），再彈反接下來的突進",
                    "空中迴旋在結束前一瞬間彈反；他的攻擊範圍很大，貼身打反而安全"]),
            I("Lingran's Pendant", ["acc"], "用 Chain Sickle 鉤到 The Beginning Bell 附近的寶箱平台。", img=pp(WCV, 41)),
            I("Sha-Chi Tower Base Camp Gate Key", ["key"], "用 Chain Sickle 爬上塔頂取得，打開 Creek Valley Plains Entrance Bell 附近的門。",
              "這條路線通往 Crimson Manor，但莊園要到很後期（取得 Puppet's Tongue）才能攻略。",
              img=pp(WCV, "key-item-5")),
            I("Long Pillar Overlook Bell", ["pillar"], "鎖住的門後、橋前的小屋內。", img=pp(WCV, 42)),
            I("Congealeaf", ["key"], "從 Long Pillar Overlook Bell 過橋、爬鷹架後地上（有敵人）。藥草 2/3。", img=pp(WCV, "key-item-7")),
            B("Gold-Masked One #1", "可選 · 泣溪谷長柱", PG + "gold-masked-one-550x309.jpg", map=pp(WCV, 45)[0],
              opt=True, reward="Counterstrike Bracers（飾品）＋ Bloodline Awakening 進度 1/5",
              gear=[("武器", "Outlaw Warblade（破防關鍵，第二章 Jing Ye 掉落）＋ Jagged Steel"),
                    ("Phantom Edge", "Dread Axe、Hunter's Chain Sickle"),
                    ("飾品", "Shenji's Ring（格擋耗 Sha-Chi 降低）、Resonance Talisman（Sha-Chi 上限）"),
                    ("道具", "Healing Gourd、Simmering Brew")],
              note="攻略普遍建議先別打，拿到 Outlaw Warblade 後再回來。五根長柱是真結局條件之一。",
              tips=["破防後他會短暫無敵——把連段塞在破防窗口內",
                    f"{R}：翻劍跳斬、滑鏟、轉身後突刺、眼睛發紅時的抓取 → 完美閃避",
                    f"{BL}：第五道劍氣後的跳斬、長距離後空翻斬 → 彈反",
                    "等他連段結束再找完美閃避 / 彈反繞到背後；切換武器管理 Sha-Chi"]),
            I("Blemish Goldweed", ["key"], "Weeping Creek Long Pillar 流出的河流盡頭。藥草 3/3。", img=pp(WCV, "key-item-8")),
            I("Medicine Case", ["acc", "miss"], "三種藥草交給 Yu'er 後獲得。",
              miss="Jing Ye（第二章）被擊敗後 Apprentice Healer 失敗，就拿不到。", img=pp(WCV, 47)),
            I("Reflex Device", ["acc"], "用 Inspection Crank 打開 Sha-Chi Tower Base Bell 旁的熔爐。", img=pp(WCV, 51)),
            B("Aberrant Three-Faced Puppet", "可選 · Challenge Rift 神殿廣場", KG + "Aberrant-Three-Faced-Puppet.jpg",
              opt=True, reward="Three-Headed Doll",
              note="第一次來時她非常耐打，攻略一致建議後期再回來。",
              tips=["她會躲進鏡子裡——消失時先閃避",
                    f"從鏡中衝出時是 {R}，完美閃避後反擊"]),
        ]),
    ]))

# ---------------------------------------------------------------- 2
CHAPTERS.append(dict(
    id="ch2", num="第二章", title="赤林", en="Crimson Forest",
    cover=KG + "Fighting-Bai-Chilian.jpg",
    lead="整個遊戲最大的「錯過不再」關卡。章末頭目 Bai Chilian 被擊敗後，Outpost 與盜賊營地的居民全部變成敵人，"
         "所有相關支線、飾品一起失效。另外 Jing Ye 是 Yu'er 藥草任務的死線。",
    sections=[
        ("赤林 Crimson Forest", "依遊玩順序", [
            W("本章重要死線", "<ul><li><b>Jing Ye</b>：擊敗前必須把三種藥草交給 Yu'er（Apprentice Healer / Medicine Case）。</li>"
              "<li><b>Bai Chilian</b>：擊敗後 Purge the Sect、Festering Secrets、Honor Among Thieves、A Healer's Mercy、Silent Wrap、Calming Gourd、Boulderguard、Feather Bow 全部失效。</li></ul>"),
            I("Shieldbreaker Talisman", ["acc"], "斷橋之後、敵人旁的小鷹架上的寶箱。", "對盾牌傷害 +50%，打 Jing Ye 很好用。", img=pp(CF, 4)),
            B("Hua Qianxiao", "The Sword Fanatic · Pangzhen Bridge Overlook", KG + "Fighting-Hua-Qianxiao.jpg", map=pp(CF, 7)[0],
              reward="The Fanatic's Broken Blade（主武器）", weak="稍弱雷", resist="毒 / 水 / 出血",
              gear=[("武器", "Jagged Steel ＋ Sanguine Twin（快攻）"),
                    ("Phantom Edge", "Dread Axe（打斷喝酒）"),
                    ("提示", "附近 Bell 先把武器升到 5 級")],
              tips=["他開始拿葫蘆喝酒 = 準備兩段範圍攻擊 → 用 Dread Axe 打斷（藍光即可）直接打滿硬直",
                    f"側旋橫掃是 {R}，完美閃避",
                    "他的硬直條恢復很快，要持續施壓；倒地後他會擲劍，可能致命——一定要閃",
                    "地板霹靂舞旋轉是大範圍攻擊，往外閃"]),
            I("Quick Hand Zhang（牢籠中的人）", ["tale", "miss", "true"], "Trail of Cages Bell 附近被關在籠子裡的 Quick Hand Zhang，用附近機關放他出來。",
              "他之後會在各地開藏身處（Quick Hand's Request），是真結局條件之一。同一個平台下層有 Cavalrybane 飾品。",
              miss="必須在本章內救出，否則失去 Quick Hand Pendant 與整條真結局線。", img=pp(CF, 13)),
            I("Cavalrybane", ["acc"], "救 Zhang 的那個鷹架平台下層。", "對騎乘敵人增傷，打 Jing Ye 第一階段好用。", img=pp(CF, 13)),
            I("Crimson Forest Tunnel Crank", ["key"], "Outlaw Trap 前方洞穴內。用來進入地下通道找 Jing Ye。", img=pp(CF, "key-item-1")),
            I("Honor Among Thieves", ["tale", "miss"], "擊敗坡上營火旁的敵人後接取。",
              "把 Nimble Thief 的血書交給 Gentle Thief → 回答三個問題 → Silent Wrap。",
              miss="Bai Chilian 被擊敗後失效。", img=pp(CF, 16)),
            W("打 Jing Ye 之前", "Apprentice Healer 的三種藥草交了嗎？擊敗 Jing Ye 會讓這條支線與 Medicine Case 永久失敗。"),
            B("Jing Ye", "The Outlaw · 主線", KG + "Fighting-Jing-Ye.jpg", map=pp(CF, 21)[0],
              reward="Outlaw Warblade（主武器，抗打斷蓄力）", weak="稍弱冰、雷", resist="極抗火 / 毒 / 出血",
              gear=[("武器", "Scarlet Wraithblade（削 Sha-Chi）＋ Jagged Steel 交替"),
                    ("Phantom Edge", "Dread Axe（破盾、打掉藍條），有射程的破盾武器更好"),
                    ("飾品", "Cavalrybane（騎乘增傷）、Shieldbreaker Talisman（對盾 +50%）")],
              tips=["第一階段騎馬：開場跳擊＋三連擊一定要完美閃避，被打到很痛；其餘多數攻擊可以格擋",
                    "左手袋子丟出的紅色飛彈：格擋與閃避混用，最後幾發格擋仍會受傷",
                    "約 1/3 血後換持盾：用 Dread Axe 破盾，注意盾擊造成的出血累積",
                    f"出現煙霧 = 遠跳，落地後必接一記快速 {BL} 斬擊；畫面變灰時預判彈反"]),
            I("Secrets of the Baishan Sect（Lanlan）", ["tale", "miss", "true"], "巨大木橋上與 Lanlan 交談接取。",
              "後續在第五章 Mandate Encampment 繼續（獎盃 The Last of Baishan）。",
              miss="必須在 Bai Chilian 之前接取。", img=pp(CF, 23)),
            I("Silent Wrap", ["acc", "miss"], "Gentle Thief 問你三個問題（Honor Among Thieves 獎勵）。",
              miss="Bai Chilian 被擊敗後失效。", img=pp(CF, 25)),
            I("A Healer's Mercy", ["tale", "miss"], "Thieves' Camp Bell 附近的 Yu'er。治療四名受傷盜賊：Outlaw Trap 附近洞穴兩名、"
              "Cliffside Lodge 地窖（用 Cellar Crank）一名、Thieves' Camp 地牢一名。",
              miss="Bai Chilian 被擊敗後失效（The Healer's Legacy 獎盃的一部分）。", img=pp(CF, 26)),
            I("Quick Hand Pendant", ["acc"], "Thieves' Camp Bell 旁牆上的小洞穴（需先救出 Zhang）。", "單手武器傷害 +10%。", img=pp(CF, 27)),
            I("Quick Hand's Request / The Wily Hare's Three Dens", ["tale", "true"], "與 Quick Hand Zhang 交談。",
              "收集指定寶物交給他，各地藏身處會給不同獎勵（本區是 Flying Dagger）。", img=pp(CF, 28)),
            I("Crimson Forest Cellar Crank", ["key"], "Cliffside Lodge Bell 爬梯子、穿過毒氣房間到陽台。", img=pp(CF, "key-item-3")),
            I("Thieves' Camp Dungeon Key", ["key"], "跳到下方岩石平台上。", img=pp(CF, "key-item-4")),
            I("Calming Gourd", ["acc", "miss"], "四名盜賊全部救治後，回 Thieves' Camp Bell 找 Yu'er。",
              miss="Bai Chilian 被擊敗後失效。", img=pp(CF, 41)),
            I("Flying Dagger", ["edge"], "收集三件寶物後交給 Quick Hand Zhang。", "遠程牽制用，打 Iron Fever 很實用。", img=pp(CF, 42)),
            B("Stone Hand Iron Fever", "主線 · Mirrorwood Entrance 附近", KG + "Fighting-Stone-Hand-Iron-Fever.jpg", map=pp(CF, 45)[0],
              reward="Iron Gauntlets（Phantom Edge，破盾）", weak="稍弱冰", resist="火 / 雷，極抗水",
              gear=[("武器", "Outlaw Warblade（蓄力硬吃連段）＋ Jagged Steel（出血、Rampage）"),
                    ("Phantom Edge", "Flying Dagger（遠距離風箏）"),
                    ("提示", "資源夠的話武器升到 10 級")],
              tips=["純近戰、沒有突進技，可以拉開距離用 Flying Dagger 消耗",
                    f"空中翻身攻擊最後是無法格擋的 {R}——他停手開始升空時就閃",
                    "他閒置時不要用蓄力攻擊，他會擋掉一部分並大量削你的 Sha-Chi"]),
            B("Gold-Masked One #2", "可選 · Mirrorwood 長柱", None, map=pp(CF, 49)[0],
              opt=True, reward="Miraculous Scabbard（飾品）＋ Bloodline Awakening 2/5",
              gear=[("武器", "Outlaw Warblade（破防）"), ("飾品", "Shenji's Ring、Resonance Talisman")],
              note="與龍雕像互動開始。難度高，可以之後再來。",
              tips=["新增兩招會讓畫面變黑白——一定要閃避，格擋會吃光所有 Sha-Chi",
                    f"蹲下發紅光 = 約 1 秒後衝刺，他一動就閃",
                    "其餘招式與第一戰相同"]),
            W("最後確認（Bai Chilian 之前）", "<ul><li>Purge the Sect / Feather Bow（交 Broken-String Bow）</li><li>Festering Secrets（用 Dread Axe 斬鐵鍊）</li>"
              "<li>Honor Among Thieves / Silent Wrap</li><li>A Healer's Mercy / Calming Gourd</li><li>Boulderguard（墳墓）</li>"
              "<li>Secrets of the Baishan Sect 已接取</li><li>Quick Hand Zhang 已救出</li></ul>"),
            B("Bai Chilian", "Lady of the Twin Serpents · 章節頭目（兩階段）", KG + "Fighting-Bai-Chilian.jpg", map=pp(CF, 63)[0],
              reward="White Serpent & Crimson Viper（主武器）、Resonance Talisman（飾品）", weak="火、冰、出血", resist="雷",
              gear=[("武器", "Outlaw Warblade：她消失時蓄力，她出現時放出"),
                    ("飾品", "Shenji's Ring（大量格擋時省 Sha-Chi）")],
              tips=["至今最快的頭目，會在場上瞬移；空中攻擊時保持鎖定（她飛很高時可暫時解鎖鏡頭）",
                    "側翻飛刀 → 格擋；背後兩下可格擋，之後有很長的反擊窗口",
                    "她消失後會偷襲削 Sha-Chi，接近時閃避；三連擊最後的突刺可閃",
                    f"二階段：五連揮 → 五連蛇擊 → {BL} 突刺，彈反後貼身打她倒地空檔",
                    f"旋轉五連擊全部格擋，最後高位一擊看 {R} 閃避；起飛時離開風圈、閃落地再完美閃避反擊"]),
        ]),
    ]))

# ---------------------------------------------------------------- 3
CHAPTERS.append(dict(
    id="ch3", num="第三章", title="盧村", en="Village of Lu",
    cover=KG + "Fighting-Mu-Xiaokui.jpg",
    lead="本章有兩個大陷阱：Young Mistress 的五條髮帶必須在搭電梯去章末頭目前收齊；章末頭目打完後，碼頭上的 Wild Oriole Sword 不撿就永遠拿不到。",
    sections=[
        ("盧村 Village of Lu", "依遊玩順序", [
            I("Jewel's Knot", ["acc"], "Jewel 正後方的寶箱。", img=pp(VL, 2)),
            I("The Journey Home（Old Man Gen）", ["tale", "miss"], "Old Man Gen's Hideout Bell 附近與他交談。",
              "後續會拿到 Old Man Gen's Brass Key；完成才會在第六章 Meigu Lake 出現 War Wagon（Phantom Edge）與獎盃 Together Till the End。",
              miss="他提出請求時立刻答應。第一步最晚要在第四章 Town of Death 結束（Pangzhen 後巷）前完成。",
              img=pp(VL, 7)),
            I("Young Master Lan", ["tale", "miss"], "Young Master Lan's Hideout Bell 附近與他交談。",
              miss="第一個目標必須在進入 Pangzhen 之前完成（獎盃 A Wanderer's Honor）。", img=pp(VL, 9)),
            B("Zhuo Bi", "The Gatekeeper · 主線", KG + "Fighting-Zhuo-Bi.jpg", map=pp(VL, 10)[0],
              reward="Bastion（Phantom Edge，可擋箭）", weak="雷，稍弱冰", resist="毒，極抗火 / 水，免疫出血",
              gear=[("武器", "Outlaw Warblade 或 White Serpent & Crimson Viper"),
                    ("Phantom Edge", "Dread Axe 或 Iron Gauntlets（破盾）"),
                    ("飾品", "Shenji's Ring ＋ Resonance Talisman（一直擋也不會被破防）、Hunter's Insight"),
                    ("道具", "Healing Gourd、Simmering Brew")],
              tips=["巨盾必須先打破才能讓他硬直；大部分傷害來自處決，一次約 1/4 血",
                    "他從硬直恢復時畫面變灰 → 滑行盾擊（削 Sha-Chi），閃避或用武技打斷",
                    "盾砸連段：前幾下格擋，最後一下完美彈反",
                    "後跳＋盾砸會召喚地刺，兩下都要閃；他攻擊後倒地時趁機打"]),
            I("Young Mistress（髮帶 1/5）", ["tale", "miss"], "Zhuo Bi 戰場後方大門外，綁在樹上的髮帶。",
              "其餘四條：有頂橋（Covered Bridge）柱子、地下路線（Yuzan 附近）的橋柱、以及通往章末頭目電梯前的兩處。",
              miss="必須在搭電梯前往章末頭目前收齊五條，否則頭目沒有第三階段，失去 Fiend Saws、Fist Fragment: Core 等獎勵。",
              img=pp(VL, 13)),
            I("A Puppet's Wooden Heart", ["tale"], "Well of the Three Puppets 的 Songstress Puppet。",
              "要在 Temple of Blue Fireflies 收集六朵 Firefly 記憶之花——收齊後才會出現隱藏頭目 Dusk。", img=pp(VL, 19)),
            I("Mother's Talisman", ["acc"], "樓梯頂的建築裡，擊敗內部敵人後取得。", img=pp(VL, 22)),
            B("Master Bi Yuan", "of the Tianxuan Sect · 主線", KG + "Fighting-Master-Bi-Yuan.jpg", map=pp(VL, 33)[0],
              reward="Tianxuan Bronze Sword（主武器）、Sha-Chi Amber", weak="火，稍弱毒", resist="雷",
              gear=[("武器", "火屬性武器 / 附魔"), ("提示", "貼身打，離太遠他會一直放飛劍")],
              tips=["很多招式會打破你的 Sha-Chi：先閃避，再彈反接下來的追擊",
                    "保持近距離，避免遠程劍氣"]),
            I("Livingwood Talisman", ["acc"], "從庭院跳下後，下一個小區域的房子裡。", img=pp(VL, 39)),
            I("Arrowward", ["acc", "miss"], "把 Thief's Manual 交給門邊的 Wounded Thief。",
              "Thief's Manual 在 Crimson Forest 的 Zhang 藏身處入口附近，需要本章拿到的 Bastion 才能取得——拿到 Bastion 後馬上回去。",
              miss="這名盜賊會隨劇情推進死亡，越早交越好。", img=pp(VL, 41)),
            B("Master Bi Hai", "of Kuye Temple · 主線", PG + "bi-yuan-boss-550x309.jpg", map=pp(VL, 42)[0],
              reward="Kuye Temple Prayer Beads（Phantom Edge）、Arrowward 相關", weak="火，稍弱毒", resist="雷",
              gear=[("Phantom Edge", "破盾類（Dread Axe / Iron Gauntlets）——破金鐘必備")],
              tips=[f"快速連段之後接 {R}",
                    "他會罩上金鐘並召喚三個銅人：擊倒銅人才能破鐘，需要破盾武器"]),
            B("Acolyte Yanru", "可選 · Terraces 下方的稻草人", None, map=pp(VL, 48)[0], opt=True,
              reward="Yanru's Blazing Mask（Acolyte 面具 1/4）", weak="冰、水", resist="毒，免疫火",
              note="四個 Acolyte 面具是 Meigu Lake 隱藏區與真結局的必要條件。",
              tips=["火系敵人：火球、跳擊、分身雨、火圈、袖火", "帶冰或水屬性武器"], true=True),
            I("Agarwood Prayer Beads", ["acc", "miss"], "與 Stately Monk 交談，選「Do not believe」，再把 Prayer Beads 交給他。",
              "Prayer Beads 來自泣溪谷 Outpost 商店旁的和尚（之後的回訪）。",
              miss="選「Believe」他會變成石頭，飾品永久消失。", img=pp(VL, 53)),
            I("Dahuang", ["tale"], "Survivors' Courtyard 後建築裡床上的 NPC。", img=pp(VL, 55)),
            I("Fine Thread", ["acc"], "收集三件寶物後，在 Zhang's Hideout（Village of Lu）交給 Quick Hand Zhang。", img=pp(VL, 58)),
            I("A Puppet's Wooden Heart（飾品）", ["acc"], "完成前一目標後回 Temple of Blue Fireflies Bell 找 Puppet Songstress。", img=pp(VL, 59)),
            B("Dusk", "The Puppeteer · 隱藏頭目", KG + "Fighting-Dusk.jpg", map=pp(VL, 61)[0], opt=True,
              reward="Puppeteer's Bell、Illusory Pipa Head（真結局用的琵琶零件）", weak="無特別弱點",
              note="收齊六朵 Firefly 記憶之花後，才會在 Broken Puppet Pit Entrance 後的峽谷（漁夫旁）出現。",
              tips=["先處理召喚物，再格擋他的射擊", "二階段他會分裂成兩個"], true=True),
            B("Yuzan", "No. 3 Musician Puppet · 井底主線", KG + "Fighting-Yuzan.jpg", map=pp(VL, 65)[0],
              reward="Heartrend Pipa（Phantom Edge）",
              tips=[f"樂器發出 {R} 時閃避",
                    "白色光球可以彈反，把藍色彈幕打回去",
                    "她消失到場地中央時，退到外圈並閃避大型灰色光球"]),
            I("Cui", ["tale"], "Puppet Testing Grounds Bell 附近哭泣的小孩人偶。",
              "要在最終章 The Crusher and the Saw 之前完成，才能拿到 Baishan Headband。", img=pp(VL, 67)),
            I("Old Man Gen's Brass Key", ["key"], "從 Puppet Testing Grounds Bell 打開走私隧道後，回去接受 Old Man Gen 的下一個請求。",
              img=pp(VL, "key-item-1")),
            I("Remnant Spark Cage", ["acc"], "Smuggler's Treasure Cellar Bell 後的地窖寶箱（Tunnel Cage Key → Cellar Key）。", img=pp(VL, 72)),
            W("搭電梯前往章末頭目之前", "Young Mistress 五條髮帶收齊了嗎？否則頭目第三階段不會出現，Fiend Saws 等獎勵直接錯過。"),
            B("Mu Xiaokui", "Young Mistress of the Order · 章節頭目（三階段）", KG + "Fighting-Mu-Xiaokui.jpg", map=pp(VL, 68)[0],
              reward="Wild Oriole Sword；第三階段：Fiend Saws、Fist Fragment: Core、Puppet No. 44's Eye",
              gear=[("Phantom Edge", "破盾類（第三階段的護衛要破防）")],
              tips=["雙遠程斬擊接飛行物追擊：完美閃避後有很長的反擊窗口",
                    "削 Sha-Chi 的突刺後會接劍舞＋旋轉投擲；高跳先閃跳擊，再閃接下來的突刺",
                    f"二階段：{R} 快速衝刺開啟無法打斷的連段，完美閃避；注意紫色裂縫生成的幻影",
                    "第三階段（需完成 Young Mistress）：Iron Fiend 與 Jade Dancer 2 打 1，盡量讓兩人都在視野內、分開處理",
                    f"Iron Fiend 的高抬膝與拍手後接 {R}"]),
            I("Wild Oriole Sword", ["weapon", "miss"], "擊敗章末頭目後，前方碼頭上。",
              miss="離開碼頭後電梯會壞掉，無法再回來。旁邊樹下寶箱的 Sha-Chi Amber Fragment 也一起拿。",
              img=pp(VL, 69)),
        ]),
    ]))

# ---------------------------------------------------------------- 4
CHAPTERS.append(dict(
    id="ch4", num="第四章", title="龐鎮", en="Pangzhen",
    cover=KG + "Fighting-Wu-Xuan.jpg",
    lead="大型城鎮，支線密度最高。重點：打 Flame 前一定要先打可選頭目 You Loong 拿到 You Loong's Deluge；"
         "從碼頭出發前往 Meigu Lake 前先確認 Old Man Gen 的支線進度。",
    sections=[
        ("龐鎮 Pangzhen", "依遊玩順序", [
            I("Flameward", ["acc"], "South Gate Bridge Bell 旁上樓梯的小陽台寶箱。", "火焰傷害與燃燒累積 -50%，下一個頭目 Blaze 必備。", img=pp(PZ, 6)),
            B("Blaze", "Shadow Warden Captain · 主線（兩階段）", KG + "Fighting-Blaze.jpg", map=pp(PZ, 7)[0],
              reward="Fire Meteor（Phantom Edge）、Soulrend Storeroom Key", weak="—",
              gear=[("飾品", "Flameward（剛剛那個寶箱）")],
              tips=["側身旋轉六連鎖鏈 → 按住格擋，並在演出提示時閃避跳擊，可造成大硬直",
                    "鎖鏈連段後的地面重擊是範圍攻擊，閃開；與鎖鏈保持距離",
                    "二階段吐息後會跳撲成一擊抓取——閃避突進；頭頂鎖鏈形成火圈時跳過邊緣",
                    "小技巧：他會召喚兩隻小兵，打其中一隻直到出現處決提示，處決會同時秒殺兩隻（擊殺周圍敵人也能回血）"]),
            I("Crimson Flesh Lily", ["key"], "Blaze 戰鬥後正前方。", img=pp(PZ, "key-item-1")),
            I("Crimson Resolve", ["acc"], "Young Master Lan 交給你 Lan Manor Key 後，進入 Lan Manor。", img=pp(PZ, 15)),
            B("Cavalrybane", "Elite Shadow Warden · 主線", KG + "Fighting-Cavalrybane.jpg", map=pp(PZ, 18)[0],
              reward="Armybreaker（主武器）",
              tips=[f"空中旋轉之後的 {BL} 彈反", "他衝鋒時先格擋，再閃避接著的踢擊"]),
            I("The Sword and the Way", ["tale"], "Cavalrybane 戰場後方建築下的酒館，水邊的 Daoist Bi Di。", img=pp(PZ, 21)),
            I("The Undying Heroic Spirit", ["tale", "miss"], "Myst's Tavern Bell 後大房間的 Purple-Robed \"Wolf\" Leader。",
              "要找到六位 Mandate 大師的英靈。",
              miss="每位大師跪下時要立刻處決；等約 10 秒他會變身，失敗三次整條支線失敗。", img=pp(PZ, 23)),
            I("The Star Performer", ["tale"], "Myst's Tavern 的 Leading Opera Actress。完成後換到 Dance Fan。", img=pp(PZ, 24)),
            I("The Cube", ["tale"], "Myst's Tavern 的漁夫（Fisherman），後續在 Meigu Lake 收集碎片。", img=pp(PZ, 25)),
            I("Manor Medicine Pot", ["acc"], "Huang Manor（鑰匙找 Myst's Tavern 的 Shopkeeper Niu）內四個碎片：Chain、Handle、Body、Lid。", img=pp(PZ, 28)),
            I("A Brother Once More", ["tale"], "與 Manor Medicine Pot 同一個房間。", img=pp(PZ, 29)),
            I("Dance Fan", ["acc"], "取得 Tattered Dance Fan 後交給 Myst's Tavern 的 Leading Opera Actress。", img=pp(PZ, 31)),
            B("Wu Xuan", "The Fallen General · 主線（兩階段）", KG + "Fighting-Wu-Xuan.jpg", map=pp(PZ, 35)[0],
              reward="Wolfjaw（Phantom Edge，優秀的破盾武器）",
              gear=[("武器", "高破防（Guard Break）武器與招式"), ("飾品", "增加破防值的飾品"),
                    ("Phantom Edge", "破盾類")],
              tips=["他的 Guard 條很長，必須打破才能處決；完美彈反削得最快",
                    f"{BL} 收尾：鏟子最後一揮、磨錘後的重掃、連續重砸的最後一擊、頭上轉錘",
                    f"兩招不可擋：四連段最後一下、近身揮臂抓取（{R} 閃避）",
                    f"二階段紫焰加傷並追加範圍與追蹤彈；紫爆＋旋風揮最後是 {BL}"]),
            I("Congeal Talisman", ["acc"], "Blackstone 掉落點後的巷子盡頭。", img=pp(PZ, 43)),
            B("Gu Wanyue", "The Wailing Wraith · 主線", PG + "mu-xuan-boss-550x309.jpg", map=pp(PZ, "key-item-9")[0],
              reward="Fanatic's Fragment: Fixation（關鍵道具）",
              tips=["她很難追蹤，全程保持鎖定",
                    f"發出紫光時射出的投射物是 {BL}，彈反",
                    "之後場地變暗：持續格擋並打破她的防禦"]),
            I("Mandate Encampment Outer Gate Key", ["key"], "Gu Wanyue 的井後、棺材旁。",
              "→ 第五章 Mandate Encampment（可選，但真結局必要）就此開放，可以現在去或稍後再去。", img=pp(PZ, 50)),
            B("Xie Qiudong", "The Divine Healer · 主線", PG + "healer-boss-550x309.jpg",
              reward="Everflow（藥品）",
              tips=["他會治療被紅線連起來的敵人——先殺掉連線的人",
                    f"單手舉起並停頓 = {R} 要來了",
                    "清完連線者後集中打本體"]),
            I("Thunderward", ["acc"], "Green Serpent House Bell 左側建築盡頭的寶箱。雷電減傷。", img=pp(PZ, 60)),
            W("Serpent Houses 注意", "Green Serpent House 的門打開前，先把各 Serpent House 的收集品拿齊（PBZ Codex 標註為錯過點）。", info=True),
            B("You Loong", "Leader of the Blackwater Crew · 可選（但打 Flame 前必打）", KG + "You-Loong.jpg", map=pp(PZ, 63)[0], opt=True,
              reward="You Loong's Deluge（Phantom Edge，水——可熄滅 Flame 的火焰）",
              tips=["注意水下的氣泡位置",
                    f"三叉戟旋轉後接 {R}",
                    "噴水的紅光攻擊：閃開，或攻擊他來打斷"]),
            I("Kin Against Kin", ["tale"], "從 Lion Dance Hall Bell 用鉤索到橋上再往左。", img=pp(PZ, 66)),
            B("Chang Hong", "The Thunder Spear · 主線（第二階段騎馬）", KG + "Fighting-Chang-Hong.jpg", map=pp(PZ, 69)[0],
              reward="Thunder Spear（Phantom Edge）、Heavy Lion Hall Gate Key",
              tips=["劍掃之後地面會放電，閃開", "旋轉跳躍時完美閃避", "第二階段騎馬：馬抬起前蹄時完美閃避"]),
            I("Blessed Jade Pendant", ["acc"], "Chang Hong 戰場前方的建築，救出老人。需要泣溪谷的 Flesh Lily。", img=pp(PZ, 70)),
            B("Flame", "The Mask-Bound Lion Dance Grandmaster · 主線（兩階段）", KG + "Fighting-Flame.jpg", map=pp(PZ, "key-item-12")[0],
              reward="Dormant Flaming Mane（由 Lei Dang 在 Jingyang Hall 修復成 Flaming Mane）", weak="水",
              gear=[("Phantom Edge", "You Loong's Deluge（熄滅火焰 Buff，移除爆炸並封印部分招式）"),
                    ("飾品", "Flameward")],
              tips=["四連踩第四下可彈反；挑釁後的砸地可彈反；旋風砸地不可擋要閃；頰刃旋轉第二下可彈反",
                    "火球閃藍光：格擋反彈回去造成大量 Sha-Chi 傷害",
                    f"二階段在柱子上：快速紅光落下不可擋要閃；較慢的 {BL} 跳躍可以精準格擋彈開",
                    "舞獅階段：撿綠色錦囊提高 Sha-Chi 傷害，削空他的 Sha-Chi 讓他暈眩；處決最後一名弟子進入該階段"]),
            I("Goldblaze", ["edge"], "在 Zhang's Hideout（Pangzhen）與 Quick Hand Zhang 交談。", img=pp(PZ, 78)),
            I("Flaming Mane", ["edge"], "Jingyang Hall Bell 後的門內，Lei Dang 幫你修復。可燒掉樹枝路障。", img=pp(PZ, 79)),
            I("Formless Divine Mirror", ["acc"], "Black Hill Pavilion Bell 附近。", img=pp(PZ, 81)),
            I("A Mother's Heart", ["tale"], "從 Backstreet Cellar Crank 平台順梯子下去。", img=pp(PZ, 82)),
            B("Acolyte Lei Ting", "可選 · Old Man Gen's House 下方稻草人", None, map=pp(PZ, 88)[0], opt=True,
              reward="Leiting's Thunder Mask（Acolyte 面具 2/4）", true=True,
              note="Flame 之後即可挑戰。", tips=["雷系敵人，帶 Thunderward 減傷"]),
            B("Soulclaimer", "Elite Shadow Warden · 主線", KG + "Fighting-Soulclaimer.jpg", map=pp(PZ, 91)[0],
              reward="Parting Hooks（主武器）",
              tips=[f"他跑開再旋轉衝向你之後，彈反 {BL}"]),
            W("搭船離開 Pangzhen 之前", "<ul><li>The Journey Home 第一步必須已完成，否則第六章 War Wagon 與 Old Man Gen 劇情會錯過。</li>"
              "<li>Young Master Lan 第一目標應已完成。</li><li>建議先完成第五章 Mandate Encampment。</li></ul>"),
        ]),
    ]))

# ---------------------------------------------------------------- 5
CHAPTERS.append(dict(
    id="ch5", num="第五章", title="天命營", en="Mandate Encampment",
    cover=PG + "chief-disciple-550x309.jpg",
    lead="可選區域（Pangzhen 拿到 Outer Gate Key 後即可進入），但真結局必要。兩大陷阱：不要殺掉屋頂上的 Red；"
         "打 Yubi 之前先在花田檢查屍體。",
    sections=[
        ("天命營 Mandate Encampment", "依遊玩順序", [
            I("Guardian Idol Fragment: Head / Arm", ["key"], "Head：跳回之前的樓梯，巨大雕像頭旁；Arm：過橋後跳到右邊另一座橋上的小神龕。",
              "四個碎片合成 Guardian Idol 飾品。", img=pp(ME, "key-item-1")),
            I("Mandate Valley Gate Key", ["key"], "爬上巨大梯子後，弓手旁的地上。", img=pp(ME, "key-item-3")),
            B("Corpse-Eating Xue", "可選 · 上鎖的門後", PG + "corpse-eater-550x309.jpg", opt=True,
              reward="開啟支線 Xue, Admirer of Heroes",
              tips=["先清小怪", "揮刃快攻全部格擋"]),
            I("Xue, Admirer of Heroes", ["tale"], "擊敗 Corpse-Eating Xue 後接取，收集三件道具。",
              "完成後回 Pangzhen 找 Child of Insight 換 Sha-Chi Headscarf。", img=pp(ME, 11)),
            B("Wan Jun", "The Coppermaul · 可選", PG + "Untitled-Design-14-550x309.jpg", map=pp(ME, 21)[0], opt=True,
              reward="Bashpole（Phantom Edge，可打破脆弱地板）",
              tips=["他屁股著地後先閃，然後趁他躺著時攻擊（即使沒破防）",
                    f"畫面充滿沙塵 = {R}，閃避", "沿地面推進的錘擊要閃"]),
            I("Daughter of the Dark Sect", ["tale", "miss"], "Dovecote Bell 附近的女子。",
              "屋頂上會遇到 Red, the Mysterious Swordswoman——<b>不要擊敗她，脫離戰鬥即可</b>。",
              miss="殺了她 = 支線結束，且她不會參加 Seven-Stars 戰，掉落的記憶之花與 Twin Fish Pendant 永久錯過。",
              img=pp(ME, 26)),
            B("Red", "The Mysterious Swordswoman · 屋頂（不要殺）", PG + "Untitled-Design-15-1-550x309.jpg", opt=True,
              reward="無——饒過她才有後續",
              note="這一戰的正確做法是脫離戰鬥。之後她會在 Seven-Stars 戰中登場，並在最終戰前再度出現。",
              tips=["空間很小，注意她的尖塔跳躍", f"絲線抓取後接 {R}"]),
            B("Chief Disciple of the Seven-Stars", "可選（兩階段，含六名弟子）", PG + "chief-disciple-550x309.jpg", map=pp(ME, 31)[0], opt=True,
              reward="Swordsman's Summon（Phantom Edge）、Training Grounds Key",
              tips=["先殺六名弟子",
                    f"二階段 Sword of Despair：衝刺後的 {BL} 彈反；三連揮的第三下是 {BL}",
                    "天上飛來的投射物在接近時閃避"]),
            I("Memory Flower & Twin Fish Pendant", ["acc", "miss"], "Chief Disciple 與 Red 戰鬥的場地。",
              miss="只有之前沒殺 Red，她才會參戰並掉落。", img=pp(ME, 32)),
            I("Guardian Idol Fragment: Torso", ["key"], "Road to the Training Grounds Bell 往下跳，沿路右轉進左邊建築。", img=pp(ME, "key-item-5")),
            I("Nameless Thumb Ring", ["acc"], "同一棟建築樓上的寶箱。", img=pp(ME, 36)),
            B("Wu Lengshuang", "The Soft Sword · 可選", None, map=pp(ME, 42)[0], opt=True,
              reward="Soft Snake Sword（主武器）、Blackstone Fragment",
              tips=["攻略站尚未公開詳細打法；按 紅光閃 / 藍光彈 的基本原則應對"]),
            I("Guardian Idol", ["acc"], "Wu Lengshuang 戰場樹旁的 Leg 碎片，四片合成。", img=pp(ME, 44)),
            I("Secrets of the Baishan Sect（花田屍體）", ["tale", "miss", "true"], "上樓梯後，在花田中檢查屍體。",
              miss="一定要在擊敗 Training Grounds 盡頭的頭目（Yubi）之前檢查，且要在「Defeat Bi Taotao's puppet form」目標出現後才擊殺 Yubi，否則支線失敗、拿不到 Broken Vessel。",
              img=(PP + "mandate-encampment-saishan-sect-objective-1-1.jpg", PP + "mandate-encampment-saishan-sect-objective-1-2.jpg")),
            B("Yubi", "No. 21 Swordfighter Puppet · 區域頭目", PG + "no.21-boss-550x309.jpg", map=pp(ME, 50)[0], opt=True,
              reward="Baishan Stormswords（主武器，後半段很強）、Broken Vessel（飾品）、Illusory Pipa 零件",
              tips=[f"帶電旋轉之後接 {R}", "她跳到空中或屋頂後，落下時完美閃避"]),
            I("Illusory Pipa Backplate", ["key", "true"], "Yubi 戰場內的建築。琵琶零件，真結局需要。", img=pp(ME, "key-item-6")),
            W("回 Pangzhen 收尾", "擊敗 Chief Disciple 後回 Myst's Tavern 找 Purple-Robed \"Wolf\" Leader 拿 Shattered \"Heroes Courage\"；"
              "Xue 的三件道具交給 Child of Insight 換 Sha-Chi Headscarf；Marketplace Bell 的 Don't Forget Me 支線。", info=True),
            I("Sha-Chi Headscarf", ["acc"], "Pangzhen Pavilion of Knowledge Crossroads Bell 右邊建築頂樓的 Child of Insight（需 Xue 的三件道具）。", img=pp(PZ, 97)),
            I("Don't Forget Me", ["tale"], "Pangzhen Marketplace Bell 後左邊建築，解除屏障後頂樓的女孩。", img=pp(PZ, 99)),
            I("Auspicious Lion Fireball", ["acc"], "Pangzhen Sealed Lion Bell 上坡，解除屏障後樹旁。", img=pp(PZ, 101)),
        ]),
    ]))

# ---------------------------------------------------------------- 6
CHAPTERS.append(dict(
    id="ch6", num="第六章", title="梅姑湖", en="Meigu Lake（第一次造訪）",
    cover=PG + "zither-maiden-550x309.jpg",
    lead="開船探索的湖區。Zhu Yuan 是真結局必打；War Wagon 取決於第三章 The Journey Home。"
         "四個 Acolyte 面具收齊後才能進入第二次造訪的隱藏區域（見第七章頁面）。",
    sections=[
        ("梅姑湖 Meigu Lake", "依遊玩順序", [
            I("Battleforged", ["acc"], "沿碼頭往左、上坡、左邊建築爬梯子的寶箱。", img=pp(ML, 1)),
            B("Zhu Yuan", "The Searing Blade · 可選（真結局必要）", PG + "Untitled-Design-17-550x309.jpg", map=pp(ML, "key-item-1")[0],
              opt=True, true=True, reward="Scorching Flames（Sanguine Reach 的 Soul Tempering 素材）",
              note="用會爆炸的敵人炸開籠子，搭電梯到 Sha-Chi Tower 底部。必須在 The Last Chance 鐘之前擊敗。",
              gear=[("飾品", "Flameward（火傷減半）")],
              tips=["全身發橘光 = 往遠處閃，或用破防技打斷",
                    "旋轉會在地面送出火焰，閃開",
                    f"之後的跳擊是 {R}——等他真的落到你身上再閃"]),
            B("Yan Qiansui", "The Zither Maiden · 可選", PG + "zither-maiden-550x309.jpg", map=pp(ML, 18)[0], opt=True, true=True,
              reward="Illusory Pipa Strings（琵琶零件）、Fanatic's Fragment: Attachment",
              note="Allure of Vanity：坐船在 Meigu Songhouse 周圍收集六朵 Yan'er 記憶之花後，在 Meigu Songhouse Dock 出現。",
              tips=[f"{BL} 光球彈反、{R} 光球閃避、大白球直接躲開",
                    "彩色光球消失後常常接紅光攻擊"]),
            B("Grief-Stricken Jin", "主線 · Village of Lu Shallows Dock（群戰）", PG + "grief-stricken-jin-550x309.jpg",
              reward="Embroidered Shoes（Scarlet Wraithblade 的 Soul Tempering 素材）",
              tips=["先清較弱的敵人，最後才打 Jin"]),
            I("Rouge Box", ["acc"], "擊敗 Grief-Stricken Jin 後的碼頭上。", img=pp(ML, 22)),
            I("Deathlock", ["acc"], "燒掉右邊的樹枝，把 Preservation Jar 放到祭壇上。", img=pp(ML, 36)),
            B("Acolyte Guhe", "可選 · Meigu Village East Dock 稻草人", None, map=pp(ML, 37)[0], opt=True, true=True,
              reward="Guhe's Venom Mask（Acolyte 面具 3/4）", tips=["毒系敵人，帶 Venom Pouch 之類的毒抗飾品"]),
            B("You Loong（狂暴）", "The Frenzied Blackwater Crew Leader · 可選", PG + "you-loong-2-550x309.jpg", map=pp(ML, 40)[0], opt=True,
              reward="Loong Trident（Phantom Edge）、High-Power Pump（Deluge 的 Soul Tempering 素材）",
              note="湖中島嶼 Blackwater Crew Dock。",
              tips=[f"開場就是 {R}", "速度更快，其餘與 Pangzhen 第一戰相同"]),
            I("Venom Pouch", ["acc"], "沿海岸往右、經過 Lake Banyan 挑戰點，敵人旁地上。", img=pp(ML, 47)),
            B("Gold-Masked One #3", "可選 · Midlake Long Pillar Dock", None, map=pp(ML, 49)[0], opt=True, true=True,
              reward="Flaming Grip / Quenched Flaming Grip ＋ Bloodline Awakening 3/5",
              tips=["招式延續前兩戰：紅光閃、藍光彈、黑白畫面的招式只能閃"]),
            I("Treasure Basin", ["acc"], "White Serpent House Dock Bell 右邊建築。", img=pp(ML, 52)),
            B("Heartpiercer", "Elite Shadow Warden · 主線（White Serpent House）", PG + "heartpiercer-550x309.jpg", map=pp(ML, 57)[0],
              reward="Sundering Dual Axes（主武器）、White Serpent Eye",
              tips=["大部分攻擊可格擋，保守打、等連段收尾的閃光",
                    f"最危險：削 Sha-Chi 的跳踢接 {BL} 旋轉——跳踢沒閃到就彈反旋轉",
                    f"後空翻跳之後的 {R} 完美閃避；他硬直時待在攻擊範圍內"]),
            B("One-Eyed Archer", "可選 · One-Eyed Isle Dock", PG + "one-eyed-archer-550x309.jpg", map=pp(ML, 61)[0], opt=True,
              reward="One-Eyed Bow（Phantom Edge）",
              tips=["持續射箭；他衝到中央會射紅色雷射", "雷射發射前跑到場地邊緣，打到邊緣的雷射用跳的躲"]),
            I("Sharpshooter's Eye", ["acc"], "One-Eyed Archer 戰場上方樓梯的房子。", img=pp(ML, 62)),
            I("War Wagon", ["edge", "miss"], "開船往西穿過冰湖裂縫，靠岸後往前走觸發 Old Man Gen 的過場。",
              miss="必須已完成 The Journey Home（第三章開始），否則 Old Man Gen 不會出現；他腳邊的記憶之花與 Old Wooden Comb 也一併錯過。",
              img=pp(ML, 63)),
            I("Secrets at the Heart of the Lake", ["tale", "miss", "true"], "本區主要支線，在 Realm of Mirage 與 Inanis 對話取得 Violet Blossom。",
              "需要四個 Acolyte 面具與兩顆 Crystal Puppet Eye（放到 Mirror Realm 的紅色雕像）。",
              miss="進入 Mirage Estate 之前必須完成（獎盃 Forbidden Arts Beneath the Lake，真結局必要）。"),
            W("前往 Mountain of Imprisonment", "完成 Illusory Pipa（琵琶零件：Head、Backplate、Strings）後，到湖最北邊 Weeping Mistgate Bell 的霧牆 → 第七章。"
              "注意：進入 Mirage Estate 後，Mountain of Imprisonment 入口會被封鎖。", info=True),
        ]),
    ]))

# ---------------------------------------------------------------- 7
CHAPTERS.append(dict(
    id="ch7", num="第七章", title="囚山", en="Mountain of Imprisonment ＋ 回訪",
    cover=PG + "huangxing-550x309.jpg",
    lead="可選但真結局必要的山區，之後依序回 Crimson Manor 拿最後一個面具與 Crystal Puppet Eye，再回 Meigu Lake 進入隱藏區域。"
         "本章兩個對話選項會讓支線永久消失。",
    sections=[
        ("囚山 Mountain of Imprisonment", "依遊玩順序", [
            I("Baishan Writ", ["acc"], "The Lady's Path Bell 之後路上受傷 NPC 的屍體。", img=pp(MI, 2)),
            I("Talisman of Despair", ["acc"], "完成 Cui 目標後，燒掉樹枝下山，籠中男子給你。", img=pp(MI, 8)),
            I("The Broad Saber", ["tale"], "打開附近牢房，與 Wulin Fighter 交談。", img=pp(MI, 11)),
            I("Hero's Lament", ["tale", "miss"], "上坡用鎖鏈放下籠子，與 Liu Yi 交談。",
              "過程中要給他看 Moji's Bloodstained Sword，完成後得到 Ink Cut（Phantom Edge）。",
              miss="Liu Yi 死亡則支線與 Ink Cut 一起失敗——保護他。", img=pp(MI, 12)),
            B("Iron Butcher", "The Frenzied Brute · 可選", PG + "iron-butcher-550x309.jpg", opt=True,
              reward="Iron Butcher Mask（Jagged Steel 的 Soul Tempering 素材）",
              note="The Lady's Path Bell 附近。",
              tips=["三個紫色毒罐要閃開", "單獨丟出的毒罐會立刻爆炸，同樣要閃"]),
            B("Bi Feng", "Giant Saber Commander · 可選（真結局必要）", PG + "bi-feng-550x309.jpg", map=pp(MI, 14)[0], opt=True, true=True,
              reward="Juggernaut（主武器）",
              note="Cavern Passage Bell 附近。必須在 The Last Chance 鐘之前擊敗。",
              tips=[f"灰色揮砍之後接 {R}，完美閃避", "刀氣投射物彈反", f"原地垂直起跳是 {R}"]),
            I("Rootless Dew", ["key"], "Bi Feng 戰場左邊樓梯上的岩石。", "之後救出 Lu Sanqian 時要給他（見 Crude Radiant Heart）。", img=pp(MI, "key-item-2")),
            I("Ledger of Atonement", ["tale"], "持續與 Agonized Ironmask 對話，直到他請你找帳本。", img=pp(MI, 18)),
            B("Kui Yanyan", "The Deranged · 可選", PG + "kui-yanyan-550x309.jpg", map=pp(MI, 21)[0], opt=True,
              reward="Missing Lift Crank（啟動升降梯）、Sha-Chi Amber",
              tips=["貼身打來打斷他的攻擊", "丟出的匕首彈反"]),
            I("Ink Cut", ["edge"], "取得 Moji's Bloodstained Sword 後，在 Cavern Passage Bell 附近跟 Liu Yi 談 Moji's Relic。",
              "Game8 提示：之後打 Huangxing 時裝備 Ink Cut 可觸發額外對話。", img=pp(MI, 24)),
            I("Ironmask 對話選項", ["key", "miss"], "Commander's Platform 路上與 Ironmask 交談。",
              "必須選「This won't absolve you of your sins」開戰。",
              miss="選錯會失去下一條支線 Bai Xue，以及 Pangzhen 的一整組收集品（Ultimate Talisman、Snow and Blood 等）。",
              img=pp(MI, 25)),
            I("Bai Xue", ["tale", "miss"], "擊敗 Ironmask Assassin 後，與他身後的人偶交談。",
              miss="選「Leave him alone」人偶會消失，支線永久錯過。", img=pp(MI, 26)),
            I("Crude Radiant Heart", ["acc", "miss"], "前一個道具之後上樓梯，Lu Sanqian 躺在地上（需完成他的所有目標）。",
              miss="救出他時要給 Rootless Dew；拒絕的話他到不了 The Lady's Shrine，本周目錯過。", img=pp(MI, 30)),
            B("Jade-Face", "可選 · The Lady's Shrine Bell 附近", None, map=pp(MI, 32)[0], opt=True,
              reward="Seamless Death（主武器）",
              tips=["攻略站尚未公開詳細打法；按 紅光閃 / 藍光彈 的基本原則應對"]),
            I("Desperate Stand", ["acc"], "與 Jade-Face 記憶之花同一個房間（右邊房間）。", img=pp(MI, 34)),
            B("Huangxing", "The Kunlun Renegade · 可選（兩階段）", PG + "huangxing-550x309.jpg", map=pp(MI, 35)[0], opt=True,
              reward="Flying Guillotine（Phantom Edge，可打開封鎖區域）",
              gear=[("Phantom Edge", "Ink Cut（觸發額外對話）")],
              tips=[f"一階段：越轉越快的鏈錘旋轉最後是 {R}；場地小，利用柱子",
                    "二階段 Whirling Executioner：他衝到你面前前一刻翻滾閃避",
                    f"兩道風斬＋一道劍斬後是 {BL}，接著常常再來一個 {R}"]),
            I("Inanis' Radiant Fan", ["edge"], "在 Huangxing 戰場用 Flying Guillotine 打開隱藏通道往下跳，過場後取得。", img=pp(MI, 36)),
            I("Crystal Puppet Eye [Yin] / Puppet's Tongue", ["key", "true"], "進入前方橘色傳送門（攻略假設為第三個進入的門），與中央的人偶互動。",
              "Puppet's Tongue 用來進入 Crimson Manor；兩顆 Crystal Puppet Eye 是真結局條件。", img=pp(MI, "key-item-5")),
            W("Whence the Weeping", "過橋之前，先完成「到達山頂神社找出哭聲來源」與「進入神社地底」兩個步驟，否則這兩步會被鎖住。"),
        ]),
        ("回訪：Crimson Manor", "從泣溪谷的 Long Pillar Overlook 進入（需要 Puppet's Tongue）", [
            I("Ancient Armor Fragment", ["acc"], "Crimson Manor Bell 左邊。", img=pp(WCV, 54)),
            B("The Puppet Scavenger & Acolyte Hansui", "可選 · Scavenger Pens（雙頭目）", PG + "puppet-scavenger-550x309.jpg", map=pp(WCV, 60)[0],
              opt=True, true=True, reward="Hansui's Frost Mask（面具 4/4）、Crystal Puppet Eye [Yang]、Alloyed Scythe Blade",
              tips=["Scavenger 很慢很好打，優先集中火力打會冰凍你的 Acolyte",
                    "避開地上的冰圈，以及會冰凍爆炸的分身",
                    "建議下降時踩在絲線上避免摔落傷害"]),
        ]),
        ("回訪：Meigu Lake 第二次造訪", "需要四個 Acolyte 面具", [
            I("Phantom Illusionist Ruins Long Pillar", ["pillar", "true"], "從第三個 Ruins Bell 打破路障，左邊區域。Gold-Masked One #4，另有 Chaos Iron Fragment I。",
              img=pp(ML, 74)),
            I("Acolyte Whisk", ["acc"], "#78 記憶之花旁。", img=pp(ML, 79)),
            I("Acolyte Icicle", ["acc"], "第五個 Phantom Illusionist Ruins Bell 旁。", img=pp(ML, 82)),
            B("Blizzard Blademaster", "可選 · Whiteshadow's Fall", PG + "Blizzard-blademaster-550x309.jpg", map=pp(ML, 96)[0], opt=True,
              reward="Whiteshadow（主武器）",
              gear=[("飾品", "元素傷害減免飾品（冰抗）")],
              tips=["第一擊在最後一刻閃避——它會折返", f"他衝刺後的第二擊是 {R}，完美閃避"]),
            W("Pangzhen 回收", "若 Ironmask 選對了選項，回 Pangzhen Green Serpent House Bell 對面上鎖的門：兩朵記憶之花、Ultimate Talisman、Snow and Blood（飾品）。", info=True),
            I("Snow and Blood", ["acc", "miss"], "Pangzhen：Green Serpent House Bell 過橋上樓梯、左邊上鎖的門，沿屋頂到床上的屍體 → 田野 → 樹下岩石。",
              miss="Ledger of Atonement 結尾若選了「Leave him alone」則整組錯過。", img=pp(PZ, 106)),
        ]),
    ]))

# ---------------------------------------------------------------- 8
CHAPTERS.append(dict(
    id="ch8", num="後期區域", title="蜃樓莊園", en="Mirage Estate ＋ 赤林收尾",
    cover=KG + "Fighting-Lei-Dang.jpg",
    lead="從 Green Serpent House 的門進入。<b>踏進 Mirage Estate 就是不歸點</b>：Meigu Lake 與 Pangzhen 的紫色支線、Mountain of Imprisonment 入口都會鎖住。"
         "（此區的地圖截圖攻略站尚未公開，先以戰鬥截圖代替。）",
    sections=[
        ("進入前", "最後檢查", [
            W("Mirage Estate 不歸點", "<ul><li>Secrets at the Heart of the Lake 已完成</li><li>Pangzhen / Meigu Lake 所有紫色支線（真結局必要）</li>"
              "<li>Mountain of Imprisonment 已完成（Bi Feng、Crystal Puppet Eye）</li><li>Zhu Yuan 已擊敗</li>"
              "<li>走到紅線樓梯時 Inanis 會警告你——還沒完成就回頭</li></ul>"),
        ]),
        ("蜃樓莊園 Mirage Estate", "依遊玩順序", [
            I("Feather Fan Plume", ["acc"], "Nuo Mask Altar：爬梯後、下一個 Bell 前建築前方的桌上。"),
            I("Quick Hand's Request（Mirage Estate）", ["tale", "true"], "Zhang's Hideout Bell 後方洞穴，與 Zhang 交談拿清單。"),
            I("Zhang 的玉箱（Opera House）", ["key", "miss", "true"], "Opera House 內的玉箱，Quick Hand's Request 需要。",
              miss="第一次經過時就要拿——歌劇結束後門會鎖上。"),
            I("Executioner's Headscarf", ["acc"], "Opera House 爬梯子、經過人偶敵人後的寶箱。"),
            B("Yuding", "No. 12 Crescent Blade Puppet · 主線", None,
              reward="Crescent Blade（主武器）", note="Training Grounds Bell 附近。",
              tips=["攻略站尚未公開詳細打法；按 紅光閃 / 藍光彈 的基本原則應對"]),
            I("Opera Ticket", ["key"], "Training Grounds 北側祭壇。"),
            B("Qiu Feng", "The Crimson Boneblade · 主線", KG + "Qiu-Feng-Boss.jpg",
              reward="Wraith Mask（飾品）", note="Mourning Hall Bell 附近的建築。",
              tips=["雙臂舉起 → 閃避接下來兩擊", f"最後的砸地是 {R}，完美閃避",
                    f"紅色飛刃彈反，最後一把是 {BL}"]),
            I("Nuo Mask", ["acc"], "收集 Sorrow（Back Hill）、Wrath（Opera House 東側祭壇）、Joy（Willow Pavilion）三個碎片，交給 Nuo Mask Altar 的 Old Beggar。"),
            I("Thundermoon Lantern", ["acc", "true"], "把 Mirage Estate 的寶物交給 Zhang's Hideout 的 Zhang。完成 Quick Hand Zhang 線。"),
            B("Lei Dang", "The Order's Envoy · 主線（兩階段）", KG + "Fighting-Lei-Dang.jpg",
              reward="Tiger Cannon（Phantom Edge，可轟開脆弱牆壁）", note="Perfect Vessel Pond Bell 附近。PCGamesN 評為最難頭目之一。",
              tips=["他跳起後會發出全場衝擊波——躲到石頭後面",
                    "攻擊來自各個方向，保持移動、不要貪刀"]),
            B("Mo Yuan", "Leader of the Bastion of Mo · 可選（Mirage Estate 長柱）", PG + "mo-yuan-550x309.jpg", opt=True, true=True,
              reward="Bastion of Mo Mask（Soul Tempering）＋ 完成 Bloodline Awakening 5/5",
              tips=[f"蓄力跳擊是 {R}，幾乎一擊必殺，一定要完美閃避", "他會從天上召喚光柱，持續移動閃避"]),
        ]),
        ("赤林收尾 Crimson Forest Cleanup", "現在可以處理的舊區域內容", [
            I("Frostward", ["acc"], "Burial Grounds Bell 往西南，穿過結冰水面到第一個區域。冰屬性減傷。"),
            I("Chaos Ring", ["acc"], "Mirrorwood Depths Bell 的傳送門謎題區第二段，舊東側傳送門前。"),
            B("Yucong", "No. 34 Twisted Puppet · 可選（Threadbound Great Tree）", None, opt=True,
              reward="Freezing Chaos（主武器）；第三階段：Chaos Iron Fragment II",
              note="就是第一章 Triple Threat 支線的目標。",
              gear=[("武器", "Game8：戰前裝備 Blazing Edge，否則戰鬥只到第二階段，錯過額外過場與 Chaos Iron Fragment II（Shadowless Edge 需要）")],
              tips=["攻略站尚未公開詳細打法；按 紅光閃 / 藍光彈 的基本原則應對"]),
            I("A Severed Mindseal（赤林塔）", ["tale"], "Crimson Forest Sha-Chi Tower 6F 的 Bell 旁。到塔底盪到熔爐取得 Primal Stone 與塔鑰匙，交給 Spectral Blade。"),
            I("Use It Against Them / Heart of the Fist", ["tale"], "同在 6F：Jade Dancer 邀你只用 Fiend Saws ＋ Iron Gauntlets 切磋；Iron Fiend 的支線在 Burial Grounds Bell 西南的大墓碑完成。",
              "需要第三章頭目第三階段掉落的 Fiend Saws。"),
        ]),
    ]))

# ---------------------------------------------------------------- 9
CHAPTERS.append(dict(
    id="ch9", num="最終章", title="裂魂山", en="Mount Soulrend",
    cover=KG + "Soulrend-Cliff-Bell.jpg",
    lead="最終區域。頭目名稱與截圖預設模糊處理，點擊才會顯示。"
         "<b>The Last Chance 鐘之後無法離開</b>，手動存檔並確認真結局條件。",
    sections=[
        ("真結局條件", "在 The Last Chance 之前全部完成", [
            W("真結局 checklist（With Heart and Blood）", "<ul>"
              "<li>兩顆 Crystal Puppet Eye（Crimson Manor、Mountain of Imprisonment）放到 Meigu Lake Mirror Realm</li>"
              "<li>四個 Acolyte 面具</li><li>修好 Illusory Pipa（Head / Backplate / Strings）</li>"
              "<li>五根長柱 Bloodline Awakening</li><li>Secrets at the Heart of the Lake</li>"
              "<li>Quick Hand Zhang 整條線</li><li>Zhu Yuan、Bi Feng 已擊敗</li><li>所有紫色支線</li></ul>"
              "<p>多數攻略建議：在 The Last Chance 鐘前手動存檔。</p>", info=True),
        ]),
        ("裂魂山 Mount Soulrend", "依遊玩順序", [
            I("Cui（完成）", ["tale"], "Last Mandate Encampment：Bell 西邊圍欄區，坐在箱子上的男女。",
              miss="必須在 The Crusher and the Saw 之前完成，否則拿不到 Baishan Headband。"),
            B("The Crusher and the Saw", "Giant's Lair（兩階段）", PG + "crusher-boss-550x309.jpg",
              reward="Bonesaw（主武器）；完成 Cui：Baishan Headband",
              tips=["一階段先鎖定 Saw 打", f"二階段 Crusher：錘擊後接空中 {R}，完美閃避"]),
            B("連戰：舊敵再臨", "多名先前頭目同場", PG + "puppet-scavenger-2-550x309.jpg",
              note="完成過的角色支線越多，這裡就會有越多同伴幫忙。",
              tips=["每個敵人的打法同其原本頭目戰"]),
            W("The Last Chance 不歸點", "過了這個鐘就被鎖在最終頭目連戰中，直到通關。請先手動存檔。"),
            B("Leng Tu", "Herald of the Veil", KG + "Fighting-Leng-Tu.jpg", spoil=True,
              reward="無",
              note="AllThingsHow：開始這一戰後結局路線就鎖定。",
              tips=["先清召喚物", "注意天上手臂的陰影落點", "光球蓄力會把你推開，不需要閃"]),
            B("Meng Hua", "The Merciful Lady of the Blossom Veil", PG + "lady-boss-fight-550x309.jpg", spoil=True,
              reward="The Lady's Fan（主武器）、The Lady's Crown、Herald's Lingering Threads",
              tips=["旋轉雷射用跳或閃躲過", f"蓄白色光球且畫面變暗後接 {R}"]),
            B("真結局頭目", "The Fallen Dream（Soulrend Cliff 頂端的金色傳送門）", KG + "Zuo-Shang-Boss.jpg", spoil=True, true=True,
              reward="Aureate（主武器）、Radiant Heart、Broken Long Body",
              note="只有達成所有真結局條件才會出現。攻略站為避免劇透未提供打法。",
              tips=["紅光閃、藍光彈；帶上你最強的配置"]),
        ]),
    ]))


# =====================================================================
#  RENDERING
# =====================================================================

def esc(s):
    return html.escape(s, quote=True)


def head(title, desc):
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="referrer" content="no-referrer">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23c8322b'/%3E%3Ctext x='32' y='45' font-size='38' text-anchor='middle' fill='white' font-family='serif'%3E影%3C/text%3E%3C/svg%3E">
</head>
"""


def topbar(active):
    links = ['<a href="index.html"%s>目錄</a>' % (' class="on"' if active == "index" else "")]
    for c in CHAPTERS:
        links.append(f'<a href="{c["id"]}.html"{" class=\"on\"" if c["id"] == active else ""}>{esc(c["title"])}</a>')
    return f"""<header class="topbar"><div class="wrap">
<a class="brand" href="index.html"><span class="seal">影</span>影之刃零 攻略<small>PHANTOM BLADE ZERO</small></a>
<nav class="chapnav">{''.join(links)}</nav>
</div></header>
"""


FOOTER = """<footer><div class="wrap">
<p>非官方粉絲攻略。遊戲畫面與名稱版權屬 S-GAME 所有。物品、頭目名稱使用英文版遊戲名稱。</p>
<p>截圖來源（外部連結）：地圖截圖 © <a href="https://www.powerpyx.com/phantom-blade-zero-collectibles-guide-100-completion/" target="_blank" rel="noopener">PowerPyx</a>；
頭目截圖 © <a href="https://www.keengamer.com/articles/guides/phantom-blade-zero-all-bosses-and-their-rewards/" target="_blank" rel="noopener">KeenGamer</a>、
<a href="https://www.pcgamesn.com/phantom-blade-zero/bosses" target="_blank" rel="noopener">PCGamesN</a>。</p>
<p>資料整理自：<a href="https://game8.co/games/Phantom-Blade-Zero/archives/634952" target="_blank" rel="noopener">Game8</a>、
<a href="https://allthings.how/phantom-blade-zero-missables/" target="_blank" rel="noopener">AllThingsHow</a>、
<a href="https://phantombladezerocodex.com/missables" target="_blank" rel="noopener">PBZ Codex</a>、
<a href="https://grindnstrat.com/phantom-blade-zero-bosses/" target="_blank" rel="noopener">grindnstrat</a>（屬性弱點）、
<a href="https://www.keengamer.com/articles/guides/phantom-blade-zero-complete-walkthrough-all-quests/" target="_blank" rel="noopener">KeenGamer Walkthrough</a>。
各站資料偶有出入，以遊戲內實際情況為準。</p>
</div></footer>
<script src="assets/app.js"></script>
</body></html>
"""


def tag_html(t):
    label, cls = TAGS[t]
    return f'<span class="tag {cls}">{esc(label)}</span>'


def shots_html(img, name):
    if not img:
        return ""
    m, s = img
    return (f'<div class="shots">'
            f'<div class="shot" data-zoom="{esc(name)}・地圖位置"><img loading="lazy" data-hide-broken src="{m}" alt="{esc(name)} 地圖位置"><span class="cap">地圖</span></div>'
            f'<div class="shot" data-zoom="{esc(name)}・實地畫面"><img loading="lazy" data-hide-broken src="{s}" alt="{esc(name)} 實地畫面"><span class="cap">實地</span></div>'
            f'</div>')


def render_item(e, n, eid):
    tags = e["tags"]
    filt = " ".join(sorted(set(tags + (["miss"] if e["miss"] else []))))
    cls = "entry" + (" miss" if ("miss" in tags or e["miss"]) else "")
    tg = "".join(tag_html(t) for t in tags)
    if e["miss"] and "miss" not in tags:
        tg = tag_html("miss") + tg
    dl = f'<div class="deadline"><b>死線：</b>{e["miss"]}</div>' if e["miss"] else ""
    note = f'<p class="note">{e["note"]}</p>' if e["note"] else ""
    has_img = bool(e["img"])
    return f"""<div class="{cls}" data-id="{eid}" data-tags="{filt}">
<div class="step">{n}</div>
<div class="card"><div class="item-grid{' has-img' if has_img else ''}">
{shots_html(e["img"], e["name"])}
<div class="body"><div class="tags">{tg}</div>
<h3>{esc(e["name"])}</h3>
<p class="where">{e["where"]}</p>{note}{dl}
<label class="check"><input type="checkbox"> 已完成</label>
</div></div></div></div>
"""


def render_boss(e, n, eid):
    sp = " spoiler" if e["spoil"] else ""
    label = e["label"] or ("可選頭目" if e["opt"] else "頭目")
    tg = []
    if e["opt"]:
        tg.append(tag_html("opt"))
    if e["true"]:
        tg.append(tag_html("true"))
    tagrow = f'<div class="tags">{"".join(tg)}</div>' if tg else ""
    title = (f'<div class="title"><div class="label">{esc(label)}</div>'
             f'<h3><span class="{sp.strip()}">{esc(e["name"])}</span>'
             f'{"<span class=spoil-hint>（點擊顯示）</span>" if e["spoil"] else ""}</h3>'
             f'<div class="sub">{esc(e["sub"])}</div></div>')
    if e["img"]:
        hero = (f'<div class="boss-hero" data-zoom="{esc(e["name"]) if not e["spoil"] else ""}">'
                f'<img class="{sp.strip()}" loading="lazy" data-hide-broken src="{e["img"]}" alt="頭目截圖">{title}</div>')
    else:
        hero = f'<div class="boss-hero noimg">{title}</div>'
    kv = []
    if e["reward"]:
        kv.append(f'<dt>獎勵</dt><dd>{esc(e["reward"])}</dd>')
    if e["weak"]:
        kv.append(f'<dt>弱點</dt><dd class="weak">{esc(e["weak"])}</dd>')
    if e["resist"]:
        kv.append(f'<dt>抗性</dt><dd class="resist">{esc(e["resist"])}</dd>')
    kvh = f'<dl class="kv">{"".join(kv)}</dl>' if kv else ""
    gear_cls = {"武器": "t-weapon", "Phantom Edge": "t-edge", "飾品": "t-acc", "道具": "t-key", "提示": "t-opt"}
    gear = "".join(f'<div class="row"><span class="tag {gear_cls.get(k, "t-opt")}">{esc(k)}</span><span>{esc(v)}</span></div>'
                   for k, v in e["gear"])
    gearh = f'<h5>推薦配置</h5><div class="loadout">{gear}</div>' if gear else ""
    note = f'<p class="note" style="margin:0 0 12px">{e["note"]}</p>' if e["note"] else ""
    tips = "".join(f"<li>{t}</li>" for t in e["tips"])
    maph = ""
    if e["map"]:
        maph = (f'<h5 style="margin-top:6px">地圖位置</h5><div class="mapthumb" data-zoom="{esc(e["name"]) if not e["spoil"] else "頭目"}・地圖位置">'
                f'<img loading="lazy" data-hide-broken src="{e["map"]}" alt="頭目地圖位置"><span class="cap">地圖</span></div>')
    tags = "boss" + (" opt" if e["opt"] else "") + (" true" if e["true"] else "")
    return f"""<div class="entry boss" data-id="{eid}" data-tags="{tags}">
<div class="step">{n}</div>
<div class="card">{hero}
<div class="boss-body">
<div>{tagrow}{note}<h5>戰術</h5><ul class="tips">{tips}</ul></div>
<div>{kvh}{gearh}{maph}<label class="check"><input type="checkbox"> 已擊敗</label></div>
</div></div></div>
"""


def render_banner(e):
    cls = "banner info" if e["info"] else "banner"
    body = e["body"] if e["body"].startswith("<") else f"<p>{e['body']}</p>"
    return f'<div class="entry banner-entry" data-tags="always"><div class="{cls}"><h4>{esc(e["title"])}</h4>{body}</div></div>\n'


def counts(ch):
    m = b = t = 0
    for _, _, entries in ch["sections"]:
        for e in entries:
            if e["kind"] == "boss":
                b += 1
            elif e["kind"] == "item":
                t += 1
                if e["miss"] or "miss" in e["tags"]:
                    m += 1
    return m, b, t


def render_chapter(i, ch):
    m, b, t = counts(ch)
    out = [head(f'{ch["title"]} {ch["en"]}｜影之刃零 攻略', ch["lead"]),
           f'<body data-page="{ch["id"]}">', topbar(ch["id"])]
    out.append(f"""<section class="hero"><div class="bgimg" style="background-image:url('{ch["cover"]}')"></div>
<div class="wrap"><div class="kicker">{esc(ch["num"])}</div>
<h1>{esc(ch["title"])}<span class="en">{esc(ch["en"])}</span></h1>
<p class="lead">{ch["lead"]}</p>
<div class="stats"><div class="stat red"><b>{m}</b>錯過不再</div><div class="stat"><b>{b}</b>頭目</div><div class="stat"><b>{t}</b>道具 / 支線</div></div>
</div></section>
<div class="toolbar"><div class="wrap">
<button class="chip on" data-f="all">全部</button>
<button class="chip" data-f="miss">錯過不再</button>
<button class="chip" data-f="boss">頭目</button>
<button class="chip" data-f="weapon">武器</button>
<button class="chip" data-f="edge">Phantom Edge</button>
<button class="chip" data-f="acc">飾品</button>
<button class="chip" data-f="tale">支線</button>
<button class="chip" data-f="true">真結局</button>
<span class="spacer"></span>
<button class="chip" id="hidedone">隱藏已完成</button>
<span class="progress" id="prog"></span>
</div></div>
<main><div class="wrap">""")
    n = 0
    for si, (stitle, ssub, entries) in enumerate(ch["sections"]):
        out.append(f'<div class="section-title"><h2>{esc(stitle)}</h2><span>{esc(ssub)}</span></div><div class="timeline">')
        for ei, e in enumerate(entries):
            eid = f"s{si}e{ei}"
            if e["kind"] == "banner":
                out.append(render_banner(e))
                continue
            n += 1
            out.append(render_item(e, n, eid) if e["kind"] == "item" else render_boss(e, n, eid))
        out.append("</div>")
    prev = CHAPTERS[i - 1] if i > 0 else None
    nxt = CHAPTERS[i + 1] if i + 1 < len(CHAPTERS) else None
    pg = '<div class="pager">'
    pg += (f'<a href="{prev["id"]}.html"><small>← 上一章</small><b>{esc(prev["title"])}</b></a>' if prev
           else '<a href="index.html"><small>← 返回</small><b>目錄</b></a>')
    pg += (f'<a class="next" href="{nxt["id"]}.html"><small>下一章 →</small><b>{esc(nxt["title"])}</b></a>' if nxt
           else '<a class="next" href="index.html"><small>返回 →</small><b>目錄</b></a>')
    pg += "</div>"
    out.append(pg + "</div></main>" + FOOTER)
    return "\n".join(out)


def render_index():
    out = [head("影之刃零 攻略｜錯過不再的道具、支線與頭目打法",
                "Phantom Blade Zero 中文攻略：每章容易錯過的道具、支線、武器，以及每個頭目的打法與推薦配置。"),
           '<body data-page="index">', topbar("index")]
    out.append(f"""<section class="hero idx-hero"><div class="bgimg" style="background-image:url('{KG}Phantom-Blade-Zero-Bosses-Cover.jpg')"></div>
<div class="wrap"><div class="kicker">Phantom Blade Zero · 非官方攻略</div>
<h1>影之刃零<span class="en">錯過不再的一切，與每個頭目的打法</span></h1>
<p class="lead">每一章只列出容易忘記、容易忽略、錯過就再也拿不到的道具、支線、武器與飾品，以及頭目的戰術與推薦配置。
全部依實際遊玩順序排列，並附地圖截圖。盡量不劇透。</p>
<div class="legend">{tag_html("miss")}{tag_html("weapon")}{tag_html("edge")}{tag_html("acc")}{tag_html("tale")}{tag_html("key")}{tag_html("true")}</div>
</div></section>
<main><div class="wrap">
<div class="section-title"><h2>選擇章節</h2><span>依劇情順序</span></div>
<div class="grid">""")
    for ch in CHAPTERS:
        m, b, t = counts(ch)
        lead = html.unescape(ch["lead"]).replace("<b>", "").replace("</b>", "")
        short = lead.split("。")[0] + "。"
        out.append(f"""<a class="chcard" href="{ch["id"]}.html">
<div class="img" style="background-image:url('{ch["cover"]}')"><span class="num">{esc(ch["num"])}</span></div>
<div class="txt"><h3>{esc(ch["title"])}</h3><div class="en">{esc(ch["en"])}</div>
<p>{esc(short)}</p>
<div class="meta"><span class="m">錯過不再 {m}</span><span>頭目 {b}</span><span>道具 / 支線 {t}</span></div></div></a>""")
    out.append("""</div>
<div class="section-title"><h2>使用方式</h2><span>三個重點</span></div>
<div class="how">
<div><h4>紅色 = 錯過不再</h4><p>紅框卡片都有「死線」，告訴你在哪個頭目 / 事件之前一定要完成。每章開頭也有不歸點提醒。</p></div>
<div><h4>紅光閃、藍光彈</h4><p>頭目攻擊發出<span class="glint g-red">紅光</span>要完美閃避，<span class="glint g-blue">藍光</span>要彈反。戰術內都用這兩個標記。</p></div>
<div><h4>打勾記錄進度</h4><p>每張卡片可勾選「已完成」，進度會存在你的瀏覽器裡；上方可以篩選類型或隱藏已完成項目。</p></div>
<div><h4>防劇透</h4><p>只寫地點與操作，不寫劇情。最終章的頭目名稱與截圖預設模糊，點擊才顯示。</p></div>
</div>
</div></main>""" + FOOTER)
    return "\n".join(out)


def main():
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index())
    for i, ch in enumerate(CHAPTERS):
        with open(os.path.join(ROOT, f'{ch["id"]}.html'), "w", encoding="utf-8") as f:
            f.write(render_chapter(i, ch))
    print("built", 1 + len(CHAPTERS), "pages")


if __name__ == "__main__":
    main()
