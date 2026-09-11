# 敘事發酵週報 — 2026-09-11

**本期無可評估標的(0 檔)。** 兩個上游資料來源本週仍然沒有產出可用的候選名單,與上一期(09/04)狀況相同、根因也相同——但本期已直接調閱最新一次排程執行(09/05, run #45)的完整 job log,確認 streak 管線的批次限流問題**仍未解決,且已找到一個現成但從未被合併的修復分支**,詳見第 4 節。這份報告本身就是本期的成功心跳:即使沒有標的可評,仍照常產出、commit、push。

框架回顧:找「市場半信半疑的高成長」——分析師估計持續上修、但估值倍數仍打折(PEG<0.7 或 forward P/E 明顯落後於成長率)、財報能兌現、敘事可命名且有主題群聚。發酵分數 = S1 估計上修(0-3) + S2 半信半疑落差(0-3) + S3 財報兌現(0-2) + S4 敘事可命名/群聚(0-2) + S5 已全信扣分(0~-2),滿分 10。

## 1. 總覽表

無。本期 `output/candidates_20260905.csv` 為 0 檔(僅表頭),`output/streak_20260710.csv` 仍是 63 天前的舊快照(自 08/21 起編輯判斷已不再沿用此舊快照冒充當週訊號)。沒有可放進總覽表的標的。

## 2. 高分標的(≥7)

無標的可評估,本節從缺。

## 3. 其餘標的(一行帶過)

無。

## 4. 附註

### 4.1 本期 CSV 狀態

| 檔案 | 日期 | 距今 | 狀態 |
|---|---|---|---|
| `candidates_20260905.csv` | 2026-09-05 | 6 天 | 存在,但**僅表頭、0 檔候選**(未逾 8 天新鮮度門檻,candidates 管線本身仍在跑,只是本週沒有標的通過篩選) |
| `streak_20260710.csv` | 2026-07-10 | **63 天** | 遠逾 8 天新鮮度門檻;自 08/21 期報告起,編輯判斷已不再沿用此舊快照當作本週候選來源 |

### 4.2 根因追蹤:streak 管線的批次限流問題本期仍未解除

直接調閱 GitHub Actions(`a05031113/stock-screener` repo,`Weekly Early Momentum Screener` workflow)最新一次排程執行——**run #45(run id 33965297900,2026-09-05 12:10 UTC 觸發,對應 `screener: 2026-09-04 results` 提交)**——job log 顯示錯誤鏈與上期完全一致:

```
[INFO] Finviz Weekly Up: 3640 tickers
[INFO] Weekly streak screening 3640 tickers...
[WARNING] Consecutive empty chunks — rate-limited, aborting round early to preserve budget (aborted_remaining: 2920)
[INFO] [20/3640] daily closes downloaded (attempt 1, failed 3620)
[WARNING] Retrying failed downloads after backoff (attempt 1, backoff_sec 120)
... (attempt 2, 3, 4,退避 120s→240s→360s,coverage 始終卡在 20/3640)
Traceback: main.py:25 → screener.py:693 run_weekly_streak_screener → screener.py:576 _download_daily_closes
RuntimeError: Batch download coverage 20/3640 below 50% after 4 attempts — aborting instead of producing incomplete streak results
```

比對排程執行歷史(workflow run 列表),`screener.yml` 自 **run #31(2026-07-25)起到本期 run #45(2026-09-05)為止,總計 14 次排程/手動執行全數 conclusion=failure**,已連續超過 6 週未曾成功產出 streak 結果。這不是單週偶發:同一批次限流問題已橫跨兩次 fix 合併(`fix/rate-limit-resilience`、`fix/paced-download-from-start`)仍未解決。

**本期新發現**:repo 裡有一條較早期、從未合併進 main 的分支 `fix/batch-retry-fail-loud`(領先 main 3 個 commit:`70ddd7a`、`4ca46a3`、`4fe44d3`),其 commit 訊息記錄了一輪獨立的實跑診斷,結論與本期現象高度吻合——**Yahoo 擋的是「併發 batch burst」模式,不是整個 IP 全面封鎖**;序列(逐檔、非併發)請求在同一輪測試中可以正常跑完。該分支的修法是:在 `GITHUB_ACTIONS=true` 環境下完全放棄 `yf.download` 批次併發,改為逐檔序列下載(每檔一次日K請求,仍比舊版月K+週K兩次省一半流量),並將連續失敗(含靜默回空,不只是 exception)≥30 次才觸發冷卻。相對地,目前 main 上已合併的 `fix/paced-download-from-start`(098d756)只是把批次下載「從第一個請求就放慢節奏」,並未真正改成序列 fallback——而本期 run #45 的 log 顯示批次下載仍在使用併發模式(20 檔後即連續空 chunk),與 `fix/batch-retry-fail-loud` 診斷的病因相符。

**建議持有人**:檢視 `fix/batch-retry-fail-loud` 分支的序列 fallback 邏輯是否仍適用(該分支較舊,合併前建議先 rebase 到目前 main 並在 workflow_dispatch 手動跑一次驗證),或用同樣的診斷方向重新實作——這比繼續加大批次重試次數或退避時間更可能解決問題。此外也可考慮:換一個對批次友善的資料源(付費 API key)、把週六補跑觸發時段拉開更大間隔、或改用非 GitHub Actions 的固定出口 IP 執行 streak 掃描。

### 4.3 candidates 側:非故障,但低水位持續了超過一個月

candidates 這條線本身正常執行完畢(job log 顯示是先跑完 `run_screener()` 才進入 streak 階段失敗),0 檔是 Stage 2 / Base Breakout 門檻下的有效結果,不是程式錯誤。近 7 週檔數:

| 日期 | candidates 檔數 | 標的 |
|---|---|---|
| 2026-08-01 | 1 | EEA |
| 2026-08-07~08-15 | 0 | — |
| 2026-08-21 / 08-22 | 2(同一組,週六補跑) | SSD、TTAN |
| 2026-08-29 | 0 | — |
| 2026-09-04 | 0 | — |
| 2026-09-05 | 0 | — |

已連續 5 週(含本期)落在 0 檔,是目前這波觀察期最長的空窗。可能單純是近期美股缺乏同時滿足「Stage 2 + 量能 + 技術面 8 分門檻」的標的,但持續一個多月的 0 檔也可能反映 `universe.py` 的 Finviz 篩選門檻(relative volume、SMA 排列)相對目前市況偏嚴。此判斷仍待更長區間或持有人手動檢視門檻設定確認。

### 4.4 本期評估與跳過

- 評估檔數:**0**。
- 跳過檔數:candidates 0 檔(沒有東西可跳);streak 63 天陳舊,依 08/21 期建立的編輯原則整批不採用,不算「跳過個別標的」而是整個來源本期不使用。
- 未對任何標的做六訊號評分或對抗性審查,因為沒有輸入資料,強行評分等同杜撰。

### 4.5 簡介頁計畫

本期沒有新評估標的,**不會有新的或更新的簡介頁**,也不會有 `profiles:` commit。既有的 `reports/profiles/SSD.md`、`reports/profiles/TTAN.md`(2026-08-21 建立/更新)已超過 90 天效期前緣但尚未過期,留待下次真正評估到這兩檔時再視需要更新。

---
本報告為研究彙整,非投資建議,不構成買賣任何證券之要約或建議。所有數字如有時效性差異,請以來源網站當下顯示為準。
