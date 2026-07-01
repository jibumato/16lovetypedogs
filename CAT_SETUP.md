# 🐱 16cat（猫版）セットアップ引き継ぎ書

このリポジトリ（`16lovetypedogs` = 犬版）を複製して **猫版（16にゃんこ恋愛診断 / 16 Love Type Cats）** を立ち上げるための手順書です。
新しいClaude Codeチャットで、このファイルを最初に読ませれば一気に進められます。

> **基本方針**：コードの「構造・機能・デザイン」はそのまま流用。変えるのは①中身（犬→猫）②外部サービスの紐付け（Stripe/R2/GA4/ドメイン/KV）③デザイン（案Bを全面適用）。

---

## 0. 事前準備（GitHub）

1. このリポジトリを **Template** 化（Settings → "Template repository" ON）するか、全ファイルをコピーして新リポジトリ `16lovetypecats` を作成
2. 新チャットで新リポジトリをスコープに追加
3. 新チャット冒頭で伝える例：
   > 「このリポジトリは16lovetypedogsの複製。CAT_SETUP.mdを読んで、犬版を猫版に変換して。まずブランド名・ドメイン・データ層から。」

---

## 1. ブランド名・ドメイン（5言語）

| 項目 | 犬版 | 猫版（案） |
|---|---|---|
| ja | 16わんこ恋愛診断 | 16にゃんこ恋愛診断 |
| en | 16 Love-Type Dogs / 16lovetypedogs | 16 Love-Type Cats / 16lovetypecats |
| ko | 16 연애견 진단 | 16 연애묘 진단 |
| zh | 16恋爱犬测验 | 16恋爱猫测验 |
| tw | 16戀愛犬測驗 | 16戀愛貓測驗 |
| ドメイン | 16lovetypedogs.com | 16lovetypecats.com（要取得） |
| ハッシュタグ | #16わんこ恋愛診断 | #16にゃんこ恋愛診断 |
| 絵文字 | 🐶🐾わんこ | 🐱🐾にゃんこ |

## 2. 一括置換リスト（安全なものから）

新チャットのClaudeに「以下を全ファイル一括置換」と指示：

- `16lovetypedogs.com` → `16lovetypecats.com`（**374ファイル**に出現。ドメイン取得後）
- `16lovetypedogs` → `16lovetypecats`（wrangler名・Resend送信元など）
- `16わんこ` → `16にゃんこ`（101ファイル）
- `わんこ` → `にゃんこ` / `犬種` → `猫種` / `わんちゃん` → `猫ちゃん`
- `Love-Type Dogs` / `Love Type Dogs` → `Love-Type Cats`
- `恋爱犬` → `恋爱猫`、`戀愛犬` → `戀愛貓`、`연애견` → `연애묘`
- 絵文字 `🐶` → `🐱`、`🐕` → `🐈`（🐾は猫にも使えるので維持可）

⚠️ **置換してはいけないもの**：GA4測定ID、Stripeリンク、R2 URL、KV namespace id（すべて後述の「新規発行」で差し替え）。

## 3. データ層の書き換え（最重要・工数大）

`index.html` 内の以下のJSオブジェクトを猫版に。**5言語すべて**必要。

| 定数 | 行付近 | 内容 | 対応 |
|---|---|---|---|
| `LOC` | 1157 | 16タイプ×5言語の core データ（`breed`猫種 / `name` / `tag` / `role` / `personality` / `love` / `couple` / `fight` / `pros` / `cons` / `howto` / `hook` 等） | **全面書き換え**（犬種→猫種、性格文も猫の生態に寄せる） |
| `BASE` | 1156 | `{em:絵文字, g:グループ}` | 絵文字を猫顔に |
| `OMK` | 1175 | おみくじ（levels/colors/act）| ラッキーわんこ→ラッキーにゃんこ等、文言調整 |
| `LUCKY` / `SEASON` | 1171-72 | ラッキーアイテム | ほぼ流用可、犬用語だけ調整 |
| `I18N` | 1169 | UI全文言（超大） | `nav_dex`「わんこ図鑑」→「にゃんこ図鑑」等、犬語のみ調整 |
| `NAV_I18N` | 1351 | 下部ナビ | 同上 |
| `GUIDE_I18N` / `GUIDE_EXTRA` | 2096/1943 | プレミアムレポート紹介文・目次 | 犬→猫の表現調整 |
| `FB_I18N` / `SAVE_I18N` | 1819/1768 | 感想・メール保存 | ほぼ流用可 |
| `PARAM` / `RARITY` / `GROUP` / `GROUP_COLOR` | — | 数値・色 | **そのまま流用OK**（MBTI軸は共通） |

