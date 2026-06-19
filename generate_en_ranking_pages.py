#!/usr/bin/env python3
"""Generate the 4 missing English ranking pages (devotion/marriage/jealousy/
dokidoki) to complete the EN ranking set alongside the existing
ranking-loyalty-en.html.

Ranking order is parsed from the Japanese source pages; breed names and the
type subtitle come from the translated LOC data in index.html; the per-rank
commentary is translated to natural English here. Stars come from the shared
STARS table.
"""
import re, os, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
LOC = json.loads(re.search(r'\nconst LOC=(\{.*?\});\n', src, re.DOTALL).group(1))
EN = LOC["en"]

STARS = {
 'devotion':{'INTJ':3,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':4,'ENFJ':5,'ENFP':4,'ISTJ':3,'ISFJ':5,'ESTJ':4,'ESFJ':5,'ISTP':2,'ISFP':3,'ESTP':3,'ESFP':4},
 'marriage':{'INTJ':4,'INTP':2,'ENTJ':4,'ENTP':2,'INFJ':4,'INFP':3,'ENFJ':4,'ENFP':2,'ISTJ':5,'ISFJ':5,'ESTJ':5,'ESFJ':4,'ISTP':2,'ISFP':3,'ESTP':2,'ESFP':3},
 'jealousy':{'INTJ':4,'INTP':1,'ENTJ':3,'ENTP':2,'INFJ':3,'INFP':3,'ENFJ':3,'ENFP':4,'ISTJ':2,'ISFJ':3,'ESTJ':3,'ESFJ':5,'ISTP':2,'ISFP':2,'ESTP':3,'ESFP':5},
 'dokidoki':{'INTJ':2,'INTP':2,'ENTJ':3,'ENTP':5,'INFJ':2,'INFP':3,'ENFJ':3,'ENFP':5,'ISTJ':1,'ISFJ':1,'ESTJ':2,'ESFJ':3,'ISTP':3,'ISFP':3,'ESTP':5,'ESFP':5},
}
def stars(n): return "★"*n + "☆"*(5-n)

META = {
 "devotion": {
   "ja_file":"ranking-devotion.html",
   "title":"Most Devoted MBTI Ranking TOP16 – Which love type gives the most? [by dog breed]",
   "sub":"Whose love overflows with care and attention? Meet the most devoted pups.",
   "intro":"Some people simply can't help giving to the one they love. How much you naturally devote yourself in a relationship has a lot to do with your personality type. This ranking lines up MBTI's 16 types, matched to dog breeds, from the most to the least devoted in love."},
 "marriage": {
   "ja_file":"ranking-marriage.html",
   "title":"Best MBTI for Marriage Ranking TOP16 – Which types make you happy as partners? [by dog breed]",
   "sub":"Steady, dependable and warm at home — which pups are built for married life?",
   "intro":"\"Fun to date\" and \"happy to marry\" aren't always the same thing. How well-suited you are to building a stable home depends a lot on your personality type. This ranking lines up MBTI's 16 types, matched to dog breeds, from the most to the least marriage-ready."},
 "jealousy": {
   "ja_file":"ranking-jealousy.html",
   "title":"Most Jealous MBTI Ranking TOP16 – Which love types get the most possessive? [by dog breed]",
   "sub":"A little jealousy can be cute — but who feels it the hardest?",
   "intro":"A pang of jealousy is proof you care, but how strongly it shows depends a lot on your personality type. This ranking lines up MBTI's 16 types, matched to dog breeds, from the most to the least jealous in love."},
 "dokidoki": {
   "ja_file":"ranking-dokidoki.html",
   "title":"Most Exciting MBTI Ranking TOP16 – Which love types keep your heart racing? [by dog breed]",
   "sub":"Never a dull moment — which pups keep the butterflies coming?",
   "intro":"Some partners keep your heart racing every single day. How much excitement you bring to a relationship depends a lot on your personality type. This ranking lines up MBTI's 16 types, matched to dog breeds, from the most to the least thrilling in love."},
}

# English commentary keyed by metric + MBTI code (translated from the JA source)
TX = {
 "devotion": {
  "ENFJ":"The Golden Retriever tops the devotion charts. Your partner's happiness is its own, and it nails every anniversary and tiny kindness. It gives so much it forgets itself, so be sure to give that love back.",
  "ISFJ":"The Shih Tzu is a pro at devoting itself quietly. It notices and acts before you even ask — the kind of care that reaches the exact spot that itches.",
  "ESFJ":"The Labrador shows love straight and without holding back. Frequent messages, home-cooked meals, surprises — it makes sure you really feel adored.",
  "ENTJ":"The Corgi devotes itself through action: protecting, supporting, and leading the way. It's the one you can rely on most when things get hard.",
  "INFJ":"The Cavalier is a delicate giver who reads even the feelings you never put into words. Few are better at caring for your heart.",
  "INFP":"The Maltese is a pure devotee who naturally goes the extra mile for the one it loves. Its no-strings-attached way of loving is its charm.",
  "ENFP":"The Toy Poodle pours out love by enjoying things together. When it comes to planning surprises and events, nobody does it better.",
  "ESTJ":"The Boston Terrier devotes itself through stability and planning. No flash, but its power to support daily life is the real deal.",
  "ESFP":"The Pomeranian loves being adored, but loves delighting its partner just as much. Reactions included, its devotion is pure fun.",
  "INTJ":"The Chihuahua reserves its devotion for the one. The pampering it never shows in public comes out only when you're alone together.",
  "ISTJ":"The Shiba may be short on words, but it shows love through action. Keeping promises, being on time — those small consistencies are its love language.",
  "ISFP":"The French Bulldog heals you simply by being there. Its devotion is less about \"doing\" something and more about \"being\" with you.",
  "ESTP":"The Beagle is the entertainer who brings you fun experiences. On a gloomy day, this is the one that drags you out of the house.",
  "INTP":"The Schnauzer is clumsy at it, but it remembers what you're into better than anyone — an observer at heart. Its rare, well-aimed words land deep.",
  "ENTP":"The Jack Russell entertains more than it devotes. Its gift is a different kind: a life that's never, ever boring.",
  "ISTP":"The Dachshund seems aloof day to day, but when you're truly in trouble it quietly steps up — a \"when it counts\" kind of devotion.",
 },
 "marriage": {
  "ISTJ":"The Shiba keeps its promises and builds trust brick by brick. It never forgets anniversaries and plans both the budget and daily life. The very picture of \"someone safe to marry.\"",
  "ISFJ":"The Shih Tzu sits at the very top for marriage. Quiet attentiveness, devotion and stability — all three — make it a partner who warmly supports everyday life.",
  "ESTJ":"The Boston Terrier runs the \"team\" that is a household with precision. Strong on responsibility, it's the dependable pillar that protects the family.",
  "INTJ":"The Chihuahua treats marriage as a serious life strategy. It's cautious until it decides, but once it does, its stability is outstanding.",
  "ENTJ":"The Corgi reliably leads even the long-term plan for the home. Its planning means you won't be left doing everything alone, even in a two-income household.",
  "INFJ":"The Cavalier is a lifelong partner who can build a deep emotional bond. No flash, but it creates a home full of genuine connection.",
  "ENFJ":"The Golden Retriever finds its own happiness in the family's happiness. It becomes the sun at the center of a warm home.",
  "ESFJ":"The Labrador is a loving type that treasures family occasions. It builds a lively, warm household.",
  "INFP":"The Maltese brings ideals and gentleness into the home — a romantic at heart. With someone it feels safe with, it builds a deeply bonded family.",
  "ISFP":"The Frenchie is a peace-lover who prefers a calm, conflict-free home. The result is a relaxed, easy place to live.",
  "ESFP":"The Pomeranian is the mood-maker who keeps home bright. It makes every day fun — though a partner who helps with planning the chores is a plus.",
  "INTP":"The Schnauzer values its intellectual world over domestic routine. It's comfortable with a partner who can systematize the division of chores.",
  "ENTP":"The Jack Russell is an adventurer who loves freedom and stimulation. It needs a partner who can build a marriage that's \"theirs\" rather than by the book.",
  "ENFP":"The Toy Poodle never wants to lose that dating feeling, even after marriage. It lasts with a partner who enjoys fighting the routine together.",
  "ISTP":"The Dachshund prefers an independent couple dynamic without too much meddling. A grown-up, non-clingy married life suits it best.",
  "ESTP":"The Beagle is the family's fun-and-games department. With energy and drive it creates events at home — the calm settling-down is still to come.",
 },
 "jealousy": {
  "ESFJ":"The Labrador wants to be loved \"just as much\" in return. When it senses the love coming back is thin, jealousy and loneliness surface.",
  "ESFP":"The Pomeranian takes a proud first place. It loves attention and being adored, so when its partner's focus drifts elsewhere, it gets visibly restless. That easy-to-read jealousy is part of the charm.",
  "INTJ":"A surprising high ranker: the Chihuahua. Cool on the surface, but possessiveness quietly grows inside. Since it doesn't say it out loud, it tends to bottle things up.",
  "ENFP":"The Poodle is lively and free, yet secretly prone to loneliness. When messages from its partner slow down, anxiety builds and jealousy slips out.",
  "ENTJ":"The Corgi's possessiveness comes with a competitive streak. When a rival appears, it fights back with drive rather than sulking.",
  "INFJ":"The Cavalier is a deep lover that wants to be the only one. It usually endures, but once it crosses its limit, the feelings quietly overflow.",
  "INFP":"The Maltese feels so deeply that anxiety grows easily too. Unable to say it aloud, it sometimes ends up hurting quietly on its own.",
  "ENFJ":"The Golden puts its partner's happiness ahead of its own jealousy — a selfless love. If anything, the worry is that it endures too much.",
  "ISFJ":"The Shih Tzu hides its jealousy and quietly puts up with it — devoted to a fault. Whether you notice is the key.",
  "ESTJ":"The Boston feels uneasy when a partner's behavior \"doesn't add up.\" Less jealousy, more a matter of order being broken.",
  "ESTP":"The Beagle is refreshingly quick to let go. It may bristle for a second, but the moment something fun comes along it forgets all about it.",
  "ENTP":"The Jack Russell loves the chase, so jealousy feels more like a game. A rival can even become fuel.",
  "ISTJ":"The Shiba dates on a foundation of trust. Doubting is simply not its style — it protects the bond with sincerity rather than jealousy.",
  "ISTP":"The Dachshund is the cool, low-attachment champion. It dislikes both clinging and jealousy, wanting a relationship of freedom and trust.",
  "ISFP":"The Frenchie is a calm peace-lover. It can shrug most things off with a \"meh, whatever\" — a type with little jealousy.",
  "INTP":"The Schnauzer finds jealousy \"irrational\" and meets it with logic. It's not that it doesn't feel it — it analyzes and processes it instead.",
 },
 "dokidoki": {
  "ENTP":"Number one for excitement: the Jack Russell Terrier. Quick-witted talk, unpredictable energy, perfectly timed push-and-pull — \"boring\" simply isn't in its dictionary.",
  "ENFP":"The Poodle is a ball of curiosity and passion. New games, new places, big emotional reactions — the flutter just keeps coming.",
  "ESTP":"The Beagle is a thrill machine that acts the instant it gets an idea. \"Let's go to the beach right now\" actually happens — love with a live, in-the-moment feel.",
  "ESFP":"The Pomeranian is an entertainer who makes every day feel like the main event. Just being together turns the relationship into a celebration.",
  "ENTJ":"The Corgi gives you the thrill of being swept along. Its fast decisions and dependability catch you off guard and make your heart skip.",
  "INFP":"The Maltese sets hearts fluttering with its romantic worldview. Letters, anniversary surprises — it creates moments that stay with you.",
  "ENFJ":"The Golden is a classic source of butterflies. A skilled escort, it turns the feeling of being cherished into pure excitement.",
  "ESFJ":"The Labrador makes you blush with straightforward affection. Its honesty in never sparing a \"love you\" is its weapon.",
  "ISTP":"The Dachshund is cool day to day, but wins you over with how dependable it is when it counts — a slow-acting kind of thrill.",
  "ISFP":"The Frenchie melts you with a sudden, unguarded glimpse of its true self amid all that calm. It creeps up on you over time.",
  "INTJ":"The Chihuahua is all about the gap — cool one moment, sweet the next. The rare flash of clinginess shoots you straight through the heart.",
  "INTP":"The Schnauzer's charm is the intellectual spark of a perspective no one else noticed. Catnip for anyone who loves a clever mind.",
  "INFJ":"The Cavalier sets hearts racing in the moment a deep conversation closes the distance — an emotional, soulful kind of flutter.",
  "ESTJ":"The Boston's appeal is stability, so the excitement is on the milder side. In exchange, you get a love with no fear of betrayal.",
  "ISTJ":"The Shiba is a person of trust over thrills. Light on butterflies, maybe, but it gives you the strongest foundation of all: lasting security.",
  "ISFJ":"The Shih Tzu's excitement comes paired with reassurance. A small, unexpected kindness moves your heart, warmly and gently.",
 },
}

TYPE_COLOR_GRP = {}
for grp,codes in {"NT":["INTJ","INTP","ENTJ","ENTP"],"NF":["INFJ","INFP","ENFJ","ENFP"],
                  "SJ":["ISTJ","ISFJ","ESTJ","ESFJ"],"SP":["ISTP","ISFP","ESTP","ESFP"]}.items():
    for c in codes: TYPE_COLOR_GRP[c]=grp

def parse_order(ja_file):
    s=open(os.path.join(ROOT,ja_file),encoding="utf-8").read()
    items=re.findall(r'(?:<div class="medal"[^>]*>([^<]*)</div>|<div class="no"[^>]*>([0-9]+)</div>).*?src="/([a-z]{4})\.webp"', s, re.DOTALL)
    out=[]
    for med,no,code in items:
        if med:
            rank={"🥇":1,"🥈":2,"🥉":3}.get(med.strip(),1)
            marker=f'<div class="medal" style="font-size:24px">{med.strip()}</div>'
        else:
            rank=int(no)
            marker=f'<div class="no" style="font-family:Baloo 2;font-weight:800;font-size:20px;color:var(--pink-deep)">{no}</div>'
        out.append((rank, marker, code.upper()))
    return out

def esc(s): return html.escape(s, quote=True)

def rank_items(metric):
    order=parse_order(META[metric]["ja_file"])
    blocks=""
    for rank, marker, code in order:
        breed=esc(EN[code]["breed"]); name=esc(EN[code]["name"]); c=code.lower()
        st=stars(STARS[metric][code])
        tx=esc(TX[metric][code])
        blocks+=(f'<div class="rankitem">\n'
          f'  <div class="rk">{marker}<img loading="lazy" decoding="async" src="/{c}.webp" alt="{breed}" style="width:54px;height:auto;border-radius:12px;margin-top:4px" onerror="this.style.display=\'none\'"></div>\n'
          f'  <div class="rbody">\n'
          f'    <div class="nm">#{rank} {breed}（{code}）</div>\n'
          f'    <div class="bd">{name}</div>\n'
          f'    <div class="st" style="color:#c79a3f;font-size:14px;letter-spacing:1.5px">{st}</div>\n'
          f'    <p class="tx" style="font-size:13.5px;line-height:1.8;margin-top:5px">{tx}</p>\n'
          f'    <a href="/type-{c}-en.html" style="font-size:12px;font-weight:700">→ See full profile {breed}</a>\n'
          f'  </div>\n</div>')
    return blocks

ALL = ["loyalty","marriage","jealousy","devotion","dokidoki"]
REL_LABEL = {"loyalty":"Most Loyal MBTI Ranking TOP16","marriage":"Best MBTI for Marriage Ranking TOP16",
             "jealousy":"Most Jealous MBTI Ranking TOP16","devotion":"Most Devoted MBTI Ranking TOP16",
             "dokidoki":"Most Exciting MBTI Ranking TOP16"}

def langbar(metric):
    # only ja + en ranking pages exist; keep langbar to existing targets
    return ('<div class="langbar" style="display:flex;justify-content:center;gap:6px;padding:12px 0;flex-wrap:wrap">'
      f'<a href="ranking-{metric}.html" style="font-size:12.5px;font-weight:700;color:var(--ink-soft);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:5px 13px;text-decoration:none">日本語</a>'
      '<span style="font-size:12.5px;font-weight:800;color:#fff;background:var(--pink-deep);border:2px solid var(--pink-deep);border-radius:999px;padding:5px 13px">English</span>'
      '</div>')

def related(metric):
    out=""
    for m in ALL:
        if m==metric: continue
        out+=(f'<a href="/ranking-{m}-en.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);'
              f'border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">{REL_LABEL[m]}</a>')
    out+=('<a href="/types-en.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);'
          'border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;text-decoration:none">Type List</a>')
    return out

STYLE = open(os.path.join(ROOT,"ranking-loyalty-en.html"),encoding="utf-8").read()
STYLE = re.search(r'<style>(.*?)</style>', STYLE, re.DOTALL).group(1)
# ensure rankitem layout css present (loyalty-en relies on global .rk/.rbody? add safe styles)
EXTRA_CSS = ".rankitem{display:flex;gap:14px;align-items:flex-start;padding:16px 0;border-bottom:1px solid var(--beige)}.rankitem:last-child{border-bottom:0}.rk{flex:0 0 auto;text-align:center;width:60px}.rbody{flex:1 1 auto;min-width:0}.nm{font-weight:800;font-size:15px;color:var(--ink)}.bd{font-size:12.5px;color:var(--ink-soft);font-weight:700;margin:2px 0}"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{sub}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{sub}">
<meta property="og:url" content="https://16lovetypedogs.com/ranking-{metric}-en.html">
<meta property="og:image" content="https://16lovetypedogs.com/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://16lovetypedogs.com/ranking-{metric}-en.html">
<link rel="alternate" hreflang="ja" href="https://16lovetypedogs.com/ranking-{metric}.html">
<link rel="alternate" hreflang="en" href="https://16lovetypedogs.com/ranking-{metric}-en.html">
<link rel="alternate" hreflang="x-default" href="https://16lovetypedogs.com/ranking-{metric}-en.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800&family=Baloo+2:wght@500;700;800&family=Zen+Maru+Gothic:wght@500;700&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9187493483642692" crossorigin="anonymous"></script>
<style>{style}{extra_css}</style>
</head><body>
<header>
  <div class="hinner">
    <a class="site-logo" href="/">🐾 16 Love-Type Dogs</a>
    <nav>
      <a href="/">Take Quiz</a>
      <a href="/types-en.html">Type List</a>
      <a href="/privacy-en.html">Privacy</a>
    </nav>
  </div>
</header><div class="wrap">
  {langbar}
  <div class="breadcrumb"><a href="/">Take Quiz</a> › <a href="/types-en.html">Type List</a> › {short}</div>
  <div class="hero"><h1 style="font-size:clamp(18px,4.5vw,24px);font-weight:800;color:var(--pink-deep);line-height:1.5">{title}</h1><p class="sub">{sub}</p></div>
  <div class="card"><p>{intro}</p><p style="font-size:12.5px;color:var(--ink-soft)">For reference only. Based on the love stats of 16 Love-Type Dogs, for entertainment.</p></div>
  <div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--beige)">Ranking</h2>{items}</div>
  <div class="card" style="text-align:center"><p style="margin-bottom:12px;font-size:14.5px">🐾 16 Love-Type Dogs</p><a class="btn-back" href="/" style="background:var(--pink-deep);color:#fff;border-color:var(--pink-deep)">🐶 Take the quiz</a></div>
  <div class="card"><h2 style="font-size:17px;font-weight:800;color:var(--pink-deep);margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid var(--beige)">Related articles</h2>{related}</div>
  <div class="notice">Rankings and diagnosis results are for entertainment only.</div>
