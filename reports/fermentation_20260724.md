# 敘事發酵週報 — 2026-07-24

**本週 screener 未產出新結果。**

## 1. 總覽表

本期無新資料可評估，故無總覽表。最新可用資料仍為 `output/candidates_20260710.csv`（12 檔）與 `output/streak_20260710.csv`，兩者皆已於 [fermentation_20260711](fermentation_20260711.md)（tag `report-20260711`）完整評估過。

## 2. 高分標的（≥7）

無（本期未評估）。

## 3. 其餘標的（一行帶過）

無（本期未評估）。

## 4. 附註

**本期 CSV 日期**：`output/` 目錄中最新檔案仍是 `candidates_20260710.csv`／`streak_20260710.csv`（2026-07-10），距本報告產出日 **14 天**，已超過原訂 8 天的檔案時效門檻。查證 GitHub Actions 確認**本週上游 screener 第三週連續執行失敗**，而且這次是全新的失敗型態，並非上週那種逾時：

- Workflow `Weekly Early Momentum Screener` run [30129294403](https://github.com/a05031113/stock-screener/actions/runs/30129294403)（2026-07-24 21:54 UTC 觸發，main 分支，commit `9b8f223`）於 22:03 UTC 以 **exit code 1** 失敗，耗時約 9 分鐘——這次不是撞到 job timeout（上週的 timeout-minutes 已從 30 分鐘放寬到 60 分鐘），而是程式主動拋出例外中止。
- Log 顯示技術面篩選（Finviz Stage 2 + Base Breakout，共 146 檔候選）本身順利跑完，但結果是 **`No candidates found this week`**——本週沒有任何標的通過技術門檻，這部分是正常結果，只是這個結果從未被寫回 repo，因為緊接著的週 K 連漲掃描（streak scan）拋出例外，讓整個 job 失敗，`Commit results` 步驟因而被跳過（`if` 條件預設不執行於失敗之後的 job），**候選為 0 這件事和舊資料都沒有被提交**。
- Streak 掃描本期 Finviz「本週上漲」清單有 2438 檔。上週（7/19）持有人已在 `fix/batch-download-streak-scan` 與 `fix/batch-retry-fail-loud` 兩個分支修好舊的逐檔序列請求逾時問題，改成批次下載＋退避重試＋覆蓋率 <50% 時 fail loud（commit `5ad8037`、`72cfc81`，已於 `9b8f223`／PR #5 併入 main）。但本期批次下載首輪只成功取得 **55/2438（2.3%）**檔的日K，退避重試 30 秒、60 秒後兩輪仍卡在同一個 55/2438，第三次仍未突破 50% 覆蓋率門檻，觸發新加的 fail-loud 保護機制主動中止：`RuntimeError: Batch download coverage 55/2438 below 50% after 3 attempts`（`screener.py:509`）。
- 值得注意：log 中完全沒有出現「Download failure reasons (sample)」這行警告（`screener.py:498-505` 本應在有例外訊息時印出取樣），代表這次失敗的 2383 檔並非逐檔拋出可辨識的錯誤訊息，而是批次請求整批傳回空結果（`data.empty`），研判是 Yahoo Finance 對 GitHub Actions runner 的來源 IP 做了較上週更嚴格的批次端點限流／封鎖，且退避時間內未解除。也就是說，**上週的修復方向（改批次下載）雖然解決了「單檔序列請求太慢導致 timeout」的問題，但暴露出「批次端點本身更容易被整批限流」的新風險**，兩者是不同故障模式，不能互相替代。
- **本期評估 0 檔**（無新資料），未跳過任何候選（因根本沒有候選清單可讀）。
- 本期未新建或更新任何 `reports/profiles/` 簡介頁。
- **建議修復方向**（供持有人參考，非本 routine 職責範圍）：(a) 批次下載失敗時可考慮 fallback 回退到小批次或單檔請求，而非直接中止整個 streak scan；(b) 覆蓋率 <50% 才 fail loud 的門檻可能太晚——本次第一輪就只有 2.3%，或可提早在覆蓋率極低（如 <10%）時就縮短重試次數，改用更長的退避或換一個資料來源；(c) 若 Yahoo 批次端點的限流是週期性的（例如固定時段封鎖 CI IP range），可考慮把 streak scan 排到 screener 主流程之後單獨重試，或錯開執行時間；(d) 目前候選為 0 的正常結果會因為後段 streak scan 失敗而整批不提交，建議讓 `Commit results` 步驟改用 `if: always()`（搭配 job 內兩段式錯誤處理），讓「候選 0 檔」這種有效結果不因下游模組失敗而被吞掉。

---
本報告為研究彙整，非投資建議，不構成買賣任何證券之要約或建議。所有數字如有時效性差異，請以來源網站當下顯示為準。

---
*本期無新評估對象，未產出新的公司簡介頁。*
