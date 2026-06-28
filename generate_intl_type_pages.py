#!/usr/bin/env python3
"""Generate international (en/zh/ko/tw) MBTI type landing pages.

Content (personality / love / couple / fight / howto / pros / cons / hook)
is sourced verbatim from the already-translated LOC data embedded in
index.html, so these are full content pages, not thin/duplicate stubs.
Only the UI chrome (section headings, nav, footer) is localized here.

Outputs: type-<code>-<lang>.html for lang in {en, zh, ko, tw}.
Also wires the hreflang cluster across ja/en/ko/zh-Hans/zh-Hant.
"""
import json, re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
LOC = json.loads(re.search(r'\nconst LOC=(\{.*?\});\n', src, re.DOTALL).group(1))

NAV_ORDER = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
             "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
GROUP_OF = {}
GROUP_COLOR = {"NT":"#b9a0d6","NF":"#f0a0ad","SJ":"#9fd6bd","SP":"#f4c781"}
for code in NAV_ORDER:
    n,s,t,j = code[0],code[1],code[2],code[3]
    GROUP_OF[code] = (("N"+("T" if "T" in code else "F")) if "N" in code
                      else ("S"+("J" if "J" in code else "P")))
GROUPS = {"NT":["INTJ","INTP","ENTJ","ENTP"],"NF":["INFJ","INFP","ENFJ","ENFP"],
          "SJ":["ISTJ","ISFJ","ESTJ","ESFJ"],"SP":["ISTP","ISFP","ESTP","ESFP"]}