### 猫種マッピング（案・調整可）

MBTIタイプの性格イメージに合わせた提案。犬版の犬種と対応：

| Type | 犬版 | 猫版（案） |
|---|---|---|
| INTJ | チワワ | ロシアンブルー |
| INTP | ミニチュアシュナウザー | アビシニアン |
| ENTJ | コーギー | ベンガル |
| ENTP | ジャックラッセルテリア | オリエンタルショートヘア |
| INFJ | キャバリア | ラグドール |
| INFP | マルチーズ | ペルシャ |
| ENFJ | ゴールデンレトリバー | メインクーン |
| ENFP | トイプードル | ソマリ |
| ISTJ | 柴犬 | ブリティッシュショートヘア |
| ISFJ | シーズー | スコティッシュフォールド |
| ESTJ | ボストンテリア | アメリカンショートヘア |
| ESFJ | ラブラドールレトリバー | ラガマフィン |
| ISTP | ミニチュアダックス | エジプシャンマウ |
| ISFP | フレンチブルドッグ | ノルウェージャンフォレストキャット |
| ESTP | ビーグル | ボンベイ |
| ESFP | ポメラニアン | スフィンクス／デボンレックス |

（各言語の猫種名も要翻訳）

## 4. 画像アセット（新規制作が必要）

犬画像は流用不可。以下を猫版で用意：

- **猫イラスト**：`{code}.webp` ×16（結果表示・図鑑用）＋ `{code}.png` ×16（OGP合成用、犬版と同じ絵柄推奨）
- **ヒーローロゴ**：`logo-hero{,-en,-ko,-zh,-tw}.{webp,jpg}`（5言語）
- **OGP画像 80枚**：`ogp/{ja,en,ko,zh,tw}/*.png` は生成スクリプトで**再生成**（下記）
- その他：`icon-192.png` / `apple-touch-icon` / `manifest.json` のname・アイコン、`line-icon.png`（流用可）、`paypay-logo.png`（流用可）

### OGP再生成スクリプト（猫画像を差し替えてから実行）
- `generate_ja_ogp.py`（ja・希少性バッジ込み）
- `generate_share_pages.py`（en/zh/ko/tw、eyebrow文言も猫用に）
- `overlay_rarity_ogp.py`（en/ko/zh/tw に希少性バッジ再オーバーレイ）
- 依存：`/tmp/LOC.json` `/tmp/I18N.json` `/tmp/RARITY.json`（index.htmlからダンプ）、M PLUS Rounded 1cフォント
- eyebrow文言「16タイプ × 恋愛 × 犬種」→「…× 猫種」に変更

## 5. デザイン（案B＝フラット厚塗りシャドウ を全面適用）

韓国キャラアプリ風のポップな配色。`index.html`（＋各サブページ）のCSSトークンを差し替え。

```css
/* カラートークン */
--bg:        #fdf2fa;   /* 背景（薄ピンク） */
--ink:       #2c1b3d;   /* 濃紺プラム（文字＆太縁の色） */
--primary:   #b98af0;   /* ラベンダー紫（主要ボタン） */
--accent:    #d896e8;   /* アクセント紫ピンク（カード影） */
--pink:      #f584bb;   /* ピンク */
--yellow:    #ffe27a;   /* バッジ黄 */

/* パーツの型 */
・縁取り: border:2.5〜3px solid var(--ink)
・影: box-shadow: 6px 6px 0 var(--ink)   （ボタン・ピル）
      box-shadow: 8px 8px 0 var(--accent) （カード）
・角丸: 20〜24px
・ボタン文字色は濃紺(--ink)、背景は--primary
・バッジは黄背景＋濃紺縁
```

※ 猫イラストは繊細な絵柄だと太縁と喧嘩しやすいので、**やや太めの輪郭・はっきりした色**のイラストにすると案Bと馴染む。

## 6. 外部サービスの新規セットアップ（順序）

猫版は別サービスなので下記はすべて新規。**この順序**が安全：

