#!/usr/bin/env python3
"""Generate 15 missing MBTI type pages for 16わんこ恋愛診断."""

import json
import re
import os

# Read LOC data from index.html
with open('/home/user/16lovetypedogs/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the LOC JSON
loc_match = re.search(r'const LOC=(\{.*?\});', content, re.DOTALL)
if not loc_match:
    raise ValueError("Could not find LOC data in index.html")

loc_json_str = loc_match.group(1)
LOC = json.loads(loc_json_str)
ja_data = LOC['ja']

# Star rating data
STARS = {
    'loyalty': {  # 一途度
        'INTJ': '★★★★★', 'INTP': '★★★★☆', 'ENTJ': '★★★★☆', 'ENTP': '★★☆☆☆',
        'INFJ': '★★★★★', 'INFP': '★★★★★', 'ENFJ': '★★★★☆', 'ENFP': '★★★☆☆',
        'ISTJ': '★★★★★', 'ISFJ': '★★★★★', 'ESTJ': '★★★★☆', 'ESFJ': '★★★★☆',
        'ISTP': '★★★☆☆', 'ISFP': '★★★☆☆', 'ESTP': '★★☆☆☆', 'ESFP': '★★★☆☆',
    },
    'marriage': {  # 結婚向き
        'INTJ': '★★★★☆', 'INTP': '★★☆☆☆', 'ENTJ': '★★★★☆', 'ENTP': '★★☆☆☆',
        'INFJ': '★★★★☆', 'INFP': '★★★☆☆', 'ENFJ': '★★★★☆', 'ENFP': '★★☆☆☆',
        'ISTJ': '★★★★★', 'ISFJ': '★★★★★', 'ESTJ': '★★★★★', 'ESFJ': '★★★★☆',
        'ISTP': '★★☆☆☆', 'ISFP': '★★★☆☆', 'ESTP': '★★☆☆☆', 'ESFP': '★★★☆☆',
    },
    'jealousy': {  # 嫉妬深さ
        'INTJ': '★★★★☆', 'INTP': '★☆☆☆☆', 'ENTJ': '★★★☆☆', 'ENTP': '★★☆☆☆',
        'INFJ': '★★★☆☆', 'INFP': '★★★☆☆', 'ENFJ': '★★★☆☆', 'ENFP': '★★★★☆',
        'ISTJ': '★★☆☆☆', 'ISFJ': '★★★☆☆', 'ESTJ': '★★★☆☆', 'ESFJ': '★★★★★',
        'ISTP': '★★☆☆☆', 'ISFP': '★★☆☆☆', 'ESTP': '★★★☆☆', 'ESFP': '★★★★★',
    },
    'devotion': {  # 尽くし度
        'INTJ': '★★★☆☆', 'INTP': '★★☆☆☆', 'ENTJ': '★★★★☆', 'ENTP': '★★☆☆☆',
        'INFJ': '★★★★☆', 'INFP': '★★★★☆', 'ENFJ': '★★★★★', 'ENFP': '★★★★☆',
        'ISTJ': '★★★☆☆', 'ISFJ': '★★★★★', 'ESTJ': '★★★★☆', 'ESFJ': '★★★★★',
        'ISTP': '★★☆☆☆', 'ISFP': '★★★☆☆', 'ESTP': '★★★☆☆', 'ESFP': '★★★★☆',
    },
    'dokidoki': {  # ドキドキ度
        'INTJ': '★★☆☆☆', 'INTP': '★★☆☆☆', 'ENTJ': '★★★☆☆', 'ENTP': '★★★★★',
        'INFJ': '★★☆☆☆', 'INFP': '★★★☆☆', 'ENFJ': '★★★☆☆', 'ENFP': '★★★★★',
        'ISTJ': '★☆☆☆☆', 'ISFJ': '★☆☆☆☆', 'ESTJ': '★★☆☆☆', 'ESFJ': '★★★☆☆',
        'ISTP': '★★★☆☆', 'ISFP': '★★★☆☆', 'ESTP': '★★★★★', 'ESFP': '★★★★★',
    },
}

# Group data
GROUPS = {
    'NT': {
        'color': '#b9a0d6',
        'members': [
            ('INTJ', 'チワワ'),
            ('INTP', 'ミニチュアシュナウザー'),
            ('ENTJ', 'コーギー'),
            ('ENTP', 'ジャックラッセル・テリア'),
        ]
    },
    'NF': {
        'color': '#f0a0ad',
        'members': [
            ('INFJ', 'キャバリア'),
            ('INFP', 'マルチーズ'),
            ('ENFJ', 'ゴールデン・レトリバー'),
            ('ENFP', 'トイ・プードル'),
        ]
    },
    'SJ': {
        'color': '#9fd6bd',
        'members': [
            ('ISTJ', '柴犬'),
            ('ISFJ', 'シーズー'),
            ('ESTJ', 'ボストン・テリア'),
            ('ESFJ', 'ラブラドール・レトリバー'),
        ]
    },
    'SP': {
        'color': '#f4c781',
        'members': [
            ('ISTP', 'ミニチュア・ダックスフンド'),
            ('ISFP', 'フレンチ・ブルドッグ'),
            ('ESTP', 'ビーグル'),
            ('ESFP', 'ポメラニアン'),
        ]
    },
}

# Navigation order
NAV_ORDER = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP',
]

