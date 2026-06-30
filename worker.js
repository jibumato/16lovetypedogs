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

const j = (obj, status = 200) => Response.json(obj, { status });

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

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
          return j({ ok: false, error: "invalid" }, 400);
        }

        const id = "lead:" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
        await env.COUNTER.put(id, JSON.stringify({ email, type, lang, breed, typeName, ts: new Date().toISOString() }), { expirationTtl: 60 * 60 * 24 * 730 });
        await env.COUNTER.put(rlKey, "1", { expirationTtl: 300 });

        // Resendでメール送信（RESEND_API_KEYが設定されている場合のみ）
        if (env.RESEND_API_KEY && email) {
          const subjectMap = {
            ja: `あなたの恋愛わんこは ${breed}（${type}）🐾`,
            en: `Your Love Dog Result: ${breed} (${type}) 🐾`,
            ko: `나의 연애 강아지는 ${breed}（${type}）🐾`,
            zh: `你的恋爱汪汪是 ${breed}（${type}）🐾`,
            tw: `你的戀愛汪汪是 ${breed}（${type}）🐾`,
          };
          const ctaMap = {
            ja: "サイトで結果を見る",
            en: "View your result",
            ko: "결과 보기",
            zh: "查看结果",
            tw: "查看結果",
          };
          const noteMap = {
            ja: "このメールは16lovetypedogs.comの診断結果保存機能からお送りしています。",
            en: "This email was sent from the result-save feature at 16lovetypedogs.com.",
            ko: "이 이메일은 16lovetypedogs.com의 결과 저장 기능에서 발송되었습니다.",
            zh: "此邮件由 16lovetypedogs.com 的结果保存功能发送。",
            tw: "此郵件由 16lovetypedogs.com 的結果儲存功能發送。",
          };
          const subject = subjectMap[lang] || subjectMap.ja;
          const cta = ctaMap[lang] || ctaMap.ja;
          const note = noteMap[lang] || noteMap.ja;
          const siteUrl = "https://16lovetypedogs.com";
          const html = `<!DOCTYPE html><html><body style="font-family:sans-serif;max-width:520px;margin:0 auto;padding:24px;background:#fff9f5;color:#3a2e28">
<div style="text-align:center;margin-bottom:24px"><span style="font-size:48px">🐾</span></div>
<h1 style="color:#e58aa0;font-size:20px;margin:0 0 8px">${breed}</h1>
<p style="color:#7a6258;font-size:15px;margin:0 0 24px">${typeName} · ${type}</p>
<a href="${siteUrl}" style="display:inline-block;background:#e58aa0;color:#fff;text-decoration:none;border-radius:999px;padding:13px 28px;font-weight:800;font-size:15px">${cta} →</a>
<hr style="margin:32px 0;border:none;border-top:1px solid #f0e0d0">
<p style="font-size:11px;color:#b0a09a;line-height:1.7">${note}</p>
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
