# 敘事發酵週報 — 2026-09-04

**本期無可評估標的(0 檔)。** 兩個上游資料來源本週都沒有產出可用的候選名單,原因不同、且均非「隨意跳過」——已逐一查證根因,詳見第 4 節。這份報告本身就是本期的成功心跳:即使沒有標的可評,仍照常產出、commit、push。

框架回顧:找「市場半信半疑的高成長」——分析師估計持續上修、但估值倍數仍打折(PEG<0.7 或 forward P/E 明顯落後於成長率)、財報能兌現、敘事可命名且有主題群聚。發酵分數 = S1 估計上修(0-3) + S2 半信半疑落差(0-3) + S3 財報兌現(0-2) + S4 敘事可命名/群聚(0-2) + S5 已全信扣分(0~-2),滿分 10。

## 1. 總覽表

無。本期 `output/candidates_20260829.csv` 為 0 檔(僅表頭),`output/streak_20260710.csv` 仍是 56 天前的舊快照(自 08/21 起已比照編輯判斷不再沿用)。沒有可放進總覽表的標的。

## 2. 高分標的(≥7)

無標的可評估,本節從缺。

## 3. 其餘標的(一行帶過)

無。

## 4. 附註

### 4.1 本期 CSV 狀態

| 檔案 | 日期 | 距今 | 狀態 |
|---|---|---|---|
| `candidates_20260829.csv` | 2026-08-29 | 6 天 | 存在,但**僅表頭、0 檔候選**(未逾 8 天新鮮度門檻,判定 candidates 管線本身仍在跑,只是本週沒有標的通過篩選) |
| `streak_20260710.csv` | 2026-07-10 | **56 天** | 遠逾 8 天新鮮度門檻;自 08/21 期報告起,編輯判斷已不再沿用此舊快照當作本週候選來源(避免拿兩個月前的市場快照冒充當週訊號) |

### 4.2 根因追查:streak 管線已連續 8 週失敗(非本期新發現,但本期首次查到精確錯誤)

直接調閱 GitHub Actions 執行紀錄(`a05031113/stock-screener` repo 的 `Weekly Early Momentum Screener` workflow):**自 2026-07-27(run #34)起到本週 2026-08-29(run #43)為止,連續 10 次排程執行,job 結論全部是 `failure`**——但 workflow 的 Commit 步驟用了 `if: always()`,所以 candidates 側已寫出的檔案仍會被提交,只是 streak 部分永遠沒機會落地,才會造成「candidates 每週都有新檔、streak 卡在 07/10」這個外觀。

本期實際調出 2026-08-29 那次執行(run id 33256544261)的完整 job log,錯誤鏈非常清楚:

```
[INFO] Finviz Weekly Up: 3354 tickers
[INFO] Weekly streak screening 3354 tickers...
[WARNING] Consecutive empty chunks — rate-limited, aborting round early to preserve budget (aborted_remaining: 2194)
[INFO] [40/3354] daily closes downloaded (attempt 1, failed 3314)
[WARNING] Retrying failed downloads after backoff (attempt 1, backoff_sec 120)
... (attempt 2, 3, 4,退避 120s→240s→360s,coverage 始終卡在 40/3354)
Traceback: main.py:25 → screener.py:693 run_weekly_streak_screener → screener.py:576 _download_daily_closes
RuntimeError: Batch download coverage 40/3354 below 50% after 4 attempts — aborting instead of producing incomplete streak results
```

白話講:GitHub Actions 執行環境的出口 IP 一連上 Yahoo Finance 批次下載日 K 線,幾乎立刻被限流(3354 檔裡只抓得到 40 檔),4 次退避重試(2→4→6→10 分鐘間隔)都沒能突破封鎖,最後撞到 `screener.py:576` 「覆蓋率低於 50% 就不產生不完整結果」的保護閾值,主動中止並丟出例外——這是刻意設計的 fail-loud 行為(見 `fix: rate-limit resilience` 系列 commit),不是靜默吃錯,但代價是 streak 這條線已經連續兩個月產不出任何新資料。這比較像是 Yahoo 對這個 CI IP 段/User-Agent 做了長期封鎖或極嚴格限流,單純加大退避重試次數大概率無法解決,建議持有人考慮:换一個資料源(如改批次呼叫可用 API key 的付費資料商)、把週六補跑的觸發時段也拉開更大間隔、或改用非 GitHub Actions 的固定出口 IP 執行 streak 掃描。

### 4.3 candidates 側:非故障,但近期持續掛零值得留意

candidates 這條線本身正常執行完畢(job log 顯示是先跑完 `run_screener()` 才進入 streak 階段失敗),0 檔是 Stage 2 / Base Breakout 門檻下的有效結果,不是程式錯誤。但把最近 5 週檔數攤開來看:

| 日期 | candidates 檔數 | 標的 |
|---|---|---|
| 2026-08-01 | 1 | EEA |
| 2026-08-07 | 0 | — |
| 2026-08-08 | 0(週六補跑) | — |
| 2026-08-14 | 0 | — |
| 2026-08-15 | 0(週六補跑) | — |
| 2026-08-21 | 2 | SSD、TTAN |
| 2026-08-22 | 2(週六補跑,同一組) | SSD、TTAN |
| 2026-08-29 | **0** | — |

連續多週落在 0-2 檔的低水位,可能單純是近期美股缺乏同時滿足「Stage 2 + 量能 + 技術面 8 分門檻」的標的(市場本身動能不足),但也可能是 `universe.py` 的 Finviz 篩選門檻(relative volume、SMA 排列)相對目前市況偏嚴。這件事無法靠本期報告單獨判斷,列出來供持有人參考是否要調整篩選閾值或觀察更長區間再下結論。

### 4.4 本期評估與跳過

- 評估檔數:**0**。
- 跳過檔數:candidates 0 檔(沒有東西可跳);streak 56 天陳舊,依 08/21 期建立的編輯原則整批不採用,不算「跳過個別標的」而是整個來源本期不使用。
- 未對任何標的做六訊號評分或對抗性審查,因為沒有輸入資料,強行評分等同杜撰。

### 4.5 簡介頁計畫

本期沒有新評估標的,**不會有新的或更新的簡介頁**,也不會有 `profiles:` commit。既有的 `reports/profiles/SSD.md`、`reports/profiles/TTAN.md`(2026-08-21 建立/更新)仍在 90 天效期內,留待下次真正評估到這兩檔時再視需要更新。

---
本報告為研究彙整,非投資建議,不構成買賣任何證券之要約或建議。所有數字如有時效性差異,請以來源網站當下顯示為準。
