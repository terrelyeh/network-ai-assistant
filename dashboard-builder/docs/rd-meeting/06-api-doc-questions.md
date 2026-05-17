# 給 RD 的 API 文件補充請求

> Last updated: 2026-05-17
> 目的：拿到這些資訊後，我們能**自己包**剩下的 op，不用 RD 寫 script

---

## TL;DR

我們已經盤點完 `api-skills/` 全部 96 個 op，狀況：

- ✅ **53 個 op 可以今天就 DIY**（READ / MUT / DL — 文件齊全 + framework 已有）
- ⚠️ **43 個 op 缺關鍵資訊**（RPC 19 個 + Subscribe 24 個）
- ⚠️ **history API 沒被包成 skill**（但 GUI 已在用，所以 backend 必然存在）

**我們不需要你們寫任何新 script、不需要建任何新 backend**，只需要下面這些資訊就能自己包。

### ⚠ 重要區分 · 兩種 ask 的本質不同

| 類型 | 例 | RD 工作量 | 期待 |
|---|---|---|---|
| **Documentation gap**（這份文件大部分）| Q1+Q2 dolphin URL · Q5-Q8 文件補強 · Q9 GUI 用的 history endpoint | **5 分鐘**（寫 curl 範例 / 補一兩行 markdown） | 同 meeting 內可答 |
| **Architecture gap**（這份文件**沒有**這類）| 真的要 RD 從零建新 backend service | 數工作週 | 這份文件**不要求**這類 |

⚠ 04-history-api-proposal.md 是 **Plan B fallback** — 萬一 Q9 拿不到 GUI 用的 endpoint，才會走那條重投資路線。先預設你們已經有，就是 5 分鐘的 ask。

---

## P0 · 必要（解鎖 19 個 RPC + 部分 subscribe 的 polling 模擬）

### Q1. Dolphin 的 URL pattern 是什麼？

> **背景**：我們已經知道 `TROUBLESHOOT_URL = https://dolphin.staging.engenius.ai`（從 engenius-env skill 的 staging.md 拿到），也讀完 96 個 op 的 reference md，但**沒有任何文件**告訴我們 dolphin 下面的 URL path 結構。我們試過 GET `/`、`/v2/`、`/openapi.json` 全部 404，所以無從推測。

請告訴我們：

1. **RPC op 的 URL pattern** — 例如要呼叫 `rpc_led_dance`，要 POST 到哪個 path？
   - 是 `POST /v2/orgs/{orgId}/networks/{networkId}/devices/{deviceMac}/rpc` 嗎？
   - 還是 `POST /v2/networks/{networkId}/rpc/{method_name}` 之類？
   - 或者其他結構？

2. **Request body 結構** — 是直接送 reference md 裡的「Internal RPC Format」嗎？
   ```json
   {"method": "led_dance", "params": {...}, "timeout": 10}
   ```
   還是要包一層 wrapper（例如 `{"action": {"method":..., "params":...}}`）？

3. **Auth header** — 跟 falcon 一樣用 `api-key: <key>` 嗎？還是 Bearer token / 別的方式？

4. **回應的 polling pattern** — RPC 是 fire-and-forget 一次回應拿到結果，還是要分兩步（先 POST 拿到 job_id，再 GET 拿結果）？如果是 async，那 result endpoint 長什麼樣？

### Q2. 有沒有一個能跑的 curl 範例？

> **背景**：上面 Q1 四個問題其實都可以從一個 working curl 範例「逆向推導」出來。對你們最省時間、對我們也最不會誤解。

請給我們任何一個 troubleshoot op 的 working curl，例如：

```bash
curl -X POST 'https://dolphin.staging.engenius.ai/v2/<path>' \
  -H 'api-key: <staging-key>' \
  -H 'Content-Type: application/json' \
  -d '{"method": "led_dance", "params": {...}}'
```

我們對著範例就能反推所有 19 個 RPC op 的呼叫方式。建議用副作用最小的 op 當範例，例如 `rpc_speedtest_serverlist`（只是「給我可用的 speedtest server 清單」，不會真的對設備動手腳）。

---

## P0 · Subscribe 類（解鎖 24 個串流 op）

### Q3. Subscribe ops 用什麼傳輸協定？

> **背景**：24 個 `subscribe_*` op 的 reference md 都只描述了「Internal Subscribe Format」（topic + options 的 JSON 結構），但沒寫**怎麼跟 dolphin 建立連線**。subscribe 顧名思義是 server push 到 client，這通常要 WebSocket、SSE、long-polling 或 MQTT 之一，但我們不知道你們用哪個。

請告訴我們：

