# Scenario Candidates — Live Demo Brainstorm

> 基於 13 skills / 94 ops（47 runnable + 47 troubleshoot 規劃中）排列組合
> Last updated: 2026-05-17（+S11/S12 強調 AI orchestration · 不是「每次都 dashboard」）

## ★ 重要架構提醒（2026-05-17 加）

我們的架構**止於 skill 層**。Skill = primitives（AI 能做什麼）。
上面這些 layer 由 AI 在 run-time 自己判斷：

- **Persona**（[`skill/references/network-admin-persona.md`](../skill/references/network-admin-persona.md)）— Voice + **升級條件**（text → dashboard → action 三種 output 形式何時挑哪個）
- **Design**（[`skill/references/design.md`](../skill/references/design.md)）— 如果 AI 決定走 dashboard，視覺守則怎麼套
- **House-rules**（規劃中）— EnGenius 品牌觀點（HVS 分數推薦邏輯等）
- **Playbook**（規劃中）— 任務型 mental model（configure / troubleshoot / monitor）

**所以新 scenario 不等於新 dashboard**。同一個 user query，AI 可能回 text、可能組 dashboard、可能直接動手 — **由 persona 升級條件決定**。下面新加的 S11/S12 兩個情境特別示範這個原則。

## 可行性標記

- 🟢 **今天能做** — 全部 op 都有 script，今天可跑通
- 🟡 **缺 1-2 op** — 補一兩個 op 就能跑（高 ROI 的 RD action item）
- 🔴 **要 RD 大改** — 缺 4+ op 或需要新協定（streaming / device-channel）

## ICP 模式

- **A 員工** — 一般使用者問 wifi、找設備、抱怨慢
- **B SMB IT** — IT 管理員做 audit、provisioning、incident response
- **C Partner/SI** — 跨 org 設定、批次部署、收購整併

---

## 10 個情境候選

### 🟢 S1. 新分店一鍵開站 (Provisioning) — B / C
**故事**：「我們在台中開新分店，幫我用台北旗艦店的設定建好、邀請新店長、確認 license 夠。」

**Skill 組合**（4 skill / 5 op）：
- `org-network-templates.get_network_template_candidates` — 找台北旗艦店為樣板
- `org-network-templates.create_network_template` — 建模板
- `org-network-templates.apply_network_template` — 套到新 network
- `team-members.create_org_member_user_invitation` — 邀請新店長
- `org-licenses.get_licenses` + `assign_license` — 確認/派 license

**Wow 點**：過去人工要點 30 次 GUI 跨 4 個頁面，AI 60 秒做完
**Dashboard widget**：步驟進度條 / 設定 diff 對照 / license 分配圖

---

### 🟢 S2. 多 Org 安全 Audit — B / C  *(已做過原型)*
**故事**：「我管 5 個 org，幫我看哪些 network 的 ACL/policy 不合規。」

**Skill 組合**（3 skill / 4 op）：
- `init-orgs.get_user_orgs`
- `hvs.get_hierarchy_views`
- `networks.get_network_acls` × N
- `networks.get_general_policy_plus` × N

**Wow 點**：跨 5 org 30 networks 的 audit，人工要看 30 個 GUI 頁
**Dashboard widget**：合規 heatmap / 異常 highlight / 一鍵修正建議
**狀態**：✅ 已有 `prototype/canvas.html` 跑通

---

### 🟢 S3. 設備 RMA 換貨 + 設定遷移 — B
**故事**：「3F 那台 AP 壞了，幫我準備 RMA、把新機到貨設定接上。」

**Skill 組合**（3 skill / 5 op）：
- `org-devices.get_inventory` — 找壞掉那台
- `org-devices.get_expired_devices_info` — 確認保固
- `org-devices.create_device_replacement` — 開 RMA
- `org-backups.create_org_backup` — 備份壞掉那台設定
- `org-backups.restore_network_backup` — 新機到貨後還原

**Wow 點**：「設定不會掉」是 IT 最痛點，AI 整個 incident 接手
**Dashboard widget**：時間軸 / 設定 diff / RMA 狀態

---

### 🟢 S4. 離職員工權限大掃除 — B
**故事**：「上個月有 2 個同事離職，幫我清查他們的權限有沒有撤乾淨。」

**Skill 組合**（2 skill / 2 op）：
- `team-members.get_org_memberships_overall` — 列出所有人
- `team-members.delete_org_user_membership` — 移除指定人員

