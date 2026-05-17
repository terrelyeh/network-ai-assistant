# URLs Reference

> 所有跟這個專案有關的 URL 一次列清楚
> Last updated: 2026-05-17

## 🌐 你的專案線上（Vercel auto-deploy from main）

| URL | 是什麼 |
|---|---|
| **[network-ai-assistant.vercel.app](https://network-ai-assistant.vercel.app)** | ★ 主站首頁 — 「專業 AI 網管」入口 |
| [/api-docs.html](https://network-ai-assistant.vercel.app/api-docs.html) | ★ 互動式 API 文件（Swagger UI · 94 ops） |
| [/openapi.json](https://network-ai-assistant.vercel.app/openapi.json) | OpenAPI 3.1 spec（給 Postman / SDK generator 用） |
| [/dashboard-builder/architecture.html](https://network-ai-assistant.vercel.app/dashboard-builder/architecture.html) | Dashboard Builder 完整架構說明 + gallery |
| [/dashboard-builder/widget-catalog.html](https://network-ai-assistant.vercel.app/dashboard-builder/widget-catalog.html) | 12 widget spec viewer |
| [/proposal-archive/](https://network-ai-assistant.vercel.app/proposal-archive/) | 📚 早期 proposal 歷史檔案 |

## 📦 GitHub Repo

| URL | 是什麼 |
|---|---|
| **[github.com/terrelyeh/network-ai-assistant](https://github.com/terrelyeh/network-ai-assistant)** | Repo 主頁 |
| [`README.md`](https://github.com/terrelyeh/network-ai-assistant/blob/main/README.md) | 對外簡介（內部狀態文件） |
| [`README.oss-draft.md`](https://github.com/terrelyeh/network-ai-assistant/blob/main/README.oss-draft.md) | OSS release 用對外文件草稿（未來 launch 時取代 README） |
| [`CLAUDE.md`](https://github.com/terrelyeh/network-ai-assistant/blob/main/CLAUDE.md) | AI session 接手導讀（內部狀態 / 踩坑） |
| [`URLS.md`](https://github.com/terrelyeh/network-ai-assistant/blob/main/URLS.md) | 你正在看 |
| [`dashboard-builder/docs/rd-meeting/06-api-doc-questions.md`](https://github.com/terrelyeh/network-ai-assistant/blob/main/dashboard-builder/docs/rd-meeting/06-api-doc-questions.md) | ★ 給 RD 的 10 題（forward 給 RD 用） |
| [`dashboard-builder/docs/scenario-candidates.md`](https://github.com/terrelyeh/network-ai-assistant/blob/main/dashboard-builder/docs/scenario-candidates.md) | 12 個 scenario 候選清單 |

## 🦅 EnGenius Falcon — manage system API（✅ 已驗證 work）

主要 CRUD API · 47 個 op 都在這 · auth: `api-key: <key>` header

| Env | URL | 何時用 |
|---|---|---|
| staging | `https://falcon.staging.engenius.ai/v2` | 我們開發測試用 ← **主要** |
| dev | `https://falcon.dev.engenius.ai/v2` | RD 內部開發 |
| prod | `https://falcon.production.engenius.ai/v2` | 真實 customer-facing |

範例（已測過）：
```bash
curl https://falcon.staging.engenius.ai/v2/user/orgs -H "api-key: $KEY"
curl https://falcon.staging.engenius.ai/v2/orgs/{orgId}/memberships/overall -H "api-key: $KEY"
```

## 🐬 EnGenius Dolphin — troubleshoot service（⚠ URL pattern TBD）

47 個 RPC + Subscribe op 在這 · auth: 看起來是 `Authorization` header（從 CORS 推測，未確認）· **path 未知**

| Env | URL | 何時用 |
|---|---|---|
| staging | `https://dolphin.staging.engenius.ai` | RPC / Subscribe ops |
| dev | `https://dolphin.dev.engenius.ai` | dev |
| prod | `https://dolphin.production.engenius.ai` | prod |

⚠ 卡在 RD 給 URL pattern — 見 [06-api-doc-questions.md Q1+Q2](dashboard-builder/docs/rd-meeting/06-api-doc-questions.md)

2026-05-17 探測證據（14 種 path 全 404）：
```bash
# 我們試過這些都不對
POST /v2/orgs/{org}/networks/{net}/devices/{mac}/rpc          # 404
POST /v2/networks/{net}/devices/{mac}/rpc                     # 404
POST /v2/devices/{mac}/rpc                                    # 404
POST /v2/orgs/{org}/networks/{net}/devices/{mac}/commands     # 404
POST /v2/troubleshoot/{mac}                                   # 404
# ... 還有 9 種，全 404
```

## 🐦 EnGenius Lark — membership invitation redirect

被邀請進 org 的人點 email link 後的 redirect 目標 · 用在 `team-members.create_org_member_user_invitation`

| Env | URL |
|---|---|
| staging | `https://lark.staging.engenius.ai/dlink/cloud2go` |
| dev | `https://lark.dev.engenius.ai/dlink/cloud2go` |
| prod | `https://lark.engenius.ai/dlink/cloud2go` |

env 變數叫 `MEMBERSHIP_INVITATION_REDIRECT_URL`，由 [`api-skills/skills/_shared/manage_system/hooks.py`](api-skills/skills/_shared/manage_system/hooks.py) 自動注入到 invitation request。

## 🛠 External 工具 / 文件

| URL | 是什麼 |
|---|---|
| [claude.com/claude-code](https://claude.com/claude-code) | Claude Code 主站 |
| [docs.claude.com/claude-code](https://docs.claude.com/claude-code) | Claude Code 官方文件（plugin / skill 機制） |
| [swagger.io/tools/swagger-ui](https://swagger.io/tools/swagger-ui/) | Swagger UI（我們 api-docs.html 用的） |
| [unpkg.com/swagger-ui-dist@5.17.14](https://unpkg.com/swagger-ui-dist@5.17.14/) | Swagger UI CDN（我們直接抓的版本） |
| [spec.openapis.org/oas/v3.1.0](https://spec.openapis.org/oas/v3.1.0) | OpenAPI 3.1.0 spec（我們生成的格式）|

## 🔑 你個人的東西

| 東西 | 位置 |
|---|---|
| API key（staging）| `~/.claude/engenius_env.json`（由 `engenius-env` skill 寫入） |
| Claude Code plugin install dir | `~/.claude/plugins/cache/` |
| 萬一 key 漏出去要去哪 rotate | EnGenius Cloud → user profile → API Keys → revoke |

## 📂 環境設定來源（給 AI session 參考）

URL 資訊都來自：

- [`api-skills/skills/engenius-env/reference/staging.md`](api-skills/skills/engenius-env/reference/staging.md)
- [`api-skills/skills/engenius-env/reference/dev.md`](api-skills/skills/engenius-env/reference/dev.md)
- [`api-skills/skills/engenius-env/reference/prod.md`](api-skills/skills/engenius-env/reference/prod.md)

切換 env 用 `engenius-env` skill：對話打「切到 staging」、「use dev」等等。

## 🎯 對話 cheatsheet

「我想看 demo」 → [network-ai-assistant.vercel.app](https://network-ai-assistant.vercel.app)
「我想看 API 文件」 → [/api-docs.html](https://network-ai-assistant.vercel.app/api-docs.html)
「我想看 repo」 → [github.com/terrelyeh/network-ai-assistant](https://github.com/terrelyeh/network-ai-assistant)
「我要 forward 給 RD」 → [06-api-doc-questions.md](https://github.com/terrelyeh/network-ai-assistant/blob/main/dashboard-builder/docs/rd-meeting/06-api-doc-questions.md) + [api-docs.html](https://network-ai-assistant.vercel.app/api-docs.html)
「我要用 Postman 試 API」 → import [/openapi.json](https://network-ai-assistant.vercel.app/openapi.json)
