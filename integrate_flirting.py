#!/usr/bin/env python3
import os, re

D = '/home/user/16lovetypedogs'
NEW = 'mbti-flirting-en.html'
TITLE = 'How Each MBTI Type Flirts: Obvious & Subtle Signs'

BLOCK = f'    <a href="/{NEW}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{TITLE}</a>'
LI    = f'<li style="padding:10px 0;font-size:14px"><a href="/{NEW}">{TITLE}</a></li>'

ok = warn = skip = 0

def update(path, old, new):
    global ok, warn, skip
    fname = os.path.basename(path)
    with open(path) as f: c = f.read()
    if NEW in c: print(f'SKIP: {fname}'); skip += 1; return
    nc = c.replace(old, new, 1)
    if nc == c: print(f'WARN: {fname}'); warn += 1; return
    with open(path, 'w') as f: f.write(nc)
    print(f'OK:   {fname}'); ok += 1

# ── Ranking pages ────────────────────────────────────────────────────────────
RANK_OLD = 'MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush</a>\n  </div>'
RANK_NEW = f'MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush</a>\n{BLOCK}\n  </div>'
for fn in ['ranking-devotion-en.html','ranking-dokidoki-en.html','ranking-jealousy-en.html','ranking-loyalty-en.html','ranking-marriage-en.html']:
    update(os.path.join(D, fn), RANK_OLD, RANK_NEW)

# ── Type pages ───────────────────────────────────────────────────────────────
TYPE_OLD  = '<li style="padding:10px 0;font-size:14px"><a href="/mbti-unrequited-love-en.html">MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush</a></li>\n</ul></div></div>'
TYPE_NEW  = f'<li style="padding:10px 0;font-size:14px"><a href="/mbti-unrequited-love-en.html">MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush</a></li>\n{LI}\n</ul></div></div>'
for t in ['enfj','enfp','entj','entp','esfj','esfp','estj','estp','infj','infp','intj','intp','isfj','isfp','istj','istp']:
    update(os.path.join(D, f'type-{t}-en.html'), TYPE_OLD, TYPE_NEW)

# ── types-en.html (slightly different closing) ───────────────────────────────
TYPES_OLD = '<li style="padding:10px 0;font-size:14px"><a href="/mbti-unrequited-love-en.html">MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush</a></li>\n</ul></div>\n</div>'
TYPES_NEW = f'<li style="padding:10px 0;font-size:14px"><a href="/mbti-unrequited-love-en.html">MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush</a></li>\n{LI}\n</ul></div>\n</div>'
update(os.path.join(D, 'types-en.html'), TYPES_OLD, TYPES_NEW)

# ── Guide pages (block style, plain &) ───────────────────────────────────────
BLOCK_ANCHOR = '<a href="/mbti-unrequited-love-en.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush</a>'
BLOCK_NEW_ANCHOR = BLOCK_ANCHOR + '\n' + BLOCK
for fn in ['mbti-approach-en.html','mbti-breakup-en.html','mbti-cheating-en.html','mbti-confess-en.html',
           'mbti-dating-tips-en.html','mbti-fight-en.html','mbti-jealousy-en.html','mbti-long-distance-en.html',
           'mbti-love-language-en.html','mbti-marriage-en.html','mbti-relationship-style-en.html','mbti-shy-love-en.html']:
    update(os.path.join(D, fn), BLOCK_ANCHOR, BLOCK_NEW_ANCHOR)

# ── crush-en.html (display:block but &amp; and ends in </li>) ────────────────
CRUSH_OLD = '<a href="/mbti-unrequited-love-en.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">MBTI &amp; Unrequited Love: How Each Type Handles a One-Sided Crush</a></li>'
CRUSH_LINK = f'    <a href="/{NEW}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{TITLE}</a>'
CRUSH_NEW  = '<a href="/mbti-unrequited-love-en.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">MBTI &amp; Unrequited Love: How Each Type Handles a One-Sided Crush</a>\n' + CRUSH_LINK + '</li>'
update(os.path.join(D, 'mbti-crush-en.html'), CRUSH_OLD, CRUSH_NEW)

# ── index.html ───────────────────────────────────────────────────────────────
INDEX_OLD = '<li><a href="/mbti-unrequited-love-en.html">MBTI & Unrequited Love: How Each Type Handles a One-Sided Crush (English)</a></li>'
INDEX_NEW = INDEX_OLD + f'\n<li><a href="/{NEW}">{TITLE} (English)</a></li>'
update(os.path.join(D, 'index.html'), INDEX_OLD, INDEX_NEW)

# ── sitemap.xml ──────────────────────────────────────────────────────────────
sitemap_path = os.path.join(D, 'sitemap.xml')
with open(sitemap_path) as f: sm = f.read()
if NEW in sm:
    print(f'SKIP: sitemap.xml'); skip += 1
else:
    SITEMAP_ANCHOR = '    <loc>https://16lovetypedogs.com/mbti-unrequited-love-en.html</loc>'
    m = re.search(r'<url>\s*' + re.escape(SITEMAP_ANCHOR[4:]) + r'.*?</url>', sm, re.DOTALL)
    if m:
        entry = f'''  <url>
    <loc>https://16lovetypedogs.com/{NEW}</loc>
    <lastmod>2026-06-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>'''
        sm2 = sm[:m.end()] + '\n' + entry + sm[m.end():]
        with open(sitemap_path, 'w') as f: f.write(sm2)
        print(f'OK:   sitemap.xml'); ok += 1
    else:
        print(f'WARN: sitemap.xml'); warn += 1

# ── Add first-date link to flirting-en Related Guides ───────────────────────
FIRST_DATE = 'mbti-first-date-en.html'
FIRST_DATE_TITLE = 'Perfect First Date for Every MBTI Type: Ideas That Actually Work'
FIRST_LINK = f'    <a href="/{FIRST_DATE}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{FIRST_DATE_TITLE}</a>'
FLIRT_PATH = os.path.join(D, NEW)
with open(FLIRT_PATH) as f: fc = f.read()
if FIRST_DATE not in fc:
    ANCHOR_IN_FLIRT = '<a href="/mbti-unrequited-love-en.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">MBTI &amp; Unrequited Love: How Each Type Handles a One-Sided Crush</a>'
    NEW_ANCHOR_IN_FLIRT = ANCHOR_IN_FLIRT + '\n' + FIRST_LINK
    fc2 = fc.replace(ANCHOR_IN_FLIRT, NEW_ANCHOR_IN_FLIRT, 1)
    if fc2 != fc:
        with open(FLIRT_PATH, 'w') as f: f.write(fc2)
        print(f'OK:   {NEW} (added first-date link)'); ok += 1
    else:
        print(f'WARN: {NEW} (could not add first-date link)'); warn += 1
else:
    print(f'SKIP: {NEW} (first-date already linked)'); skip += 1

print(f'\nDone: {ok} updated, {warn} warnings, {skip} skipped')
