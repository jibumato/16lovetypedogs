#!/usr/bin/env python3
"""Integrate mbti-approach-en.html into the entire site."""

import os

BASE = "/home/user/16lovetypedogs"

# ─── 1. Ranking pages ────────────────────────────────────────────────────────
RANKING_FILES = [
    "ranking-devotion-en.html",
    "ranking-dokidoki-en.html",
    "ranking-jealousy-en.html",
    "ranking-loyalty-en.html",
    "ranking-marriage-en.html",
]

RANKING_OLD = (
    '<a href="/mbti-love-language-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI Love Languages: How Each Type Gives &amp; Receives Love</a></div>'
)
RANKING_NEW = (
    RANKING_OLD
    + '\n      <a href="/mbti-approach-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'How to Approach Each MBTI Type: Win Their Heart</a></div>'
)

for fname in RANKING_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-approach-en" in text:
        print(f"SKIP: {fname}")
        continue
    if RANKING_OLD not in text:
        print(f"WARN: {fname}")
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
    '<a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
    '</li></ul></div></div>'
)
TYPE_NEW_PLAIN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
    '</li>\n              '
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-approach-en.html">How to Approach Each MBTI Type: Win Their Heart</a>'
    '</li></ul></div></div>'
)

TYPE_OLD_TYPESEN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
    '</li></ul></div>\n</div>'
)
TYPE_NEW_TYPESEN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
    '</li>\n              '
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-approach-en.html">How to Approach Each MBTI Type: Win Their Heart</a>'
    '</li></ul></div>\n</div>'
)

for fname in TYPE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-approach-en" in text:
        print(f"SKIP: {fname}")
        continue
    if fname == "types-en.html":
        if TYPE_OLD_TYPESEN not in text:
            print(f"WARN types-en.html pattern not found")
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
    "mbti-acts-cold-en.html",
    "mbti-confess-en.html",
    "mbti-love-language-en.html",
]

LOVE_LANG_LINK = (
    '<a href="/mbti-love-language-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
)
APPROACH_LINK = (
    '\n<a href="/mbti-approach-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'How to Approach Each MBTI Type: Win Their Heart</a>'
)

for fname in GUIDE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-approach-en" in text:
        print(f"SKIP: {fname}")
        continue
    if LOVE_LANG_LINK not in text:
        print(f"WARN (love-language pattern not found): {fname}")
        continue
    text = text.replace(LOVE_LANG_LINK, LOVE_LANG_LINK + APPROACH_LINK, 1)
    open(path, "w", encoding="utf-8").write(text)
    print(f"OK guide: {fname}")

# ─── 4. sitemap.xml ──────────────────────────────────────────────────────────
sitemap_path = os.path.join(BASE, "sitemap.xml")
sitemap = open(sitemap_path, encoding="utf-8").read()

if "mbti-approach-en" not in sitemap:
    LOVE_LANG_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-love-language-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    APPROACH_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-approach-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    sitemap = sitemap.replace(LOVE_LANG_ENTRY, LOVE_LANG_ENTRY + "\n" + APPROACH_ENTRY, 1)
    open(sitemap_path, "w", encoding="utf-8").write(sitemap)
    print("OK sitemap.xml")
else:
    print("SKIP sitemap.xml")

# ─── 5. index.html ───────────────────────────────────────────────────────────
index_path = os.path.join(BASE, "index.html")
index = open(index_path, encoding="utf-8").read()

if "mbti-approach-en" not in index:
    LOVE_LANG_LI = '<li><a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love (English)</a></li>'
    APPROACH_LI = '\n<li><a href="/mbti-approach-en.html">How to Approach Each MBTI Type: The Best Strategy to Win Their Heart (English)</a></li>'
    index = index.replace(LOVE_LANG_LI, LOVE_LANG_LI + APPROACH_LI, 1)
    open(index_path, "w", encoding="utf-8").write(index)
    print("OK index.html")
else:
    print("SKIP index.html")

print("\nDone!")