1. **独自ドメイン** `16lovetypecats.com` を取得しCloudflareに追加
2. **KV名前空間**を新規作成 → `wrangler.jsonc` の `kv_namespaces[].id` を差し替え（犬版のid `bc0214...` は使わない）
3. **GA4プロパティ**を新規作成 → 測定ID（`G-XXXX`）を全ファイルの `G-C3W7FBQRCD`（287ファイル）と置換
4. **Cloudflare Worker**を新規デプロイ（`wrangler.jsonc` name=`16lovetypecats`）＋Git連携
5. **R2バケット**（猫PDF用）を作成しPublic access有効化 → `love-guide-thanks.html` の `PDF_URLS` を猫PDFのURLに
6. **Stripe**：猫版の商品・Payment Link（USD/JPY）を作成 → `STRIPE_LINKS_BY_LANG` に反映（`redirect-urls.html`ツールでリダイレクトURL生成）
7. **Resend**：`16lovetypecats.com` ドメイン認証 → 送信元 `noreply@16lovetypecats.com` に変更
8. **シークレット登録**（Cloudflare Workers → Settings → Variables and Secrets）：
   - `ADMIN_TOKEN`（管理ページ用パスワード）
   - `RESEND_API_KEY`
   - `GA_MP_API_SECRET`（GA4 Measurement Protocol）
   - `STRIPE_WEBHOOK_SECRET`（Stripe Webhook）
   - `UNSUB_SECRET`（任意）
9. **Stripe Webhook**：`https://16lovetypecats.com/api/stripe-webhook` を `checkout.session.completed` で登録
10. **worker.js** 内のGA既定ID `G-C3W7FBQRCD`（`env.GA_MEASUREMENT_ID`で上書き可）と Resend送信元ドメインを確認

### KV/Worker/APIエンドポイント（構造は流用）
`worker.js` のエンドポイントはそのまま使える：
`/api/diagnoses`（カウンタ）`/api/feedback(+/admin)`（感想）`/api/leads/admin`（メール一覧）`/api/save-result`（メール保存）`/api/unsubscribe`（配信停止）`/api/stripe-webhook`（購入計測）

## 7. 有料PDF（新規制作・工数大）

- 16タイプ × （日本語版・英語版）のPDF内容を**猫版に書き直し**
- R2にアップ → `love-guide-thanks.html` の `PDF_URLS.ja / .en` に公開URLを登録
- 価格は `GUIDE_CFG_BY_LANG` で設定（犬版：ja ¥1180 / en $9.99→$7.99 DISCOUNT20）

## 8. 法務（犬版と同じ対応が必要）

- `privacy.html`：特商法表記（**運営統括責任者：下山 慧**、所在地、価格＝猫版の実売価格、返金保証30日）
- `about.html`：運営者情報を猫版に
- レビュー：現状は自作。**ステマ規制**（景表法2023.10〜）に留意（「イメージです」注記 or 実ユーザー承認制へ）
- MBTI商標：OGP・見出しは「16タイプ性格診断」表記を踏襲、フッターに商標帰属注記あり（犬版と同じ仕組みを流用）
- メール配信停止リンク（特定電子メール法）：`/api/unsubscribe` の仕組みをそのまま流用

## 9. デプロイ

犬版と同じ：Cloudflare Workers（Git連携で自動デプロイ）。mainにマージ → 自動反映。
手動なら `npx wrangler deploy`。

---

## ✅ 変換チェックリスト

- [ ] 新リポジトリ作成・新チャットにスコープ追加
- [ ] ブランド名・ドメイン一括置換
- [ ] `LOC`（16タイプ×5言語）を猫版に書き換え
- [ ] `OMK`/`I18N`/`NAV_I18N`/`GUIDE_*` の犬語を猫語に
- [ ] 猫イラスト16枚（.webp/.png）＋ヒーローロゴ制作
- [ ] OGP画像80枚を再生成（eyebrow文言も猫用に）
- [ ] デザイン案Bのカラートークン適用
- [ ] ドメイン取得・KV新規・GA4新規・測定ID置換
- [ ] Worker新規デプロイ・Git連携
- [ ] R2バケット（猫PDF）・Stripe商品/リンク・Resendドメイン認証
- [ ] シークレット5種登録・Stripe Webhook登録
- [ ] 有料PDF（日英×16）制作・`PDF_URLS`登録・価格設定
- [ ] 特商法・about・レビュー・商標注記の法務対応
- [ ] テスト購入で一連の導線（表示→決済→DL→GA4計測）を確認

---

_この引き継ぎ書は 16lovetypedogs（犬版）の実装状況をもとに作成。犬版で構築済みの機能（希少性バッジ・おみくじ紙吹雪・感想承認制・メール取得＆配信停止・購入計測Stripe Webhook→GA4・多言語OGP）はすべて猫版でも流用可能。_
