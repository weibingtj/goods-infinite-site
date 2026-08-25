# Project Memory — GOODSINFINITE TRADE LIMITED 英文官网

## 战略定位
- 官网读者 = 海外品牌决策层（欧美 B2B）；使命 = 帮海外品牌进入中国大陆市场。
- GOODSINFINITE 自身定位：HK 进口商/分销主体（GOODSINFINITE TRADE LIMITED），提供大陆市场开拓、产业带调研、采购代理。
- **New Media 集群战略（2026-08-20 Ben 最终拍板）**：写**中国国内平台**，帮海外品牌在国内平台（微信/抖音/小红书 RED/快手）上宣传——即海外品牌进入中国后的中国社媒营销 how-to。读者是海外品牌决策层，GOODSINFINITE 定位为代运营/顾问。注意：Ben 中途一度想改成"面向海外受众获客"，当日 12:27 已 revert 回国内平台主线。

## 技术约定
- Insights 文章源：`content/insights/*.md`；构建：`python build_insights.py`（自动注入 GA G-68HRE7BJFK、BreadcrumbList、作者 Person schema、dateModified、权威机构引用块）。
- 每篇必须含：Definition Lead 写法、stat card、3–5 条指向 customs/mofcom/samr/chinatax 的内联引用、Sources 小节、2–3 条站内内链、FAQPage JSON-LD。
- 发布节奏：验证期（2026-08-19 起两周）3 篇/天；约 2026-09-02 起下调到 1–2 篇/天，优先保质量与内链。
- 推送：读 `.github_token` 内联 PAT 推送 `weibingtj/goods-infinite-site` main；推送后 `git remote set-url` 还原干净 URL。沙箱内 curl 无外网出口，无法验证线上 200（git push 正常）。
- **Git 凭据（本机 2026-08-20 修）**：全局 `credential.helper = store`，凭据预填 `C:/Users/Administrator/.git-credentials`（格式 `https://weibingtj:<PAT>@github.com`）。GitHub 操作静默无弹窗。勿改回 manager（会触发 GCM 弹窗）。
