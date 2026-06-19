#!/usr/bin/env python3
"""Integrate mbti-ideal-date-en.html into the entire site."""

import re
import os

BASE = "/home/user/16lovetypedogs"

NEW_SLUG = "ideal-date"
NEW_TITLE = "Perfect Date Ideas for Every MBTI Type"
NEW_TITLE_LONG = "Perfect Date Ideas for Every MBTI Type: What Each Type Actually Wants"

# ─── 1. Ranking pages ────────────────────────────────────────────────────────
RANKING_FILES = [
    "ranking-devotion-en.html",
    "ranking-dokidoki-en.html",
    "ranking-jealousy-en.html",
    "ranking-loyalty-en.html",
    "ranking-marriage-en.html",
]

RANKING_OLD = (
    '<a href="/mbti-marriage-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI &amp; Marriage: Which Types Make the Best Lifelong Partners</a></div>'
)
RANKING_NEW = (
    RANKING_OLD
    + '\n      <a href="/mbti-ideal-date-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'Perfect Date Ideas for Every MBTI Type</a></div>'
)

for fname in RANKING_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-ideal-date-en" in text:
        print(f"SKIP (already has link): {fname}")
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

TYPE_OLD = (
    '<li style="padding:10px 0;font-size:14px">'
    '<a href="/mbti-marriage-en.html">MBTI &amp; Marriage: Which Types Make the Best Lifelong Partners</a>'
    '</li></ul></div></div>'
)
TYPE_NEW = (
    TYPE_OLD.replace("</li></ul></div></div>", "")
    + '</li>\n              '
    + '<li style="padding:10px 0;font-size:14px">'
    + '<a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type</a>'
    + '</li></ul></div></div>'
)

for fname in TYPE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-ideal-date-en" in text:
        print(f"SKIP (already has link): {fname}")
        continue
    if TYPE_OLD not in text:
        print(f"WARN (pattern not found): {fname}")
        continue
    text = text.replace(TYPE_OLD, TYPE_NEW, 1)
    open(path, "w", encoding="utf-8").write(text)
    print(f"OK type: {fname}")

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
]

GUIDE_MARRIAGE_LINK = (
    '<a href="/mbti-marriage-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'MBTI &amp; Marriage: Which Types Make the Best Lifelong Partners</a>'
)
IDEAL_DATE_LINK = (
    '\n<a href="/mbti-ideal-date-en.html" style="display:block;background:var(--bg);'
    'border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;'
    'font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">'
    'Perfect Date Ideas for Every MBTI Type</a>'
)

for fname in GUIDE_FILES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-ideal-date-en" in text:
        print(f"SKIP (already has link): {fname}")
        continue
    if GUIDE_MARRIAGE_LINK not in text:
        print(f"WARN (marriage pattern not found): {fname}")
        continue
    text = text.replace(GUIDE_MARRIAGE_LINK, GUIDE_MARRIAGE_LINK + IDEAL_DATE_LINK, 1)
    open(path, "w", encoding="utf-8").write(text)
    print(f"OK guide: {fname}")

# ─── 4. mbti-date.html hreflang + multilingual card ──────────────────────────
date_path = os.path.join(BASE, "mbti-date.html")
date_text = open(date_path, encoding="utf-8").read()

if "hreflang" not in date_text:
    CANONICAL = '<link rel="canonical" href="https://16lovetypedogs.com/mbti-date.html">'
    HREFLANG_BLOCK = (
        CANONICAL + "\n"
        + '  <link rel="alternate" hreflang="ja" href="https://16lovetypedogs.com/mbti-date.html">\n'
        + '  <link rel="alternate" hreflang="en" href="https://16lovetypedogs.com/mbti-ideal-date-en.html">\n'
        + '  <link rel="alternate" hreflang="x-default" href="https://16lovetypedogs.com/mbti-ideal-date-en.html">'
    )
    date_text = date_text.replace(CANONICAL, HREFLANG_BLOCK, 1)
    print("OK hreflang: mbti-date.html")
else:
    print("SKIP hreflang (already present): mbti-date.html")

if "mbti-ideal-date-en" not in date_text:
    RELATED_H2 = "<h2>関連記事</h2>"
    MULTI_CARD = (
        '<div class="card" style="background:#f0f8ff;border:1.5px solid #b0d0ef">\n'
        '    <h2 style="font-size:16px;font-weight:800;margin-bottom:8px">🌐 他の言語でも読む</h2>\n'
        '    <ul style="padding-left:1.4em;margin:0;font-size:13px;line-height:2">\n'
        '      <li><a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type (English)</a></li>\n'
        '    </ul>\n'
        '  </div>\n  '
        + RELATED_H2
    )
    date_text = date_text.replace(RELATED_H2, MULTI_CARD, 1)
    print("OK multilingual card: mbti-date.html")
else:
    print("SKIP multilingual card (already present): mbti-date.html")

open(date_path, "w", encoding="utf-8").write(date_text)

# ─── 5. sitemap.xml ──────────────────────────────────────────────────────────
sitemap_path = os.path.join(BASE, "sitemap.xml")
sitemap = open(sitemap_path, encoding="utf-8").read()

if "mbti-ideal-date-en" not in sitemap:
    MARRIAGE_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-marriage-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    DATE_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-ideal-date-en.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    sitemap = sitemap.replace(MARRIAGE_ENTRY, MARRIAGE_ENTRY + "\n" + DATE_ENTRY, 1)
    open(sitemap_path, "w", encoding="utf-8").write(sitemap)
    print("OK sitemap.xml")
else:
    print("SKIP sitemap.xml (already present)")

# ─── 6. index.html ───────────────────────────────────────────────────────────
index_path = os.path.join(BASE, "index.html")
index = open(index_path, encoding="utf-8").read()

if "mbti-ideal-date-en" not in index:
    MARRIAGE_LI = '<li><a href="/mbti-marriage-en.html">MBTI &amp; Marriage: Which Types Make the Best Lifelong Partners (English)</a></li>'
    DATE_LI = '\n<li><a href="/mbti-ideal-date-en.html">Perfect Date Ideas for Every MBTI Type: What Each Type Actually Wants (English)</a></li>'
    index = index.replace(MARRIAGE_LI, MARRIAGE_LI + DATE_LI, 1)
    open(index_path, "w", encoding="utf-8").write(index)
    print("OK index.html")
else:
    print("SKIP index.html (already present)")

print("\nDone!")
