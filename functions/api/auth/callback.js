// Decap CMS GitHub OAuth — callback step (Cloudflare Pages Function)
// Serves: https://www.goods-infinite.com/api/auth/callback
// GitHub redirects here with ?code=...&state=...; we exchange the code for a
// token, then run Decap's postMessage handshake so the CMS popup receives it.
export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");

  if (!code) {
    return new Response("Missing code from GitHub", { status: 400 });
  }

  const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code: code,
      state: state,
    }),
  });

  const tokenJson = await tokenRes.json();
  const accessToken = tokenJson.access_token || "";

  const html = `<!doctype html>
<html>
<head><meta charset="utf-8"><title>Authorizing GOODSINFINITE CMS...</title></head>
<body>
<script>
(function () {
  var token = ${JSON.stringify(accessToken)};
  function receiveMessage(e) {
    if (e.data === "authorizing:github") {
      e.source.postMessage(token, e.origin);
    }
  }
  window.addEventListener("message", receiveMessage, false);
  window.opener.postMessage("authorizing:github", window.opener.origin);
})();
</script>
</body>
</html>`;

  return new Response(html, {
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}
