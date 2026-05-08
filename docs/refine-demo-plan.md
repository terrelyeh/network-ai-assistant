# Refine 互動 Demo 規劃

> **狀態**：📝 規劃中（未實作）
> **目的**：標注哪些 demo 場景值得擴充第二輪互動（chip 點擊 → chat 續 → dashboard mutation），呈現 wedge 招牌的「再加一個 X」refine loop。
>
> Last updated: 2026-05-08 · Owner: ___

---

## 為什麼要做

Dashboard Builder 跟傳統工具的最大差異是 **refine loop**（implementation.html / prep.html 都把它當核心賣點），但目前 demo 裡 chips 是裝飾的、不會動。10 個 scenario 中只有 S6 的 chat trace 有真正秀 refine 兩輪對話。

**問題**：客戶看完只 get「AI 一次生 dashboard」，沒看到「dashboard 跟著問題演化」這個更強的故事。

**解法**：選 hero 場景擴充第二輪互動，讓 chip 點下去真的有 chat + 視覺變化。

---

## 場景候選分類

| Scenario | 標籤 | 理由 |
|---|---|---|
| **S1** 本週健康狀況 | ⭐ **Refine candidate** | 預設場景、第一個被看到 · 對比週次有清楚視覺變化 |
| **S2** AP 負載 | ⛔ Skip | 場景已完整，refine 加不出新故事 |
| **S3** 員工會議室（Mode A） | ⛔ Skip | 故意做小，refine 不符 Mode A 風格 |
| **S4** 跨分點分析 | ⛔ Skip | 場景已完整 |
| **S5** 設備 timeline | ⭐ **Refine candidate** | 並列雙軸對比能秀資料拼接 |
| **S6** 訪客 Wi-Fi | ✅ Already has refine | chat trace 已有「先建 → 再加每店尖峰」兩輪，不再加 |
| **S7** PoE 容量 | ⭐ **Refine candidate** | What-if 推演（加 N 台設備）— 視覺戲劇 |
| **S8** Blast Radius | ⛔ Skip | 場景已完整、需嚴肅，refine 不適合 |
| **S9** 頻寬流向 | ⛔ Skip | 場景本身已有 6 widget 跨資料分析，refine 過度 |
| **S10** Wi-Fi 覆蓋 | ⭐ **Refine candidate（強）** | Coverage Map 整張地圖重畫 — **視覺最戲劇** |

**結論：4 個 hero 候選 — S1 / S5 / S7 / S10**

---

## 每個 Hero 場景的 refine 規格

### S1 — 「💬 對比上週同期」

**Chip 觸發後**：
- **chat 續**：
  - User: 「對比上週同期看看」
  - AI: 「已疊加上週資料 ✓ 看到本週 anomaly 比上週同期 **降 8%**，但週四峰值 +20% — 推測是上週四 AP-3F-N2 那波 sticky 還沒解。」
- **dashboard mutation**：
  - 既有 「本週 anomaly 趨勢」 Time Series widget 從單線 → 雙線（本週實線 + 上週虛線 dashed）
  - 圖例自動顯示「本週 / 上週」
  - 標出週四峰值差異
- **新 chip 列**：
  - 💬 看週四到底發生什麼
  - 📅 排每週同期對比
  - ⚙️ 設 anomaly 警報

---

### S5 — 「💬 對比同樓層其他 client」

**Chip 觸發後**：
- **chat 續**：
  - User: 「拉同樓層其他 client 平均比一下」
  - AI: 「已疊加 ✓ 同 7F 樓層其他 23 個 client 平均斷線 0.5 次 — Sandy 的 3 次明顯偏高（+500%）。**確認不是 Sandy 個別問題，是 AP-7F-N3 sticky 影響**整層樓特定時段。」
- **dashboard mutation**：
  - 4 KPI 旁邊各加一個小 sub-text「樓層平均：0.5 / 1 / 0 / −63 dBm」對比
  - Timeline 主軸不變（仍是 Sandy 個人）
  - 新增一張小 widget：「7F 樓層平均斷線分布」（Status Grid，N3 紅）
- **新 chip 列**：
  - 💬 看哪幾個 client 受影響
  - 🎫 升級 → 修整層樓 N3 issue
  - 📩 通知 7F 員工

---

### S7 — 「⚡ 模擬加 5 台 IP 攝影機」

**Chip 觸發後**（這個應該替換「📋 輸出採購規格表」chip 為「⚡ 模擬加 5 台」）：
- **chat 續**：
  - User: 「模擬加 5 台 IP 攝影機（30W class）」
  - AI: 「模擬完成 ✓ 加 5 台 30W (150W) 後，全網 PoE 利用率從 **74% → 84%**（warning 區）。<br>個別 switch 推薦：3 台接 SW-3F-Core（最充裕）、2 台接 SW-7F。**SW-2F 已 87%，不適合再加任何 PoE 設備**。」
