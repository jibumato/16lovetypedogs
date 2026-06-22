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
    ja: '944円はプロモコード適用後の価格です',
    en: '¥944 is the price after the promo code is applied.',
    ko: '944엔은 프로모션 코드 적용 후 가격입니다.',
    zh: '944日元为使用促销代码后的价格。'
  }[lang] || '944円はプロモコード適用後の価格です';
  var JP_ONLY = {
    ja: '🇯🇵 攻略書は現在、日本語版のみの限定販売です',
    en: '🇯🇵 The love guide is currently sold in Japanese only.',
    ko: '🇯🇵 공략서는 현재 일본어판만 한정 판매 중입니다.',
    zh: '🇯🇵 攻略书目前仅限日文版发售。'
  }[lang] || '🇯🇵 攻略書は現在、日本語版のみの限定販売です';
  var REFUND = {
    ja: '満足保証・全額返金',
    en: 'Money-back guarantee',
    ko: '만족 보장·전액 환불',
    zh: '不满意全额退款'
  }[lang] || '満足保証・全額返金';

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
    ".wanko-coupon{font-size:11px;color:#9c8676;margin:8px 0 0;}",
    ".wanko-jponly{font-size:11px;font-weight:700;color:#e58aa0;margin:10px 0 0;}",
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
    '  <a class="wanko-btn" href="' + url + '">',
    '    あなたのタイプ専用のトリセツを見る',
    '    <small>全16タイプ相性・LINE攻略・30日プランまで全14ページ</small>',
    '  </a>',
    '  <div class="wanko-coupon">🎟 ' + COUPON_NOTE + '</div>',
    '  <div class="wanko-reassure">',
    '    <span>購入後すぐ読める</span>',
    '    <span>スマホ／PC対応</span>',
    '    <span>追加課金なし</span>',
    '    <span>' + REFUND + '</span>',
    '  </div>',
    '  <div class="wanko-jponly">' + JP_ONLY + '</div>',
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

  /* ---- 計測: 結果ページ→攻略書ページへの遷移クリック（ファネル） ---- */
  var btn = div.querySelector(".wanko-btn");
  if (btn) {
    btn.addEventListener("click", function () {
      try {
        if (window.gtag) gtag("event", "select_promotion", {
          promotion_name: "love-guide-upsell",
          creative_slot: "result_inject",
          items: [{ item_id: type, item_name: "love-guide" }]
        });
      } catch (e) {}
    });
  }

  /* ---- Google Fonts が未読み込みの場合に読み込む ---- */
  if (!document.querySelector("link[href*='Zen+Maru+Gothic']")) {
    var lnk = document.createElement("link");
    lnk.rel  = "stylesheet";
    lnk.href = "https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700&display=swap";
    document.head.appendChild(lnk);
  }

})();
