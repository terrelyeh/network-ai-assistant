# RD Meeting Pack

> 推進 P0 troubleshoot scripts 補完，解鎖最戲劇的 booth demo 時刻

## 5 份文件 · 使用順序

| # | 文件 | 給誰 | 何時用 |
|---|---|---|---|
| 1 | [01-agenda.md](01-agenda.md) | 你自己 | 會議前 1 小時複習，會議中當 talking points |
| 2 | [02-ask-sheet.md](02-ask-sheet.md) | RD 工程師 | 會議前 24h 寄出，作為 pre-read；會議中投影逐項過 |
| 3 | [03-demo-storyboard.md](03-demo-storyboard.md) | RD 主管 | 會議前 24h 寄出；會議中只快速翻過給「為什麼」感 |
| 4 | [04-history-api-proposal.md](04-history-api-proposal.md) | 下次會議 | **這次不要拿出來**，鋪梗就好 |
| 5 | [05-persona-proposal.md](05-persona-proposal.md) | RD 工程師 + 主管 | < 1 小時 ask，可塞在 P0 sprint 結尾 5 分鐘，或併在任何 P0 PR |

## 會議前 checklist

- [ ] 約 30 分鐘 meeting（RD 主管 + 1-2 工程師）
- [ ] 提前 24h 寄信，附 02 + 03 + 連結到 `architecture-demo.html`
- [ ] 自己練 1 遍 `01-agenda.md` 的 talking points
- [ ] 確認 `refresh-all.sh` 跑得起來（會議中如果要 live demo 隨時可用）
- [ ] 準備好 1-2 個展會日期當「deadline anchor」
- [ ] 預想 3 個最可能的 pushback + 你的回應（agenda 文件裡有）

## 會議成功的 3 個指標

1. ✅ 散會時有 **明確 owner**（人名 + 工程師）
2. ✅ 散會時有 **明確時程**（日期 + 不是「儘快」）
3. ✅ 散會時有 **下次 check-in**（建議 weekly Friday 15 分鐘）

## 散會後的 follow-up

1. 1 小時內寄會議備忘錄（agenda 文件最後段有模板）
2. 第一週五 check-in：「上週進度如何」
3. 補完任一 op 後：跑 acceptance test（ask-sheet 最後一段）→ 截 dashboard 證明

## 下次（2 週後）會議：history API

- 拿 04-history-api-proposal.md 出來
- 跟這次同 RD 主管，但工程師可能不同（backend / pipeline team）
- 不是同一場——是「下個迭代」的討論
