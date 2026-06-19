#!/usr/bin/env python3
import os, re

D = '/home/user/16lovetypedogs'
NEW = 'mbti-first-date-en.html'
TITLE = 'Perfect First Date for Every MBTI Type: Ideas That Actually Work'
FLIRT = 'mbti-flirting-en.html'
FLIRT_TITLE = 'How Each MBTI Type Flirts: Obvious & Subtle Signs'

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
RANK_FLIRT_BLOCK = f'    <a href="/{FLIRT}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{FLIRT_TITLE}</a>'
RANK_OLD = RANK_FLIRT_BLOCK + '\n  </div>'
RANK_NEW = RANK_FLIRT_BLOCK + '\n' + BLOCK + '\n  </div>'
for fn in ['ranking-devotion-en.html','ranking-dokidoki-en.html','ranking-jealousy-en.html','ranking-loyalty-en.html','ranking-marriage-en.html']:
    update(os.path.join(D, fn), RANK_OLD, RANK_NEW)

# ── Type pages ───────────────────────────────────────────────────────────────
FLIRT_LI = f'<li style="padding:10px 0;font-size:14px"><a href="/{FLIRT}">{FLIRT_TITLE}</a></li>'
TYPE_OLD  = FLIRT_LI + '\n</ul></div></div>'
TYPE_NEW  = FLIRT_LI + '\n' + LI + '\n</ul></div></div>'
for t in ['enfj','enfp','entj','entp','esfj','esfp','estj','estp','infj','infp','intj','intp','isfj','isfp','istj','istp']:
    update(os.path.join(D, f'type-{t}-en.html'), TYPE_OLD, TYPE_NEW)

# ── types-en.html ────────────────────────────────────────────────────────────
TYPES_OLD = FLIRT_LI + '\n</ul></div>\n</div>'
TYPES_NEW = FLIRT_LI + '\n' + LI + '\n</ul></div>\n</div>'
update(os.path.join(D, 'types-en.html'), TYPES_OLD, TYPES_NEW)

# ── Guide pages (block style) ─────────────────────────────────────────────────
FLIRT_BLOCK_BARE = f'    <a href="/{FLIRT}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{FLIRT_TITLE}</a>'
for fn in ['mbti-approach-en.html','mbti-breakup-en.html','mbti-cheating-en.html','mbti-confess-en.html',
           'mbti-dating-tips-en.html','mbti-fight-en.html','mbti-jealousy-en.html','mbti-long-distance-en.html',
           'mbti-love-language-en.html','mbti-marriage-en.html','mbti-relationship-style-en.html','mbti-shy-love-en.html']:
    update(os.path.join(D, fn), FLIRT_BLOCK_BARE, FLIRT_BLOCK_BARE + '\n' + BLOCK)

# ── crush-en.html (flirt link ends with </li>) ───────────────────────────────
CRUSH_FLIRT_LINK = f'    <a href="/{FLIRT}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{FLIRT_TITLE}</a></li>'
CRUSH_NEW_FIRST = f'    <a href="/{NEW}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{TITLE}</a></li>'
update(os.path.join(D, 'mbti-crush-en.html'), CRUSH_FLIRT_LINK, CRUSH_FLIRT_LINK.replace('</li>', '') + '\n' + CRUSH_NEW_FIRST)

# ── index.html ───────────────────────────────────────────────────────────────
INDEX_FLIRT = f'<li><a href="/{FLIRT}">{FLIRT_TITLE} (English)</a></li>'
INDEX_OLD   = INDEX_FLIRT
INDEX_NEW   = INDEX_FLIRT + f'\n<li><a href="/{NEW}">{TITLE} (English)</a></li>'
update(os.path.join(D, 'index.html'), INDEX_OLD, INDEX_NEW)

# ── sitemap.xml ──────────────────────────────────────────────────────────────
sitemap_path = os.path.join(D, 'sitemap.xml')
with open(sitemap_path) as f: sm = f.read()
if NEW in sm:
    print(f'SKIP: sitemap.xml'); skip += 1
else:
    m = re.search(r'<url>\s*<loc>https://16lovetypedogs\.com/' + re.escape(FLIRT) + r'</loc>.*?</url>', sm, re.DOTALL)
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

# ── Add flirting link to first-date-en Related Guides ───────────────────────
FD_PATH = os.path.join(D, NEW)
with open(FD_PATH) as f: fc = f.read()
if FLIRT not in fc:
    ANCHOR_IN_FD = '<a href="/mbti-unrequited-love-en.html" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">MBTI &amp; Unrequited Love: How Each Type Handles a One-Sided Crush</a>'
    FLIRT_LINK = f'    <a href="/{FLIRT}" style="display:block;background:var(--bg);border:1.5px solid var(--beige);border-radius:12px;padding:10px 14px;font-size:13px;font-weight:700;margin-top:6px;text-decoration:none">{FLIRT_TITLE}</a>'
    fc2 = fc.replace(ANCHOR_IN_FD, ANCHOR_IN_FD + '\n' + FLIRT_LINK, 1)
    if fc2 != fc:
        with open(FD_PATH, 'w') as f: f.write(fc2)
        print(f'OK:   {NEW} (added flirting link)'); ok += 1
    else:
        print(f'WARN: {NEW} (could not add flirting link)'); warn += 1
else:
    print(f'SKIP: {NEW} (flirting already linked)'); skip += 1

# ── Fix first-date-en.html footer to standard format ─────────────────────────
with open(FD_PATH) as f: fc = f.read()
OLD_FOOTER = '''<footer>
  <div>
    <a href="/">🐾 16 Love Type Dogs</a> &nbsp;&middot;&nbsp;
    <a href="/about-en.html">About</a> &nbsp;&middot;&nbsp;
    <a href="/privacy-en.html">Privacy</a> &nbsp;&middot;&nbsp;
    <a href="/contact-en.html">Contact</a>
  </div>
  <div style="margin-top:8px;color:#a09080;font-size:11.5px">
    &copy; 2026 16 Love Type Dogs. All rights reserved.
  </div>
</footer>'''
NEW_FOOTER = '<footer><div><a href="/">16 Love Type Dogs</a> &nbsp;|&nbsp; <a href="/types-en.html">All 16 Types</a> &nbsp;|&nbsp; <a href="/privacy.html">Privacy</a></div><div style="margin-top:6px;color:#c4a0c8">© 2026 16 Love Type Dogs</div></footer>'
if OLD_FOOTER in fc:
    fc2 = fc.replace(OLD_FOOTER, NEW_FOOTER)
    with open(FD_PATH, 'w') as f: f.write(fc2)
    print(f'OK:   {NEW} (fixed footer)'); ok += 1
else:
    print(f'SKIP: {NEW} (footer already standard)'); skip += 1

print(f'\nDone: {ok} updated, {warn} warnings, {skip} skipped')
