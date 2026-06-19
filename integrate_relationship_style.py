#!/usr/bin/env python3
"""Integrate mbti-relationship-style-en.html into all relevant pages."""

import os, re

BASE = "/home/user/16lovetypedogs"
NEW_SLUG = "mbti-relationship-style-en"
NEW_TITLE = "MBTI Types as Partners: What Each Type Is Like in a Relationship"
NEW_SHORT = "MBTI Types as Partners: What Each Type Is Like in a Relationship"
ANCHOR_SLUG = "mbti-shy-love-en"
ANCHOR_TITLE_SHORT = "MBTI Types That Pull Away When They Like You"

# 1. Ranking pages — use <div> link format with style
RANKING_PAGES = [
    "ranking-en.html",
    "ranking-compatibility-en.html",
    "ranking-communication-en.html",
    "ranking-jealousy-en.html",
    "ranking-fall-en.html",
]

ANCHOR_RANKING = f'<a href="/{ANCHOR_SLUG}.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{ANCHOR_TITLE_SHORT}</a></div>'
INSERT_RANKING = f'\n    <a href="/{NEW_SLUG}.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{NEW_SHORT}</a>'

for fname in RANKING_PAGES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f"SKIP (not found): {fname}")
        continue
    text = open(path, encoding="utf-8").read()
    if NEW_SLUG in text:
        print(f"SKIP (already has link): {fname}")
        continue
    if ANCHOR_RANKING in text:
        text = text.replace(ANCHOR_RANKING, ANCHOR_RANKING[:-6] + INSERT_RANKING + "\n  </div>", 1)
        open(path, "w", encoding="utf-8").write(text)
        print(f"OK ranking: {fname}")
    else:
        print(f"WARN ranking anchor not found: {fname}")

# 2. Type pages — use <li> format
TYPE_PAGES = [f"type-{t}-en.html" for t in [
    "intj","intp","entj","entp",
    "infj","infp","enfj","enfp",
    "istj","isfj","estj","esfj",
    "istp","isfp","estp","esfp",
]]

ANCHOR_TYPE_LI = f'<li style="padding:10px 0;font-size:14px"><a href="/{ANCHOR_SLUG}.html">{ANCHOR_TITLE_SHORT}</a></li></ul></div></div>'
INSERT_TYPE_LI = f'\n<li style="padding:10px 0;font-size:14px"><a href="/{NEW_SLUG}.html">{NEW_SHORT}</a></li>'

for fname in TYPE_PAGES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f"SKIP (not found): {fname}")
        continue
    text = open(path, encoding="utf-8").read()
    if NEW_SLUG in text:
        print(f"SKIP (already has link): {fname}")
        continue
    if ANCHOR_TYPE_LI in text:
        text = text.replace(ANCHOR_TYPE_LI,
            f'<li style="padding:10px 0;font-size:14px"><a href="/{ANCHOR_SLUG}.html">{ANCHOR_TITLE_SHORT}</a></li>' +
            INSERT_TYPE_LI + "\n</ul></div></div>", 1)
        open(path, "w", encoding="utf-8").write(text)
        print(f"OK type: {fname}")
    else:
        print(f"WARN type anchor not found: {fname}")

# 3. types-en.html
types_en_path = os.path.join(BASE, "types-en.html")
text = open(types_en_path, encoding="utf-8").read()
if NEW_SLUG not in text:
    ANCHOR_TYPES_EN = f'<li style="padding:10px 0;font-size:14px"><a href="/{ANCHOR_SLUG}.html">{ANCHOR_TITLE_SHORT}</a></li></ul></div>\n</div>'
    INSERT_TYPES_EN = f'\n<li style="padding:10px 0;font-size:14px"><a href="/{NEW_SLUG}.html">{NEW_SHORT}</a></li>'
    if ANCHOR_TYPES_EN in text:
        text = text.replace(ANCHOR_TYPES_EN,
            f'<li style="padding:10px 0;font-size:14px"><a href="/{ANCHOR_SLUG}.html">{ANCHOR_TITLE_SHORT}</a></li>' +
            INSERT_TYPES_EN + "\n</ul></div>\n</div>", 1)
        open(types_en_path, "w", encoding="utf-8").write(text)
        print("OK types-en.html")
    else:
        print("WARN types-en.html anchor not found")
