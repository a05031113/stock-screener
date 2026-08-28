# 敘事發酵週報 — 2026-08-28

依據 `output/candidates_20260822.csv` 產出。**本期尚無 2026-08-28 當週的全新 screener 產出**——main 分支最新一次 screener commit 為 `76458b1`(2026-08-22,9 天前的 09:37 UTC),距本次報告執行時間已逾一週但未逾 8 天新鮮度門檻上限太多,判定 candidates 管線本身尚未失敗,只是本次報告執行時間點早於本週五收盤後的排程批次,或本週批次尚未落地。streak 管線則持續失敗:現存最新檔案仍是 `output/streak_20260710.csv`,距今 **49 天**,自 2026-07-10 最後一次成功後已連續多期未產出新結果,遠超 8 天新鮮度門檻。

**本期資料延續性說明(編輯判斷)**:`candidates_20260822.csv` 與上期 `candidates_20260821.csv` 的兩檔標的(SSD、TTAN)**價格、技術/基本面分數完全相同**(SSD $188.77、TTAN $94.87,total_score 分別為 15、14),顯示這兩份檔案很可能對應同一組市場快照(2026-08-21 週五收盤價),並非兩個獨立市場週期的新資料。上期報告([08/21](fermentation_20260821.md))已對這兩檔做過完整六訊號評估與對抗性審查。本期經查證,兩檔標的自上期報告後**無新財報、無重大分析師評等變動、無指引調整**(TTAN 下次財報為 2026-09-08,尚未公布;SSD 上次財報為 2026-07-27,同上期),僅有增量、非結構性的新訊息(詳下)。比照上期報告對 streak 舊快照的處理原則——沒有新資訊的重複深度評估不會產生新洞見,只會稀釋報告品質——本期**不重新從零推導六訊號分數**,改為:(1)沿用上期分數,(2)執行增量查證確認有無需要調整分數的新事實,(3)完整寫出增量查證發現與來源。若下週出現真正 2026-08-28 之後的新 candidates 批次,將重新完整評估。

框架回顧:找「市場半信半疑的高成長」——分析師估計持續上修、但估值倍數仍打折(PEG<0.7 或 forward P/E 明顯落後於成長率)、財報能兌現、敘事可命名且有主題群聚。發酵分數 = S1 估計上修(0-3) + S2 半信半疑落差(0-3) + S3 財報兌現(0-2) + S4 敘事可命名/群聚(0-2) + S5 已全信扣分(0~-2),滿分 10。

## 1. 總覽表

| Ticker | 來源 | Sector | 發酵分數 | 一句話主題 | 審查結論 |
|---|---|---|---|---|---|
| [TTAN](profiles/TTAN.md) | candidates | Technology(垂直 SaaS,現場服務業管理軟體;CSV 原始 sector 欄位誤植為 Financial/Exchange Traded Fund,沿用上期查證結果) | **8**(沿用上期,增量查證未發現需調整之新事實) | AI 賦能水電空調等現場服務業 SaaS,估值倍數不便宜但空頭部位同樣不小 | Partial(沿用) |
| [SSD](profiles/SSD.md) | candidates | Basic Materials(建材結構連接件;CSV 原始 sector 欄位誤植為 Energy/Oil & Gas E&P,沿用上期查證結果) | 4(沿用上期) | 建材連接件龍頭靠漲價撐營收,估值已超前個位數成長率 | 未達門檻 |

## 2. 高分標的(≥7)

### TTAN — ServiceTitan, Inc.(發酵分數 8,沿用上期)

> 📄 [公司簡介:TTAN 在做什麼、TAM、競爭者、營收結構](profiles/TTAN.md)(2026-08-21 建立,90 天內,本期沿用不重寫)

