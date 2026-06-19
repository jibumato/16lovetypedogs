#!/usr/bin/env python3
"""Generate the 5 Traditional-Chinese (Taiwan) ranking pages.

Reuses the Simplified-Chinese ranking copy and converts it to Traditional
(Taiwan standard) with OpenCC s2tw; breed/type names come from LOC['tw'].
"""
import re, os, json, html, opencc
import generate_zh_ranking_pages as zh

ROOT=os.path.dirname(os.path.abspath(__file__))
LOC=json.loads(re.search(r'\nconst LOC=(\{.*?\});\n',
    open(os.path.join(ROOT,"index.html"),encoding="utf-8").read(),re.DOTALL).group(1))
TW=LOC["tw"]; LANG="tw"
cc=opencc.OpenCC('s2tw')
def t(s): return cc.convert(s)

STARS=zh.STARS; stars=zh.stars
META={m:{"ja":zh.META[m]["ja"],"title":t(zh.META[m]["title"]),"sub":t(zh.META[m]["sub"]),"intro":t(zh.META[m]["intro"])} for m in zh.ALL}
TX={m:{c:t(v) for c,v in zh.TX[m].items()} for m in zh.TX}
REL_LABEL={m:t(v) for m,v in zh.REL_LABEL.items()}
ALL=zh.ALL
CHROME={k:(t(v) if isinstance(v,str) and k not in ("htmllang","locale","types_href","privacy_href") else v)
        for k,v in zh.CHROME.items()}
CHROME["htmllang"]="zh-TW"; CHROME["locale"]="zh_TW"; CHROME["types_href"]="/types-tw.html"
CHROME["site"]="🐾 16戀愛犬測驗"
SELF_LABEL="繁體中文"
OTHER_LANGS=[("ja","日本語","ranking-{m}.html"),("en","English","ranking-{m}-en.html"),
             ("zh","简体中文","ranking-{m}-zh.html"),("ko","한국어","ranking-{m}-ko.html")]

def esc(s): return html.escape(s,quote=True)

def rank_items(metric):
    blocks=""
    for rank,marker,code in zh.parse_order(META[metric]["ja"]):
        breed=esc(TW[code]["breed"]); name=esc(TW[code]["name"]); c=code.lower()
        blocks+=(f'<div class="rankitem">\n  <div class="rk">{marker}<img loading="lazy" decoding="async" src="/{c}.webp" alt="{breed}" style="width:54px;height:auto;border-radius:12px;margin-top:4px" onerror="this.style.display=\'none\'"></div>\n'
          f'  <div class="rbody">\n    <div class="nm">#{rank} {breed}（{code}）</div>\n    <div class="bd">{name}</div>\n'
          f'    <div class="st" style="color:#c79a3f;font-size:14px;letter-spacing:1.5px">{stars(STARS[metric][code])}</div>\n'
          f'    <p class="tx" style="font-size:13.5px;line-height:1.8;margin-top:5px">{esc(TX[metric][code])}</p>\n'
          f'    <a href="/type-{c}-{LANG}.html" style="font-size:12px;font-weight:700">→ {CHROME["profile"]} {breed}</a>\n  </div>\n</div>')
    return blocks

def related(metric):
    out=""
    for m in ALL:
        if m==metric: continue
        out+=(f'<a href="/ranking-{m}-{LANG}.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">{REL_LABEL[m]}</a>')
    out+=(f'<a href="{CHROME["types_href"]}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">{CHROME["types"]}</a>')
    return out

def langbar(metric):
    parts=[]
    for lg,label,patt in OTHER_LANGS:
        parts.append(f'<a href="{patt.format(m=metric)}" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">{label}</a>')
    parts.append(f'<span style="font-size:12.5px;font-weight:800;color:#fff;background:var(--pink-deep);border:2px solid var(--pink-deep);border-radius:999px;padding:5px 13px">{SELF_LABEL}</span>')
    return '<div class="langbar" style="display:flex;justify-content:center;gap:6px;padding:12px 0;flex-wrap:wrap">'+"".join(parts)+'</div>'

STYLE=re.search(r'<style>(.*?)</style>', open(os.path.join(ROOT,"ranking-loyalty-en.html"),encoding="utf-8").read(), re.DOTALL).group(1)
HREF=('<link rel="alternate" hreflang="ja" href="https://16lovetypedogs.com/ranking-{metric}.html">\n'
 '<link rel="alternate" hreflang="en" href="https://16lovetypedogs.com/ranking-{metric}-en.html">\n'
 '<link rel="alternate" hreflang="ko" href="https://16lovetypedogs.com/ranking-{metric}-ko.html">\n'
 '<link rel="alternate" hreflang="zh-Hans" href="https://16lovetypedogs.com/ranking-{metric}-zh.html">\n'
 '<link rel="alternate" hreflang="zh-Hant" href="https://16lovetypedogs.com/ranking-{metric}-tw.html">\n'
 '<link rel="alternate" hreflang="x-default" href="https://16lovetypedogs.com/ranking-{metric}-en.html">')

TEMPLATE=zh.TEMPLATE  # identical structure

def build(metric):
    M=META[metric]
    ldjson=json.dumps({"@context":"https://schema.org","@type":"Article","headline":M["title"],"description":M["sub"],
        "inLanguage":CHROME["htmllang"],"url":f"https://16lovetypedogs.com/ranking-{metric}-{LANG}.html",
        "publisher":{"@type":"Organization","name":"16 Love-Type Dogs","url":"https://16lovetypedogs.com"}},ensure_ascii=False)
    # zh.TEMPLATE has fixed hreflang lines for ja/en/zh; replace that block via our own by formatting then swapping
    out=TEMPLATE.format(htmllang=CHROME["htmllang"],locale=CHROME["locale"],title=esc(M["title"]),sub=esc(M["sub"]),
        intro=esc(M["intro"]),metric=metric,lang=LANG,style=STYLE,site=CHROME["site"],quiz=CHROME["quiz"],
        types=CHROME["types"],types_href=CHROME["types_href"],privacy=CHROME["privacy"],privacy_href=CHROME["privacy_href"],
        langbar=langbar(metric),short=esc(REL_LABEL[metric]),reference=CHROME["reference"],ranking=CHROME["ranking"],
        items=rank_items(metric),cta=CHROME["cta"],related_h=CHROME["related"],related=related(metric),
        ldjson=ldjson,disc=CHROME["disc"])
    # zh.TEMPLATE hardcodes 3 hreflang lines; replace them with the full TW cluster
    out=re.sub(r'<link rel="alternate" hreflang="ja"[^\n]*\n<link rel="alternate" hreflang="en"[^\n]*\n<link rel="alternate" hreflang="zh-Hans"[^\n]*\n<link rel="alternate" hreflang="x-default"[^\n]*',
               HREF.format(metric=metric), out)
    open(os.path.join(ROOT,f"ranking-{metric}-{LANG}.html"),"w",encoding="utf-8").write(out)

if __name__=="__main__":
    for m in ALL: build(m)
    print("generated 5 TW ranking pages")