</div>
<script type="application/ld+json">{ldjson}</script>
<footer>
  <div style="margin-bottom:8px"><a href="/">Take Quiz</a> ｜ <a href="/types-en.html">Type List</a> ｜ <a href="/privacy-en.html">Privacy</a></div>
  ※Rankings and diagnosis results are for entertainment only and are not psychological or medical assessments.<br>※This site uses affiliate links (Amazon Associates) and Google AdSense.<br>© 2025 16 Love-Type Dogs / Mymatrix
</footer>
</body></html>
"""

def build(metric):
    M=META[metric]
    short=REL_LABEL[metric]
    ldjson=json.dumps({"@context":"https://schema.org","@type":"Article","headline":M["title"],
        "description":M["sub"],"inLanguage":"en",
        "url":f"https://16lovetypedogs.com/ranking-{metric}-en.html",
        "publisher":{"@type":"Organization","name":"16 Love-Type Dogs","url":"https://16lovetypedogs.com"}},
        ensure_ascii=False)
    out=TEMPLATE.format(title=esc(M["title"]), sub=esc(M["sub"]), intro=esc(M["intro"]),
        metric=metric, style=STYLE, extra_css=EXTRA_CSS, langbar=langbar(metric),
        short=esc(short), items=rank_items(metric), related=related(metric), ldjson=ldjson)
    open(os.path.join(ROOT,f"ranking-{metric}-en.html"),"w",encoding="utf-8").write(out)

if __name__=="__main__":
    for metric in ["devotion","marriage","jealousy","dokidoki"]:
        build(metric)
    print("generated 4 EN ranking pages")
