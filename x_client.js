// X(Twitter) API クライアント（Cloudflare Worker用・OAuth 1.0a / HMAC-SHA1）
// 用途: 自分のアカウントへ画像付きツイートを自動投稿するのみ。
// 必要なシークレット: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET

import { X_ORDER, X_CAPTIONS } from "./x_posts.js";

const pct = (s) =>
  encodeURIComponent(s).replace(/[!*'()]/g, (c) => "%" + c.charCodeAt(0).toString(16).toUpperCase());

async function hmacSha1(key, msg) {
  const enc = new TextEncoder();
  const k = await crypto.subtle.importKey("raw", enc.encode(key), { name: "HMAC", hash: "SHA-1" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", k, enc.encode(msg));
  return btoa(String.fromCharCode(...new Uint8Array(sig)));
}

// method/url と（form-urlencodedやquery由来の）extraParams から OAuth ヘッダを生成。
// JSON本文やmultipartのバイナリは署名対象に含めない（＝extraParamsに入れない）のがX仕様。
async function oauthHeader(env, method, url, extraParams = {}) {
  const oauth = {
    oauth_consumer_key: env.X_API_KEY,
    oauth_token: env.X_ACCESS_TOKEN,
    oauth_signature_method: "HMAC-SHA1",
    oauth_timestamp: Math.floor(Date.now() / 1000).toString(),
    oauth_nonce: crypto.randomUUID().replace(/-/g, ""),
    oauth_version: "1.0",
  };
  const all = { ...oauth, ...extraParams };
  const paramStr = Object.keys(all).sort().map((k) => pct(k) + "=" + pct(all[k])).join("&");
  const base = method.toUpperCase() + "&" + pct(url) + "&" + pct(paramStr);
  const signingKey = pct(env.X_API_SECRET) + "&" + pct(env.X_ACCESS_TOKEN_SECRET);
  oauth.oauth_signature = await hmacSha1(signingKey, base);
  return "OAuth " + Object.keys(oauth).sort().map((k) => pct(k) + '="' + pct(oauth[k]) + '"').join(", ");
}

// 画像バイナリを v1.1 media/upload（multipart）でアップロード → media_id_string を返す
async function uploadMedia(env, bytes) {
  const url = "https://upload.twitter.com/1.1/media/upload.json";
  const auth = await oauthHeader(env, "POST", url); // multipartは署名対象パラメータ無し
  const fd = new FormData();
  fd.append("media", new Blob([bytes], { type: "image/png" }), "image.png");
  const res = await fetch(url, { method: "POST", headers: { Authorization: auth }, body: fd });
  const txt = await res.text();
  if (!res.ok) throw new Error("media upload " + res.status + ": " + txt.slice(0, 200));
  return JSON.parse(txt).media_id_string;
}

// v2 POST /2/tweets（JSON本文は署名対象外）
async function createTweet(env, text, mediaIds) {
  const url = "https://api.twitter.com/2/tweets";
  const auth = await oauthHeader(env, "POST", url);
  const body = { text };
  if (mediaIds && mediaIds.length) body.media = { media_ids: mediaIds };
  const res = await fetch(url, {
    method: "POST",
    headers: { Authorization: auth, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const txt = await res.text();
  if (!res.ok) throw new Error("tweet " + res.status + ": " + txt.slice(0, 300));
  return JSON.parse(txt);
}

// ASSETS から画像を取得してバイナリ化（social/*.png はサイトに同梱）
async function assetBytes(env, path) {
  const res = await env.ASSETS.fetch(new Request("https://x.local/" + path));
  if (!res.ok) throw new Error("asset " + path + " " + res.status);
  return new Uint8Array(await res.arrayBuffer());
}

// キューを1件進めて投稿。dry=true なら投稿せず内容だけ返す。
export async function runXPost(env, { dry = false } = {}) {
  const hasKeys = env.X_API_KEY && env.X_API_SECRET && env.X_ACCESS_TOKEN && env.X_ACCESS_TOKEN_SECRET;
  if (!hasKeys && !dry) return { ok: false, error: "missing X secrets" };

  const IDX_KEY = "x_post_idx";
  let idx = parseInt((await env.COUNTER?.get(IDX_KEY)) || "0", 10) || 0;
  if (idx >= X_ORDER.length) return { ok: true, done: true, msg: "queue finished", idx };

  const code = X_ORDER[idx];
  const text = X_CAPTIONS[code];
  const imgPaths = [`social/${code.toLowerCase()}_1.png`, `social/${code.toLowerCase()}_3.png`];

  if (dry) return { ok: true, dry: true, idx, code, text, images: imgPaths };

  // 画像アップロード（失敗した分はスキップ＝画像0でも本文は投稿してキューは進める）
  const mediaIds = [];
  for (const p of imgPaths) {
    try {
      mediaIds.push(await uploadMedia(env, await assetBytes(env, p)));
    } catch (e) {
      console.log("media skip", p, String(e).slice(0, 120));
    }
  }
  const tw = await createTweet(env, text, mediaIds);
  await env.COUNTER?.put(IDX_KEY, String(idx + 1));
  return { ok: true, idx, code, tweet_id: tw?.data?.id, media: mediaIds.length };
}
