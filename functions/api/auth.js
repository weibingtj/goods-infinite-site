// Decap CMS GitHub OAuth — authorize step (Cloudflare Pages Function)
// Serves: https://www.goods-infinite.com/api/auth
// Decap opens this in a popup; we redirect to GitHub's OAuth authorize page.
export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const clientId = env.GITHUB_CLIENT_ID;
  if (!clientId) {
    return new Response("Missing GITHUB_CLIENT_ID env var", { status: 500 });
  }
  const redirectUri = url.origin + "/api/auth/callback";
  const ghAuthorize =
    "https://github.com/login/oauth/authorize" +
    "?client_id=" + encodeURIComponent(clientId) +
    "&redirect_uri=" + encodeURIComponent(redirectUri) +
    "&scope=" + encodeURIComponent("repo") +
    "&state=github";
  return Response.redirect(ghAuthorize, 302);
}
