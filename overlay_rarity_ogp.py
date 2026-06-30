#!/usr/bin/env python3
# 既存OGPカード(ogp/{en,ko,zh,tw}/*.png)に希少性バッジ（MBTI出現率%）をオーバーレイ追加。
# JA(ogp/ja)は generate_ja_ogp.py 側でバッジ込み生成済み。
# 依存: /tmp/RARITY.json（index.html の RARITY をダンプ）
# フォント: en=DejaVuSans-Bold / ko,zh,tw=WQY Zen Hei（Hangul・繁体・簡体を描画可）
import json, os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.abspath(__file__))
RARITY = json.load(open("/tmp/RARITY.json", encoding="utf-8"))
WQY = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
WHITE = (255, 255, 255)
ORDER = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
         "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
# lang: font, 希少/人気ラベル, %書式, バッジ中心x, カード上端y
CFG = {
    "en": {"font": DEJA, "rare": "RARE",  "common": "COMMON", "pct": lambda p: f"  {p}%",  "tcx": 925, "top": 80},
    "zh": {"font": WQY,  "rare": "稀有",   "common": "人气",   "pct": lambda p: f" 约{p}%", "tcx": 925, "top": 80},
    "tw": {"font": WQY,  "rare": "稀有",   "common": "人氣",   "pct": lambda p: f" 約{p}%", "tcx": 925, "top": 80},
    "ko": {"font": WQY,  "rare": "희귀",   "common": "인기",   "pct": lambda p: f" 약{p}%", "tcx": 940, "top": 80},
}
for lang, c in CFG.items():
    fnt = ImageFont.truetype(c["font"], 23)
    n = 0
    for code in ORDER:
        path = os.path.join(ROOT, "ogp", lang, code.lower() + ".png")
        if not os.path.exists(path):
            print("skip(missing)", lang, code); continue
        p = RARITY[code]; rare = p <= 5
        rt = (c["rare"] if rare else c["common"]) + c["pct"](p)
        img = Image.open(path).convert("RGB"); dr = ImageDraw.Draw(img)
        rbg = (142, 84, 184) if rare else (200, 140, 40)
        rw = dr.textlength(rt, font=fnt); ph = 40; pw = int(rw) + 36
        tcx = c["tcx"]; top = c["top"]
        bx1 = tcx - pw // 2; by1 = top - ph // 2; bx2 = tcx + pw // 2; by2 = by1 + ph
        dr.rounded_rectangle([bx1, by1, bx2, by2], ph // 2, fill=rbg)
        dr.text((tcx, by1 + ph // 2), rt, font=fnt, fill=WHITE, anchor="mm")
        img.save(path); n += 1
    print("overlaid", lang, n)
