# Demo Storyboard · 5 個 P0 ops 解鎖什麼戲

> 給：RD 主管 + 工程師（看了知道「為什麼這 5 個值得做」）
> 每個 op 對應 1 個 90 秒 demo 故事

每個故事都是「**before（現在做不到）→ after（補完後）**」對照。

---

## 故事 ① · 「Show Me The AP」(物理 wow，最高優先)

> Op: `rpc_led_dance` · Skill: network-ap-troubleshoot

### Before（現在）

訪客：「我們大樓有 50 顆 AP，哪一顆是 11F 那個訊號最強的？」

操作員：（沒辦法答。只能秀 Cloud GUI 的 floorplan 圖，但訪客已經懂 floorplan，不算 wow）

### After（補完 rpc_led_dance）

```
[訪客] 「我們大樓有 50 顆 AP，哪一顆是 11F 訊號最強的？」
                                                       │
[操作員 → Claude] 「找 11F 最近一台 AP，讓它閃 LED 20 秒」
                                                       │
[Claude]
  ├─ get_hierarchy_views → 找 11F network                            (~2s)
  ├─ get_inventory → 列出該 network 的 AP                            (~2s)
  ├─ rpc_led_dance({"duration_sec":20}) → 觸發那台 AP LED 閃        (~1s)
  └─ 回應「我讓 ECW220-7F 閃了，請看天花板靠走廊那台」                (~1s)
                                                       │
[訪客抬頭] 看到天花板某顆 AP 真的在閃 🔴🟢🔵
                                                       │
[爆點]
  「AI 從數位世界跨進物理世界」
  「過去要派工讀生爬梯找 AP，現在 5 秒」
```

**Dashboard 影響**：可在現有 `canvas-multi-org-governance` 的 topology tree 加「LED dance」按鈕，讓訪客在 dashboard 上點任一 device → 觸發實體閃光。

---

## 故事 ② · 「飯店 7F 客人抱怨 wifi 慢」(經典應用)

> Ops: `subscribe_client_list` + `rpc_kick_clients` · Skill: network-ap-troubleshoot

### Before（現在）

訪客：「客戶有飯店連鎖，他們最常的 ticket 是『wifi 慢』」

操作員：（只能秀 cloud GUI 的 client list 表格，靜態。沒有「找出兇手 + 處置」一條龍故事）

### After（補完 subscribe_client_list + rpc_kick_clients）

```
[訪客] 「飯店 7F 客人抱怨 wifi 慢，幫我看一下」
                                                       │
[操作員 → Claude] 「找 7F 那台 AP 看現在誰連著、誰佔頻寬」
                                                       │
[Claude]
  ├─ hierarchy_views → 7F network                                       (~2s)
  ├─ get_inventory → 7F-AP-corridor                                     (~2s)
  ├─ subscribe_client_list (SSE, max_events=3) → 拿 3 個快照            (~6s)
  └─ 即時 dashboard:
     [client_list widget] 列 12 個連線 client + 各自流量              ← NEW
     有 1 個 MAC 占了 70% rx_bytes，hostname="MacBook-Mr-Wang"
                                                       │
[訪客]「就是這個！踢掉！」
                                                       │
[操作員 → Claude] 「踢這台 MAC，加進黑名單 1 小時」
                                                       │
[Claude]
  └─ rpc_kick_clients({"clients":[{"mac":"...", "add_to_blocklist":true, "blocklist_ttl_min":60}]})
                                                       │
[爆點]
  「90 秒從『發現 ticket』到『處理完』」
  「客人會議室『等等先繼續開會吧』」
```

**Dashboard 影響**：S8 的「飯店 wifi 抱怨」情境 (`docs/scenario-candidates.md`) 現況 🟡 缺這 2 個 op，補完即可上線。

**新 widget 候選**：`live_client_list`（基於 subscribe stream）—— 等補完後做 ~30 分鐘。

---

## 故事 ③ · 「Switch port 故障診斷」(IT manager 級需求)

> Op: `subscribe_cable_diag` · Skill: network-switch-troubleshoot

### Before（現在）

訪客：「我們最常的 case 是『某個 port 沒網』——是線壞了還是設備掛了？」

操作員：（沒辦法。要派人現場拿 cable tester 量）

### After（補完 subscribe_cable_diag）

```
[訪客] 「3F 會議室那個 port 沒網，幫我看是線壞還是設備」
                                                       │
[操作員 → Claude] 「跑那台 switch port 5-8 的 cable diag」
                                                       │
[Claude]
  ├─ hierarchy_views → 3F                                              (~2s)
  ├─ get_inventory → 3F switch (借Hom-ECS1528FP)                       (~2s)
  ├─ subscribe_cable_diag (ports=5,6,7,8)                              (~8s)
  └─ dashboard:
     [cable_diag widget]                              ← NEW
       Port 5: ✅ ok       length=8.2m
       Port 6: ⚠ open      fault_at=4.1m  ← 線路斷在 4.1 公尺處
       Port 7: ✅ ok       length=12m
       Port 8: ✅ ok       length=8m
                                                       │
[爆點]
  「不是設備壞，是 Port 6 的線在 4.1 公尺處斷了」
  「省一趟現場 + 一個工程師半天時間」
```