1. **協定** — WebSocket / SSE / long-polling / MQTT / 其他？
2. **URL** — 連到 dolphin 的哪個 path？例如 `wss://dolphin.../v2/subscribe`？
3. **訊息格式** — subscribe / unsubscribe / heartbeat 訊息的 wire format 是什麼？
4. **Auth** — 怎麼帶 token？放 query string、HTTP header、還是第一個訊息 body 裡？
5. **Sample code or wire dump** — 一段能 connect 且收到至少一筆資料的範例（任何語言都行，bash / Python / Go / Postman trace 都可以）。

### Q4. 如果短期內不方便給 streaming，有 polling 替代方案嗎？

> **背景**：streaming 協定（特別是 WebSocket）通常文件比較重，如果你們暫時不方便整理完整資料，我們可以接受 polling 退路 — 用 REST 每 6 秒打一次同樣資料，dashboard 看起來幾乎一樣是「即時」。

請幫我們確認：

- 大部分 `subscribe_*` 是不是有對應的 one-shot REST 版本可以用？
- 例如 `subscribe_client_list` 跟 `rpc_client_info_list` 看起來資料是一樣的（一個 stream、一個 one-shot）— 是嗎？
- 哪些 subscribe 找得到 one-shot 對應、哪些**只能**走 streaming？

只要知道對應關係，我們可以**每 6 秒 poll 一次**做「假即時」dashboard，先把 demo 跑起來，streaming 那邊不急也沒關係。

---

## P1 · 文件一致性問題（順手修）

### Q5. 麻煩補一下 `hvs/get_hierarchy_views.md` 的開頭兩行

> **背景**：96 個 reference md 裡面，**只有這一個**沒有開頭的 method/path metadata。其他全部都長這樣（範例 `org-licenses/references/get_licenses.md`）：
> ```
> - method: GET
> - path: /orgs/{orgId}/licenses
>
> Return licenses under the target organization.
> ```
> 但 `hvs/references/get_hierarchy_views.md` 是這樣（缺前兩行）：
> ```
> Return hierarchy views and networks of the organization.
> ```

**請直接在這個檔案最上方加兩行**，格式：

```
- method: <GET/POST/...>
- path: </whatever-the-actual-path-is>

Return hierarchy views and networks of the organization.
...（原本內容）
```

我們不知道實際的 method 跟 path，請你幫我們填正確的值。

### Q6. 兩個 `metadata/` 資料夾是不是其中一個可以刪？

> **背景**：repo 裡有兩個位置都叫 metadata，內容**幾乎一模一樣**：
> - `api-skills/metadata/`（15 個 JSON）
> - `api-skills/skills/metadata/`（16 個 JSON）
>
> 我們跑了 `diff -rq` 比較，唯一差異是 `skills/metadata/` 多了一個 `gateway_subscribe_speedtest.json`，其他 15 個檔兩邊內容一字不差。

請告訴我們：

1. **哪一個是 source-of-truth？** 我們以後加新 op 要去哪個資料夾放？
2. 另一個是不是可以刪掉？還是它有特殊用途（例如其中一個是給 framework 用、另一個是給 plugin install 用）？
3. 為什麼 `gateway_subscribe_speedtest.json` 只在 `skills/metadata/` 有？是漏 sync 還是故意？

### Q7. Operation registry 在哪？我們要怎麼加新 op？

> **背景**：我們讀過 `_shared/manage_system/client.py`，看到它用 `operation_id` 查 method/path 來打 API：
> ```python
> operation = get_operation(skill_dir=skill_dir, operation_id=operation_id)
> # 然後用 operation["method"] + operation["path"] 打 requests
> ```
> 但 `get_operation()` 是從 `skill_loader.py` 引入，我們沒完全看懂它從哪讀。如果我們想自己加新 op（例如我們想做新 skill），不知道要去哪登記。

請說明：

1. `operation_id → {method, path}` 的對應表存在哪？是上面那兩個 `metadata/` 資料夾的 JSON 嗎？
2. 我們**自己加新 op** 的步驟是什麼？最少要碰幾個檔案？
3. 有沒有現成的「加新 op 教學」文件可以給我們參考？

### Q8. 4 個 `download_*` op 缺 method/path

> **背景**：reference md 裡有 4 個 download op，但跟 hvs 那個一樣，**沒有開頭的 method/path metadata**：
> - `network-gateway-troubleshoot/references/download_esg_eap_cert.md`
> - `network-gateway-troubleshoot/references/download_esg_root_ca.md`
> - `network-gateway-troubleshoot/references/download_firewall_log.md`
> - `network-gateway-troubleshoot/references/download_packet_file.md`

請補上：

- HTTP method（應該是 GET 吧？）
- Path pattern
- Response content-type（是 `application/octet-stream` binary 嗎？還是 `application/zip`？）
- 跟一般 op 的 auth 差異 — 是不是要先打另一個 endpoint 拿 pre-signed URL 才下載？還是直接帶 `api-key` 就能下？

---

## P2 · 長期 / 策略性

### Q9. History data API — 應該是 documentation gap，不是 architecture gap

