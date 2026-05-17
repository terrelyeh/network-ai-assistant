# Playbook · Monitor

> **Version**: v0.1 (draft) · **Last reviewed**: 2026-05-18
> **Loaded by**: `network-admin-persona.md §3.3` task triage · 或 `hvs` / `org-devices` / `init-orgs` / `dashboard-builder` 系列 skill
> **Purpose**: 看狀態 / 巡檢 / 健康度的心智模型 — 不是 dashboard 生成 SOP

---

## TL;DR — 這個任務最容易踩什麼

AI 在 monitor 預設會做三件錯的事：

- **把所有指標都丟出來** — 客戶要的是過濾、不是 dump
- **沒 baseline 就硬下「異常」判斷** — 沒比較怎麼知道是異常
- **每次都把 license / upsell 再講一輪** — Noisy 就失去「主動觀察」的價值

---

## 思考骨架 · 3 層

按「會變大的速度」分層：

1. **Now** — 現在這刻有沒有人受影響？
   - 典型：device offline、業務斷、客人連不上
2. **Soon** — 這週 / 這月會出事嗎？
   - 典型：capacity 接近 ceiling、firmware EOL、異常 traffic pattern 累積
3. **Later** — 長期 risk
   - 典型：license 到期、設備 lifecycle、規模成長 vs 現有 capacity

對應 persona §3 的輸出選擇：Now → 文字、Soon/Later → dashboard（趨勢、比較）。

---

## 必問 · 3 定問

開撈資料前先問：

1. **對誰有影響？** （業務 vs 內部 vs 訪客 — 嚴重度不同）
2. **Baseline 是什麼？** （跟昨天 / 上週 / 同 vertical 比；沒 baseline 就承認）
3. **從什麼時候開始偏？** （突變 = 找事件 · 漂移 = 找趨勢）

模糊就用 persona §1.3 ④ 模板。

---

## 反直覺紀律 · 不要做

- **不要 dump 全部指標** — 過濾才是價值；30 個 device 列表沒幫客戶過濾
- **沒 baseline 就不要硬下「異常」標籤** — 承認「目前手上沒歷史可比」比硬講好
- **不要每次都重講 upsell** — License 快到期講一次就好，重複講會 noisy
- **不要把 monitor 拉成 troubleshoot** — 看到真實異常要明確切換、不要悄悄滑進去

---

## 給 LLM

Voice 規則永遠由 persona.md 管，本 playbook 只管「怎麼想」。
Now / Soon / Later 對應 persona §3 的 text / dashboard 選擇。
看到真實異常 → 切 troubleshoot。走 dashboard → 載 design.md。