else:
    print("SKIP types-en.html")

# 4. Guide pages (EN) — use styled <a> block format
EN_GUIDE_PAGES = [
    "mbti-love-language-en.html",
    "mbti-approach-en.html",
    "mbti-shy-love-en.html",
    "mbti-dating-tips-en.html",
    "mbti-confess-en.html",
    "mbti-breakup-en.html",
    "mbti-jealousy-en.html",
    "mbti-first-date-en.html",
    "mbti-cheating-en.html",
    "mbti-long-distance-en.html",
    "mbti-communication-en.html",
    "mbti-flirting-en.html",
    "mbti-gift-en.html",
    "mbti-apology-en.html",
    "mbti-reunion-en.html",
    "mbti-marriage-en.html",
    "mbti-fall-in-love-en.html",
    "mbti-heartbreak-en.html",
    "mbti-fight-en.html",
]

ANCHOR_GUIDE = f'<a href="/{ANCHOR_SLUG}.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{ANCHOR_TITLE_SHORT}</a>'
INSERT_GUIDE = f'\n    <a href="/{NEW_SLUG}.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{NEW_SHORT}</a>'

for fname in EN_GUIDE_PAGES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f"SKIP (not found): {fname}")
        continue
    text = open(path, encoding="utf-8").read()
    if NEW_SLUG in text:
        print(f"SKIP (already has link): {fname}")
        continue
    if ANCHOR_GUIDE in text:
        text = text.replace(ANCHOR_GUIDE, ANCHOR_GUIDE + INSERT_GUIDE, 1)
        open(path, "w", encoding="utf-8").write(text)
        print(f"OK guide: {fname}")
    else:
        print(f"WARN guide anchor not found: {fname}")

# 5. sitemap.xml
sitemap_path = os.path.join(BASE, "sitemap.xml")
sitemap = open(sitemap_path, encoding="utf-8").read()
if NEW_SLUG not in sitemap:
    ANCHOR_SITEMAP = f"  <url>\n    <loc>https://16lovetypedogs.com/{ANCHOR_SLUG}.html</loc>"
    NEW_ENTRY = f"""  <url>
    <loc>https://16lovetypedogs.com/{NEW_SLUG}.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>\n"""
    if ANCHOR_SITEMAP in sitemap:
        sitemap = sitemap.replace(ANCHOR_SITEMAP, NEW_ENTRY + ANCHOR_SITEMAP, 1)
        open(sitemap_path, "w", encoding="utf-8").write(sitemap)
        print("OK sitemap.xml")
    else:
        print("WARN sitemap anchor not found")
else:
    print("SKIP sitemap.xml")

# 6. index.html
index_path = os.path.join(BASE, "index.html")
index = open(index_path, encoding="utf-8").read()
if NEW_SLUG not in index:
    ANCHOR_INDEX = f'<li><a href="/{ANCHOR_SLUG}.html">{ANCHOR_TITLE_SHORT}: Shy Love Explained (English)</a></li>'
    NEW_INDEX_LI = f'<li><a href="/{NEW_SLUG}.html">{NEW_SHORT} (English)</a></li>\n'
    if ANCHOR_INDEX in index:
        index = index.replace(ANCHOR_INDEX, NEW_INDEX_LI + ANCHOR_INDEX, 1)
        open(index_path, "w", encoding="utf-8").write(index)
        print("OK index.html")
    else:
        print("WARN index.html anchor not found")
else:
    print("SKIP index.html")

print("\nDone!")