- **dashboard mutation**：
  - 大 Gauge：74% → 84%（弧形重畫，色從黃 → 偏紅）
  - 6 mini-Gauge：SW-3F-Core 78% → 90%（紅）、SW-7F 68% → 75%（黃）
  - 「再加 N 台 X 等級設備」表格內容自動刷新（剩餘可加數變少）
  - 新增 alert row：「⚠ 模擬後 SW-3F-Core 達 critical 區，建議避免」
- **新 chip 列**：
  - 💬 試其他配置
  - 📋 輸出最終採購規格
  - ⚙️ 套用模擬結果

---

### S10 — 「💬 模擬加 2 台 AP 效果」

**Chip 觸發後**：
- **chat 續**：
  - User: 「模擬加 2 台（會議室 B + 茶水區）」
  - AI: 「模擬完成 ✓ 預估覆蓋率從 **76% → 99%**（+23pp）— 死角完全消除、各區域 RSSI 平均改善 7 dBm。**會議室 B 從 −82 → −58 dBm**（從死角到良好）。」
- **dashboard mutation**（**最戲劇的視覺變化**）：
  - Coverage Map 整張重畫：
    - 會議室 B 死角紅塊消失
    - 加 2 個新 AP 圖示（虛線標「模擬」）
    - 新 radial gradient 覆蓋整層樓
  - 4 KPI 全部更新數字（76% → 99%、18 m² → 0 m² 等）
  - Bar Chart 各區域 RSSI 全部往上推
  - AI 建議卡片更新成「採購 2× ECW230 = $560 + 2 hr 施工」
- **新 chip 列**：
  - 💬 試只加 1 台位置
  - 📋 採購 2× ECW230
  - 🗺 比較 5GHz vs 2.4GHz 改善

---

## 實作技術備註

### 動畫 / 互動 flow

```
chip click
  → chip 進入 disabled state（防止重複觸發）
  → extendScenario(scenarioId, refineId) 被呼叫
  → 新 user msg DOM 注入 chat（reveal-hidden）
  → typing bubble 顯示 700ms
  → AI msg 顯示
  → 在 dashScenario 內找對應 widget mutation：
      a. 新 widget 滑入（從底部 fade-in + slide-up）
      b. 既有 widget 局部更新（數字 / SVG path 替換 + 高亮閃爍）
      c. widget 替換（淡出舊 → 淡入新）
  → 新 followup-chips 出現
  → 標記場景為 "refined-state" class（再切換 scenario 時要 reset）
```

### Reset 邏輯

切換到不同 scenario 時，`animateScenario()` 需要把 refined scenario 還原成初始狀態（移除注入的 DOM、復原 mutation 過的 widget）。建議實作方式：

- 把第二輪 DOM 用 `data-refine="true"` 標記，reset 時 query 移除
- 既有 widget 的 mutation 走 `data-original-html` 備份 / 還原模式

### 不要做的事

- ❌ 把 chip 寫成 chained refine（一直可以加更多 X）— 只支援 1 輪 refine，避免狀態爆炸
- ❌ Coverage Map 的 SVG 重畫不要做 morph 動畫（D3-style）— 太重、純 fade swap 即可
- ❌ 不要把 「📅 / 📩 / ⚙️」action chip 也綁互動 — 它們是 export/automation 性質，演不出 dashboard 變化

---

## 工時估算

| 範圍 | 預估 | 適用情境 |
|---|---|---|
| **A. 4 hero 全做（S1 / S5 / S7 / S10）** | 2-3 hr | 業務 1-on-1 慢慢 walk through |
| **B. 只做 2（S1 + S10）** | 1-1.5 hr | 安全選 — 預設場景 + 視覺最戲劇場景 |
| **C. 只做 S10（最戲劇）** | 30-45 min | 試水溫 / 展會 demo loop |
| **D. 不做** | 0 | 維持現狀（純動畫 narrative） |

---

## 使用情境對照

| 你的 demo 使用情境 | 推薦範圍 |
|---|---|
| 業務 1-on-1 慢慢 walk through · 客戶會手摸 | **A** — refine 互動是亮點 |
| 展會 / 滾動播放 · 觀眾路過看 | **C** — 只做 S10 起手震撼 |
| Pitch deck · sales 講解時點到 | **B** — 雙 hero 演示 refine 概念 |
| RD review / 內部對齊 | **D** — 規劃在這份文件就夠 |

---

## 相關文件

- [widget-catalog.md](./widget-catalog.md) — 12 widget 規格
- [prompt-templates.md](./prompt-templates.md) — LLM refine prompt 模板（intent_type "refine_of"）
- [../dashboard-builder-demo.html](../dashboard-builder-demo.html) — 目前 demo 實作（10 場景）
