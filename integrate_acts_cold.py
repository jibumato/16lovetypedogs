#!/usr/bin/env python3
"""Integrate mbti-acts-cold-en.html into the entire site."""

import os

BASE = "/home/user/16lovetypedogs"

NEW_TITLE = "MBTI Types That Act Cold When They Like You"
NEW_TITLE_LONG = "MBTI Types That Act Cold When They Like You: Why & How to Reach Them"

# ─── 1. Ranking pages ────────────────────────────────────────────────────────
RANKING_FILES = [
    "ranking-devotion-en.html",
    "ranking-dokidoki-en.html",
    "ranking-jealousy-en.html",
    "ranking-loyalty-en.html",
    "ranking-marriage-en.html",
]

RANKING_OLD = (
    '<a href="/mbti-ideal-date-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'Perfect Date Ideas for Every MBTI Type</a></div>'
)
RANKING_NEW = (
    RANKING_OLD
    + '\n      <a href="/mbti-acts-cold-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI Types That Act Cold When They Like You</a></div>'
)

for fname in RANKING_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-acts-cold-en" in text:
        print(f"SKIP: {fname}")
        continue
    if RANKING_OLD not in text:
        print(f"WARN (pattern not found): {fname}")
        continue
    text = text.replace(RANKING_OLD, RANKING_NEW, 1)
    open(path, "w", encoding="utf-8").write(text)
    print(f"OK ranking: {fname}")

# ─── 2. Type pages ────────────────────────────────────────────────────────────
TYPE_FILES = (
    [f"type-{t}-en.html" for t in [
        "intj","intp","entj","entp","infj","infp","enfj","enfp",
        "istj","isfj","estj","esfj","istp","isfp","estp","esfp"
    ]]
    + ["types-en.html"]
)

TYPE_OLD_PLAIN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type</a>'
    '</li></ul></div></div>'
)
TYPE_NEW_PLAIN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type</a>'
    '</li>\n              '
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-acts-cold-en.html">MBTI Types That Act Cold When They Like You</a>'
    '</li></ul></div></div>'
)

# types-en.html variant
TYPE_OLD_TYPESEN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type</a>'
    '</li></ul></div>\n</div>'
)
TYPE_NEW_TYPESEN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type</a>'
    '</li>\n              '
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-acts-cold-en.html">MBTI Types That Act Cold When They Like You</a>'
    '</li></ul></div>\n</div>'
)

for fname in TYPE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-acts-cold-en" in text:
        print(f"SKIP: {fname}")
        continue
    if fname == "types-en.html":
        if TYPE_OLD_TYPESEN not in text:
            print(f"WARN types-en.html pattern not found")
            idx = text.find("/mbti-ideal-date-en.html")
            if idx >= 0:
                print(f"  Context: {repr(text[idx-10:idx+120])}")
        else:
            text = text.replace(TYPE_OLD_TYPESEN, TYPE_NEW_TYPESEN, 1)
            open(path, "w", encoding="utf-8").write(text)
            print(f"OK: {fname}")
        continue
    if TYPE_OLD_PLAIN not in text:
        print(f"WARN: {fname}")
        continue
    text = text.replace(TYPE_OLD_PLAIN, TYPE_NEW_PLAIN, 1)
    open(path, "w", encoding="utf-8").write(text)
    print(f"OK: {fname}")

# ─── 3. Guide pages ──────────────────────────────────────────────────────────
GUIDE_FILES = [
    "mbti-compatibility-en.html",
    "mbti-jealousy-en.html",
    "mbti-dating-tips-en.html",
    "mbti-crush-en.html",
    "mbti-cheating-en.html",
    "mbti-losing-interest-en.html",
    "mbti-breakup-en.html",
    "mbti-exback-en.html",
    "mbti-fight-en.html",
    "mbti-signs-en.html",
    "mbti-long-distance-en.html",
    "mbti-texting-en.html",
    "mbti-marriage-en.html",
    "mbti-ideal-date-en.html",
]

GUIDE_IDEAL_DATE_LINK = (
    '<a href="/mbti-ideal-date-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'Perfect Date Ideas for Every MBTI Type</a>'
)
ACTS_COLD_LINK = (
    '\n<a href="/mbti-acts-cold-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI Types That Act Cold When They Like You</a>'
)

