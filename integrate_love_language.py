#!/usr/bin/env python3
"""Integrate mbti-love-language-en.html into the entire site."""

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
    '<a href="/mbti-confess-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'How to Confess to Each MBTI Type</a></div>'
)
RANKING_NEW = (
    RANKING_OLD
    + '\n      <a href="/mbti-love-language-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI Love Languages: How Each Type Gives &amp; Receives Love</a></div>'
)

for fname in RANKING_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-love-language-en" in text:
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
    '<a href="/mbti-confess-en.html">How to Confess to Each MBTI Type</a>'
    '</li></ul></div></div>'
)
TYPE_NEW_PLAIN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-confess-en.html">How to Confess to Each MBTI Type</a>'
    '</li>\n              '
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
    '</li></ul></div></div>'
)

TYPE_OLD_TYPESEN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-confess-en.html">How to Confess to Each MBTI Type</a>'
    '</li></ul></div>\n</div>'
)
TYPE_NEW_TYPESEN = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-confess-en.html">How to Confess to Each MBTI Type</a>'
    '</li>\n              '
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
    '</li></ul></div>\n</div>'
)

for fname in TYPE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-love-language-en" in text:
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
]

CONFESS_LINK = (
    '<a href="/mbti-confess-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'How to Confess to Each MBTI Type</a>'
)
LOVE_LANG_LINK = (
    '\n<a href="/mbti-love-language-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI Love Languages: How Each Type Gives &amp; Receives Love</a>'
)

for fname in GUIDE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-love-language-en" in text:
        print(f"SKIP: {fname}")
        continue
    if CONFESS_LINK not in text:
        print(f"WARN (confess pattern not found): {fname}")
        continue
    text = text.replace(CONFESS_LINK, CONFESS_LINK + LOVE_LANG_LINK, 1)
    open(path, "w", encoding="utf-8").write(text)
    print(f"OK guide: {fname}")

# ─── 4. sitemap.xml ──────────────────────────────────────────────────────────
sitemap_path = os.path.join(BASE, "sitemap.xml")
sitemap = open(sitemap_path, encoding="utf-8").read()

if "mbti-love-language-en" not in sitemap:
    CONFESS_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-confess-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    LOVE_LANG_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-love-language-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    sitemap = sitemap.replace(CONFESS_ENTRY, CONFESS_ENTRY + "\n" + LOVE_LANG_ENTRY, 1)
    open(sitemap_path, "w", encoding="utf-8").write(sitemap)
    print("OK sitemap.xml")
else:
    print("SKIP sitemap.xml")

# ─── 5. index.html ───────────────────────────────────────────────────────────
index_path = os.path.join(BASE, "index.html")
index = open(index_path, encoding="utf-8").read()

if "mbti-love-language-en" not in index:
    CONFESS_LI = '<li><a href="/mbti-confess-en.html">How to Confess to Each MBTI Type: The Words &amp; Timing That Actually Work (English)</a></li>'
    LOVE_LANG_LI = '\n<li><a href="/mbti-love-language-en.html">MBTI Love Languages: How Each Type Gives &amp; Receives Love (English)</a></li>'
    index = index.replace(CONFESS_LI, CONFESS_LI + LOVE_LANG_LI, 1)
    open(index_path, "w", encoding="utf-8").write(index)
    print("OK index.html")
else:
    print("SKIP index.html")

print("\nDone!")
