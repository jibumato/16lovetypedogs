#!/usr/bin/env python3
"""Add mbti-nayami.html and mbti-mannerism.html links to key JA pages."""

import os
import re

BASE = "/home/user/16lovetypedogs"

NAYAMI_LINK = '<li><a href="/mbti-nayami.html">MBTI×恋愛の悩み解決ガイド（シチュエーション別まとめ）</a></li>'
MANNERISM_LINK = '<li><a href="/mbti-mannerism.html">MBTIタイプ別「マンネリ・倦怠期の原因と乗り越え方」</a></li>'

# Pages that have 関連記事 with <ul> lists (using <li> format)
# We'll add nayami link after the last <li> and before </ul>
LI_PAGES = [
    "mbti-kataomoi.html",
    "mbti-myuari.html",
    "mbti-suki-na-hito.html",
    "mbti-renai-aruaru.html",
    "mbti-shitsuren.html",
    "mbti-myuari2.html",
]

for fname in LI_PAGES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    changed = False

    # Add nayami link
    if "mbti-nayami" not in text:
        # Find the last </li> before </ul> in the 関連記事 section
        # Pattern: </li>\n    </ul>  (with various indentation)
        m = re.search(r'(</li>)(\s*</ul>)', text[::-1])
        if m:
            pos = len(text) - m.start() - len(m.group(1))
            indent = "      "
            text = text[:pos] + f"\n{indent}{NAYAMI_LINK}" + text[pos:]
            changed = True
            print(f"OK nayami→{fname}")
        else:
            print(f"WARN nayami pattern not found: {fname}")

    # Add mannerism link to kenka/yakimochi/sameru if they link to related
    if "mbti-mannerism" not in text and fname in ["mbti-shitsuren.html", "mbti-renai-aruaru.html"]:
        m = re.search(r'(</li>)(\s*</ul>)', text[::-1])
        if m:
            pos = len(text) - m.start() - len(m.group(1))
            indent = "      "
            text = text[:pos] + f"\n{indent}{MANNERISM_LINK}" + text[pos:]
            changed = True
            print(f"OK mannerism→{fname}")

    if changed:
        open(path, "w", encoding="utf-8").write(text)

# Pages that use <p> tags for links (sukiave, fukuen, kenka, sameru, yakimochi)
P_PAGES = [
    "mbti-sukiave.html",
    "mbti-kenka.html",
    "mbti-sameru.html",
    "mbti-yakimochi.html",
    "mbti-fukuen.html",
]

for fname in P_PAGES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    changed = False

    if "mbti-nayami" not in text:
        # Find 関連記事 section and add before </div>
        # Pattern: last </p> before </div> in the related section
        m = re.search(r'関連記事.*?</div>', text, re.DOTALL)
        if m:
            end = m.end()
            nayami_p = f'\n    <p><a href="/mbti-nayami.html">MBTI×恋愛の悩み解決ガイド（シチュエーション別まとめ）</a></p>'
            # Insert before </div>
            text = text[:end-6] + nayami_p + "\n  </div>" + text[end:]
            changed = True
            print(f"OK nayami→{fname}")
        else:
            print(f"WARN p-pattern not found: {fname}")

    if changed:
        open(path, "w", encoding="utf-8").write(text)

# Add nayami and mannerism to kenka + sameru specifically (they're related to mannerism)
MANNERISM_P_PAGES = ["mbti-kenka.html", "mbti-sameru.html"]
for fname in MANNERISM_P_PAGES:
    path = os.path.join(BASE, fname)
    text = open(path, encoding="utf-8").read()
    if "mbti-mannerism" not in text:
        m = re.search(r'関連記事.*?</div>', text, re.DOTALL)
        if m:
            end = m.end()
            mannerism_p = f'\n    <p><a href="/mbti-mannerism.html">MBTIタイプ別「マンネリ・倦怠期の原因と乗り越え方」</a></p>'
            text = text[:end-6] + mannerism_p + "\n  </div>" + text[end:]
            open(path, "w", encoding="utf-8").write(text)
            print(f"OK mannerism→{fname}")
        else:
            print(f"WARN mannerism p-pattern not found: {fname}")

# Update sitemap.xml
sitemap_path = os.path.join(BASE, "sitemap.xml")
sitemap = open(sitemap_path, encoding="utf-8").read()
added_sitemap = False

if "mbti-nayami" not in sitemap:
    # Add after the last JA guide entry (before the EN entries or at end)
    # Use approach.html as anchor
    APPROACH_JA_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-approach.html</loc>"""
    if APPROACH_JA_ENTRY in sitemap:
        NAYAMI_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-nayami.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://16lovetypedogs.com/mbti-mannerism.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>\n"""
        sitemap = sitemap.replace(APPROACH_JA_ENTRY, NAYAMI_ENTRY + APPROACH_JA_ENTRY, 1)
        open(sitemap_path, "w", encoding="utf-8").write(sitemap)
        print("OK sitemap.xml (nayami + mannerism)")
    else:
        print("WARN sitemap: approach.html entry not found, appending before </urlset>")
        NAYAMI_ENTRY = """  <url>
    <loc>https://16lovetypedogs.com/mbti-nayami.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://16lovetypedogs.com/mbti-mannerism.html</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""
        sitemap = sitemap.replace("</urlset>", NAYAMI_ENTRY + "</urlset>")
        open(sitemap_path, "w", encoding="utf-8").write(sitemap)
        print("OK sitemap.xml (appended)")
else:
    print("SKIP sitemap (nayami already present)")

# Update index.html
index_path = os.path.join(BASE, "index.html")
index = open(index_path, encoding="utf-8").read()

if "mbti-nayami" not in index:
    # Add near the JA guide links
    APPROACH_LI = '<li><a href="/mbti-approach.html">'
    if APPROACH_LI in index:
        NAYAMI_LI = '<li><a href="/mbti-nayami.html">MBTI×恋愛の悩み解決ガイド｜シチュエーション別まとめ</a></li>\n<li><a href="/mbti-mannerism.html">MBTIタイプ別「マンネリ・倦怠期の原因と乗り越え方」</a></li>\n'
        index = index.replace(APPROACH_LI, NAYAMI_LI + APPROACH_LI, 1)
        open(index_path, "w", encoding="utf-8").write(index)
        print("OK index.html")
    else:
        print("WARN index.html: approach li not found")
else:
    print("SKIP index.html")

print("\nDone!")
