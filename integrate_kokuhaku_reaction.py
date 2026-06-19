#!/usr/bin/env python3
import os, re

D = '/home/user/16lovetypedogs'
NEW = 'mbti-kokuhaku-reaction.html'
TITLE = 'MBTIタイプ別「告白されたときの反応」'
TITLE_FULL = 'MBTIタイプ別「告白されたときの反応」｜OKしやすい・断りやすい・迷うタイプ'

ok = warn = skip = 0

def update(path, old, new, label=None):
    global ok, warn, skip
    fname = os.path.basename(path)
    tag = f'[{label}]' if label else ''
    with open(path) as f: c = f.read()
    if NEW in c: print(f'SKIP: {fname}{tag}'); skip += 1; return
    nc = c.replace(old, new, 1)
    if nc == c: print(f'WARN: {fname}{tag}'); warn += 1; return
    with open(path, 'w') as f: f.write(nc)
    print(f'OK:   {fname}{tag}'); ok += 1

# ── mbti-nayami.html — insert card after kokuhaku card ─────────────────────
NAYAMI_OLD = '''      <a href="/mbti-kokuhaku.html" class="article-card">
        <span class="card-label">告白</span>
        <span class="card-title">タイプ別「告白のタイミング・言葉と仕方」</span>
        <span class="card-desc">タイプ別に響く告白の言葉とベストなシチュエーション</span>
      </a>
    </div>
  </div>'''
NAYAMI_NEW = '''      <a href="/mbti-kokuhaku.html" class="article-card">
        <span class="card-label">告白</span>
        <span class="card-title">タイプ別「告白のタイミング・言葉と仕方」</span>
        <span class="card-desc">タイプ別に響く告白の言葉とベストなシチュエーション</span>
      </a>
      <a href="/mbti-kokuhaku-reaction.html" class="article-card">
        <span class="card-label">告白されたとき</span>
        <span class="card-title">MBTIタイプ別「告白されたときの反応」</span>
        <span class="card-desc">OKしやすい・断りやすい・長期間迷うタイプ別の反応パターン</span>
      </a>
    </div>
  </div>'''
update(os.path.join(D, 'mbti-nayami.html'), NAYAMI_OLD, NAYAMI_NEW)

# ── mbti-kataomoi.html — add after kokuhaku li ─────────────────────────────
update(os.path.join(D, 'mbti-kataomoi.html'),
    '<li><a href="/mbti-kokuhaku.html">MBTIタイプ別「告白の成功法」まとめ</a></li>',
    f'<li><a href="/mbti-kokuhaku.html">MBTIタイプ別「告白の成功法」まとめ</a></li>\n      <li><a href="/{NEW}">{TITLE}</a></li>')

# ── mbti-kakekiki.html — add after kataomoi li ─────────────────────────────
update(os.path.join(D, 'mbti-kakekiki.html'),
    '<li><a href="/mbti-kataomoi.html">MBTIタイプ別「片思いの行動・気持ちの伝え方」</a></li>',
    f'<li><a href="/mbti-kataomoi.html">MBTIタイプ別「片思いの行動・気持ちの伝え方」</a></li>\n      <li><a href="/{NEW}">{TITLE}</a></li>')

# ── mbti-sukiave.html — add after kokuhaku p ───────────────────────────────
update(os.path.join(D, 'mbti-sukiave.html'),
    '<p><a href="/mbti-kokuhaku.html">MBTIタイプ別「告白のタイミング・仕方」</a></p>',
    f'<p><a href="/mbti-kokuhaku.html">MBTIタイプ別「告白のタイミング・仕方」</a></p>\n    <p><a href="/{NEW}">{TITLE}</a></p>')

# ── index.html — add after kakekiki li ─────────────────────────────────────
update(os.path.join(D, 'index.html'),
    '<li><a href="/mbti-kakekiki.html">MBTIタイプ別「恋愛の駆け引き」一覧｜する・しない・見抜き方</a></li>',
    f'<li><a href="/mbti-kakekiki.html">MBTIタイプ別「恋愛の駆け引き」一覧｜する・しない・見抜き方</a></li>\n<li><a href="/{NEW}">{TITLE_FULL}</a></li>')

# ── sitemap.xml — add after kakekiki entry ─────────────────────────────────
sitemap_path = os.path.join(D, 'sitemap.xml')
with open(sitemap_path) as f: sm = f.read()
if NEW in sm:
    print(f'SKIP: sitemap.xml'); skip += 1
else:
    m = re.search(r'<url>\s*<loc>https://16lovetypedogs\.com/mbti-kakekiki\.html</loc>.*?</url>', sm, re.DOTALL)
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

print(f'\nDone: {ok} updated, {warn} warnings, {skip} skipped')
