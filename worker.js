/**
 * 16lovetypedogs — Cloudflare Worker (Static Assets + 診断数カウンタ + 感想コメント)
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
const KEY = "diagnoses_total";
const PUB = "pub:comments";   // 承認済みコメントの公開フィード（JSON配列・1キー）
const PUB_MAX = 120;          // 公開フィードに保持する最大件数
const RL_TTL = 45;            // 同一IPの連投制限（秒）

// MBTI出現率（%）。<=5 を希少タイプとして演出する。
const RARITY = { INTJ:2.1, INTP:3.3, ENTJ:1.8, ENTP:3.2, INFJ:1.5, INFP:4.4, ENFJ:2.5, ENFP:8.1,
                 ISTJ:11.6, ISFJ:13.8, ESTJ:8.7, ESFJ:12.3, ISTP:5.4, ISFP:8.8, ESTP:4.3, ESFP:8.5 };

const j = (obj, status = 200) => Response.json(obj, { status });
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;" }[c]));

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

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

        // Resendでメール送信（RESEND_API_KEYが設定されている場合のみ）
        if (env.RESEND_API_KEY && email) {
          const T = {
            ja: { subject:`あなたの恋愛わんこは ${breed}（${type}）🐾`, header:"恋愛血統書", rare:"希少タイプ", common:"人気タイプ", pct:(p)=>`約${p}%`, cta:"サイトで詳しい結果を見る", share:"📸 結果カードを保存して友だちにもシェア🐾", note:"このメールは16lovetypedogs.comの診断結果保存機能からお送りしています。", brand:"16わんこ恋愛診断" },
            en: { subject:`Your Love Dog: ${breed} (${type}) 🐾`, header:"Pedigree of Love", rare:"RARE type", common:"Popular type", pct:(p)=>`~${p}%`, cta:"See your full result", share:"📸 Save your card and share it with friends 🐾", note:"This email was sent from the result-save feature at 16lovetypedogs.com.", brand:"16 Love Type Dogs" },
            ko: { subject:`나의 연애 강아지는 ${breed}（${type}）🐾`, header:"연애 혈통서", rare:"희귀 타입", common:"인기 타입", pct:(p)=>`약${p}%`, cta:"사이트에서 자세한 결과 보기", share:"📸 결과 카드를 저장해서 친구에게도 공유해요 🐾", note:"이 이메일은 16lovetypedogs.com의 결과 저장 기능에서 발송되었습니다.", brand:"16 연애 강아지 진단" },
            zh: { subject:`你的恋爱汪汪是 ${breed}（${type}）🐾`, header:"恋爱血统书", rare:"稀有类型", common:"人气类型", pct:(p)=>`约${p}%`, cta:"在网站查看详细结果", share:"📸 保存结果卡片，分享给朋友吧 🐾", note:"此邮件由 16lovetypedogs.com 的结果保存功能发送。", brand:"16汪汪恋爱诊断" },
            tw: { subject:`你的戀愛汪汪是 ${breed}（${type}）🐾`, header:"戀愛血統書", rare:"稀有類型", common:"人氣類型", pct:(p)=>`約${p}%`, cta:"在網站查看詳細結果", share:"📸 儲存結果卡片，分享給朋友吧 🐾", note:"此郵件由 16lovetypedogs.com 的結果儲存功能發送。", brand:"16汪汪戀愛診斷" },
          };
          const t = T[lang] || T.ja;
          const subject = t.subject;
          const siteUrl = "https://16lovetypedogs.com";
          const dogUrl = type ? `${siteUrl}/${type.toLowerCase()}.webp` : "";
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
<a href="${siteUrl}" style="display:inline-block;margin-top:16px;background:#d2628f;color:#fff;text-decoration:none;border-radius:999px;padding:15px 34px;font-size:15px;font-weight:900">${t.cta} →</a>
<div style="margin-top:18px;font-size:12px;color:#938aa3">${t.share}</div>
</td></tr></table>
</td></tr>
<tr><td align="center" style="padding:20px 20px 8px"><div style="font-size:11px;color:#b0a4bd;line-height:1.7">${t.note}<br>${t.brand}</div></td></tr>
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

    // それ以外は静的アセットへフォールバック
    return env.ASSETS.fetch(request);
  },
};
