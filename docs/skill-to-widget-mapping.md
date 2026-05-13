# Skill ↔ Widget Mapping · Dashboard Builder 對齊文件

> **給誰看**：RD（senao-api-skills 維護者）、PM、Prompt Engineer
> **目的**：把「使用者問題 → AI 呼叫哪些 skill op → 組哪幾個 widget」這條鏈寫清楚，避免 widget catalog 跟 API 各做各的。
> **狀態**：v1，基於 falcon.staging.engenius.ai 實測（2026-05-13）
> **前置閱讀**：[widget-catalog.md](./widget-catalog.md) · [dashboard-builder-implementation-guide.md](./dashboard-builder-implementation-guide.md)
> **PoC 證據**：`prototype/dashboard-live.html`（3 個真實 API 串通的 scenario）

---

## 0. TL;DR

1. **既有 skill 強在「實時 + 動作 + 設定讀寫」，弱在「歷史聚合」** — 8 個 demo scenario 裡有 3 個（s4 churn / s5 client timeline / s6 訪客月報）需要歷史 API，先用 real-data 場景替換掉
2. **5 個 widget 已經有完整 op 對應**（KPI / Table / Bar / Status Grid / Heatmap-as-Grid），可以直接做
3. **3 個 widget 需要 RD 新 op 才能填**（Time Series 缺歷史 / Topology Graph 缺 link metadata / Coverage Map 缺座標）
4. **Dolphin 平台支援還在開發中**，目前 skill 只支援 Falcon — Dolphin 上線後增加 ~30 個 op，會解鎖更多場景

---

## 1. 鏈條總覽

```
使用者問句
    ↓
LLM 規劃 → 解析 ID（orgId / hvId / networkId / deviceId）
    ↓
LLM 呼叫 N 個 skill op（read-only）
    ↓
回傳資料映射到 Widget Schema（Zod 驗證）
    ↓
前端 render dashboard（widget 組合）
    ↓
使用者看到 + 可採取後續 action
```

**示意**：
```
「我管的 org 狀況怎樣」
    ↓
get_user_orgs → 5 orgs
get_hierarchy_views × 5 → 14 networks
get_inventory(accessible orgs) → 1 device
get_licenses(accessible orgs) → 3 licenses
    ↓
組合 widget:
  KPI Card × 4 + Table × 2 + Bar Chart × 1 + Alert List × 3
    ↓
render → 使用者看 multi-org overview
```

---

## 2. Widget ↔ Op 對應表

每個 widget 列出**至少一個可立即使用的 op 來源**。標記符號：

- ✅ 完整對應（既有 skill 直接可用）
- 🟡 部分對應（缺欄位或需 client-side aggregate）
- 🔴 需要 RD 新 op（目前 skill 沒有）

| Widget | Tool Name | 主要對應 op | 狀態 |
|---|---|---|---|
| KPI Card | `render_kpi_card` | 任何回傳 count / total / status 的 op（get_inventory, get_licenses, get_user_orgs ...）→ aggregate | ✅ |
| Time Series | `render_time_series` | **缺**：歷史 metric 沒有 batch query API。subscribe_* 是 real-time stream，要前端自己累積 | 🔴 |
| Bar Chart | `render_bar_chart` | get_inventory（依 type/model 分組）、get_licenses（依 status 分組） | ✅ |
| Table | `render_table` | get_inventory / get_licenses / get_user_orgs / get_ssid_profiles 直接列 | ✅ |
| Status Grid | `render_status_grid` | get_hierarchy_views + get_inventory cross-ref（每 network 是否健康） | ✅ |
| Heatmap | `render_heatmap` | `rpc_all_chan_util`（AP × channel × util）、policy snapshot drift（network × field × consistent?） | 🟡 |
| Alert List | `render_alert_list` | get_licenses（expired ones）+ AI-derived observations from any op | ✅ |
| Gauge | `render_gauge` | `subscribe_throughput`（current / max）、license `time_remaining/duration` ratio、PoE budget usage | 🟡 |
| Site Map | `render_site_map` | **缺**：get_hierarchy_views 沒回傳座標（lat/lon）— 需要 RD 補 location 欄位或加 op | 🔴 |
| Topology Graph | `render_topology` | `subscribe_arp_list` + `subscribe_fdb_list`（switch）→ derive downstream tree | 🟡（需 client-side build） |
| Sankey | `render_sankey` | **缺**：traffic flow data 目前 API 沒有 | 🔴 |
| Coverage Map | `render_coverage_map` | **缺**：floor plan + AP 座標 — 需要 RD 補 site map data | 🔴 |

