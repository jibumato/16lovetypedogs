#!/usr/bin/env python3
"""Generate per-type OGP cards and share/redirect pages for EN and ZH.

Mirrors the existing JA (/ogp/ja, type-*.html) and KO (/ogp/ko, /ko/*.html)
setup so that shared links in English and Chinese show the user's own dog
breed in the link preview instead of the generic site card.

Outputs:
  ogp/en/<code>.png , ogp/zh/<code>.png   (1200x630 OGP cards)
  en/<code>.html    , zh/<code>.html       (OGP redirect pages -> SPA result)
"""
import json, os, re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
LOC = json.load(open("/tmp/LOC.json", encoding="utf-8"))
I18N = json.load(open("/tmp/I18N.json", encoding="utf-8"))

ORDER = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
         "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

# palette taken from the site's brand tokens / JA OGP card
CREAM   = (252, 244, 239)
BLOB    = (247, 224, 233)
PINK    = (210, 98, 143)
PINK_BD = (242, 184, 204)
PILL_BG = (247, 217, 228)
INK     = (87, 79, 99)
INK_SOFT= (147, 138, 163)
WHITE   = (255, 255, 255)

FONTS = {
    "en": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "en_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "zh": "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "zh_bold": "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
}

LABEL   = {"en": "My love-dog is", "zh": "我的恋爱犬是"}
EYEBROW = {"en": "MBTI  ×  LOVE  ×  DOG", "zh": "MBTI  ×  恋爱  ×  犬种"}
RESULT  = {"en": "16 Love-Type Dogs  result", "zh": "16恋爱犬测验  结果"}
SITE    = "16lovetypedogs.com"


def fnt(lang, kind, size):
    return ImageFont.truetype(FONTS[f"{lang}_bold"] if kind == "bold" else FONTS[lang], size)


def wrap(draw, text, font, max_w, space_join):
    tokens = text.split(" ") if space_join else list(text)
    join = " " if space_join else ""
    lines, line = [], ""
    for t in tokens:
        cand = (line + join + t) if line else t
        if draw.textlength(cand, font=font) > max_w and line:
            lines.append(line); line = t
        else:
            line = cand
    if line:
        lines.append(line)
    return lines


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius, fill=255)
    return m


