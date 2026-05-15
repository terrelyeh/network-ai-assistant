# Ask Sheet · 5 個 P0 troubleshoot ops + method/path 標註

> 給：RD 工程師
> 目的：照下面 spec 直接寫，不用「猜需求」
> 估時：每個 op 0.5-1.5 工作天（含 unit test）；總計 ~1 工作週

## 共同 conventions

照 `networks` skill 既有模式：

- **Auth header**: `x-auth-token` 或 `api-key`（看你們現有 pattern）
- **Path 前綴**: `/v2/orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices/{deviceMac}/`
- **Response 格式**: `{ "code": <int>, ... }`
- **Error 4xx/5xx**: 標準 HTTP error code + `{ "code": <int>, "message": "...", "detailed_message": "..." }`

對應 `_shared/manage_system/client.py` 既有的 `requests.request()` wrapper，**RPC ops 不用改 client.py**；只有 subscribe ops 需要新的 stream client。

---

## P0-1 · `rpc_led_dance` — 讓 AP LED 閃爍

**為什麼優先**：展會現場物理 wow 最高。AI 觸發 → 觀眾抬頭看到天花板某顆 AP 真的在閃。

### 建議 spec

```yaml
op_id: rpc_led_dance
skill: network-ap-troubleshoot
method: POST
path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices/{deviceMac}/rpc/led_dance
auth: x-auth-token
description: Trigger LED dance pattern on AP for physical identification.

path_params:
  - orgId       string  required
  - hvId        string  required
  - networkId   string  required
  - deviceMac   string  required  # device MAC address from inventory

request_body:
  duration_sec: integer  optional  default=10  range=1..60

response_200:
  code: 200
  device: <mac>
  result:
    status: ok | failed
    message: string  optional

example_curl:
  curl -X POST \
    -H "x-auth-token: $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"duration_sec": 10}' \
    "https://.../v2/orgs/.../devices/00:90:7f:06:61:14/rpc/led_dance"
```

**Edge cases to handle**：
- 設備離線 → 503 + `device_offline`
- 設備不支援 LED dance（舊韌體）→ 400 + `unsupported_firmware`
- duration > 60 → 400

---

## P0-2 · `rpc_kick_clients` — 踢掉指定 client

**為什麼優先**：飯店 / 辦公室場景必備。「7F 客人抱怨 wifi 慢」→ AI 找出兇手 → 一鍵踢。

### 建議 spec

```yaml
op_id: rpc_kick_clients
skill: network-ap-troubleshoot
method: POST
path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices/{deviceMac}/rpc/kick_clients
auth: x-auth-token

path_params:
  - orgId       string  required
  - hvId        string  required
  - networkId   string  required
  - deviceMac   string  required  # AP MAC

request_body:
  clients:        array   required  min_items=1
    - mac:        string  required
      reason:     string  optional   default="manual"
      add_to_blocklist: boolean  optional  default=false
      blocklist_ttl_min: integer  optional   # only when add_to_blocklist=true

response_200:
  code: 200
  device: <ap_mac>
  result:
    kicked:    array  # of {mac, status}
    failed:    array  optional

example_curl:
  -d '{"clients": [{"mac": "aa:bb:cc:00:11:22", "reason": "bandwidth_abuse"}]}'
```

---

## P0-3 · `subscribe_client_list` — 即時看誰連 wifi

**為什麼優先**：上面 kick 的前提（要先看誰連才能踢）；也是飯店 wifi 抱怨情境的核心 widget。

### 建議 spec

**選 streaming 協定**（請 RD 決定）：

| 選項 | 我們的偏好 | 理由 |
|---|---|---|
| **SSE (Server-Sent Events)** | ⭐⭐⭐ | 前端用 `EventSource` API 一行 wire up；Claude Code 容易跑；單向 ok |
| WebSocket | ⭐⭐ | 雙向能力我們不需要；多一層協定複雜度 |
| Long-poll | ⭐ | 最保守但體驗最差，5 秒間隔可接受 |

**Spec（假設 SSE）**：

```yaml
op_id: subscribe_client_list
skill: network-ap-troubleshoot
method: GET
path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices/{deviceMac}/subscribe/client_list
auth: x-auth-token
content_type_response: text/event-stream
description: SSE stream of connected wifi clients, updated every 5 seconds.

path_params:
  - orgId / hvId / networkId / deviceMac  (same)

query_params:
  - ssid_id     string   optional   # filter to one SSID
  - band        string   optional   # 2.4 | 5 | 6
  - max_events  integer  optional   # cap stream length (for demo cases)

event_format:
  event: client_list
  id: <iso8601_or_seq>
  data: |
    {
      "topic": "client_list",
      "device": "<ap_mac>",
      "timestamp": 1715852800000,
      "clients": [
        {
          "mac": "aa:bb:cc:...",
          "ip": "192.168.1.42",
          "hostname": "iPhone-Alice",
          "ssid_name": "Guest-WiFi",
          "band": "5",
          "rssi_dbm": -52,
          "rx_bytes": 1234567,
          "tx_bytes": 8901234,
          "connected_at": 1715852700000
        }
      ]
    }

example_curl:
  curl -N -H "x-auth-token: $TOKEN" \
    "https://.../v2/orgs/.../devices/00:90:7f:06:61:14/subscribe/client_list?max_events=20"
```

