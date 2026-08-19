// Serve Google Search Console verification file content directly.
// Cloudflare Pages auto-strips .html extensions (308 redirect), which breaks
// Google's HTML-file ownership check. This Function intercepts the exact path
// and returns the required verification string, bypassing the extension strip.
export async function onRequest() {
  return new Response(
    "google-site-verification: google33bc9d4e74be2ca0.html",
    {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store",
      },
    }
  );
}