### 統計
- **直接可用（✅）**：5 個 widget（**P0 MVP 4 個全部可做**）
- **部分對應（🟡）**：3 個 widget（可做但要 client-side processing）
- **需 RD 補 API（🔴）**：4 個 widget（多數是 P2 進階 widget，先 skip）

> **結論**：P0 4 個 MVP widget（KPI / Time Series / Bar / Table）中只有 Time Series 缺資料 —
> 這也是為什麼 demo 那 3 個「歷史」scenario 跑不起來的根因。**RD 補一個歷史 metric query API 就解鎖 60% 的痛點**。

---

## 3. Scenario ↔ Op 對應表

8 個 dashboard demo scenario 對應到實際 op chain：

### s1 · 本週網路健康狀況檢查（Mode B SMB IT）
- **使用者問**：「我想看這週網路有沒有什麼異常」
- **Op chain（理想版）**：
  1. `init-orgs/get_user_orgs` → orgId
  2. `hvs/get_hierarchy_views` → networkId
  3. `org-devices/get_inventory` → device list (count, type breakdown)
  4. **`?/get_anomaly_history`（缺）** → 過去 7 天 anomaly 趨勢
  5. **`?/get_health_score`（缺）** → site 健康分數
- **目前狀態**：🟡 部分可做（即時 inventory ✓，歷史趨勢 ✗）
- **Widget 組合**：KPI Cards (3) + Time Series (1) + Table (1) + Status Grid (1)
- **RD action item**：補歷史 anomaly + health score API

### s2 · 哪些 AP 太忙（Mode B）
- **使用者問**：「找出 5GHz utilization > 80% 的 AP」
- **Op chain**：
  1. `org-devices/get_inventory` → AP list
  2. `network-ap-troubleshoot/subscribe_channel_utilization` × N → per-AP util
  3. `network-ap-troubleshoot/subscribe_client_list` × N → per-AP load
- **目前狀態**：✅ 完整可做
- **Widget 組合**：Bar Chart (top N) + KPI Cards + Heatmap (AP × band) + Action Toolbar (load balance)

### s3 · 我的會議室 Wi-Fi（Mode A 員工）
- **使用者問**：「我會議室 Wi-Fi 怎樣」
- **Op chain**：
  1. `org-devices/get_inventory` → 找該員工樓層的 AP
  2. `network-ap-troubleshoot/rpc_client_info_list` → 找該員工的 client info
  3. `network-ap-troubleshoot/subscribe_ping` + `subscribe_speedtest` → 即時性能
- **目前狀態**：✅ 完整可做（只是要員工 identity 解析 — 假設前端已知 user MAC）
- **Widget 組合**：KPI Cards (signal/speed/latency) + Time Series (last hour) + Gauge (signal quality)

### s4 · 跨 org License & Inventory 健檢（NEW，取代 site churn）
- **使用者問**：「我管的這些 org 整體狀況怎樣 — 設備、授權有沒有要注意的」
- **Op chain**（**已實測通過**，見 `prototype/dashboard-live.html#s1`）：
  1. `init-orgs/get_user_orgs` → 5 orgs
  2. `hvs/get_hierarchy_views` × 5 → 14 networks
  3. `org-devices/get_inventory` × accessible orgs → device list
  4. `org-licenses/get_licenses` × accessible orgs → license status
- **目前狀態**：✅ 完整可做
- **Widget 組合**：KPI Cards (4) + Table × 2 (org matrix + device) + Tree (network hierarchy) + Alert List (expired licenses)
- **取代原因**：原本 s4 (site churn) 需要 client roaming 歷史 API，目前 skill 沒有

