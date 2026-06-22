/*!
 * 16わんこ恋愛診断 — 購入導線インジェクター v1.0
 * 使い方: 診断結果ページの</body>直前に1行追加するだけ
 *
 * <script src="result_inject.js" data-type="INFP" data-lang="ja"></script>
 *
 * data-type: MBTIコード（大文字 例: INFP）
 *            省略時: URLパラメータ ?type= または window.WANKO_TYPE から自動取得
 * data-lang: 言語コード（ja / en / ko / zh）デフォルト ja
 */
(function () {
  "use strict";

  /* ---- 設定 ---- */
  var UPSELL_PAGE = "https://16lovetypedogs.com/love-guide"; /* upsell_v2.htmlのURL */
  var PRICE       = "944円";
  var PRICE_ORIG  = "1180円";
  var PRICE_OFF   = "20%OFF";

  /* ---- タイプ解決 ---- */
  var sc   = document.currentScript;
  var type = (sc && sc.dataset.type)
    || new URLSearchParams(location.search).get("type")
    || window.WANKO_TYPE   /* 既存サイトがグローバル変数を持つ場合 */
    || "INFP";
  type = type.toUpperCase();

  var lang = (sc && sc.dataset.lang)
    || new URLSearchParams(location.search).get("lang")
    || "ja";

  /* ---- タイプ別キャッチコピー ---- */
  var COPY = {
    INFP:"ベスト相性1位は？あの人の脈ありサインは？",
    INFJ:"魂の相手が誰か、攻略書が教えます。",
    ENFJ:"全16タイプ相性と、あなたに向く「脈ありサイン」とは？",
    ENFP:"可能性の恋人は誰？全16タイプ相性マップで確認。",
    INTJ:"分析タイプのあなたが知るべき「感情の落とし穴」。",
    INTP:"恋愛の仮説を現実にする攻略書。",
    ENTJ:"恋でも戦略的に動くあなたへの完全マニュアル。",
    ENTP:"刺激を保ちながら深まる関係のつくり方。",
    ISFJ:"尽くしすぎない秘訣と、あなたが幸せになれる相手。",
    ISFP:"言葉にしなくても伝わる愛の育て方。",
    ESFJ:"期待値のコントロール法と全16タイプ相性。",
    ESFP:"今の熱量を長続きさせる恋愛の深め方。",
    ISTJ:"不器用なあなたが確実に距離を縮める方法。",
    ISTP:"距離感を守りながら深まる愛の攻略法。",
    ESTJ:"正しさより関係を選ぶ、恋愛の技術。",
    ESTP:"刺激の先にある「深い絆」のつかみ方。",
  };

  var copy = COPY[type] || "あなたのタイプ専用の恋愛トリセツ。";
  var url  = UPSELL_PAGE + "?type=" + type + "&lang=" + lang;
  var COUPON_NOTE = {
    ja: 'リンク先の右上の詳細からクーポンコード「DISCOUNT20」を使うとこの価格になります。',
    en: 'On the linked page, open the details at the top right and use coupon code "DISCOUNT20" to get this price.',
    ko: '연결된 페이지 우측 상단의 상세에서 쿠폰 코드 "DISCOUNT20"을 입력하면 이 가격이 됩니다.',
    zh: '在链接页面右上角的详情中使用优惠码“DISCOUNT20”即可享受此价格。'
  }[lang] || 'リンク先の右上の詳細からクーポンコード「DISCOUNT20」を使うとこの価格になります。';
  var JP_ONLY = {
    ja: '🇯🇵 恋愛攻略書は現在、日本語版のみの<u>限定販売</u>です',
    en: '🇯🇵 The love guide is currently available in <u>Japanese only</u>.',
    ko: '🇯🇵 연애 공략서는 현재 <u>일본어판 한정 판매</u> 중입니다.',
    zh: '🇯🇵 恋爱攻略书目前<u>仅限日文版发售</u>。'
  }[lang] || '※恋愛攻略書は現在、日本語版のみの販売です。';

  /* ---- スタイル注入 ---- */
  var style = document.createElement("style");
  style.textContent = [
    ".wanko-upsell{",
    "  font-family:'Zen Maru Gothic','Hiragino Maru Gothic Pro',sans-serif;",
    "  max-width:520px;margin:32px auto;padding:0 16px;",
    "}",
    ".wanko-card{",
    "  background:linear-gradient(135deg,#fff8fb,#fffdf9);",
    "  border:1.5px solid #e0c894;border-radius:20px;",
    "  padding:22px 20px;box-shadow:0 6px 24px rgba(176,120,80,.12);",
    "  text-align:center;",
    "}",
    ".wanko-eyebrow{",
    "  font-size:11px;letter-spacing:.22em;color:#9c7430;margin-bottom:10px;",
    "}",
    ".wanko-hed{",
    "  font-size:17px;font-weight:700;color:#4a3f35;line-height:1.5;margin-bottom:6px;",
    "}",
    ".wanko-hed em{font-style:normal;color:#d35d85;}",
    ".wanko-sub{font-size:12px;color:#7a6e62;margin-bottom:16px;}",
    ".wanko-btn{",
    "  display:inline-block;width:100%;max-width:340px;padding:15px 10px;",
    "  border-radius:13px;font-size:16px;font-weight:700;color:#fff;",
    "  text-decoration:none;letter-spacing:-.01em;line-height:1.4;",
    "  background:linear-gradient(135deg,#e0779a,#d35d85);",
    "  box-shadow:0 6px 18px rgba(211,93,133,.34);",
    "  -webkit-tap-highlight-color:transparent;",
    "}",
    ".wanko-btn small{display:block;font-size:11px;opacity:.9;margin-top:2px;}",
    ".wanko-reassure{",
    "  display:flex;flex-wrap:wrap;justify-content:center;gap:4px 12px;",
    "  margin-top:12px;font-size:11px;color:#7a6e62;",
    "}",
    ".wanko-reassure span::before{content:'✓ ';color:#5bb89a;font-weight:700;}",
    ".wanko-price{",
    "  font-size:13px;color:#9c7430;margin:0 0 14px;",
    "}",
    ".wanko-price strong{font-size:20px;color:#e58aa0;}",
    ".wanko-price .wanko-off{display:inline-block;background:#e58aa0;color:#fff;font-size:11px;font-weight:800;border-radius:5px;padding:1px 6px;margin-right:5px;}",
    ".wanko-price .wanko-orig{text-decoration:line-through;color:#b6a596;margin-right:5px;}",
    ".wanko-coupon{display:inline-block;font-size:11.5px;font-weight:700;color:#e58aa0;background:#fff0f5;border:1px dashed #e58aa0;border-radius:8px;padding:4px 9px;margin:0 0 8px;}",
    ".wanko-jponly{font-size:13px;font-weight:800;color:#e58aa0;background:#fff0f5;border:2px solid #e58aa0;border-radius:12px;padding:10px 12px;margin:0 auto 14px;line-height:1.45;}",
  ].join("");
  document.head.appendChild(style);

  /* ---- HTML構築 ---- */
  var div = document.createElement("div");
  div.className = "wanko-upsell";
  div.innerHTML = [
    '<div class="wanko-card">',
    '  <div class="wanko-eyebrow">PREMIUM EDITION ・ 16わんこ恋愛診断</div>',
    '  <div class="wanko-hed">続きは、<em>あなたのタイプ専用</em>の恋愛トリセツで。</div>',
    '  <div class="wanko-sub">' + copy + '</div>',
    '  <div class="wanko-price"><span class="wanko-off">' + PRICE_OFF + '</span>買い切り <span class="wanko-orig">' + PRICE_ORIG + '</span><strong>' + PRICE + '</strong>（税込）</div>',
    '  <div class="wanko-coupon">🎟 ' + COUPON_NOTE + '</div>',
    '  <div class="wanko-jponly">' + JP_ONLY + '</div>',
    '  <a class="wanko-btn" href="' + url + '">',
    '    あなたのタイプ専用のトリセツを見る',
    '    <small>全16タイプ相性・LINE攻略・30日プランまで全14ページ</small>',
    '  </a>',
    '  <div class="wanko-reassure">',
    '    <span>購入後すぐ読める</span>',
    '    <span>スマホ／PC対応</span>',
    '    <span>追加課金なし</span>',
    '  </div>',
    '</div>',
  ].join("");

  /* ---- 挿入位置を探す ----
     優先順位:
     1. data-wanko-insert 属性を持つ要素の後
     2. .result-section / #result / .diagnosis-result などの共通クラスの後
     3. 見つからなければ body末尾
  */
  var anchor = document.querySelector("[data-wanko-insert]")
    || document.querySelector(".result-section, #result, .diagnosis-result, .type-result")
    || document.body;

  if (anchor === document.body) {
    anchor.appendChild(div);
  } else {
    anchor.parentNode.insertBefore(div, anchor.nextSibling);
  }

  /* ---- Google Fonts が未読み込みの場合に読み込む ---- */
  if (!document.querySelector("link[href*='Zen+Maru+Gothic']")) {
    var lnk = document.createElement("link");
    lnk.rel  = "stylesheet";
    lnk.href = "https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700&display=swap";
    document.head.appendChild(lnk);
  }

})();
