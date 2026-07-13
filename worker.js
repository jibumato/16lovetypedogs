/**
 * 16lovetypedogs — Cloudflare Worker (Static Assets + 診断数カウンタ + 感想コメント + X自動投稿)
 *
 * 静的アセットは従来どおり自動配信され、Workerは /api/* のルートだけを処理します。
 *
 * 有効化手順（KVが無い間はAPIは安全に no-op を返し、サイト表示には影響しません）:
 *   1) npx wrangler kv namespace create COUNTER   → 表示された id を控える
 *   2) wrangler.jsonc に追記:
 *        "kv_namespaces": [{ "binding": "COUNTER", "id": "<上記のid>" }]
 *   3) 承認用パスワードを設定:
 *        npx wrangler secret put ADMIN_TOKEN
 *   4) npx wrangler deploy
 *
 * 感想コメントの仕組み（承認制）:
 *   - 投稿は `fb:<id>` に approved:false で保存（公開されない）
 *   - 管理者が /admin.html で承認すると、公開フィード `pub:comments` に移動
 *   - 公開フィード(GET /api/feedback)はこの1キーだけを読む（高速・低コスト）
 */
import { runXPost, whoAmI } from "./x_client.js";

const KEY = "diagnoses_total";
const JA_TYPES = new Set(["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]);
const PUB = "pub:comments";   // 承認済みコメントの公開フィード（JSON配列・1キー）
const PUB_MAX = 120;          // 公開フィードに保持する最大件数
const RL_TTL = 45;            // 同一IPの連投制限（秒）

// MBTI出現率（%）。<=5 を希少タイプとして演出する。
const RARITY = { INTJ:2.1, INTP:3.3, ENTJ:1.8, ENTP:3.2, INFJ:1.5, INFP:4.4, ENFJ:2.5, ENFP:8.1,
                 ISTJ:11.6, ISFJ:13.8, ESTJ:8.7, ESFJ:12.3, ISTP:5.4, ISFP:8.8, ESTP:4.3, ESFP:8.5 };

const j = (obj, status = 200) => Response.json(obj, { status });
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;" }[c]));

// 配信停止リンクの改ざん防止トークン（emailのHMAC先頭24桁）
async function hmacHex(secret, msg) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
const unsubSecret = (env) => env.UNSUB_SECRET || env.ADMIN_TOKEN || "16ltd-unsub-v1";

export default {
  // 毎日21:00 JST(=12:00 UTC)に1タイプ自動投稿（wrangler.jsonc の crons で発火）
  async scheduled(event, env, ctx) {
    ctx.waitUntil(runXPost(env).then((r) => console.log("x-post", JSON.stringify(r))).catch((e) => console.log("x-post error", String(e))));
  },

  async fetch(request, env) {
    const url = new URL(request.url);

    // ───────── X自動投稿の手動トリガ（本番前の動作確認用） ─────────
    //   ?token=<ADMIN_TOKEN> 必須。 &dry=1 で投稿せず内容だけ確認。
    //   &setidx=N でキュー位置(x_post_idx)をNに設定（消えた分の投稿し直し用）。
    if (url.pathname === "/api/x-post") {
      const token = url.searchParams.get("token") || "";
      if (!env.ADMIN_TOKEN || token !== env.ADMIN_TOKEN) return j({ ok: false, error: "auth" }, 401);
      if (url.searchParams.get("whoami") === "1") {
        return j(await whoAmI(env));
      }
      const setidx = url.searchParams.get("setidx");
      if (setidx !== null) {
        const n = Math.max(0, parseInt(setidx, 10) || 0);
        await env.COUNTER?.put("x_post_idx", String(n));
        return j({ ok: true, setidx: n });
      }
      try {
        const r = await runXPost(env, { dry: url.searchParams.get("dry") === "1" });
        return j(r);
      } catch (e) {
        return j({ ok: false, error: String(e).slice(0, 300) }, 500);
      }
    }

    // ───────── 診断数カウンタ ─────────
    if (url.pathname === "/api/diagnoses") {
      if (!env.COUNTER) return j({ count: null });
      try {
        if (request.method === "POST") {
          const cur = parseInt((await env.COUNTER.get(KEY)) || "0", 10) || 0;
          const next = cur + 1;
          await env.COUNTER.put(KEY, String(next));
          return j({ count: next });
        }
        const cur = parseInt((await env.COUNTER.get(KEY)) || "0", 10) || 0;
        return j({ count: cur });
      } catch (e) {
        return j({ count: null });
      }
    }

    // ───────── 感想コメント（公開API） ─────────
    if (url.pathname === "/api/feedback") {
      if (!env.COUNTER) return j({ ok: false, comments: [] });

      // 投稿（承認待ちとして保存）
      if (request.method === "POST") {
        try {
          const ip = request.headers.get("CF-Connecting-IP") || "0";
          const rlKey = "rl:" + ip;
          if (await env.COUNTER.get(rlKey)) return j({ ok: false, error: "rate" }, 429);

          const b = await request.json();
          if (b.website) return j({ ok: true });           // ハニーポット（ボットを静かに弾く）
          const rating = Math.max(0, Math.min(5, parseInt(b.rating, 10) || 0));
          const comment = String(b.comment || "").trim().replace(/\s+/g, " ").slice(0, 300);
          const name = String(b.name || "").trim().slice(0, 24);
          const type = String(b.type || "").slice(0, 8).toUpperCase();
          if (!comment) return j({ ok: false, error: "empty" }, 400);
          // リンク/HTMLを含む投稿はスパムとして拒否
          if (/(https?:\/\/|www\.|\.com\b|\.net\b|\.ru\b|<\/?[a-z])/i.test(comment) ||
              /(https?:\/\/|www\.)/i.test(name)) {
            return j({ ok: false, error: "link" }, 400);
          }
          const id = "fb:" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
          await env.COUNTER.put(id, JSON.stringify({ id, rating, comment, name, type, ts: new Date().toISOString(), approved: false }));
          await env.COUNTER.put(rlKey, "1", { expirationTtl: RL_TTL });
          return j({ ok: true });
        } catch (e) {
          return j({ ok: false }, 400);
        }
      }

      // 公開フィード取得（承認済みのみ・1キー読み）
      try {
        const raw = await env.COUNTER.get(PUB);
        const comments = raw ? JSON.parse(raw) : [];
        return j({ ok: true, comments });
      } catch (e) {
        return j({ ok: true, comments: [] });
      }
    }

    // ───────── 感想コメント（管理API・トークン保護） ─────────
    if (url.pathname === "/api/feedback/admin") {
      if (!env.COUNTER) return j({ ok: false, error: "no-kv" });
      const token = request.headers.get("X-Admin-Token") || url.searchParams.get("token") || "";
      if (!env.ADMIN_TOKEN || token !== env.ADMIN_TOKEN) return j({ ok: false, error: "auth" }, 401);

      // 承認待ち一覧
      if (request.method === "GET") {
        try {
          const list = await env.COUNTER.list({ prefix: "fb:" });
          const pending = [];
          for (const k of list.keys) {
            const v = await env.COUNTER.get(k.name);
            if (!v) continue;
            try { const o = JSON.parse(v); if (!o.approved) pending.push(o); } catch (e) {}
          }
          pending.sort((a, b) => (a.ts < b.ts ? 1 : -1));
          return j({ ok: true, pending });
        } catch (e) {
          return j({ ok: false }, 500);
        }
      }

      // 承認 / 却下
      if (request.method === "POST") {
        try {
          const b = await request.json();
          const id = String(b.id || "");
          if (!id.startsWith("fb:")) return j({ ok: false }, 400);
          if (b.action === "reject") {
            await env.COUNTER.delete(id);
            return j({ ok: true });
          }
          if (b.action === "approve") {
            const v = await env.COUNTER.get(id);
            if (!v) return j({ ok: false }, 404);
            const o = JSON.parse(v);
            const raw = await env.COUNTER.get(PUB);
            let arr = [];
            try { arr = raw ? JSON.parse(raw) : []; } catch (e) { arr = []; }
            arr.unshift({ rating: o.rating, comment: o.comment, name: o.name, type: o.type, ts: o.ts });
            if (arr.length > PUB_MAX) arr = arr.slice(0, PUB_MAX);
            await env.COUNTER.put(PUB, JSON.stringify(arr));
            await env.COUNTER.delete(id);
            return j({ ok: true });
          }
          return j({ ok: false }, 400);
        } catch (e) {
          return j({ ok: false }, 400);
        }
      }
    }

    // ───────── メールリード一覧（管理API・トークン保護） ─────────
    if (url.pathname === "/api/leads/admin") {
      if (!env.COUNTER) return j({ ok: false, error: "no-kv" });
      const token = request.headers.get("X-Admin-Token") || url.searchParams.get("token") || "";
      if (!env.ADMIN_TOKEN || token !== env.ADMIN_TOKEN) return j({ ok: false, error: "auth" }, 401);

      if (request.method === "GET") {
        try {
          const leads = [];
          let cursor;
          do {
            const list = await env.COUNTER.list({ prefix: "lead:", cursor });
            for (const k of list.keys) {
              const v = await env.COUNTER.get(k.name);
              if (!v) continue;
              try { leads.push(JSON.parse(v)); } catch (e) {}
            }
            cursor = list.list_complete ? null : list.cursor;
          } while (cursor);
          leads.sort((a, b) => (a.ts < b.ts ? 1 : -1));
          return j({ ok: true, leads });
        } catch (e) {
          return j({ ok: false }, 500);
        }
      }
    }

    // ───────── 結果メール保存 ─────────
    if (url.pathname === "/api/save-result") {
      if (request.method !== "POST") return j({ ok: false }, 405);
      if (!env.COUNTER) return j({ ok: false, error: "no-kv" });

      try {
        const ip = request.headers.get("CF-Connecting-IP") || "0";
        const rlKey = "sr-rl:" + ip;
        if (await env.COUNTER.get(rlKey)) return j({ ok: false, error: "rate" }, 429);

        const b = await request.json();
        const email = String(b.email || "").trim().toLowerCase().slice(0, 254);
        const type  = String(b.type  || "").slice(0, 8).toUpperCase();
        const lang  = String(b.lang  || "ja").slice(0, 8);
        const breed = String(b.breed    || "").slice(0, 80);
        const typeName = String(b.typeName || "").slice(0, 80);
        const tag  = String(b.tag  || "").slice(0, 160);
        const role = String(b.role || "").slice(0, 40);

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
          return j({ ok: false, error: "invalid" }, 400);
        }

        const id = "lead:" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
        await env.COUNTER.put(id, JSON.stringify({ email, type, lang, breed, typeName, ts: new Date().toISOString() }), { expirationTtl: 60 * 60 * 24 * 730 });
        await env.COUNTER.put(rlKey, "1", { expirationTtl: 300 });

        // Resendでメール送信（RESEND_API_KEYが設定されていて、配信停止していない場合のみ）
        const isUnsub = await env.COUNTER.get("unsub:" + email);
        if (env.RESEND_API_KEY && email && !isUnsub) {
          const T = {
            ja: { subject:`あなたの恋愛わんこは ${breed}（${type}）🐾`, header:"恋愛血統書", rare:"希少タイプ", common:"人気タイプ", pct:(p)=>`約${p}%`, cta:"サイトで詳しい結果を見る", share:"📸 結果カードを保存して友だちにもシェア🐾", invite:"💌 気になるあの人にも送って、2人の相性をチェック🐾", note:"このメールは16lovetypedogs.comの診断結果保存機能からお送りしています。", brand:"16わんこ恋愛診断", unsub:"配信を停止する" },
            en: { subject:`Your Love Dog: ${breed} (${type}) 🐾`, header:"Pedigree of Love", rare:"RARE type", common:"Popular type", pct:(p)=>`~${p}%`, cta:"See your full result", share:"📸 Save your card and share it with friends 🐾", invite:"💌 Send it to your crush too — and check your compatibility 🐾", note:"This email was sent from the result-save feature at 16lovetypedogs.com.", brand:"16 Love Type Dogs", unsub:"Unsubscribe" },
            ko: { subject:`나의 연애 강아지는 ${breed}（${type}）🐾`, header:"연애 혈통서", rare:"희귀 타입", common:"인기 타입", pct:(p)=>`약${p}%`, cta:"사이트에서 자세한 결과 보기", share:"📸 결과 카드를 저장해서 친구에게도 공유해요 🐾", invite:"💌 마음에 둔 그 사람에게도 보내서 궁합을 확인해요 🐾", note:"이 이메일은 16lovetypedogs.com의 결과 저장 기능에서 발송되었습니다.", brand:"16 연애 강아지 진단", unsub:"수신 거부" },
            zh: { subject:`你的恋爱汪汪是 ${breed}（${type}）🐾`, header:"恋爱血统书", rare:"稀有类型", common:"人气类型", pct:(p)=>`约${p}%`, cta:"在网站查看详细结果", share:"📸 保存结果卡片，分享给朋友吧 🐾", invite:"💌 也发给心仪的TA，一起看看你们的契合度🐾", note:"此邮件由 16lovetypedogs.com 的结果保存功能发送。", brand:"16汪汪恋爱诊断", unsub:"退订" },
            tw: { subject:`你的戀愛汪汪是 ${breed}（${type}）🐾`, header:"戀愛血統書", rare:"稀有類型", common:"人氣類型", pct:(p)=>`約${p}%`, cta:"在網站查看詳細結果", share:"📸 儲存結果卡片，分享給朋友吧 🐾", invite:"💌 也發給心儀的TA，一起看看你們的契合度🐾", note:"此郵件由 16lovetypedogs.com 的結果儲存功能發送。", brand:"16汪汪戀愛診斷", unsub:"取消訂閱" },
          };
          const t = T[lang] || T.ja;
          const subject = t.subject;
          const siteUrl = "https://16lovetypedogs.com";
          const lc = type.toLowerCase();
          const dogUrl = type ? `${siteUrl}/${lc}.webp` : "";
          // 結果に直接飛ぶディープリンク（SPAは ?type/?lang を読んで結果を描画。koは静的タイプページ）
          const resultUrl = !type ? siteUrl
            : lang === "ko" ? `${siteUrl}/ko/${lc}.html`
            : `${siteUrl}/?type=${type}&lang=${lang}`;
          // 配信停止リンク（特定電子メール法対応・改ざん防止トークン付き）
          const unsubTok = (await hmacHex(unsubSecret(env), email)).slice(0, 24);
          const unsubUrl = `${siteUrl}/api/unsubscribe?e=${encodeURIComponent(email)}&lang=${lang}&t=${unsubTok}`;
          const p = RARITY[type];
          const rare = p != null && p <= 5;
          const badge = p == null ? "" :
            `<span style="display:inline-block;background:${rare?"#8e54b8":"#c88c28"};color:#fff;font-size:11px;font-weight:800;border-radius:999px;padding:6px 14px;letter-spacing:.03em">${rare?"✨ "+t.rare:"👑 "+t.common} ・ ${t.pct(p)}</span>`;
          const dogImg = dogUrl ?
            `<table cellpadding="0" cellspacing="0" align="center" style="margin:18px auto 0"><tr><td style="border-radius:50%;background:#fbe6ef;border:5px solid #f7d3e2;width:180px;height:180px" align="center" valign="middle"><img src="${dogUrl}" width="170" height="170" style="display:block;border-radius:50%" alt="${esc(breed)}"></td></tr></table>` : "";
          const roleLine = (typeName || role) ? `<div style="font-size:13px;color:#938aa3;margin-top:5px;font-weight:700">${esc(type)}${role?" ・ "+esc(role):(typeName?" ・ "+esc(typeName):"")}</div>` : "";
          const tagLine = tag ? `<div style="margin:14px 18px 0;font-size:14px;color:#574f63;line-height:1.85">${esc(tag)}</div>` : "";
          const html = `<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#ece6f0;font-family:'Hiragino Kaku Gothic ProN','Helvetica Neue',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#ece6f0;padding:28px 0"><tr><td align="center">
<table width="500" cellpadding="0" cellspacing="0" style="max-width:500px;width:100%">
<tr><td align="center" style="padding:6px 0 16px"><span style="font-size:13px;font-weight:800;letter-spacing:.14em;color:#b78fd6">🐾 ${t.header} 🐾</span></td></tr>
<tr><td style="background:#fffdfb;border:2px solid #f3c9da;border-radius:24px;padding:30px 26px">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
${badge}
${dogImg}
<div style="font-size:25px;font-weight:900;color:#d2628f;margin-top:18px">${esc(breed)}</div>
${roleLine}
${tagLine}
<div style="margin:20px 0 4px;color:#f3c9da;font-size:15px">🐾 ───────── 🐾</div>
<a href="${resultUrl}" style="display:inline-block;margin-top:16px;background:#d2628f;color:#fff;text-decoration:none;border-radius:999px;padding:15px 34px;font-size:15px;font-weight:900">${t.cta} →</a>
<div style="margin-top:16px;font-size:12.5px;color:#d2628f;font-weight:800">${t.invite}</div>
<div style="margin-top:12px;font-size:12px;color:#938aa3">${t.share}</div>
</td></tr></table>
</td></tr>
<tr><td align="center" style="padding:20px 20px 8px"><div style="font-size:11px;color:#b0a4bd;line-height:1.7">${t.note}<br>${t.brand}<br><a href="${unsubUrl}" style="color:#b0a4bd;text-decoration:underline">${t.unsub}</a></div></td></tr>
</table>
</td></tr></table>
</body></html>`;
          await fetch("https://api.resend.com/emails", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + env.RESEND_API_KEY,
            },
            body: JSON.stringify({
              from: "16わんこ恋愛診断 <noreply@16lovetypedogs.com>",
              to: [email],
              subject,
              html,
            }),
          });
        }

        return j({ ok: true });
      } catch (e) {
        return j({ ok: false }, 400);
      }
    }

    // ───────── メール配信停止（特定電子メール法対応） ─────────
    if (url.pathname === "/api/unsubscribe") {
      const email = (url.searchParams.get("e") || "").trim().toLowerCase();
      const lang = (url.searchParams.get("lang") || "ja").slice(0, 8);
      const tk = url.searchParams.get("t") || "";
      const M = {
        ja: { t:"配信停止", ok:"配信を停止しました", okb:"今後このメールアドレスへの配信は行いません。ご利用ありがとうございました🐾", ng:"リンクが無効です", ngb:"リンクの有効期限が切れているか、URLが正しくない可能性があります。", back:"サイトへ戻る" },
        en: { t:"Unsubscribe", ok:"You're unsubscribed", okb:"We won't send any more emails to this address. Thank you 🐾", ng:"Invalid link", ngb:"This link may be expired or incorrect.", back:"Back to site" },
        ko: { t:"수신 거부", ok:"수신을 거부했습니다", okb:"앞으로 이 주소로 메일을 보내지 않습니다. 이용해 주셔서 감사합니다 🐾", ng:"잘못된 링크", ngb:"링크가 만료되었거나 올바르지 않을 수 있습니다.", back:"사이트로 돌아가기" },
        zh: { t:"退订", ok:"已退订", okb:"今后不会再向此邮箱发送邮件。感谢您的使用 🐾", ng:"链接无效", ngb:"链接可能已过期或不正确。", back:"返回网站" },
        tw: { t:"取消訂閱", ok:"已取消訂閱", okb:"今後不會再向此信箱發送郵件。感謝您的使用 🐾", ng:"連結無效", ngb:"連結可能已過期或不正確。", back:"返回網站" },
      };
      const m = M[lang] || M.ja;
      const page = (title, body) => new Response(
        `<!DOCTYPE html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${title}</title>`
        + `<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(160deg,#fdf4f8,#f3eefb);font-family:'Hiragino Kaku Gothic ProN',sans-serif;color:#574f63;padding:24px}`
        + `.c{max-width:380px;text-align:center;background:#fffdfb;border:1px solid #f3d3e0;border-radius:22px;padding:34px 26px;box-shadow:0 18px 44px -22px rgba(180,120,160,.5)}`
        + `.e{font-size:40px}h1{font-size:18px;color:#d2628f;margin:14px 0 8px}p{font-size:13.5px;line-height:1.8;color:#7a6258;margin:0 0 20px}`
        + `a{display:inline-block;background:#d2628f;color:#fff;text-decoration:none;border-radius:999px;padding:11px 24px;font-size:13px;font-weight:800}</style></head>`
        + `<body><div class="c"><div class="e">🐾</div><h1>${title}</h1><p>${body}</p><a href="https://16lovetypedogs.com/?lang=${lang}">${m.back}</a></div></body></html>`,
        { headers: { "Content-Type": "text/html; charset=utf-8" }, status: 200 }
      );
      if (!email || !env.COUNTER) return page(m.ng, m.ngb);
      const expect = (await hmacHex(unsubSecret(env), email)).slice(0, 24);
      if (!tk || tk !== expect) return page(m.ng, m.ngb);
      try {
        await env.COUNTER.put("unsub:" + email, new Date().toISOString());
        // 既存リードからも該当メールを削除
        let cursor;
        do {
          const list = await env.COUNTER.list({ prefix: "lead:", cursor });
          for (const k of list.keys) {
            const v = await env.COUNTER.get(k.name);
            if (!v) continue;
            try { if (JSON.parse(v).email === email) await env.COUNTER.delete(k.name); } catch (e) {}
          }
          cursor = list.list_complete ? null : list.cursor;
        } while (cursor);
      } catch (e) {}
      return page(m.ok, m.okb);
    }

    // ───────── Checkout Session作成（日本語版・PayPay対応のためPayment Linksを使わずAPIで生成） ─────────
    // Payment LinksはAdaptive Pricingが常時強制ONでPayPayと非互換なため、コード経由でCheckout Sessionを都度作成する。
    if (url.pathname === "/api/checkout") {
      if (request.method !== "POST") return j({ ok: false }, 405);
      if (!env.STRIPE_SECRET_KEY) return j({ ok: false, error: "no-key" }, 500);
      try {
        const b = await request.json();
        const type = String(b.type || "").toUpperCase().slice(0, 8);
        const cid = String(b.cid || "").replace(/[^a-zA-Z0-9.\-]/g, "").slice(0, 60);
        if (!JA_TYPES.has(type)) return j({ ok: false, error: "bad-type" }, 400);

        const siteUrl = "https://16lovetypedogs.com";
        const successUrl = `${siteUrl}/thanks.html?type=${type.toLowerCase()}&session_id={CHECKOUT_SESSION_ID}`;
        const cancelUrl = `${siteUrl}/?type=${type}&lang=ja`;
        const clientReferenceId = cid ? `${type}_${cid}` : type;

        const form = new URLSearchParams();
        form.set("mode", "payment");
        form.set("success_url", successUrl);
        form.set("cancel_url", cancelUrl);
        form.set("client_reference_id", clientReferenceId);
        form.set("submit_type", "pay");
        form.set("line_items[0][quantity]", "1");
        form.set("line_items[0][price_data][currency]", "jpy");
        form.set("line_items[0][price_data][unit_amount]", "1180");
        form.set("line_items[0][price_data][product_data][name]", `${type}_love_guide_JP`);
        form.set("payment_method_types[0]", "card");
        form.set("payment_method_types[1]", "paypay");

        const res = await fetch("https://api.stripe.com/v1/checkout/sessions", {
          method: "POST",
          headers: {
            "Authorization": "Bearer " + env.STRIPE_SECRET_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: form.toString(),
        });
        const session = await res.json();
        if (!res.ok) return j({ ok: false, error: (session && session.error && session.error.message) || "stripe-error" }, 400);
        return j({ ok: true, url: session.url });
      } catch (e) {
        return j({ ok: false, error: "exception" }, 400);
      }
    }

    // ───────── Stripe Webhook → GA4 購入計測（サーバー側・取りこぼし防止） ─────────
    if (url.pathname === "/api/stripe-webhook") {
      if (request.method !== "POST") return j({ ok: false }, 405);
      const raw = await request.text();
      // 署名検証（未設定なら安全にno-opで200を返す）
      if (!env.STRIPE_WEBHOOK_SECRET) return j({ ok: true, skipped: "no-secret" });
      try {
        const sigHeader = request.headers.get("stripe-signature") || "";
        const parts = {};
        sigHeader.split(",").forEach((kv) => { const i = kv.indexOf("="); if (i > 0) parts[kv.slice(0, i).trim()] = kv.slice(i + 1).trim(); });
        const t = parts.t, v1 = parts.v1;
        const expected = await hmacHex(env.STRIPE_WEBHOOK_SECRET, `${t}.${raw}`);
        if (!t || !v1 || expected !== v1) return j({ ok: false, error: "bad-signature" }, 400);

        const event = JSON.parse(raw);
        if (event.type === "checkout.session.completed") {
          const s = event.data.object || {};
          // client_reference_id = "<TYPE>_<gaClientId(dot→dash)>"
          const crid = String(s.client_reference_id || "");
          const usx = crid.indexOf("_");
          const type = usx > 0 ? crid.slice(0, usx) : "";
          const cidRaw = usx > 0 ? crid.slice(usx + 1) : "";
          const clientId = cidRaw ? cidRaw.replace("-", ".") : (s.id || "555.555");
          const cur = String(s.currency || "jpy").toLowerCase();
          const zeroDec = cur === "jpy" || cur === "krw";
          const value = (s.amount_total != null) ? (zeroDec ? s.amount_total : s.amount_total / 100) : 1180;

          const mid = env.GA_MEASUREMENT_ID || "G-C3W7FBQRCD";
          if (env.GA_MP_API_SECRET) {
            await fetch(`https://www.google-analytics.com/mp/collect?measurement_id=${mid}&api_secret=${env.GA_MP_API_SECRET}`, {
              method: "POST",
              body: JSON.stringify({
                client_id: clientId,
                events: [{
                  name: "purchase",
                  params: {
                    transaction_id: s.id,                 // クライアント側と同一IDでGA4が自動重複排除
                    currency: cur.toUpperCase(),
                    value: value,
                    items: [{ item_id: type || "love-guide", item_name: "love-guide", price: value, quantity: 1 }],
                  },
                }],
              }),
            });
          }
        }
        return j({ ok: true });
      } catch (e) {
        return j({ ok: false }, 400);
      }
    }

    // それ以外は静的アセットへフォールバック
    return env.ASSETS.fetch(request);
  },
};