# star ratings (shared across languages)
STARS = {
 'loyalty':{'INTJ':5,'INTP':4,'ENTJ':4,'ENTP':2,'INFJ':5,'INFP':5,'ENFJ':4,'ENFP':3,'ISTJ':5,'ISFJ':5,'ESTJ':4,'ESFJ':4,'ISTP':3,'ISFP':3,'ESTP':2,'ESFP':3},
 'devotion':{'INTJ':3,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':4,'ENFJ':5,'ENFP':4,'ISTJ':3,'ISFJ':5,'ESTJ':4,'ESFJ':5,'ISTP':2,'ISFP':3,'ESTP':3,'ESFP':4},
 'marriage':{'INTJ':4,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':3,'ENFJ':4,'ENFP':2,'ISTJ':5,'ISFJ':5,'ESTJ':5,'ESFJ':4,'ISTP':2,'ISFP':3,'ESTP':2,'ESFP':3},
 'jealousy':{'INTJ':4,'INTP':1,'ENTJ':3,'ENTP':2,'INFJ':3,'INFP':3,'ENFJ':3,'ENFP':4,'ISTJ':2,'ISFJ':3,'ESTJ':3,'ESFJ':5,'ISTP':2,'ISFP':2,'ESTP':3,'ESFP':5},
 'dokidoki':{'INTJ':2,'INTP':2,'ENTJ':3,'ENTP':5,'INFJ':2,'INFP':3,'ENFJ':3,'ENFP':5,'ISTJ':1,'ISFJ':1,'ESTJ':2,'ESFJ':3,'ISTP':3,'ISFP':3,'ESTP':5,'ESFP':5},
}
def stars(n): return "★"*n + "☆"*(5-n)

# per-language chrome
LANGS = {
 "en": {"htmllang":"en","locale":"en_US","suffix":" | 16 Love-Type Dogs","site":"🐾 16 Love-Type Dogs",
   "pedigree":"Love Pedigree","stats":"Love Stats",
   "stat_labels":["Loyalty","Devotion","Marriage","Jealousy","Excitement"],
   "personality":"Personality","love":"In Love","date":"When You Date","fight":"When You Fight",
   "howto":"How to Get Closer","strengths":"Strengths","watch":"Watch out for","group":"Same-group dogs",
   "all_types":"All types","cta":"🐶 Take the quiz","nav_quiz":"Take Quiz","nav_types":"Type List","privacy":"Privacy",
   "breed_label":"Breed",
   "types_href":"/types-en.html","privacy_href":"/privacy-en.html",
   "disclaimer":"※Diagnosis results are for entertainment only and are not psychological or medical assessments.<br>※This site uses affiliate links (Amazon Associates) and Google AdSense.<br>© 2025 16 Love-Type Dogs / Mymatrix",
   "space":True},
 "zh": {"htmllang":"zh-CN","locale":"zh_CN","suffix":"｜16恋爱犬测验","site":"🐾 16恋爱犬测验",
   "pedigree":"恋爱血统书","stats":"恋爱属性",
   "stat_labels":["专一度","奉献度","结婚倾向","嫉妒心","心动度"],
   "personality":"性格","love":"恋爱倾向","date":"成为恋人时","fight":"吵架时",
   "howto":"拉近距离的方法","strengths":"优点","watch":"注意点","group":"同组的恋爱犬",
   "all_types":"全部类型","cta":"🐶 开始测验","nav_quiz":"开始测验","nav_types":"类型一览","privacy":"隐私政策",
   "breed_label":"犬种",
   "types_href":"/types-zh.html","privacy_href":"/privacy.html",
   "disclaimer":"※诊断结果仅供娱乐，并非心理学或医学诊断。<br>※本站使用联盟链接（Amazon Associates）与 Google AdSense。<br>© 2025 16 Love-Type Dogs / Mymatrix",
   "space":False},
 "ko": {"htmllang":"ko","locale":"ko_KR","suffix":"｜16 연애견 진단","site":"🐾 16 연애견 진단",
   "pedigree":"연애 혈통서","stats":"연애 스탯",
   "stat_labels":["일편단심","헌신도","결혼 적합도","질투심","설렘도"],
   "personality":"성격","love":"연애 성향","date":"연인이 되면","fight":"다툴 때",
   "howto":"가까워지는 법","strengths":"장점","watch":"주의할 점","group":"같은 그룹의 연애견",
   "all_types":"전체 유형","cta":"🐶 진단하기","nav_quiz":"진단하기","nav_types":"유형 목록","privacy":"개인정보처리방침",
   "breed_label":"견종",
   "types_href":"/types-ko.html","privacy_href":"/privacy.html",
   "disclaimer":"※진단 결과는 오락용이며 심리학적·의학적 진단이 아닙니다.<br>※본 사이트는 제휴 링크(Amazon Associates)와 Google AdSense를 사용합니다.<br>© 2025 16 Love-Type Dogs / Mymatrix",
   "space":False},
 "tw": {"htmllang":"zh-TW","locale":"zh_TW","suffix":"｜16戀愛犬測驗","site":"🐾 16戀愛犬測驗",
   "pedigree":"戀愛血統書","stats":"戀愛屬性",
   "stat_labels":["專一度","奉獻度","結婚傾向","嫉妒心","心動度"],
   "personality":"性格","love":"戀愛傾向","date":"成為戀人時","fight":"吵架時",
   "howto":"拉近距離的方法","strengths":"優點","watch":"注意點","group":"同組的戀愛犬",
   "all_types":"全部類型","cta":"🐶 開始測驗","nav_quiz":"開始測驗","nav_types":"類型一覽","privacy":"隱私政策",
   "breed_label":"犬種",
   "types_href":"/types-tw.html","privacy_href":"/privacy.html",
   "disclaimer":"※診斷結果僅供娛樂，並非心理學或醫學診斷。<br>※本站使用聯盟連結（Amazon Associates）與 Google AdSense。<br>© 2025 16 Love-Type Dogs / Mymatrix",
   "space":False},
}
LANG_LABEL = {"ja":"日本語","en":"English","ko":"한국어","zh":"简体中文","tw":"繁體中文"}

def page_path(lang, code):
    return f"type-{code.lower()}.html" if lang=="ja" else f"type-{code.lower()}-{lang}.html"

def hreflang_block(code):
    base="https://16lovetypedogs.com/"
    return "\n".join([
      f'<link rel="alternate" hreflang="ja" href="{base}{page_path("ja",code)}">',
      f'<link rel="alternate" hreflang="en" href="{base}{page_path("en",code)}">',
      f'<link rel="alternate" hreflang="ko" href="{base}{page_path("ko",code)}">',
      f'<link rel="alternate" hreflang="zh-Hans" href="{base}{page_path("zh",code)}">',
      f'<link rel="alternate" hreflang="zh-Hant" href="{base}{page_path("tw",code)}">',
      f'<link rel="alternate" hreflang="x-default" href="{base}{page_path("en",code)}">',
    ])

def esc(s): return html.escape(s, quote=True)

def langbar(code, cur):
    out=[]
    for lg in ["ja","en","ko","zh","tw"]:
        label=LANG_LABEL[lg]
        if lg==cur:
            out.append(f'<span style="font-size:12.5px;font-weight:800;color:#fff;background:var(--pink-deep);border:2px solid var(--pink-deep);border-radius:999px;padding:5px 13px">{label}</span>')
        else:
            out.append(f'<a href="/{page_path(lg,code)}" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">{label}</a>')
    return ('<div class="langbar" style="display:flex;justify-content:center;gap:6px;padding:12px 0;flex-wrap:wrap">'
            + "".join(out) + '</div>')

def stat_table(code, C):
    keys=["loyalty","devotion","marriage","jealousy","dokidoki"]
    rows=""
    for lbl,k in zip(C["stat_labels"], keys):
        rows+=(f'<tr><td style="padding:5px 8px;font-weight:700">{lbl}</td>'
               f'<td style="padding:5px 8px"><span style="color:#c79a3f;font-size:14px">{stars(STARS[k][code])}</span></td></tr>')
    return f'<table style="width:100%;border-collapse:collapse">{rows}</table>'

def section(head, body):
    return (f'<div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);'
            f'margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{head}</h2>'
            f'<p>{body}</p></div>')

def group_cards(code, lang, C, color):
    grp=GROUP_OF[code]; out=""
    for m in GROUPS[grp]:
        if m==code: continue
        mb=esc(LOC[lang][m]["breed"])
        out+=(f'<a class="typecard" href="/{page_path(lang,m)}" style="border-bottom:4px solid {color}">'
              f'<img loading="lazy" decoding="async" src="/{m.lower()}.webp" alt="{mb}" '
              f'style="width:54px;height:auto;border-radius:10px;margin-bottom:4px" onerror="this.style.display=\'none\'">'
              f'<span class="code">{m}</span><br>'
              f'<span style="font-size:11px;color:#3a2e28">{mb}</span></a>')
    return f'<div class="typegrid">{out}</div>'

def prevnext(code, lang, C):
    i=NAV_ORDER.index(code)
    prev=NAV_ORDER[(i-1)%16]; nxt=NAV_ORDER[(i+1)%16]
    pb=esc(LOC[lang][prev]["breed"]); nb=esc(LOC[lang][nxt]["breed"])
    return (f'<div style="display:flex;justify-content:space-between;margin-top:20px;gap:8px">'
            f'<a class="btn-back" href="/{page_path(lang,prev)}">← {pb}</a>'
            f'<a class="btn-back" href="{C["types_href"]}">{C["all_types"]}</a>'
            f'<a class="btn-back" href="/{page_path(lang,nxt)}">{nb} →</a></div>')

TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://16lovetypedogs.com/{self_path}">
<meta property="og:image" content="https://16lovetypedogs.com/ogp/{lang}/{code_lower}.png?v=3">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://16lovetypedogs.com/ogp/{lang}/{code_lower}.png?v=3">
<link rel="canonical" href="https://16lovetypedogs.com/{self_path}">
{hreflang}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800&family=Baloo+2:wght@500;700;800&family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9187493483642692" crossorigin="anonymous"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--pink:#f4b8cb;--pink-deep:#e58aa0;--beige:#f0e0d0;--ink:#3a2e28;--ink-soft:#7a6258;--bg:#fff9f5;--radius:22px;--shadow:0 6px 22px rgba(100,60,40,.10)}}
body{{font-family:'M PLUS Rounded 1c','Zen Maru Gothic',sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;font-size:15px}}
a{{color:var(--pink-deep);text-decoration:none}}a:hover{{text-decoration:underline}}
.wrap{{max-width:700px;margin:0 auto;padding:0 14px 60px}}
header{{background:#fff;border-bottom:2px solid var(--beige);padding:12px 16px;position:sticky;top:0;z-index:100}}
.hinner{{max-width:700px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px}}
.site-logo{{font-family:'Baloo 2',sans-serif;font-weight:800;font-size:17px;color:var(--pink-deep);text-decoration:none}}
nav{{display:flex;gap:6px;flex-wrap:wrap}}
nav a{{font-size:12px;font-weight:700;color:var(--ink-soft);background:var(--bg);border:1.5px solid var(--beige);border-radius:999px;padding:4px 10px}}
nav a:hover{{border-color:var(--pink);text-decoration:none;color:var(--pink-deep)}}
.card{{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:28px 22px;margin-top:22px}}
.card h2{{font-size:18px;font-weight:800;color:var(--pink-deep);margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--beige)}}
.card p{{margin-bottom:10px;line-height:1.85}}
.taglist{{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}}
.tag{{background:#fff6ee;border:1.5px solid #f0d9b0;border-radius:999px;padding:3px 12px;font-size:12.5px;font-weight:700}}
.tag.con{{background:#fff0f4;border-color:var(--pink)}}
.dogimg{{width:140px;height:auto;border-radius:18px;float:right;margin:0 0 14px 16px;box-shadow:var(--shadow)}}
.clearfix:after{{content:"";display:table;clear:both}}
.typegrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin-top:16px}}
.typecard{{background:#fff;border:2px solid var(--beige);border-radius:16px;padding:12px 8px;text-align:center;font-size:12px;font-weight:700;cursor:pointer;transition:.15s}}
.typecard:hover{{border-color:var(--pink-deep);box-shadow:var(--shadow);text-decoration:none}}
.typecard .code{{color:var(--pink-deep)}}
.breadcrumb{{font-size:12px;color:var(--ink-soft);margin:14px 0 0;padding:12px 0}}
.breadcrumb a{{color:var(--ink-soft)}}
.btn-back{{display:inline-block;margin-top:22px;font-weight:800;font-size:13.5px;color:var(--pink-deep);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:9px 20px}}
.btn-back:hover{{border-color:var(--pink-deep);text-decoration:none}}
footer{{margin-top:50px;padding:24px 16px;text-align:center;font-size:11.5px;color:var(--ink-soft);border-top:2px solid var(--beige);line-height:1.9}}
footer a{{color:var(--ink-soft)}}
@media(max-width:480px){{.dogimg{{width:110px}}.card{{padding:20px 14px}}}}
</style>
</head><body>
<header>
  <div class="hinner">
    <a class="site-logo" href="/">{site}</a>
    <nav>
      <a href="/">{nav_quiz}</a>
      <a href="{types_href}">{nav_types}</a>
      <a href="{privacy_href}">{privacy}</a>
    </nav>
  </div>
</header><div class="wrap">
  {langbar}
  <div class="breadcrumb"><a href="/">{nav_quiz}</a> › <a href="{types_href}">{nav_types}</a> › {breed}（{code}）</div>
  <div class="card clearfix" style="border-top:6px solid {color}">
    <img decoding="async" class="dogimg" src="/{code_lower}.webp" alt="{breed}" onerror="this.style.display='none'">
    <p style="font-size:12px;font-weight:800;color:{color};letter-spacing:.1em;margin-bottom:4px">🐾 {pedigree} 🐾 {code} · {role}</p>
    <h1 style="font-size:clamp(17px,4.5vw,22px);font-weight:800;margin-bottom:4px">{name}</h1>
    <p style="font-size:16px;font-weight:700;color:#6b5648;margin-bottom:8px">{breed_label}：{breed}</p>
    <p style="background:#fff6ee;border-left:4px solid {color};padding:10px 12px;border-radius:0 10px 10px 0;font-size:14px;line-height:1.85">{hook}</p>
  </div>
  <div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{stats}</h2>{stat_table}</div>
  {personality}{love}{date}{fight}{howto}
  <div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{strengths}</h2><div class="taglist">{pros}</div><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin:14px 0 10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{watch}</h2><div class="taglist">{cons}</div></div>
  <div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">{group}</h2>{group_cards}</div>
  {prevnext}
  <div style="text-align:center;margin-top:14px"><a class="btn-back" href="/" style="background:var(--pink-deep);color:#fff;border-color:var(--pink-deep)">{cta}</a></div>
</div>
<script type="application/ld+json">{ldjson}</script>
<footer>
  <div style="margin-bottom:8px"><a href="/">{nav_quiz}</a> ｜ <a href="{types_href}">{nav_types}</a> ｜ <a href="{privacy_href}">{privacy}</a></div>
  {disclaimer}
</footer>
</body></html>
"""

def build(lang, code):
    C=LANGS[lang]; d=LOC[lang][code]; color=GROUP_COLOR[GROUP_OF[code]]
    name=esc(d["name"]); breed=esc(d["breed"]); role=esc(d["role"])
    tag=esc(d["tag"]); hook=esc(d["hook"])
    title=f'{name}（{code}/{breed}）{C["suffix"]}'
    pros="".join(f'<span class="tag">💗 {esc(p)}</span>' for p in d["pros"])
    cons="".join(f'<span class="tag con">🦴 {esc(c)}</span>' for c in d["cons"])
    ldjson=json.dumps({"@context":"https://schema.org","@type":"Article",
        "headline":f'{d["name"]}（{code}/{d["breed"]}）',"description":d["tag"],
        "inLanguage":C["htmllang"],
        "url":f'https://16lovetypedogs.com/{page_path(lang,code)}',
        "publisher":{"@type":"Organization","name":"16 Love-Type Dogs","url":"https://16lovetypedogs.com"}},
        ensure_ascii=False)
    out=TEMPLATE.format(
        htmllang=C["htmllang"], locale=C["locale"], lang=lang, code=code, code_lower=code.lower(),
        self_path=page_path(lang,code), title=title, desc=tag, hreflang=hreflang_block(code),
        site=C["site"], nav_quiz=C["nav_quiz"], nav_types=C["nav_types"], privacy=C["privacy"],
        types_href=C["types_href"], privacy_href=C["privacy_href"],
        langbar=langbar(code,lang), breed=breed, color=color, pedigree=C["pedigree"], role=role,
        name=name, breed_label=C["breed_label"], hook=hook, stats=C["stats"], stat_table=stat_table(code,C),
        personality=section(C["personality"], esc(d["personality"])),
        love=section(C["love"], esc(d["love"])),
        date=section(C["date"], esc(d["couple"])),
        fight=section(C["fight"], esc(d["fight"])),
        howto=section(C["howto"], esc(d["howto"])),
        strengths=C["strengths"], pros=pros, watch=C["watch"], cons=cons,
        group=C["group"], group_cards=group_cards(code,lang,C,color),
        prevnext=prevnext(code,lang,C), cta=C["cta"], ldjson=ldjson, disclaimer=C["disclaimer"],
    )
    open(os.path.join(ROOT, page_path(lang,code)), "w", encoding="utf-8").write(out)

if __name__=="__main__":
    n=0
    for lang in ["en","zh","ko","tw"]:
        for code in NAV_ORDER:
            build(lang, code); n+=1
    print(f"generated {n} intl type pages (en/zh/ko/tw x16)")