def make_card(lang, code):
    d = LOC[lang][code]
    space = (lang == "en")
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), CREAM)
    dr = ImageDraw.Draw(img)

    # soft pink blobs
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse([-140, -180, 220, 180], fill=BLOB + (120,))
    bd.ellipse([W-260, H-220, W+120, H+160], fill=BLOB + (110,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), blob).convert("RGB"), (0, 0))
    dr = ImageDraw.Draw(img)

    LX = 60
    LW = 600  # left text column width

    # eyebrow pill
    ef = fnt(lang, "bold", 26)
    et = EYEBROW[lang]
    ew = dr.textlength(et, font=ef)
    dr.rounded_rectangle([LX, 44, LX + ew + 48, 96], 26, fill=PILL_BG)
    dr.text((LX + 24, 70), et, font=ef, fill=PINK, anchor="lm")

    y = 124
    lf = fnt(lang, "regular", 34)
    dr.text((LX, y), LABEL[lang], font=lf, fill=INK_SOFT, anchor="lm")
    y += 44

    # breed (big pink) – shrink to fit one line
    bsize = 92
    while bsize > 48:
        bf = fnt(lang, "bold", bsize)
        if dr.textlength(d["breed"], font=bf) <= LW:
            break
        bsize -= 4
    bf = fnt(lang, "bold", bsize)
    dr.text((LX, y), d["breed"], font=bf, fill=PINK, anchor="lm")
    y += bsize // 2 + 30

    cf = fnt(lang, "bold", 34)
    dr.text((LX, y), f"({code})", font=cf, fill=INK_SOFT, anchor="lm")
    y += 50

    # name headline (wrap up to 2 lines)
    nf = fnt(lang, "bold", 38)
    for ln in wrap(dr, d["name"], nf, LW, space)[:2]:
        dr.text((LX, y), ln, font=nf, fill=INK, anchor="lm")
        y += 48
    y += 6

    # tagline / description (wrap up to 3 lines)
    tf = fnt(lang, "regular", 28)
    for ln in wrap(dr, d["tag"], tf, LW, space)[:3]:
        dr.text((LX, y), ln, font=tf, fill=INK_SOFT, anchor="lm")
        y += 38

    # footer
    ff = fnt(lang, "regular", 26)
    dr.line([LX, H-92, LX+LW, H-92], fill=PINK_BD, width=2)
    dr.text((LX, H-58), f"{SITE}    #{I18N[lang]['hashtag']}", font=ff, fill=INK_SOFT, anchor="lm")

    # ---- right card ----
    CW, CH = 410, 470
    CX, CY = W - CW - 70, (H - CH) // 2
    card = Image.new("RGB", (CW, CH), WHITE)
    cm = rounded_mask((CW, CH), 34)
    img.paste(card, (CX, CY), cm)
    dr.rounded_rectangle([CX, CY, CX+CW, CY+CH], 34, outline=PINK_BD, width=4)

    # dog image (square, rounded)
    dog_path = os.path.join(ROOT, f"{code.lower()}.png")
    DS = 300
    if os.path.exists(dog_path):
        dog = Image.open(dog_path).convert("RGBA")
        s = max(DS / dog.width, DS / dog.height)
        dog = dog.resize((int(dog.width*s), int(dog.height*s)))
        left = (dog.width - DS)//2; top = (dog.height - DS)//2
        dog = dog.crop((left, top, left+DS, top+DS))
        bgsq = Image.new("RGBA", (DS, DS), WHITE + (255,))
        bgsq.alpha_composite(dog)
        img.paste(bgsq.convert("RGB"), (CX + (CW-DS)//2, CY + 36), rounded_mask((DS, DS), 26))

    tcx = CX + CW//2
    cyf = fnt(lang, "bold", 30)
    dr.text((tcx, CY+372), code, font=cyf, fill=INK_SOFT, anchor="mm")
    cbf = fnt(lang, "bold", 36)
    bsz = 36
    while bsz > 22 and dr.textlength(d["breed"], font=fnt(lang, "bold", bsz)) > CW-48:
        bsz -= 2
    dr.text((tcx, CY+412), d["breed"], font=fnt(lang, "bold", bsz), fill=PINK, anchor="mm")
    rrf = fnt(lang, "regular", 24)
    dr.text((tcx, CY+448), RESULT[lang], font=rrf, fill=INK_SOFT, anchor="mm")

    out_dir = os.path.join(ROOT, "ogp", lang)
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, f"{code.lower()}.png"))


REDIRECT = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://16lovetypedogs.com/ogp/{lang}/{slug}.png">
<meta property="og:url" content="https://16lovetypedogs.com/{lang}/{slug}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://16lovetypedogs.com/ogp/{lang}/{slug}.png">
<link rel="canonical" href="https://16lovetypedogs.com/{lang}/{slug}.html">
<script>location.replace('https://16lovetypedogs.com/?type={code}&lang={lang}');</script>
</head>
<body>
<p><a href="https://16lovetypedogs.com/?type={code}&lang={lang}">{cta}</a></p>
</body>
</html>
"""

LOCALE = {"en": "en_US", "zh": "zh_CN"}
OGTITLE = {"en": "My love-dog is {breed} ({code})", "zh": "我的恋爱犬是{breed}（{code}）"}
CTA = {"en": "See your 16 Love-Type Dogs result", "zh": "查看16恋爱犬测验结果"}


def make_page(lang, code):
    d = LOC[lang][code]
    slug = code.lower()
    html = REDIRECT.format(
        lang=lang, slug=slug, code=code, locale=LOCALE[lang],
        title=OGTITLE[lang].format(breed=d["breed"], code=code) + (" | 16 Love-Type Dogs" if lang=="en" else "｜16恋爱犬测验"),
        ogtitle=OGTITLE[lang].format(breed=d["breed"], code=code),
        desc=d["tag"], cta=CTA[lang],
    )
    out_dir = os.path.join(ROOT, lang)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    for lang in ("en", "zh"):
        for code in ORDER:
            make_card(lang, code)
            make_page(lang, code)
    print("generated en/zh OGP cards and share pages for", len(ORDER), "types each")