### s5 · Network 設定稽核（NEW，取代 Sandy 7-day timeline）
- **使用者問**：「審計分店 N 的 Wi-Fi 設定是否合規」
- **Op chain**（**已實測通過**，見 `prototype/dashboard-live.html#s2`）：
  1. `init-orgs/get_user_orgs` + `hvs/get_hierarchy_views` → 解析 path
  2. `networks/get_ssid_profiles` → SSID 清單
  3. `networks/get_general_policy_plus` → 32 個 policy 欄位
  4. `networks/get_network_acls` × 3 (block / vip / white) → ACL 狀態
- **目前狀態**：✅ 完整可做
- **Widget 組合**：KPI Cards + Policy Snapshot Grid + ACL Status Table + Alert List (security findings)
- **取代原因**：Sandy 7-day timeline 需要 client session 歷史 API，沒有

### s6 · AP 即時健康總覽（NEW，取代訪客 Wi-Fi 月報）
- **使用者問**：「現在每個 AP 健康嗎？哪些撐不住？」
- **Op chain**：
  1. `org-devices/get_inventory`（filter type=ap）→ AP list
  2. `network-ap-troubleshoot/subscribe_stat` × N → CPU/memory
  3. `network-ap-troubleshoot/subscribe_throughput` × N → 即時流量
  4. `network-ap-troubleshoot/subscribe_channel_utilization` × N → 即時負載
- **目前狀態**：✅ 完整可做（subscribe ops 是 real-time stream，前端要管 lifecycle）
- **Widget 組合**：Status Grid (all APs) + KPI Cards (avg CPU/mem/throughput) + Bar Chart (top 5 busiest) + Time Series (live throughput, accumulating)
- **取代原因**：訪客 Wi-Fi 月報需要歷史使用量聚合，沒有

### s7 · PoE 容量規劃（Mode B）
- **使用者問**：「再加 5 台 IP 攝影機，PoE 撐得住嗎」
- **Op chain**：
  1. `org-devices/get_inventory`（filter type=switch）→ switch list
  2. `network-switch-troubleshoot/subscribe_port_stat` × N → port 級 PoE budget
  3. **`?/get_poe_breakdown`（待確認）** → 每 port 的 PoE class / current
- **目前狀態**：🟡 待確認 `subscribe_port_stat` 是否回傳 PoE 細節
- **Widget 組合**：KPI Cards (per switch budget) + Bar Chart (per port draw) + Table (推薦 port)

### s8 · 維護 Blast Radius（Mode B）
- **使用者問**：「下週要關 SW-3F-Core，影響哪些設備 / client」
- **Op chain**：
  1. `org-devices/get_inventory` → 目標 switch
  2. `network-switch-troubleshoot/subscribe_arp_list` → 下游 client
  3. `network-switch-troubleshoot/subscribe_fdb_list` → MAC 拓樸
- **目前狀態**：✅ 完整可做
- **Widget 組合**：Topology Graph (從目標 switch 放射) + Table (受影響 device/client/VLAN) + Status Grid (替代路徑)

---

## 4. 8 Scenario 對齊度總覽

| # | Scenario | API 對齊 | 主要 op | 缺什麼 |
|---|---|---|---|---|
| s1 | 本週網路健康 | 🟡 | get_inventory + (歷史) | 歷史 anomaly API |
| s2 | 哪些 AP 太忙 | ✅ | subscribe_channel_utilization, subscribe_client_list | – |
| s3 | 會議室 Wi-Fi | ✅ | rpc_client_info_list, subscribe_ping, subscribe_speedtest | – |
| s4 | 跨 org License/Inventory（NEW） | ✅ | get_user_orgs, get_hierarchy_views, get_inventory, get_licenses | – |
| s5 | Network 設定稽核（NEW） | ✅ | get_ssid_profiles, get_general_policy_plus, get_network_acls | – |
| s6 | AP 即時健康總覽（NEW） | ✅ | subscribe_stat, subscribe_throughput | – |
| s7 | PoE 容量規劃 | 🟡 | subscribe_port_stat | PoE 細節欄位待確認 |
| s8 | 維護 Blast Radius | ✅ | subscribe_arp_list, subscribe_fdb_list | – |

**結論**：原始 8 scenario 砍掉 3 個歷史依賴（s4/s5/s6）後，**6 個立即可做、2 個小修補**。

---

## 5. RD 該做的事（按優先級）