**Dashboard 影響**：解鎖 S6（「IT incident response」類）情境。

**新 widget 候選**：`cable_diag_panel`（4-port 並排顯示 + 視覺化故障距離）

---

## 故事 ④ · 「AI 自療」(經典 reliability 故事)

> Ops: `subscribe_stat` + `rpc_reboot` · Skill: network-ap-troubleshoot

### Before（現在）

訪客：「我們 NOC 三班輪 24 小時值班，最常的事就是 AP CPU 高了去重開」

操作員：（沒辦法 demo「即時 CPU → 自動 reboot」流程）

### After（補完 subscribe_stat + rpc_reboot）

```
[操作員 → Claude] 「監控 Main_Org 所有 AP 的 CPU，如果有 > 90% 的就建議重開」
                                                       │
[Claude]
  ├─ get_inventory → 10 台 AP                                          (~2s)
  ├─ subscribe_stat (× 10, 並行)                                      (~5s)
  └─ dashboard:
     [live_stat widget × 10]                          ← NEW
     ECW230: 🟢 CPU 14%
     ECW220: 🟢 CPU 22%
     ECW115: 🔴 CPU 97% ← AI highlight
     Home_ECW120: 🟢 CPU 18%
     ...
                                                       │
[Claude 主動建議] 「ECW115 CPU 已 97% 持續 30 秒，建議重開。要繼續嗎？」
                                                       │
[操作員] 「執行」
                                                       │
[Claude] rpc_reboot({"delay_sec":0})
                                                       │
[Claude 等 60 秒] subscribe_stat 重新接上 → ECW115 CPU 回到 12%
                                                       │
[爆點]
  「夜班 NOC 不用值班的 AI assistant」
  「整個 incident response cycle 90 秒內結束」
```

**Dashboard 影響**：解鎖 S10「AP 健康自動修復」情境。

**新 widget 候選**：`live_stat_grid`（multi-device CPU/memory live grid + threshold alert）

---

## 故事 ⑤ · 「LED dance 找設備 + multi-org」（綜合題）

> Ops: 既有的所有 + `rpc_led_dance`

### Storyboard

```
[訪客] 「我們是 MSP，管 5 個客戶，能幫我們做一個 dashboard 嗎？」
                                                       │
操作員 開啟 canvas-multi-org-governance（已有）
                                                       │
[訪客] 「能不能標出哪台 AP 訊號最強？」
                                                       │
[操作員 → Claude] 「在每個 org 的 topology 加一個『閃 LED』按鈕，可以單獨點」
                                                       │
[Claude] 改 spec → 加 device 行為 → 重 compose                       (~10s)
                                                       │
[訪客點 Vertical Demo / ESG610-6971] → AI 觸發 → 現場 device 真的閃 🔴
                                                       │
[爆點]
  「dashboard 不只是看，是控制平台」
  「即時跨數位↔物理」
```

---

## 5 個 op 的 ROI 排序總表

| Op | Demo 故事 | 戲劇張力 | 估時 | ROI 排名 |
|---|---|---|---|---|
| `rpc_led_dance` | 故事①「Show me the AP」 | 🔥🔥🔥 物理 wow | 0.5 天 | **1st** |
| `rpc_kick_clients` | 故事②「飯店 wifi」處置端 | 🔥🔥🔥 可見效果 | 1 天 | **2nd** |
| `subscribe_client_list` | 故事②「飯店 wifi」找兇手 | 🔥🔥 解鎖整個故事 | 1.5 天 | **3rd** |
| `subscribe_cable_diag` | 故事③「線斷在哪」 | 🔥🔥 IT 痛點 | 1 天 | **4th** |
| `rpc_reboot` | 故事④「AI 自療」 | 🔥 classic | 0.5 天 | **5th** |

**如果只能補 3 個**：選 1+2+3（故事①+② 完整解鎖兩條 demo）。

**如果只能補 1 個**：選 `rpc_led_dance`（投資報酬率最高、估時最短、物理 wow 唯一）。

---

## 補完後的 demo 升級路線

| 階段 | 現況 | 補完後 |
|---|---|---|
| 0-30 秒 | 開 dashboard 看靜態快照 | 一樣 |
| 30-60 秒 | 對話加區塊 | 一樣 |
| 60-90 秒 | （沒有） | **AI 觸發實體動作**（LED 閃 / kick client / 重開 / cable diag）|
| **wedge 強度** | 「AI 即時組 dashboard」 | 「AI 即時組 dashboard **+ 跨數位↔物理動作**」 |

→ Wedge 故事從「visualization」升級到「**bidirectional control**」。對展會觀眾差別巨大。