# Build breed lookup from group data
BREED_LOOKUP = {}
GROUP_LOOKUP = {}
for grp_code, grp_data in GROUPS.items():
    for mbti, breed in grp_data['members']:
        BREED_LOOKUP[mbti] = breed
        GROUP_LOOKUP[mbti] = grp_code

def get_group_color(mbti):
    grp = GROUP_LOOKUP[mbti]
    return GROUPS[grp]['color']

def get_group_members_html(mbti):
    """Generate the same-group type cards, excluding current type."""
    grp = GROUP_LOOKUP[mbti]
    color = GROUPS[grp]['color']
    members = GROUPS[grp]['members']
    cards = []
    for m_mbti, m_breed in members:
        if m_mbti == mbti:
            continue
        img_src = f'/{m_mbti.lower()}.webp'
        href = f'/type-{m_mbti.lower()}.html'
        card = (
            f'<a class="typecard" href="{href}" style="border-bottom:4px solid {color}">'
            f'<img loading="lazy" decoding="async" src="{img_src}" alt="{m_breed}" style="width:54px;height:auto;border-radius:10px;margin-bottom:4px" onerror="this.style.display=\'none\'">'
            f'<span class="code">{m_mbti}</span><br>'
            f'<span style="font-size:11px;color:#3a2e28">{m_breed}</span>'
            f'</a>'
        )
        cards.append(card)
    return '<div class="typegrid">' + ''.join(cards) + '</div>'

def get_nav(mbti):
    idx = NAV_ORDER.index(mbti)
    prev_idx = (idx - 1) % len(NAV_ORDER)
    next_idx = (idx + 1) % len(NAV_ORDER)
    prev_mbti = NAV_ORDER[prev_idx]
    next_mbti = NAV_ORDER[next_idx]
    prev_breed = BREED_LOOKUP[prev_mbti]
    next_breed = BREED_LOOKUP[next_mbti]
    return prev_mbti, prev_breed, next_mbti, next_breed

