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

    // それ以外は静的アセットへフォールバック
    return env.ASSETS.fetch(request);
  },
};
