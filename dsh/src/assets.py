# -*- coding: utf-8 -*-
# 圖片清單：全部下載到 site/assets/images，不依賴外部圖床。
import os, io, requests
from PIL import Image

H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
     "Referer": "https://www.gamersky.com/"}

IMAGES = {
    # 章節主視覺
    "hero-prologue.jpg": "https://img1.gamersky.com/image2026/10/20261028_ax_156_1/1194.jpg",
    "hero-creek.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/12083.jpg",
    "hero-forest.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/13614.jpg",
    "hero-lu.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/14919.jpg",
    "hero-pang.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/18007.jpg",
    "hero-camp.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/18791.jpg",
    "hero-lake.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/19010.jpg",
    "hero-jail.jpg": "https://img1.gamersky.com/image2026/11/20261103_qy_372_44/1.jpg",
    "hero-estate.jpg": "https://img1.gamersky.com/image2026/11/20261101_ax_156_3/1329.jpg",
    "hero-soul.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/11422.jpg",
    "map-ch6.jpg": "https://media.9game.cn/gamebase/ieu-gdc-pre-process/images/20261103/0/16/26076d054b2845918c062772f470622b.jpg",
    # 頭目（游民/18183 攻略截圖）
    "boss-cangang.jpg": "https://img.18183.com/image/2026/10/29/9d67f8c5d10fe7504e52ed325527c38b.jpg",
    "boss-pengmeng.jpg": "https://img.18183.com/image/2026/10/29/7d9df8a9e46811b53c3783f6aa8da2d4.jpg",
    "boss-ahua.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/1884.jpg",
    "boss-zhuming.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/11614.jpg",
    "boss-sanmian.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/1451.jpg",
    "boss-jinmianju.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/12048.jpg",
    "boss-huaqianxiao.jpg": "https://img.18183.com/image/2026/10/29/29280547d19c748bf9e5bd0b17a99b61.jpg",
    "boss-jingye.jpg": "https://img.18183.com/image/2026/10/29/2d65028d2e8a501e1215a4f858d2829f.jpg",
    "boss-tiekuang.jpg": "https://img.18183.com/image/2026/10/29/3a9d5abbc50c3bf9482d968ddd739399.jpg",
    "boss-baichilian.jpg": "https://img.18183.com/image/2026/10/29/86fbbd091485750c6ca3f3b8c0fc61d4.jpg",
    "boss-zhuobi.jpg": "https://img.18183.com/image/2026/10/29/67be8aab61c29284fe86dfff2e590670.jpg",
    "boss-biyuan.jpg": "https://img.18183.com/image/2026/10/29/6944ee6aee525ad3eae26815218fb798.jpg",
    "boss-bihai.jpg": "https://img.18183.com/image/2026/10/29/751084ed77476f4db81bfb2a5989ecac.jpg",
    "boss-yanru.jpg": "https://img.18183.com/image/2026/10/29/324e116c37de14051c854d22d19982d4.jpg",
    "boss-danghui.jpg": "https://img.18183.com/image/2026/10/29/f6ae2eda3a48199e2b67f6defad510a2.jpg",
    "boss-yuzan.jpg": "https://img.18183.com/image/2026/10/29/fafebc8dbb56649c8bfdd6a55a43f262.jpg",
    "boss-muxiaokui.jpg": "https://img.18183.com/image/2026/10/29/a37bc021393411c39be1e37d2ea56456.jpg",
    "boss-huoliuxing.jpg": "https://img.18183.com/image/2026/10/29/6a50ea4296594b511e82ae4ef5f73a2a.jpg",
    "boss-zhanqi.jpg": "https://img.18183.com/image/2026/10/29/6a7fbd37c144adc160b68a1d269d835f.jpg",
    "boss-wuxuan.jpg": "https://img.18183.com/image/2026/10/29/6399da4003e2a26fd8a2519238ba5a04.jpg",
    "boss-guwanyue.jpg": "https://img.18183.com/image/2026/10/29/79569dafed696c9ed949fd3742c008c9.jpg",
    "boss-xieqiudong.jpg": "https://img.18183.com/image/2026/10/29/c509ef4bd49a29e7066448c6a7fa3519.jpg",
    "boss-youlong.jpg": "https://img.18183.com/image/2026/10/29/61c63bfb1599fe075cd1b670bc6ce182.jpg",
    "boss-changhong.jpg": "https://img.18183.com/image/2026/10/29/28f50d93144c731859fbc2e3cd9afdc7.jpg",
    "boss-lieyan.jpg": "https://img.18183.com/image/2026/10/29/47f311999830a4d7eee9ca8632a1dc55.jpg",
    "boss-gouhun.jpg": "https://img.18183.com/image/2026/10/29/77dd1171ad70b05bba7ff178658bbb5c.jpg",
    "boss-leiting.jpg": "https://img1.gamersky.com/image2026/11/20261101_ax_156_3/1869.jpg",
    # 後段：暫用已確認的攻略實景，卡片會標示「章節實景」
    "boss-qixing.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/18791.jpg",
    "boss-huangxingzi.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/18791.jpg",
    "boss-yubi.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/14691.jpg",
    "boss-yanqiansui.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/19059.jpg",
    "boss-duyan.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/19099.jpg",
    "boss-fengxue.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/19010.jpg",
    "boss-zhuyuan.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/111703.jpg",
    "boss-duanchang.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/112328.jpg",
    "boss-guhe.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/15237.jpg",
    "boss-moyuan.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/12048.jpg",
    "boss-bifeng.jpg": "https://img1.gamersky.com/image2026/11/20261103_qy_372_44/1.jpg",
    "boss-yumian.jpg": "https://img1.gamersky.com/image2026/11/20261103_qy_372_45/1.jpg",
    "boss-kuiyanyan.jpg": "https://img1.gamersky.com/image2026/11/20261103_qy_372_45/2.jpg",
    "boss-huangxing.jpg": "https://img1.gamersky.com/image2026/11/20261103_qy_372_45/3.jpg",
    "boss-tietufu.jpg": "https://img1.gamersky.com/image2026/11/20261103_qy_372_46/1.jpg",
    "boss-leidang.jpg": "https://img1.gamersky.com/image2026/11/20261101_ax_156_3/1329.jpg",
    "boss-qiufeng.jpg": "https://img1.gamersky.com/image2026/11/20261101_ax_156_3/1381.jpg",
    "boss-yuding.jpg": "https://img1.gamersky.com/image2026/11/20261101_ax_156_3/1520.jpg",
    "boss-lizhe.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/12083.jpg",
    "boss-lengtu.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/11422.jpg",
    "boss-menghua.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/11422.jpg",
    "boss-zuoshang-true.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_11/1451.jpg",
    # 道具／武器實拍
    "item-yingdong.jpg": "https://img1.gamersky.com/image2026/10/20261028_ax_156_1/1780.jpg",
    "item-heishang.jpg": "https://img1.gamersky.com/image2026/10/20261028_ax_156_1/1910.jpg",
    "item-nanyan.jpg": "https://img1.gamersky.com/image2026/10/20261028_ax_156_1/11793.jpg",
    "item-jianyan.jpg": "https://img1.gamersky.com/image2026/10/20261028_ax_156_1/12525.jpg",
    "item-xiangxun.jpg": "https://img1.gamersky.com/image2026/10/20261029_fxy_625_2/1987.jpg",
    "item-hunyuan.jpg": "https://img1.gamersky.com/image2026/10/20261028_ax_156_1/14929.jpg",
}

def download_all(dest):
    os.makedirs(dest, exist_ok=True)
    ok = 0
    for name, url in IMAGES.items():
        path = os.path.join(dest, name)
        if os.path.exists(path) and os.path.getsize(path) > 5000:
            ok += 1
            continue
        try:
            headers = dict(H)
            if "18183.com" in url:
                headers["Referer"] = "https://www.18183.com/"
            elif "9game.cn" in url:
                headers["Referer"] = "https://www.9game.cn/"
            else:
                headers["Referer"] = "https://www.gamersky.com/"
            r = requests.get(url, headers=headers, timeout=45)
            r.raise_for_status()
            im = Image.open(io.BytesIO(r.content))
            im = im.convert("RGB")
            w, h = im.size
            if w > 1500:
                im = im.resize((1500, int(h * 1500 / w)), Image.LANCZOS)
            im.save(path, "JPEG", quality=86, optimize=True)
            ok += 1
            print("ok", name, im.size)
        except Exception as e:
            print("FAIL", name, url, e)
    print("downloaded", ok, "/", len(IMAGES))