def generate_page(mbti):
    data = ja_data[mbti]
    breed = BREED_LOOKUP[mbti]
    role = data['role']
    tag = data['tag']
    name = data['name']
    personality = data['personality']
    love = data['love']
    couple = data['couple']
    fight = data['fight']
    pros = data['pros']
    cons = data['cons']
    howto = data['howto']
    hook = data['hook']

    color = get_group_color(mbti)
    mbti_lower = mbti.lower()

    # Stars
    s_loyalty = STARS['loyalty'][mbti]
    s_devotion = STARS['devotion'][mbti]
    s_marriage = STARS['marriage'][mbti]
    s_jealousy = STARS['jealousy'][mbti]
    s_dokidoki = STARS['dokidoki'][mbti]

    # Tags HTML
    pros_tags = ''.join(f'<span class="tag">💗 {p}</span>' for p in pros)
    cons_tags = ''.join(f'<span class="tag con">🦴 {c}</span>' for c in cons)

    # Group section
    group_html = get_group_members_html(mbti)

    # Navigation
    prev_mbti, prev_breed, next_mbti, next_breed = get_nav(mbti)

    # Breadcrumb last segment
    breadcrumb_label = f'{breed}（{mbti}）'

    # Page title and descriptions
    page_title = f'{name}（{mbti}/{breed}）｜16わんこ恋愛診断'
    og_desc = f'{tag}　{hook}'
    # Trim og_desc to reasonable length for OGP
    meta_desc = f'{tag}　{hook}'

    # Article schema headline
    article_headline = f'{name}（{mbti}/{breed}）の恋愛タイプ診断'
    article_desc = tag

    page_url = f'https://16lovetypedogs.com/type-{mbti_lower}.html'

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="ja" href="https://16lovetypedogs.com/type-{mbti_lower}.html">
<link rel="alternate" hreflang="en" href="https://16lovetypedogs.com/type-{mbti_lower}-en.html">
<link rel="alternate" hreflang="ko" href="https://16lovetypedogs.com/type-{mbti_lower}-ko.html">
<link rel="alternate" hreflang="zh-Hans" href="https://16lovetypedogs.com/type-{mbti_lower}-zh.html">
<link rel="alternate" hreflang="zh-Hant" href="https://16lovetypedogs.com/type-{mbti_lower}-tw.html">
<link rel="alternate" hreflang="x-default" href="https://16lovetypedogs.com/type-{mbti_lower}.html">
<meta property="og:type" content="website">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="https://16lovetypedogs.com/ogp.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page_title}">
<meta name="twitter:description" content="{og_desc}">
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
.hero{{text-align:center;padding:36px 0 20px}}
.hero h1{{font-size:clamp(22px,5vw,28px);font-weight:800;color:var(--pink-deep);margin-bottom:8px}}
.hero .sub{{font-size:14px;color:var(--ink-soft)}}
.card{{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:28px 22px;margin-top:22px}}
.card h2{{font-size:18px;font-weight:800;color:var(--pink-deep);margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--beige)}}
.card h3{{font-size:15px;font-weight:800;margin:18px 0 6px;color:var(--ink)}}
.card p{{margin-bottom:10px;line-height:1.85}}
.card ul{{padding-left:1.4em;margin-bottom:10px}}
.card ul li{{margin-bottom:5px;line-height:1.75}}
.pstars{{color:#c79a3f;letter-spacing:2px}}
.taglist{{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}}
.tag{{background:#fff6ee;border:1.5px solid #f0d9b0;border-radius:999px;padding:3px 12px;font-size:12.5px;font-weight:700}}
.tag.con{{background:#fff0f4;border-color:var(--pink)}}
.dogimg{{width:140px;height:auto;border-radius:18px;float:right;margin:0 0 14px 16px;box-shadow:var(--shadow)}}
.clearfix:after{{content:"";display:table;clear:both}}
.typegrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin-top:16px}}
.typecard{{background:#fff;border:2px solid var(--beige);border-radius:16px;padding:12px 8px;text-align:center;font-size:12px;font-weight:700;cursor:pointer;transition:.15s}}
.typecard:hover{{border-color:var(--pink-deep);box-shadow:var(--shadow);text-decoration:none}}
.typecard .em{{font-size:26px;display:block;margin-bottom:4px}}
.typecard .code{{color:var(--pink-deep)}}
.breadcrumb{{font-size:12px;color:var(--ink-soft);margin:14px 0 0;padding:12px 0}}
.breadcrumb a{{color:var(--ink-soft)}}
.btn-back{{display:inline-block;margin-top:22px;font-weight:800;font-size:13.5px;color:var(--pink-deep);background:#fff;border:2px solid var(--beige);border-radius:999px;padding:9px 20px}}
.btn-back:hover{{border-color:var(--pink-deep);text-decoration:none}}
.notice{{background:#fff6ee;border-left:4px solid #e7cf9f;border-radius:10px;padding:12px 14px;font-size:12.5px;color:var(--ink-soft);margin-top:20px;line-height:1.8}}
footer{{margin-top:50px;padding:24px 16px;text-align:center;font-size:11.5px;color:var(--ink-soft);border-top:2px solid var(--beige);line-height:1.9}}
footer a{{color:var(--ink-soft)}}
@media(max-width:480px){{.dogimg{{width:110px}}.card{{padding:20px 14px}}}}
</style>
</head>
<body>
<header>
  <div class="hinner">
    <a class="site-logo" href="/">🐾 16わんこ恋愛診断</a>
    <nav>
      <a href="/">診断する</a>
      <a href="/types.html">タイプ一覧</a>
      <a href="/about.html">運営者情報</a>
      <a href="/privacy.html">プライバシーポリシー</a>
    </nav>
  </div>
</header>

<div class="wrap">
  <div class="breadcrumb">
    <a href="/">ホーム</a> &rsaquo; <a href="/types.html">タイプ一覧</a> &rsaquo; {breadcrumb_label}
  </div>

  <div class="card clearfix" style="border-top:6px solid {color}">
    <img class="dogimg" decoding="async" width="640" height="640" src="/{mbti_lower}.webp" alt="{breed}の恋愛タイプ" onerror="this.style.display='none'">
    <p style="font-size:12px;font-weight:800;color:{color};letter-spacing:.1em;margin-bottom:4px">🐾 恋愛血統書 / {mbti} · {role}</p>
    <h1 style="font-size:clamp(18px,5vw,24px);font-weight:800;margin-bottom:4px">{name}</h1>
    <p style="font-size:17px;font-weight:700;color:#6b5648;margin-bottom:10px">犬種：{breed}</p>
    <p style="background:#fff6ee;border-left:4px solid {color};padding:10px 12px;border-radius:0 10px 10px 0;font-size:14.5px;line-height:1.85">{hook}</p>
  </div>

  <div class="card">
    <h2>恋愛ステータス</h2>
    <table style="width:100%;border-collapse:collapse"><tr><td style="padding:5px 8px;font-weight:700">一途度</td><td style="padding:5px 8px"><span class="pstars">{s_loyalty}</span></td></tr><tr><td style="padding:5px 8px;font-weight:700">尽くし度</td><td style="padding:5px 8px"><span class="pstars">{s_devotion}</span></td></tr><tr><td style="padding:5px 8px;font-weight:700">結婚向き</td><td style="padding:5px 8px"><span class="pstars">{s_marriage}</span></td></tr><tr><td style="padding:5px 8px;font-weight:700">嫉妬深さ</td><td style="padding:5px 8px"><span class="pstars">{s_jealousy}</span></td></tr><tr><td style="padding:5px 8px;font-weight:700">ドキドキ度</td><td style="padding:5px 8px"><span class="pstars">{s_dokidoki}</span></td></tr></table>
  </div>

  <div class="card">
    <h2>性格・特徴</h2>
    <p>{personality}</p>
  </div>

  <div class="card">
    <h2>恋愛傾向</h2>
    <p>{love}</p>
  </div>

  <div class="card">
    <h2>恋人になると</h2>
    <p>{couple}</p>
  </div>

  <div class="card">
    <h2>ケンカした時</h2>
    <p>{fight}</p>
  </div>

  <div class="card">
    <h2>長所</h2>
    <div class="taglist">{pros_tags}</div>
    <h2 style="margin-top:8px">気をつけたいところ</h2>
    <div class="taglist">{cons_tags}</div>
  </div>

  <div class="card">
    <h2>距離の縮め方</h2>
    <p>{howto}</p>
  </div>

  <div class="card">
    <h2>同じグループのわんこ</h2>
    {group_html}
  </div>

  <div style="display:flex;justify-content:space-between;margin-top:22px;gap:8px">
    <a class="btn-back" href="/type-{prev_mbti.lower()}.html">← {prev_breed}</a>
    <a class="btn-back" href="/types.html">一覧へ</a>
    <a class="btn-back" href="/type-{next_mbti.lower()}.html">{next_breed} →</a>
  </div>
  <div style="text-align:center;margin-top:16px">
    <a class="btn-back" href="/" style="background:var(--pink-deep);color:#fff;border-color:var(--pink-deep)">🐶 診断してみる</a>
  </div>

  <div class="notice" style="margin-top:24px">
    ※当サイトはアフィリエイト広告（Amazonアソシエイト含む）を利用しています。<br>
    ※診断結果はエンターテインメント目的であり、心理学的・医学的根拠に基づくものではありません。
  </div>
</div>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Article",
      "headline": "{article_headline}",
      "description": "{article_desc}",
      "url": "{page_url}",
      "datePublished": "2025-01-01",
      "dateModified": "2026-06-19",
      "publisher": {{"@type":"Organization","name":"16わんこ恋愛診断","url":"https://16lovetypedogs.com"}},
      "mainEntityOfPage": "{page_url}"
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"ホーム","item":"https://16lovetypedogs.com/"}},
        {{"@type":"ListItem","position":2,"name":"タイプ一覧","item":"https://16lovetypedogs.com/types.html"}},
        {{"@type":"ListItem","position":3,"name":"{breadcrumb_label}","item":"{page_url}"}}
      ]
    }}
  ]
}}
</script>
<footer>
  <div style="margin-bottom:8px">
    <a href="/">診断トップ</a> ｜ <a href="/types.html">タイプ一覧</a> ｜
    <a href="/about.html">運営者情報</a> ｜ <a href="/privacy.html">プライバシーポリシー</a> ｜
    <a href="/contact.html">お問い合わせ</a>
  </div>
  ※当サイトはアフィリエイト広告（Amazonアソシエイト含む）・Google AdSenseを利用しています。<br>
  © 2025 16わんこ恋愛診断 / Mymatrix (jbmt-22)
</footer>
</body></html>'''
    return html

# Generate all 15 missing pages
MISSING = ['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP',
           'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP']

output_dir = '/home/user/16lovetypedogs'

for mbti in MISSING:
    html = generate_page(mbti)
    filename = f'type-{mbti.lower()}.html'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated: {filename}')

print(f'\nDone! Generated {len(MISSING)} pages.')
