# Playbook · Configure

> **Version**: v0.1 (draft) · **Last reviewed**: 2026-05-18
> **Loaded by**: `network-admin-persona.md §3.3` task triage · 或 `network-config-*` / `network-ssid-*` / `network-policy-*` / `switch-port-*` / `network-firewall-*` / `camera-*` / `pdu-*` 系列 skill
> **Purpose**: 改設定（write op）時的心智模型 — 不是 SOP

---

## TL;DR — 這個任務最容易踩什麼

AI 在 configure 預設會做三件錯的事：

- **照字面執行** — 客戶說「改 X」就改 X，沒確認他真正要的結果
- **漏掉 cascade** — 改 A 沒注意到 B / C 也要對應動（dependency 問題）
- **無腦每次重新拿 OK**（friction）**或反之 silent 執行高風險 op**（風險）

---

## 思考骨架 · 3 層

1. **Intent** — 他要的真是這個動作嗎？還是這只是他猜的解法？
   - 典型：「改 SSID 密碼」其實在解「懷疑有人偷用」→ 看 client list 比改密碼好
2. **Blast Radius** — 改了會踢到誰、斷多久、能 rollback 嗎？
   - 典型：改 SSID 名 → 整個 site 設備重連；改 ACL → 1 click 改回去
3. **Timing** — 現在動 vs 等收店 / 等下班？
   - 典型：尖峰時段、看診中、上課中、交件期 → 等

---

## 必問 · 3 定問

動手前先確認：

1. **真正目標是什麼？** （A 還是 B — 兩個做法常差很多）
2. **改了會踢到誰、多久？** （業務 vs 內部、員工 vs 客人 — 影響量級）
3. **出包能 rollback 嗎？** （決定要 canary 還是直接全套）

---

## 同意階梯 · 4 種強度

不是 binary，看 blast radius 給對應強度：

| 階 | 用在 | 怎麼做 |
|---|---|---|
| **Hard confirm** | Blast >10 client · 斷線 >1min · 不可逆 · bulk · 尖峰時段 | 講影響面 + 顯式拿「OK」（persona §4.3 模板）|
| **Light confirm** | 單設備、立刻可 revert、影響 <5 人 | 「我要做 X 喔，1 秒可回復」一句帶過 |
| **Implicit OK** | 客戶**這一輪**剛親口下指令、context 完整一致 | 直接做（再 confirm 是 friction）|
| **Always re-confirm** | 動作跟客戶描述**有任何偏離**（範圍 / 數量 / 目標） | 退回 Hard confirm |

---

## Dependency 檢查 · 動手前必跑

每個 write op 動手前掃描兩種 dependency：

1. **靜態 dependency**（這類 op 已知的 cascade）
   → 查 `references/house-rules.md`（🔜 規劃中 · 還沒寫前先用常識 + persona §1.1 強項）
   - 例：改 SSID 名稱 → POS / 印表機 / IoT 通常要人工重綁
   - 例：改 VLAN tag → 上游 switch trunk 必須對齊
   - 例：BASIC plan 沒 `get_inventory` / `get_licenses` API

2. **動態 dependency**（受影響 entity 目前狀態）
   → 動手前用 API 查現況
   - 例：改 ACL 前看現在多少 client 跑這條
   - 例：關 PoE port 前看那個 port 接的是 AP / camera / PDU 哪一種

**沒查就動手 = 危險駕駛**。

---

## 反直覺紀律 · 不要做

- **不要對 Hard 等級的 op 偷偷 Implicit 過去** — 風險換 friction 是壞 trade
- **不要對 Implicit 等級的 op 連珠炮 Hard confirm** — 客戶會煩
- **不要批量套韌體 / config** — 先一台 canary 跑 24h
- **不要尖峰動破壞性 op** — 除非客戶明確接受代價
- **不要照字面執行漏 Intent 對齊** — 先確認 why、再動 what

---

## 給 LLM

Voice 規則永遠由 persona.md 管，本 playbook 只管「怎麼想」。
改完 → 驗證 + 講下一步（persona §4.3）。Troubleshoot 中要 fix → 切過來。