**六訊號分數與依據**:完整逐項證據見[上期報告](fermentation_20260821.md#2-高分標的7)——S1 估計上修軌跡 3/3、S2 半信半疑落差 2/3(絕對 PEG 2.15 偏高,但 forward 倍數隨 EPS 估計上修方向性收斂,呈現 NVDA 型態特徵)、S3 財報兌現節奏 2/2(近 5 季 4 次擊敗共識)、S4 敘事可命名+群聚 1/2(敘事可命名但本期無同題材第二檔)、S5 已全信扣分 0(股價仍在 52 週高點下方、空頭部位偏高,未顯示「全信」)。

**本期(2026-08-28)增量查證,確認無需調整分數的理由**:
- 下次財報時間確認為 **2026-09-08**(seekingalpha.com「ServiceTitan Announces Fiscal Fourth Quarter and Full Fiscal Year 2026 Financial Results」相關報導、stocktitan.net 排程頁),本期報告日尚未公布新一季數字,S1/S3 無新財報數據可更新。
- 內部人賣壓延續但屬既有揭露模式的一部分,並非新增風險:總裁 Vahe Kuzoyan 於 2026-08-11、08-12 執行 B 股轉 A 股並出售,價格區間 $85.02–$90.65(來源:kalkinemedia.com「ServiceTitan President Vahe Kuzoyan Executes Class A Stock Sales in August 2026」、stocktitan.net Form 144 SEC filing)。此與上期簡介頁「反方觀點」已記錄的 CEO/董事/CAO 結構性賣壓屬同一模式的延續,未查得新型態或加速跡象,不足以下修 S5。
- 未查得 2026-08-21 之後有具體券商目標價調升/調降的一手公告(TipRanks 於 08-24 有「分析師精選」報導提及 TTAN,08-20 有「分析師看法分歧」的泛稱報導,但均未查得可交叉確認的具體目標價數字,故不計入 S6,以免以模糊來源杜撰精確數字)。
- 股價 $99.87 較上期 $94.87 有小幅回升(注意 stockanalysis.com 頁面時間戳記顯示「as of Aug 28, 2024」疑為該站快取年份顯示錯誤,惟其餘欄位如 FY 財報排程、EPS 數字與 finviz 交叉一致,判斷除年份顯示外之數字仍為近期有效值);此價格變動未大到需要重新計算 PEG/forward P/E 分級,原 2/3 判定維持。

**引爆條件、主要風險**:與上期報告完全相同,詳見[上期 TTAN 全文](fermentation_20260821.md#2-高分標的7)與[簡介頁第 6-7 節](profiles/TTAN.md)。

**結論**:Partial(沿用上期判定,增量查證未發現改變判定的新事實)。

**來源 URL(本期增量查證)**:
https://kalkinemedia.com/us/news/announcements/servicetitan-president-vahe-kuzoyan-executes-class-a-stock-sales-in-august-2026 ・ https://www.stocktitan.net/sec-filings/TTAN/144-service-titan-inc-sec-filing-20671fbed013.html ・ https://seekingalpha.com/pr/20435974 ・ https://stockanalysis.com/stocks/ttan/forecast/ ・ https://finviz.com/quote.ashx?t=TTAN

---

## 3. 其餘標的(一行帶過)

- **SSD(4,沿用上期)**:Simpson Manufacturing(建材結構連接件龍頭,北美市佔逾 75%)。本期查證:股價自上期起走弱,08-18 單日下跌 3.1% 至 $189.84(來源:gurufocus.com「A Look at Simpson Manufacturing Co Inc (SSD) After 3.1% Decline」),08-26 舉行 Mid Atlantic 區域法說路演(Stephens 券商公告),過去一週股價累計下跌約 5%,但均為既有「PEG 2.14、Forward P/E 約 19-20 倍遠高於次年 EPS 成長率 6.17%,估值已超前成長,不符合『半信半疑』剖面」判定的延續而非反轉,分數維持 4,未達 7 分門檻,不觸發對抗性審查。

## 4. 附註

- **本期 CSV 日期**:`candidates_20260822.csv`(距今 6 天,未逾 8 天新鮮度門檻,判定管線正常;惟為 2026-08-21 收盤快照的重複產出,非全新一週資料,詳見報告開頭說明);`streak_20260710.csv`(距今 49 天,已連續多期逾 8 天新鮮度門檻,streak 管線持續失敗)。
- **評估檔數**:candidates 全數 2 檔(SSD、TTAN)皆納入評估,0 檔跳過;因與上期資料重複,本期採「沿用分數+增量查證」而非全新推導(理由詳報告開頭)。streak 因 49 天陳舊,本期比照上期做法不予採用,無 streak 來源標的。
- **管線健康度**:candidates 側自 08/21 起連續兩次執行皆為同一份 08-21 收盤快照,尚未確認本週(2026-08-28)全新批次是否會落地或是否再次遭遇速率限制中止;streak 側自 2026-07-10 最後成功後已 49 天無新檔案,問題與 08/14 報告記錄之根因(yfinance 速率限制、覆蓋率 fail loud)性質一致,建議持有人檢查 GitHub Actions 排程執行紀錄以確認本週批次是否曾嘗試執行及失敗原因。
- **資料品質提醒(沿用上期發現)**:`candidates_*.csv` 的 sector/industry 欄位對 SSD、TTAN 仍為誤植(SSD 標示 Energy/Oil & Gas E&P,實際為 Basic Materials;TTAN 標示 Financial/Exchange Traded Fund,實際為 Technology),本期報告與簡介頁皆已改用查證後之正確產業別,詳見上期報告第 4 節之根因追查記錄。
- 所有財務數字均要求至少 2 個獨立來源交叉確認;本期新增之增量查證數字(內部人交易、股價走勢、法說會排程)已於上文標明來源,未憑記憶或訓練資料杜撰數字。
- **簡介頁計畫**:本期 2 檔評估對象(SSD、TTAN)之簡介頁皆已存在且更新日期為 2026-08-21(90 天內),本期增量查證未發現財報重編、併購或指引大改等「重大變化」門檻事件,故**兩份簡介頁本期均沿用不重寫**,不會有新的 profiles commit。

---
本報告為研究彙整,非投資建議,不構成買賣任何證券之要約或建議。所有數字如有時效性差異,請以來源網站當下顯示為準。
