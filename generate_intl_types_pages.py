#!/usr/bin/env python3
"""Generate localized "all types" hub pages (types-zh/ko/tw.html).

Strengthens internal linking to the 48 zh/ko/tw type pages, fixes the
"Type List" nav target for those languages, and adds 3 indexable hub
pages. Breed names come from the translated LOC data.
"""
import re, os, json, html
ROOT=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(ROOT,"index.html"),encoding="utf-8").read()
LOC=json.loads(re.search(r'\nconst LOC=(\{.*?\});\n',src,re.DOTALL).group(1))

NAV_ORDER=["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
           "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
COLOR={"NT":"#b9a0d6","NF":"#e58aa0","SJ":"#6ec3a0","SP":"#eaa94e"}
def grp(c): return ("N"+("T" if "T" in c else "F")) if "N" in c else ("S"+("J" if "J" in c else "P"))

C={
 "zh":{"htmllang":"zh-CN","locale":"zh_CN","title":"16恋爱犬：全部类型一览","sub":"点击任一只狗狗，查看完整恋爱档案 🐾",
   "site":"🐾 16恋爱犬测验","quiz":"开始测验","types":"类型一览","privacy":"隐私政策","cta":"🐶 开始测验",
   "privacy_href":"/privacy.html",
   "disc":"※诊断结果仅供娱乐，并非心理学或医学诊断。<br>※本站使用联盟链接（Amazon Associates）与 Google AdSense。<br>© 2025 16 Love-Type Dogs / Mymatrix"},
 "ko":{"htmllang":"ko","locale":"ko_KR","title":"16 연애견: 전체 유형 목록","sub":"강아지를 눌러 연애 프로필을 확인해 보세요 🐾",
   "site":"🐾 16 연애견 진단","quiz":"진단하기","types":"유형 목록","privacy":"개인정보처리방침","cta":"🐶 진단하기",
   "privacy_href":"/privacy.html",
   "disc":"※진단 결과는 오락용이며 심리학적·의학적 진단이 아닙니다.<br>※본 사이트는 제휴 링크(Amazon Associates)와 Google AdSense를 사용합니다.<br>© 2025 16 Love-Type Dogs / Mymatrix"},
 "tw":{"htmllang":"zh-TW","locale":"zh_TW","title":"16戀愛犬：全部類型一覽","sub":"點擊任一隻狗狗，查看完整戀愛檔案 🐾",
   "site":"🐾 16戀愛犬測驗","quiz":"開始測驗","types":"類型一覽","privacy":"隱私政策","cta":"🐶 開始測驗",
   "privacy_href":"/privacy.html",
   "disc":"※診斷結果僅供娛樂，並非心理學或醫學診斷。<br>※本站使用聯盟連結（Amazon Associates）與 Google AdSense。<br>© 2025 16 Love-Type Dogs / Mymatrix"},
}
LANG_LABEL={"ja":"日本語","en":"English","ko":"한국어","zh":"简体中文","tw":"繁體中文"}
def types_path(lg): return "types.html" if lg=="ja" else ("types-en.html" if lg=="en" else f"types-{lg}.html")
def esc(s): return html.escape(s,quote=True)

STYLE=re.search(r'<style>(.*?)</style>', open(os.path.join(ROOT,"types-en.html"),encoding="utf-8").read(), re.DOTALL).group(1)

def langbar(cur):
    out=[]
    for lg in ["ja","en","ko","zh","tw"]:
        lab=LANG_LABEL[lg]
        if lg==cur:
            out.append(f'<span style="font-size:12.5px;font-weight:800;color:#fff;background:var(--pink-deep);border:2px solid var(--pink-deep);border-radius:999px;padding:5px 13px">{lab}</span>')
        else:
            out.append(f'<a href="/{types_path(lg)}" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">{lab}</a>')
    return '<div class="langbar" style="display:flex;justify-content:center;gap:6px;padding:12px 0;flex-wrap:wrap">'+"".join(out)+'</div>'

def cards(lang):
    out=""
    for c in NAV_ORDER:
        breed=esc(LOC[lang][c]["breed"]); col=COLOR[grp(c)]; cl=c.lower()
        out+=(f'<a class="typecard" href="/type-{cl}-{lang}.html" style="border-bottom:4px solid {col}">'
              f'<img loading="lazy" decoding="async" src="/{cl}.webp" alt="{breed}" style="width:60px;height:auto;border-radius:10px;margin-bottom:6px" onerror="this.style.display=\'none\'">'
              f'<span class="code">{c}</span><br><span style="color:#3a2e28;font-size:11.5px">{breed}</span></a>')
    return out

def hreflang():
    b="https://16lovetypedogs.com/"
    return "\n".join([
      f'<link rel="alternate" hreflang="ja" href="{b}types.html">',
      f'<link rel="alternate" hreflang="en" href="{b}types-en.html">',
      f'<link rel="alternate" hreflang="ko" href="{b}types-ko.html">',
      f'<link rel="alternate" hreflang="zh-Hans" href="{b}types-zh.html">',
      f'<link rel="alternate" hreflang="zh-Hant" href="{b}types-tw.html">',
      f'<link rel="alternate" hreflang="x-default" href="{b}types-en.html">',
    ])

TEMPLATE="""<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{sub}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{sub}">
<meta property="og:url" content="https://16lovetypedogs.com/{self_path}">
<meta property="og:image" content="https://16lovetypedogs.com/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://16lovetypedogs.com/{self_path}">
{hreflang}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800&family=Baloo+2:wght@500;700;800&family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9187493483642692" crossorigin="anonymous"></script>
<style>{style}</style>
</head><body>
<header>
  <div class="hinner">
    <a class="site-logo" href="/">{site}</a>
    <nav>
      <a href="/">{quiz}</a>
      <a href="/{self_path}">{types}</a>
      <a href="{privacy_href}">{privacy}</a>
    </nav>
  </div>
</header><div class="wrap">{langbar}<div class="hero"><h1 style="font-size:clamp(20px,5vw,24px);font-weight:800;color:var(--pink-deep)">{title}</h1><p class="sub">{sub}</p></div><div class="card"><div class="typegrid">{cards}</div></div><div style="text-align:center;margin-top:22px"><a class="btn-back" href="/">{cta}</a></div></div>
<script type="application/ld+json">{ldjson}</script>
<footer>
  <div style="margin-bottom:8px"><a href="/">{quiz}</a> ｜ <a href="/{self_path}">{types}</a> ｜ <a href="{privacy_href}">{privacy}</a></div>
  {disc}
</footer>
</body></html>
"""

def build(lang):
    cc=C[lang]; sp=types_path(lang)
    ldjson=json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":cc["title"],
        "description":cc["sub"],"inLanguage":cc["htmllang"],
        "url":f"https://16lovetypedogs.com/{sp}",
        "publisher":{"@type":"Organization","name":"16 Love-Type Dogs","url":"https://16lovetypedogs.com"}},ensure_ascii=False)
    out=TEMPLATE.format(htmllang=cc["htmllang"],locale=cc["locale"],title=esc(cc["title"]),sub=esc(cc["sub"]),
        self_path=sp,hreflang=hreflang(),style=STYLE,site=cc["site"],quiz=cc["quiz"],types=cc["types"],
        privacy=cc["privacy"],privacy_href=cc["privacy_href"],langbar=langbar(lang),cards=cards(lang),
        cta=cc["cta"],ldjson=ldjson,disc=cc["disc"])
    open(os.path.join(ROOT,sp),"w",encoding="utf-8").write(out)

if __name__=="__main__":
    for lang in ["zh","ko","tw"]:
        build(lang)
    print("generated types-zh/ko/tw.html")
