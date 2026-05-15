# RD Priorities · 整合 / API / Skill 待補項目

> 對象：RD（Backend / Skills / Cloud API teams）
> 目的：解鎖 Network AI-Assistant Line 2 路線圖上的下一波 demo 故事
> Last updated: 2026-05-16

## TL;DR

我們的 prototype 用現有 13 個 RD skill 已組出 **5 個 production-grade dashboard 情境**（org-health / off-boarding-audit / license-renewal / multi-org-governance / cross-org-reallocation）。要解鎖更多 wow 故事，請按下面 **P0 → P3 順序**處理。

每個項目都附：
- 🎯 解鎖什麼 demo
- 📊 商業價值
- ⏱ RD 估時 (我們猜的，請 RD 校準)

---

## P0 · 阻斷展會主秀的硬限制

### P0-1 · Troubleshoot skill scripts/ 補齊

**現況**：3 個 troubleshoot skill (`network-ap-troubleshoot` / `network-gateway-troubleshoot` / `network-switch-troubleshoot`) 已有 47 個 op 的 references/*.md，但**沒有 scripts/call_api.py**，所以全部 op 都不能執行。

🎯 **解鎖**：
- AP CPU 即時監控 + 自動 reboot（subscribe_stat + rpc_reboot）
- 踢可疑 wifi client（rpc_kick_clients、rpc_radius_coa）
- Switch port 故障診斷（subscribe_cable_diag、subscribe_port_stat）
- **LED dance 找設備**（rpc_led_dance）★ 展會物理 wow 最高
- VPN peer / HA status 即時監控

📊 商業價值：**讓 demo 從「audit / planning」級升級到「即時操作」級**。觀眾看到 AI 真的「重開 AP」「踢人」「閃 LED」會跟 cloud GUI 拉開差距。

⏱ 估時：4-5 工作天（每個 skill 的 scripts/call_api.py + WebSocket/SSE 協定 + RPC 路由）

**最高優先 5 個 op**（按 demo 戲劇性排序）：

| Op | Skill | 戲劇張力 | 為什麼 |
|---|---|---|---|
| 1. `rpc_led_dance` | ap-troubleshoot | 🔥🔥🔥 物理 wow | 展會現場 AP 真的閃，AI 跨數位↔物理 |
| 2. `rpc_kick_clients` | ap-troubleshoot | 🔥🔥🔥 可見效果 | 演「踢可疑 client」很直觀 |
| 3. `subscribe_client_list` | ap-troubleshoot | 🔥🔥 解鎖 S8 飯店 | 即時看誰連 wifi |
| 4. `subscribe_cable_diag` | switch-troubleshoot | 🔥🔥 故障診斷 | 「線路斷在哪裡」很有畫面 |
| 5. `rpc_reboot` | ap-troubleshoot | 🔥 經典 | 「AI 自療」橋段 |

**訊息**：先補這 5 個，剩下 42 個按需要慢慢補。

---

### P0-2 · Spec 缺 HTTP method / path 標註

**現況**：troubleshoot skill 的 `SKILL.md` 對每個 op 只寫 description + body schema，**沒寫 HTTP method 跟 URL path**。對比 `networks` skill 是寫的（每個 op 有 `method: GET` / `path: /orgs/{orgId}/...`）。

→ 即使 PMM / Claude 想自己寫 scripts/ wrapper，沒這兩個欄位也寫不出來。

🎯 **解鎖**：上面 P0-1 整套；此外可以讓外部團隊（PMM、partner）偶爾 own 補 wrapper。

⏱ 估時：1 天（填表 + 校對）

---

## P1 · 解鎖新類型 dashboard widget

### P1-1 · History aggregation API endpoint

**現況**：cloud API 只有「現在快照」endpoint。無法問「過去 7 天 throughput」「本月哪些 device 最常 reboot」「過去 30 天 stale client 累積」等。

🎯 **解鎖**（widget 等資料層）：
- `line_chart` widget — 時間序列趨勢
- `sparkline` widget — 表格內 inline 趨勢
- `area_chart` widget — 累積量

📊 商業價值：「能看趨勢」是 enterprise IT 的基本訴求。沒有歷史 = 我們 dashboard 永遠只能告訴客戶「現在」，講不出「為什麼」「趨勢往哪走」。

**建議的 endpoint shape**（不強制，給 RD 參考）：

```
GET /v2/orgs/{orgId}/metrics/aggregate
  ?metric=throughput|client_count|cpu_load|...
  &from=<ISO8601>
  &to=<ISO8601>
  &groupBy=hour|day|week
  &target=device:<mac> | network:<id> | org

Response: { timestamps: [...], values: [...], unit: "..." }
```

⏱ 估時：2-3 工作週（含 backend 聚合 pipeline）

---

### P1-2 · Cross-org membership endpoint

**現況**：`get_org_memberships_overall` 只能撈一個 org 的成員。要看「一個 user 在 5 個 org 各持有什麼權限」需要拼接 5 次 API + 用 email 比對。可做但成本高。

🎯 **解鎖**：
- 真正的 MSP / partner 多客戶治理 dashboard
- 「一個 user 在所有 org 的 access matrix」heatmap

⏱ 估時：3-5 天

---

### P1-3 · Device location 欄位

**現況**：device 沒有 GPS / 地址欄位。hierarchy_view 名稱可能含地點線索（如 "Taipei"、"LA"），但要靠地名解析推測。

🎯 **解鎖**：
- `map` widget — 地理視圖
- 「全球 5 個分店即時健康」之類的 enterprise 故事

⏱ 估時：1-2 工作週（schema migration + UI 加欄位 + cloud GUI 同步）

---

## P2 · 開發體驗 / 整合改進

### P2-1 · 把 dashboard-builder 整合進 api-skills/

詳見 [rd-handoff-dashboard-builder.md](rd-handoff-dashboard-builder.md)。

⏱ 估時：1-2 天

---

### P2-2 · multi-org-aggregator helper skill

**現況**：跨 org 聚合（topology.json）目前由 PMM 寫的 bash script 做（`prototype/scripts/build_topology.sh`、`refresh-all.sh`）。

🎯 **解鎖**：讓 Claude 直接 invoke 一個 RD-owned skill 而非依賴 shell。

⏱ 估時：1 天（包裝現有邏輯成 skill）

---

### P2-3 · 抑制 skill stdout 的 debug 噪音

**現況**：每個 skill 在 stdout 印 `AAAURL ...` + `RequestContext ...` 兩行（在 `_shared/manage_system/client.py` 第 46-47 行）。

→ Claude / 自動化腳本要 grep 過濾才能拿到 clean JSON。

🎯 **解鎖**：減少 wrapper 程式碼複雜度（10+ 個 spec 內都有 `clean()` helper）。

⏱ 估時：30 分鐘（log 改 stderr 或加 `--quiet` flag）

---

## P3 · Nice-to-have

| 項目 | 解鎖什麼 | 估時 |
|---|---|---|
| Test fixture data API | demo 環境可重置 / 不會踢真實 client | 2-3 天 |
| Webhook / SSE event stream | dashboard 真即時（不用 5 秒 poll） | 1 工作週 |
| Role-scoped temp API key | 訪客用自己權限試 demo（不洩露主帳號） | 3-5 天 |
| Bulk patch endpoints | demo 中「一次設定 100 台設備」 | 1-2 工作週 |
| Schema-validated webhook for membership changes | 即時人員變動觸發 alert | 1 工作週 |

---

## 估時總覽（按優先序）

| Priority | Items | 累積估時 | 解鎖什麼 |
|---|---|---|---|
| P0-1 (top 5 ops) | 5 個 troubleshoot scripts | 2 工作週 | LED dance、踢 client、cable diag、即時 client list、AP reboot |
| P0-2 | 補 method / path | 1 天 | 上面 5 個 op 的執行前提 |
| P1-1 | history API | 2-3 工作週 | line_chart / sparkline widget |
| P1-2 | cross-org members | 3-5 天 | MSP heatmap / access matrix |
| P1-3 | device location | 1-2 工作週 | map widget |
| P2-x | dashboard-builder 整合 + helper | 3-4 天 | 給 RD own 接手 |
| P3 | bonus items | 視情況 | 真即時 / 安全試用 / bulk ops |

**最務實的下一步**：先做 P0-1 的 top 5 op + P0-2，這樣展會的「troubleshoot 戲」就能上線。其他項目可以排在 release 後。

---

## 聯絡窗口

- Demo 故事 / 商業價值：Lulu Yeh (terrel.yeh@gmail.com)
- Spec 整合：詳見 [rd-handoff-dashboard-builder.md](rd-handoff-dashboard-builder.md)
