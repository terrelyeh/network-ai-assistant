# Playbook · Troubleshoot

> **Version**: v0.1 (draft) · **Last reviewed**: 2026-05-18
> **Loaded by**: `network-admin-persona.md §3.3` task triage · 或 `network-{ap,gateway,switch}-troubleshoot` 系列 skill
> **Purpose**: 修壞 / 找根因的心智模型 — 不是診斷腳本

---

## TL;DR — 這個任務最容易踩什麼

AI 在 troubleshoot 預設會做三件錯的事：

- **第一個合理假設就拿來答** — 沒驗證就講「應該是 channel 干擾」
- **跳過「最近改了什麼」** — 這題其實是 90% 故障的元凶
- **急著 reboot 設備** — 把證據 / log / client state 刷掉，根因永遠查不到

---

## 思考骨架 · 3 層

不分設備類型（AP / Switch / Firewall / Camera / PDU），都套同一個 3 層：

1. **設備本身** — 電、PoE、線、硬體、韌體、config drift
   - 典型：PoE 沒供電、韌體 hang、設定被改過、硬體掛
2. **上游** — 它依賴誰（uplink switch / WAN / ISP / controller）
   - 典型：uplink port link down、VLAN 跑掉、ISP 不穩、controller 失聯
3. **下游 / 使用者** — 它服務誰（client / NVR / connected load）
   - 典型：iOS vs Android 行為差異、舊裝置不支援 WPA3、特定 consumer app 掛、距離太遠

對應例：

| Device | 設備本身 | 上游 | 下游 / 使用者 |
|---|---|---|---|
| AP | PoE / 韌體 / SSID / channel | uplink switch port | Wi-Fi clients |
| Switch | 電源 / VLAN / STP / port | uplink switch / firewall | 接在它上的設備 |
| Firewall | 韌體 / policy / NAT / VPN | ISP / WAN link | LAN / VPN / 內部 user |
| Camera | PoE / 韌體 / RTSP | uplink switch | NVR / cloud upload |
| PDU | mains / 排程設定 | 大樓電源 / breaker | 插上面的負載 |

---

## 必問 · 3 定問

開撈資料前先問：

1. **多少裝置（or 多少人）受影響？** （1 台 vs 整個 SSID / 整個 network 差很多）
2. **什麼時候開始？** （持續 vs 突發 — 突發找事件、持續找設定）
3. **剛改過什麼？** （最常見的元凶 — 設定、韌體、外部廠商來動過、最近搬位置）

模糊就用 persona §1.3 ④ 模板，**不要連珠炮 5 題**。

---

## 反直覺紀律 · 不要做

- **不要先 reboot** — 重開會把 log / state / 連線資料刷掉，根因永遠查不到
- **不要建議客戶換硬體** — 先 exhaust 設定面（VLAN / firmware / policy），硬體壞是少數
- **不要單一假設就動手** — 至少準備第 2 個假設備用，避免「猜錯改錯製造新問題」
- **不要 3 個假設都不對還硬撐** — 跟客戶 sync、升級到人類 SI 比較快
- **不要對非 EnGenius 設備直接動** — 詳 persona §1.1（教看 LED / 重開可以，深度 config 找廠商）

---

## 給 LLM

Voice 規則永遠由 persona.md 管，本 playbook 只管「怎麼想」。
動手 fix → 切 configure playbook。Monitor 看到真實異常 → 切過來。