**Wow 點**：合規 / SOC2 角度，AI 自動 audit 比人工 spreadsheet 快 10×
**Dashboard widget**：人員 × network 權限矩陣 / 異常標紅 / 一鍵撤權

---

### 🟢 S5. License 將過期預警 + 自動分配 — B / C
**故事**：「下個月有 5 張 license 過期，幫我看哪些 device 會受影響、剩下可用 license 怎麼分。」

**Skill 組合**（2 skill / 3 op）：
- `org-licenses.get_licenses` — 看所有 license + 到期日
- `org-devices.get_expired_devices_info` — 哪些 device 受影響
- `org-licenses.assign_license` / `auto_associated_license_key` — 重新分配

**Wow 點**：續約決策從「猜」變「精準到 device」
**Dashboard widget**：到期時間軸 / device-license 關係圖 / 預算試算

---

### 🟢 S6. 跨國收購：Country Compliance Migration — C
**故事**：「我們剛買下日本一家公司，幫我把他們的 network country 改成 JP，記得法務 consent。」

**Skill 組合**（2 skill / 4 op）：
- `init-orgs.patch_org` — 改 org 設定
- `networks.get_user_profile` — 取 requester 資訊
- `networks.get_general_policy_plus` — 讀現有設定
- `networks.patch_general_policy_plus` — 改 country（內建 F1 法務 consent gate）

**Wow 點**：法務文件「**自動填好等簽名**」的 gate 是天然的戲劇張力
**Dashboard widget**：合規文件渲染 / 簽名欄 / 變更 audit log

---

### 🟢 S7. 跨 Org 設備調撥 — C
**故事**：「A 客戶有 3 台閒置的 AP，B 客戶剛好缺，幫我把設備跟 license 一起搬過去。」

**Skill 組合**（2 skill / 3 op）：
- `org-devices.move_devices_between_orgs`
- `org-licenses.move_licenses_between_orgs`
- `org-devices.get_inventory` × 2 (前後驗證)

**Wow 點**：partner / SI 場景超切，省一週採購流程
**Dashboard widget**：兩 org 設備清單對比 / 搬遷進度

---

### 🟡 S8. 飯店房客 wifi 抱怨 (7F 場景) — A → B
**故事**：「7F 客人抱怨 wifi 慢，幫我看是不是有人占頻寬。」

**Skill 組合**（3 skill / 4 op，缺 1 個關鍵 op）：
- 🟢 `hvs.get_hierarchy_views` — 找 7F
- 🟢 `networks.get_ssid_profiles` — 看該 SSID 設定
- 🔴 `network-ap-troubleshoot.subscribe_client_list` — **看誰連上 + 流量**
- 🟢 `networks.create_network_acls` — 把可疑 MAC 加黑名單

**RD action item**：補 1 個 op (`subscribe_client_list`) 解鎖整個故事
**Wow 點**：「找出兇手 + 處置」60 秒完成
**Dashboard widget**：client list live / 流量 bar / 一鍵 ban

---

### 🟡 S9. 員工找設備（Show Me The AP）— A
**故事**：「我在 11F，那台 wifi 訊號最強的 AP 是哪一台？讓它閃給我看。」

**Skill 組合**（2 skill / 2 op）：
- 🟢 `hvs.get_hierarchy_views` — 找 11F devices
- 🔴 `network-ap-troubleshoot.rpc_led_dance` — **物理閃燈**

**RD action item**：補 1 個 op 解鎖**展會物理 wow**（現場有 AP demo gear 就能用）
**Wow 點**：觀眾現場看到 AP 真的閃，AI 跨數位↔物理
**Dashboard widget**：3D / 平面圖標記 + 「LED 已啟動」狀態

---

### 🔴 S10. AP 健康總覽 + 自動修復 — B
**故事**：「dashboard 顯示 11F 那台 AP CPU 99%，幫我重開。」

**Skill 組合**（1 skill / 3 op，全 🔴）：
- 🔴 `network-ap-troubleshoot.subscribe_stat` — CPU/memory 即時
- 🔴 `network-ap-troubleshoot.rpc_reboot` — 重開
- 🔴 `network-ap-troubleshoot.subscribe_stat` — 確認 CPU 回到正常

**RD action item**：troubleshoot skill 全套（25 op）解鎖
**Wow 點**：classic「AI 自己治好」場景，但要 RD 大改
**Dashboard widget**：CPU live chart / 一鍵 reboot / 修復後對比

---

### 🟢 S11. 員工離職的「最後一日清算」（多 mode 升級示範）— B / C

