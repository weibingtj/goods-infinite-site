# 启用后台发文（Decap CMS）— 操作指南

目标：让你在浏览器打开 `https://www.goods-infinite.com/admin/` 就能写/改 Insights 文章，
保存后自动提交到 GitHub，Cloudflare Pages 自动重新构建并上线。全程不用碰代码。

本指南对应已准备好的文件：
- `admin/` — Decap CMS 界面与配置（`config.yml` 已改好 github 后端）
- `functions/api/auth.js` + `functions/api/auth/callback.js` — GitHub OAuth 代理（Cloudflare Pages Functions，无需单独服务器）
- 本地 git 仓库已 `init` 并提交（见文末「你只需做 3 件事」）

---

## 你只需做 3 件事
1. 在 github.com 建一个空仓库，把本地代码 push 上去。
2. 在 Cloudflare Pages 把这个仓库连上 Git（设构建命令 + 输出目录）。
3. 建一个 GitHub OAuth App，把 Client ID / Secret 填进 Cloudflare Pages 环境变量。

下面逐步展开。

---

## 步骤 1：GitHub 建仓库
1. 登录 https://github.com （用你自己的账号，建议就是 `weibingtj` 那个）。
2. 右上角 **＋ → New repository**。
3. 填写：
   - Repository name：`goods-infinite-site`（必须和 `admin/config.yml` 里的 `repo:` 后半段一致）
   - 选 **Public**（Decap 读公开仓库最简单；若要私有，OAuth scope 已是 `repo` 也能读）
   - **不要**勾选 "Add a README / .gitignore / license"（保持空仓库，避免首次 push 冲突）
4. 点 **Create repository**。
5. 记下仓库地址，形如 `https://github.com/你的用户名/goods-infinite-site.git`。

> 仓库名可以任意，但改了就要同步改 `admin/config.yml` 的 `repo:` 和 `functions` 不用动。

---

## 步骤 2：把本地代码 push 上去（二选一）

你本地仓库已经 `git init`、提交好、并且 `origin` 已指向 `https://github.com/weibingtj/goods-infinite-site.git`，只差最后一步 push。

### 方案 A：把 PAT 发给 Jarvis，我帮你推（最快，30 秒）
1. 在 GitHub 生成一个临时 PAT：
   - 打开 https://github.com/settings/tokens/new （ classic token ）
   - **Note** 填 `goods-infinite-site-push`
   - **Expiration** 选 `7 days`（用完就删，安全）
   - **Select scopes** 勾 `repo`（会全选 repo 下 4 项）
   - 点最下方 **Generate token**
   - **立刻复制**那一串 `ghp_xxxxxxxx`（只显示一次）
2. 把 PAT 发给我（这条消息我处理完你就可以在 GitHub 删了它）。
3. 我执行 `git push`，推完告诉你，你再去 GitHub 删 token。

### 方案 B：你自己在终端推
在你电脑按 `Win + R`，输入 `cmd` 回车，然后复制粘贴：

```bash
cd E:\workbuddy\2026-08-18-12-10-21\goodsinfinite
git push -u origin main
```

然后会弹窗让你登录 GitHub；如果让你输用户名/密码：
- **Username**：`weibingtj`
- **Password**：粘贴你的 PAT（不是 GitHub 登录密码）

如果你还没有 PAT，按方案 A 的第 1 步生成一个。

> 注意：GitHub 从 2021 年起**禁止用登录密码**推代码，必须用 PAT。

---

## 步骤 3：Cloudflare Pages 连接 Git
1. Cloudflare 后台 → **Workers & Pages** → 找到现有 `goods-infinite-site` 项目 → **Settings**（或在创建页选 **Connect to Git**）。
2. 连接刚建的 GitHub 仓库（首次会跳 GitHub 授权，允许 Cloudflare 访问该仓库）。
3. 构建设置：
   - Framework preset：**None**
   - **Build command**：`python build_insights.py`
   - **Build output directory**：`.`（仓库根目录）
