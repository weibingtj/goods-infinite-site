# Deploy GOODSINFINITE to Cloudflare Pages

## Current state (done)
- Domain: **goods-infinite.com** (registered; Cloudflare account weibingtj@outlook.com)
- All absolute URLs already swapped to `https://www.goods-infinite.com` across 10 root pages, 11 insight articles, `sitemap.xml`, `llms.txt`, `robots.txt`, and the build script.
- Site root directory: `goodsinfinite/` — contains 10 root HTML pages, `insights/` (11 articles), `assets/`, `admin/` (Decap CMS), `content/insights/` (Markdown sources), `build_insights.py`.
- `_headers` added for asset caching + security headers (Cloudflare Pages native).
- **Deployed & live**: `https://goods-infinite-site.pages.dev` (Cloudflare Pages, Direct Upload via wrangler). Custom domain `www.goods-infinite.com` not yet attached — see Route A/B custom-domain step.

## Route A — Connect GitHub in Cloudflare dashboard (recommended, 5–10 min)
Prereq: push `goodsinfinite/` to a GitHub repo (create the repo, then `git push`).
1. Cloudflare → **Workers & Pages** → Create → **Pages** → **Connect to Git**.
2. Select your repo.
3. Build settings:
   - Framework preset: **None**
   - Build command: `python build_insights.py`
   - Build output directory: `.` (repo root)
4. Deploy → you get a `*.pages.dev` preview URL.
5. **Custom domains** → add `www.goods-infinite.com` (and apex `goods-infinite.com`). Cloudflare auto-adds the DNS record + proxy.
6. SSL: Universal (auto, active in a few minutes).
7. **Email Routing** (Cloudflare → Email): route `goodsinfinite@goods-infinite.com` → forward to `goodsinfinite@goods-infinite.com`.

## Route B — Scripted Direct Upload via wrangler (one command)
Prereq: Node.js installed (for `npx wrangler`). Credentials live in `.deploy.env` (git-ignored, never committed):
```
CLOUDFLARE_API_TOKEN=cfat_xxx        # scoped: Account>Cloudflare Pages>Edit (+ Zone>Dns>Edit for custom domain)
CLOUDFLARE_ACCOUNT_ID=xxxxxxxx       # dashboard bottom-right
PROJECT_NAME=goods-infinite-site
```
Deploy:
```
python deploy_cloudflare.py            # build insight articles + wrangler pages deploy .
python deploy_cloudflare.py --dry-run  # build only, no upload
```
The script runs `build_insights.py` then `wrangler pages deploy . --project-name=...`. wrangler reads the token from `.deploy.env`. After deploy you add the custom domain in the dashboard.

> Note: an earlier hand-rolled multipart upload was replaced by wrangler because Cloudflare mis-parsed it and created empty deployments. wrangler is the supported, reliable path.

## Post-launch GEO checks
- Open `https://www.goods-infinite.com/llms.txt` and `https://www.goods-infinite.com/sitemap.xml` (must be live).
- Submit `sitemap.xml` in Google Search Console + Bing Webmaster Tools.
- Ask ChatGPT / Claude: *"what is 1210 bonded import China"* — verify our article is cited.

## Security note
The Cloudflare login password appeared in chat. **Change it now.** For ongoing work use a scoped **API Token** (revocable) — never share the account password again.

## Before going live
- `Case 02` in `case-studies.html` is still an *Illustrative* (sample) story — replace with a real authorized client (preferably a cosmetics brand, per Ben's content decision) before publishing.
- `admin/config.yml` still has a placeholder GitHub `repo:` — replace with your real repo before enabling the CMS backend.

## Enable browser-based CMS (Decap) — see SETUP-CMS.md
The local git repo is already initialized and committed (branch `main`, 60 files, secrets excluded).
To let Ben write/edit Insights articles from a browser:
- `functions/api/auth.js` + `functions/api/auth/callback.js` = GitHub OAuth proxy (Cloudflare Pages Functions, no separate server).
- Full click-by-click recipe (GitHub repo → connect Pages → OAuth App → env vars → optional Cloudflare Access): **SETUP-CMS.md**.
- Switching from Direct Upload to Git-connected Pages keeps the custom domain/SSL; every `git push` auto-rebuilds.
- Only remaining manual steps for Ben: create the GitHub repo, `git remote add` + `git push`, create the OAuth App, paste keys into Pages env vars.