**Edge case**：connection lost / device offline → 結束 stream 並發 `event: error`。

---

## P0-4 · `subscribe_cable_diag` — Switch 線路診斷

**為什麼優先**：IT manager 級需求。「11F 那個 port 沒網——是線壞了還是設備掛了？」

### 建議 spec

```yaml
op_id: subscribe_cable_diag
skill: network-switch-troubleshoot
method: GET
path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices/{deviceMac}/subscribe/cable_diag
auth: x-auth-token
content_type_response: text/event-stream
description: Run cable diagnostics on selected switch ports; SSE results.

path_params:
  - orgId / hvId / networkId / deviceMac

query_params:
  - ports       string   required   # CSV port list, e.g. "1,2,3,5"
  - test_type   string   optional   # tdr | full   default=tdr

event_format:
  event: cable_diag
  data: |
    {
      "topic": "cable_diag",
      "device": "<switch_mac>",
      "port": 3,
      "status": "ok | open | short | impedance_mismatch | unknown",
      "length_meters": 12.4,        # estimated cable length
      "fault_distance_meters": 5.2, # only on open/short
      "pair_status": {
        "1-2": "ok",
        "3-6": "open"
      },
      "tested_at": 1715852800000
    }
```

---

## P0-5 · `rpc_reboot` — 重開 AP

**為什麼優先**：classic「AI 自療」橋段。配合 `subscribe_stat`（CPU 監控）做完整劇情。

### 建議 spec

```yaml
op_id: rpc_reboot
skill: network-ap-troubleshoot
method: POST
path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices/{deviceMac}/rpc/reboot
auth: x-auth-token

request_body:
  delay_sec:  integer   optional   default=0    range=0..300

response_202:
  code: 202   # accepted, reboot triggered
  device: <mac>
  result:
    status: scheduled
    eta_sec: <int>
```

---

## P0-6 · SKILL.md `method:` / `path:` 標註

**問題**：troubleshoot 3 個 skill 的 SKILL.md 缺 `method:` 跟 `path:`（對比 `networks/SKILL.md` 是有的），導致即使 references/ 有 schema、scripts/ 寫好了，wrapper 也找不到 endpoint。

**要做**：每個 op 的標題下加 2 行：

```diff
  ### subscribe_stat
+ - method: GET
+ - path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices/{deviceMac}/subscribe/stat
  - description: Subscribe to real-time device statistics (CPU, memory)
```

3 個 SKILL.md × ~16 ops × 30 秒 = **30 分鐘** 工作量。先做這個，wrapper 立刻能寫。

---

## Sanity check / Acceptance criteria

每個 op 做完，RD 跑以下指令確認可呼叫：

```bash
cd api-skills
source .venv/bin/activate
export MANAGE_SYSTEM_URL="https://falcon.staging.engenius.ai"
export API_KEY="<key>"

# 1. RPC ops 應該回 200/202 + JSON
python skills/network-ap-troubleshoot/scripts/call_api.py \
  --operation-id rpc_led_dance \
  --path-params '{"orgId":"...","hvId":"...","networkId":"...","deviceMac":"..."}' \
  --body '{"duration_sec":10}'

# 2. Subscribe ops 應該 stream SSE events
python skills/network-ap-troubleshoot/scripts/call_api.py \
  --operation-id subscribe_client_list \
  --path-params '...' \
  --query-params '{"max_events":3}'
# Expected: 印出 3 個 event 後結束
```

PMM 這邊 acceptance：跑通後我們生一張用到新 op 的 dashboard、附在驗收 evidence。

---

## 總結 — 給 RD 的執行 checklist

- [ ] P0-6 method/path 標註（30 min）
- [ ] P0-1 rpc_led_dance（0.5 天）
- [ ] P0-2 rpc_kick_clients（1 天）
- [ ] P0-3 subscribe_client_list with SSE（1.5 天）
- [ ] P0-4 subscribe_cable_diag with SSE（1 天）
- [ ] P0-5 rpc_reboot（0.5 天）

**總估**：~4.5 工作天（含 testing），實際請 RD 校準。
