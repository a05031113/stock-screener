# 敘事發酵週報 — 2026-07-17

**本週 screener 未產出新結果。**

## 1. 總覽表

本期無新資料可評估，故無總覽表。最新可用資料仍為 `output/candidates_20260710.csv`（12 檔）與 `output/streak_20260710.csv`，兩者皆已於上週報告完整評估，詳見 [fermentation_20260711](fermentation_20260711.md)（tag `report-20260711`）。

## 2. 高分標的（≥7）

無（本期未評估）。

## 3. 其餘標的（一行帶過）

無（本期未評估）。

## 4. 附註

**本期 CSV 日期**：`output/` 目錄中最新檔案仍是 `candidates_20260710.csv`／`streak_20260710.csv`（2026-07-10），距本報告產出日 7 天——尚未超過原訂 8 天的檔案時效門檻，但本節查證確認**本週上游 screener 確實執行失敗**，故仍依「screener 失敗」規格產出本期報告，理由如下：

- 查詢 GitHub Actions（workflow `Weekly Early Momentum Screener`，run [29615516801](https://github.com/a05031113/stock-screener/actions/runs/29615516801)）：本應於 2026-07-17 21:40 UTC（美股收盤後）觸發，`Run screener` 步驟執行至 2026-07-17 22:11 UTC（滿 30 分鐘 job timeout）被 GitHub Actions 強制取消（`##[error]The operation was canceled.`），`Commit results` 步驟因而被跳過（skipped），**沒有任何新的 `output/` 檔案被提交**。
- 從 job log 可還原瓶頸：Finviz 週漲幅清單本期擴大到 **2647 檔**（`Finviz Weekly Up: 2647 tickers`），streak 掃描以約每 100 檔 75 秒的速度處理，取消時進度僅 1800/2647（約 68%）；以此速度跑完全部 2647 檔需要約 33 分鐘，**光是 streak 掃描本身就已經超出整個 job 的 30 分鐘預算**，還沒算上前面 Finviz 分頁抓取與後面的 candidates 技術/基本面評分。
- 對照前幾週：`streak_20260703.csv`／`streak_20260710.csv` 檔案大小分別為 36KB／5KB，本期候選/上漲清單明顯比 6/19（24KB）、7/3（36KB）更大，研判是近期大盤普遍上漲、觸發 Finviz「本週上漲」篩選條件的股票數量暴增，導致 streak 掃描的股票池從過去的數百檔膨脹到 2647 檔，超出目前逐檔序列請求（每檔約 0.75 秒）的處理能力。
- **本期評估 0 檔**（無新資料），未跳過任何候選（因根本沒有候選清單可讀）。
- 本期未新建或更新任何 `reports/profiles/` 簡介頁。
- **建議修復方向**（供持有人參考，非本 routine 職責範圍）：(a) 提高 `.github/workflows/screener.yml` 的 `timeout-minutes`（目前 30 分鐘，streak 掃描規模已不穩定，建議至少 45-60 分鐘）；(b) 為 streak 掃描加入平行/批次請求以縮短單檔延遲；(c) 若 Finviz「本週上漲」清單規模持續膨脹，考慮收緊 streak 的預篩條件（例如提高 relative volume 門檻）以控制股票池大小，避免持續逾時。

---
本報告為研究彙整，非投資建議，不構成買賣任何證券之要約或建議。所有數字如有時效性差異，請以來源網站當下顯示為準。

---
*本期無新評估對象，未產出新的公司簡介頁。*