> **背景重要 reframing（2026-05-17）**：原本我們把這當成「請 RD 從零建 time-series store + aggregation pipeline」（3 工作週的大投資）。但**仔細想想**：EnGenius Cloud GUI 已經有顯示各種歷史趨勢圖（HVS 分數變化 / throughput / client count history / alert timeline），代表 backend **必然已經持久化歷史數據 + 已經有 GUI 在 call 的 API endpoint**。只是這個 API 沒被包成 skill 給我們用。
>
> 所以 Q9 跟 Q1+Q2 是**同一類問題** — documentation gap，不是 architecture gap。

請告訴我們：

1. **Cloud GUI 顯示歷史 chart 時，frontend 在 call 哪個 endpoint？**（throughput / client count / HVS 趨勢 任一個的 URL pattern + 範例就行）
2. **Auth 跟 manage system 一樣是 `api-key` header 嗎？**
3. **Endpoint 是 falcon 還是某個專屬服務（例如 `metrics.<env>.engenius.ai`）？**

我們對 endpoint shape 的期待（給你參考、不一定要照做）寫在 [`rd-meeting/04-history-api-proposal.md`](04-history-api-proposal.md) — 那份是 **Plan B**（萬一真的沒有 clean API），實際 5 分鐘的 ask 就是把 GUI 用的 endpoint 文件分享給我們。

**估計工作量**：5 分鐘 RD 寫一個 curl 範例（同 Q1+Q2 性質），不是 3 工作週的 backend 工程。

> **🚀 替代驗證路徑**：產品端可以自己打開 cloud.engenius.ai → DevTools Network tab → 找有 timestamp + value 陣列的 XHR/Fetch → 直接抓 URL pattern。如果 GUI 的 endpoint 設計乾淨，我們甚至不用問 RD。

### Q10. 有沒有規劃公開 OpenAPI / Swagger 文件？

> **背景說明**（不確定 RD 那邊是不是熟悉這個概念，所以多寫一點）：
>
> **OpenAPI（前身叫 Swagger）是業界標準的「API 自我描述格式」** — 把所有 endpoint、HTTP method、參數、回應 schema 寫成一份機器可讀的 JSON 或 YAML 檔，通常公開在 `/openapi.json` 或 `/swagger.json` 這個 URL。
>
> 用過 Stripe、Twilio、GitHub、AWS 的 API 嗎？他們都公開 OpenAPI spec，所以：
> - **Postman 一鍵 import** 整套 API 變成可點按的 collection
> - **各語言的 SDK 自動產生**（不用人工寫）
> - **AI agent 直接讀**就懂全部 API、會自己呼叫
> - **文件永遠跟 code 同步**（從 code annotation 自動生成）
>
> 對你們的好處：
> - **不用手寫 96 份 reference md** — 從 code annotation 自動生
> - **AI tool 越來越多**（我們在做的 Claude Code 是其中之一），OpenAPI 是 universal 入口，未來 partner / SI 想做自己的 integration 也方便
> - 如果 backend 是 Go 用 swag、Python 用 FastAPI / drf-spectacular、Node 用 NestJS swagger module — 通常**加一兩個 annotation + 一個 route** 就 expose 出來了，工作量很小

請告訴我們：

1. EnGenius 內部有規劃要做 OpenAPI 公開嗎？短期 / 中期 / 長期？
2. 如果暫時沒規劃，要不要列入 backlog 評估？我們可以提供具體的使用場景證明價值

---

## 寄出前 checklist

- [ ] 確認 staging API key 有效（可以順便提供 working sample 用）
- [ ] 把 Q1-Q4 列為**這次要回的**（解鎖 booth demo 必要），Q9 也建議這次答（reframe 後是 5 分鐘的 ask），Q5-Q8 可以晚一週，Q10 可以下季再聊
- [ ] 如果 Q1+Q2 一時答不上，可以提議：「我提供準備好的 device + network_id，請 RD 用 staging 環境跑一次 `rpc_speedtest_serverlist` 並把 curl 命令貼回給我」— 這是最低成本驗證方式

---

## 拿到答案後我們能立刻做的事

| 拿到 | 解鎖 |
|---|---|
| Q1+Q2（RPC URL）| 19 RPC op 全部能 DIY、24 subscribe 用 polling 模擬 |
| Q3（streaming 協定）| 24 subscribe op 真即時 |
| Q4（polling 對應）| 即使沒 streaming 也能跑大部分 monitoring scenario |
| Q5-Q8（文件一致性）| AI 自動 retrieve 新 op 時不踩坑、加新 op 路徑清楚 |
| Q9（history endpoint URL · GUI 已在用）| line_chart / sparkline / area_chart widget 解鎖、「過去 7 天趨勢」對話可行 — 跟 Q1+Q2 同性質的 5 分鐘 ask |
| Q10（OpenAPI 公開）| 未來零維護成本、所有工具自動相容 |

**只要 Q1+Q2 就足以 unblock booth demo 全套。**