**故事**：「John 明天最後一天，幫我準備清算清單，看他在哪些 org / network 還有權限。」

**Skill 組合**（1 skill / 2 op，全 🟢 today-doable）：
- `team-members.get_org_memberships_overall` — 查 John 在所有 org / network 的角色
- `team-members.delete_org_user_membership` — 確認後才用

**AI 編排決策**（這個 scenario 真正想示範的）：

| 情境 | AI 挑哪個 output | 為什麼（依 persona 升級條件）|
|---|---|---|
| John 只在 1-2 個 network 有 viewer 角色 | **Text reply** | 「John 在 Main_Org/Lab_Net 是 viewer，要我移除嗎？」訊息簡短直接 |
| John 有 5+ 個 org / network 權限，含 admin | **Dashboard**（pivot_table：org × network × role）| 資料量大、需要對比、user 要 review 後決定 |
| User 說「都拿掉吧」確認後 | **Action mode**（delete_org_user_membership × N）| 每個 admin 角色獨立 confirmation gate；viewer 可批次 |

**Wow 點**：同一個 user query，AI 自動判斷該回 text 還是組 dashboard 還是動手 — 不是 reflex 永遠生 dashboard。
**對應 persona 章節**：persona.md「升級條件矩陣」 + 「多步驟流程的 confirmation gate」
**戰略意涵**：證明 dashboard-builder 不是每次都會被呼叫；很多時候 AI text 答完就結束，這才是好 UX。

---

### 🟢 S12. 早安網路健檢 — B

**故事**：「早安，今天網路怎麼樣？」（每天上班前的 30 秒 brief）

**Skill 組合**（4 skill / 4 op，全 🟢）：
- `init-orgs.get_user_orgs`
- `hvs.get_hierarchy_views` — 跨 org 健康
- `org-devices.get_inventory` — 找 offline 設備
- `org-licenses.get_licenses` — 找 30 天內到期

**AI 編排決策**（資料品質決定 output 形式）：

| 資料狀況 | AI 挑哪個 output | 對應內容 |
|---|---|---|
| 全部健康 · HVS > 85 · 無 offline · 無近期到期 | **Text reply（30 字內）**| 「9 個 org 全綠燈、沒事，喝杯咖啡吧 ☕」 |
| 1-2 個 minor issue（如 1 台 offline、1 張 license 28 天到期）| **Text reply + alert chip**（不開 dashboard）| 「整體 OK，但 AP-LAB-03 從昨晚 offline、需要看一下」+ 連結 |
| 多重 issue 或某個 org HVS < 70 | **Dashboard**（KPI grid + offline timeline + license expiry timeline）| 預設展開 issue summary、提供「跟我說細節」follow-up prompt |

**Wow 點**：「今天網路怎麼樣？」這個問題的**理想答案**是 30 字 text，不是 1 張 dashboard。AI 知道情況好就不開 dashboard。
**對應 persona 章節**：persona.md「網管的 cognitive load」+「summary first, drill-down on request」
**戰略意涵**：dashboard 是「複雜度的 escape hatch」，不是預設 output。

---

## 統計

| 可行性 | 數量 | 用途 |
|---|---|---|
| 🟢 今天能做 | 9 (S1-S7, S11, S12) | 展會主秀候選 |
| 🟡 缺 1-2 op | 2 (S8, S9) | RD 高 ROI action item |
| 🔴 要大改 | 1 (S10) | 願景示意（給 RD 看潛力）|

## ICP 模式分布

| 模式 | 涵蓋情境 |
|---|---|
| A 員工 | S8, S9 |
| B SMB IT | S1, S3, S4, S5, S8, S10, S11, S12 |
| C Partner/SI | S1, S2, S6, S7, S11 |

## 跨 skill 程度

- 4 skill 組合: S1, S12
- 3 skill 組合: S2, S3, S8
- 2 skill 組合: S4, S5, S6, S7, S9
- 1 skill 內: S10, S11

## Output 形式分布（2026-05-17 新加維度）

| 預設 output | 涵蓋情境 |
|---|---|
| 主要 text | S11（簡單）, S12（健康時）|
| Dashboard | S1, S2, S3, S5, S6, S7, S8, S10, S11（複雜時）, S12（有 issue 時）|
| Action（一鍵動手）| S4, S7, S8, S9, S11 |
| **多 mode 升級（依資料 / 情境動態決定）** | **S11, S12** ← 新加的兩個重點示範 |
