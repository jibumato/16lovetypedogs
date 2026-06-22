/**
 * 16lovetypedogs — Cloudflare Worker (Static Assets + 診断数カウンタAPI)
 *
 * 静的アセットは従来どおり自動配信され、Workerは未マッチのルート
 * （/api/diagnoses）だけを処理します。
 *
 * 診断数カウンタを有効化する手順（KVが無い間はAPIは count:null を返し、
 * フロントはバッジを出しません。サイト表示には影響しません）:
 *   1) npx wrangler kv namespace create COUNTER   → 表示された id を控える
 *   2) wrangler.jsonc に以下を追記:
 *        "kv_namespaces": [{ "binding": "COUNTER", "id": "<上記のid>" }]
 *   3) デプロイ
 */
const KEY = "diagnoses_total";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/diagnoses") {
      // KV未設定でも安全に動作（カウンタは出さないだけ）
      if (!env.COUNTER) {
        return Response.json({ count: null });
      }
      try {
        if (request.method === "POST") {
          const cur = parseInt((await env.COUNTER.get(KEY)) || "0", 10) || 0;
          const next = cur + 1;
          await env.COUNTER.put(KEY, String(next));
          return Response.json({ count: next });
        }
        const cur = parseInt((await env.COUNTER.get(KEY)) || "0", 10) || 0;
        return Response.json({ count: cur });
      } catch (e) {
        return Response.json({ count: null });
      }
    }

    // 感想フォームの保存（カウンタと同じKV、キー接頭辞 fb: で格納）
    if (url.pathname === "/api/feedback" && request.method === "POST") {
      if (!env.COUNTER) return Response.json({ ok: false });
      try {
        const b = await request.json();
        const rating = Math.max(0, Math.min(5, parseInt(b.rating, 10) || 0));
        const comment = String(b.comment || "").slice(0, 1000);
        const name = String(b.name || "").slice(0, 40);
        const type = String(b.type || "").slice(0, 8);
        if (!rating && !comment.trim()) return Response.json({ ok: false });
        const id = "fb:" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
        await env.COUNTER.put(id, JSON.stringify({ rating, comment, name, type, ts: new Date().toISOString() }));
        return Response.json({ ok: true });
      } catch (e) {
        return Response.json({ ok: false });
      }
    }

    // それ以外は静的アセットへフォールバック
    return env.ASSETS.fetch(request);
  },
};