### 🔥 P0 · 解鎖最大 wedge value
- [ ] **歷史 metric query API** — 給 anomaly count / health score / client session 提供 time-range query。解鎖 Time Series widget + 3 個歷史 scenario。
- [ ] **Subscribe lifecycle 文件化** — 前端怎麼正確啟動 / 停止 subscribe，何時 timeout、reconnect 策略。

### 🟡 P1 · 體驗增強
- [ ] **PoE 細節 schema 確認** — `subscribe_port_stat` 是否含 `poe_class` / `current_draw_mw` / `budget_remaining`？
- [ ] **批次 op** — `get_inventory` 跨 org 批次（目前一次只能一個 org，5 個 org 要打 5 次）。
- [ ] **Anomaly detection event stream / log API** — `get_alerts` 之類，給 Alert List widget 餵料。

### 🟢 P2 · 高階 widget 支援
- [ ] **Site geo data** — 給 Site Map widget，需要 hierarchy view 加 lat/lon。
- [ ] **Floor plan + AP placement** — 給 Coverage Map widget，需要新的 site survey API。
- [ ] **Traffic flow data** — 給 Sankey widget，需要 application identification + flow log。

### 📦 Dolphin 平台支援
RD 補丁完成後預期解鎖：
- Dolphin 系列 AP 的 spectrum scan / WiFi scan ops
- Dolphin 專屬的 advanced 功能（待 RD 補 op 列表）
- 約 30 個 op 從「不支援」變成「支援」

---

## 6. Prompt Engineering 注意事項

LLM 呼叫 skill 時要 enforce 的規則（從 PoC 觀察）：

1. **ID 解析鏈是強約束** — 先 `get_user_orgs` 拿 orgId，再 `get_hierarchy_views` 拿 networkId，再呼叫 network-level op。順序錯會 400 / 403。
2. **權限邊界要尊重** — 收到 403 不要重試，改成跟使用者解釋「沒權限」。收到 402 提示「需要升級 plan」。這已經是 PoC `s1` 視覺化的賣點。
3. **Subscribe vs RPC vs CRUD 三類分清楚**：
   - `subscribe_*` = 即時 stream（用於 Time Series / Gauge / live data）
   - `rpc_*` = on-demand 動作（用於 Action Toolbar 上的按鈕，destructive 要 confirm）
   - GET / PATCH 設定類 = 設定讀寫（用於 Network Audit scenario）
4. **每個 widget JSON 都過 Zod 驗證** — 即使是真實 API 回應，若欄位缺失或型別錯就 reject，不要 render 半成品。
5. **Closed catalog rule** — LLM 只能挑 widget catalog 裡 12 種 widget，不能發明新類型。

---

## 7. 實作 Phase 規劃

### Phase 1 · MVP（4-6 週，解鎖 P0 4 個 widget）
- 6 個 scenario 跑通（s2, s3, s4, s5, s6, s8）
- 4 個 widget 實作（KPI / Time Series / Bar / Table）
- Time Series 在沒有歷史 API 前先用 client-side accumulating from subscribe_*

### Phase 2 · 完整版（RD 補歷史 API 後）
- 加 s1, s7 scenario
- 加 P1 4 個 widget（Status Grid / Heatmap / Alert List / Gauge）
- Dolphin 平台支援上線

### Phase 3 · 進階（Wedge 上線後）
- P2 4 個 widget（Site Map / Topology / Sankey / Coverage Map）— 需 RD 補進階 API

---

## 8. 相關連結

- [widget-catalog.md](./widget-catalog.md) — 12 個 widget 的完整規格（schema, 視覺）
- [dashboard-builder-implementation-guide.md](./dashboard-builder-implementation-guide.md) — Zod / 角色分工 / kickoff
- [design-tokens.md](./design-tokens.md) — EnGenius 視覺 token
- `prototype/dashboard-live.html` — 真實 API 串通的 PoC（3 scenario）
- `prototype/api-responses/` — 實測的真實 API JSON 回應，給 RD 對欄位用
- `api-skills/` — RD 提供的 senao-api-skills v0.1.0（本機路徑，未版控）

---

## 9. 變更紀錄

| 日期 | 版本 | 變更 |
|---|---|---|
| 2026-05-13 | v1 | 初版，基於 senao-api-skills v0.1.0 在 falcon.staging 實測 |