for fname in GUIDE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-acts-cold-en" in text:
        print(f"SKIP: {fname}")
        continue
    if GUIDE_IDEAL_DATE_LINK not in text:
        print(f"WARN (ideal-date pattern not found): {fname}")
        continue
    text = text.replace(GUIDE_IDEAL_DATE_LINK, GUIDE_IDEAL_DATE_LINK + ACTS_COLD_LINK, 1)
    open(path, "w", encoding="utf-8").write(text)
    print(f"OK guide: {fname}")

# ─── 4. mbti-suki-noni-tsumeta.html hreflang + multilingual card ─────────────
src_path = os.path.join(BASE, "mbti-suki-noni-tsumeta.html")
src_text = open(src_path, encoding="utf-8").read()

if "hreflang" not in src_text:
    CANONICAL = '<link rel="canonical" href="https://16lovetypedogs.com/mbti-suki-noni-tsumeta.html">'
    HREFLANG_BLOCK = (
        CANONICAL + "\n"
        + '  <link rel="alternate" hreflang="ja" href="https://16lovetypedogs.com/mbti-suki-noni-tsumeta.html">\n'
        + '  <link rel="alternate" hreflang="en" href="https://16lovetypedogs.com/mbti-acts-cold-en.html">\n'
        + '  <link rel="alternate" hreflang="x-default" href="https://16lovetypedogs.com/mbti-acts-cold-en.html">'
    )
    src_text = src_text.replace(CANONICAL, HREFLANG_BLOCK, 1)
    print("OK hreflang: mbti-suki-noni-tsumeta.html")
else:
    print("SKIP hreflang (already present)")

if "mbti-acts-cold-en" not in src_text:
    RELATED_H2 = '<h2 style="font-size:16px;font-weight:800;margin-bottom:12px">📰 関連記事</h2>'
    MULTI_CARD = (
        '<div class="card" style="background:#f0f8ff;border:1.5px solid #b0d0ef;margin-top:22px">\n'
        '    <h2 style="font-size:16px;font-weight:800;margin-bottom:8px">🌐 他の言語でも読む</h2>\n'
        '    <ul style="padding-left:1.4em;margin:0;font-size:13px;line-height:2">\n'
        '      <li><a href="/mbti-acts-cold-en.html">MBTI Types That Act Cold When They Like You (English)</a></li>\n'
        '    </ul>\n'
        '  </div>\n\n  '
        + RELATED_H2
    )
    src_text = src_text.replace(RELATED_H2, MULTI_CARD, 1)
    print("OK multilingual card: mbti-suki-noni-tsumeta.html")
else:
    print("SKIP multilingual card (already present)")

open(src_path, "w", encoding="utf-8").write(src_text)

# ─── 5. sitemap.xml ──────────────────────────────────────────────────────────
sitemap_path = os.path.join(BASE, "sitemap.xml")
sitemap = open(sitemap_path, encoding="utf-8").read()

if "mbti-acts-cold-en" not in sitemap:
    IDEAL_DATE_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-ideal-date-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    ACTS_COLD_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-acts-cold-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    sitemap = sitemap.replace(IDEAL_DATE_ENTRY, IDEAL_DATE_ENTRY + "\n" + ACTS_COLD_ENTRY, 1)
    open(sitemap_path, "w", encoding="utf-8").write(sitemap)
    print("OK sitemap.xml")
else:
    print("SKIP sitemap.xml")

# ─── 6. index.html ───────────────────────────────────────────────────────────
index_path = os.path.join(BASE, "index.html")
index = open(index_path, encoding="utf-8").read()

if "mbti-acts-cold-en" not in index:
    IDEAL_DATE_LI = '<li><a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type: What Each Type Actually Wants (English)</a></li>'
    ACTS_COLD_LI = '\n<li><a href="/mbti-acts-cold-en.html">MBTI Types That Act Cold When They Like You: Why &amp; How to Reach Them (English)</a></li>'
    index = index.replace(IDEAL_DATE_LI, IDEAL_DATE_LI + ACTS_COLD_LI, 1)
    open(index_path, "w", encoding="utf-8").write(index)
    print("OK index.html")
else:
    print("SKIP index.html")

print("\nDone!")