4. 保存并触发一次部署。
5. 自定义域 `www.goods-infinite.com` 之前已绑好，连 Git 后保留不变；以后每次 `git push` 都会自动重新部署。
6. 验证：部署完成后打开 `https://www.goods-infinite.com/api/auth` 应**重定向到 github.com 的 OAuth 授权页**（说明 Functions 已生效）。

---

## 步骤 4：建 GitHub OAuth App（给 Decap 登录用）
1. GitHub → 右上角头像 → **Settings → Developer settings → OAuth Apps → New OAuth App**。
2. 填写：
   - **Application name**：`GOODSINFINITE CMS`（任意）
   - **Homepage URL**：`https://www.goods-infinite.com`
   - **Authorization callback URL**：`https://www.goods-infinite.com/api/auth/callback`  ← 关键，必须一字不差
3. 点 **Register application**。
4. 记下 **Client ID**；点 **Generate a new client secret** 生成并**复制保存**。

---

## 步骤 5：把 OAuth 密钥填进 Cloudflare Pages
1. Cloudflare → **Workers & Pages → goods-infinite-site → Settings → Environment variables**（或 Variables）。
2. 添加两条（Production 环境）：
   - `GITHUB_CLIENT_ID` = 步骤 4 的 Client ID
   - `GITHUB_CLIENT_SECRET` = 步骤 4 的 Client Secret
3. 保存。**重新部署一次**（每次改环境变量后需重新部署才生效）。

---

## 步骤 6：登录后台发文
1. 浏览器打开 `https://www.goods-infinite.com/admin/`。
2. 点 **Login with GitHub** → 跳 GitHub 授权 → 授权后进入 CMS。
3. 左侧 **Insights / GEO Articles → New** 写新文（标题 / 日期 / 摘要 / 标签 / FAQ / 正文 Markdown）。
4. 点 **Publish** → 自动提交到 GitHub → Cloudflare Pages 重新构建（约 1 分钟）→ 上线。
5. 改已有文章：列表里点开 → 编辑 → Publish 同样生效。

---

## 步骤 7（推荐）：用 Cloudflare Access 把 /admin 护起来
OAuth 本身已要求 GitHub 登录，但 `/admin` 登录页默认公开可见。加一层 Access 更稳：
1. Cloudflare → **Zero Trust → Access → Applications → Add application → Self-hosted**。
2. Application name：`goods-infinite-admin`；**Application domain** 子域 `www`、域 `goods-infinite.com`、**Path** `/admin*`。
3. **Policies → Add a policy**：Action `Allow`，Include 你的邮箱 `weibingtj@outlook.com`（或你常用的）。
4. 保存。此后访问 `/admin` 先过 Cloudflare Access（邮箱/Google 登录），再过 Decap 的 GitHub 登录。
5. Session Duration 可设 24 小时。

> 注意：不要对 `*.pages.dev` 或整个 `www` 域开 Access，否则网站本身会被拦。只护 `/admin*`。

---

## 常见问题
- **`/api/auth` 打开是 404？** 说明 Cloudflare Pages Functions 没生效——确认仓库根目录有 `functions/api/auth.js` 且项目是「连接 Git」部署（Direct Upload 不支持 Functions）。重新部署一次。
- **点 Login 后报 redirect_uri 不匹配？** 回到 GitHub OAuth App，确认 callback 是 `https://www.goods-infinite.com/api/auth/callback`（含 `/callback`、https、无结尾斜杠）。
- **登录后 CMS 空白/读不到文章？** 检查 `admin/config.yml` 的 `repo:` 是否和真实仓库一致、`branch: main` 是否和 GitHub 默认分支一致。
- **改了文章但网站没更新？** 看 Cloudflare Pages 部署记录是否在 push 后自动跑；没跑就手动 Retry Deployment。
- **环境变量改了不生效？** Cloudflare Pages 改环境变量后必须**重新部署**一次。

---

## 当前 config.yml 待替换占位
```
repo: YOUR_GITHUB_USERNAME/goods-infinite-site   # 改成你的 用户名/仓库名
```
其余（`base_url` / `auth_endpoint` / `site_url` / `branch`）已填好，无需改。
