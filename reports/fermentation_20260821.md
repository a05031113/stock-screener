# 敘事發酵週報 — 2026-08-21

依據 `output/candidates_20260821.csv` 產出。本期candidates管線**恢復正常執行**並產出**2檔**通過總分≥14門檻的候選（SSD 15分、TTAN 14分）——這是自2026-07-31以來candidates首次繳出有意義的非零結果。streak管線則仍未恢復：現存最新檔案為`output/streak_20260710.csv`，距本期報告日已**42天**，早已超過8天的新鮮度門檻,代表streak掃描這條線自2026-07-10最後一次成功後持續失敗（詳見第4節）。

**本期streak處理方式的編輯判斷**：過去三期報告（07/31、08/07、08/14）已連續沿用同一份`streak_20260710`舊快照，對相同12檔標的（IMMX、DAVE、KYMR、ACRS、CTNM、KURA、BLLN、DYN、AVAH、BLZE、HNGE、JXG）做了三輪重複的深度評估與對抗性審查，內容已完整記錄在前三期報告與對應簡介頁中。本期起**不再第四次沿用同一份streak快照**——沒有新價格、新財報或新分析師動作可供比對，第四輪重複評估不會產生新資訊，只會稀釋報告品質。讀者如需追蹤該12檔的最新狀態，請參閱[08/14報告](fermentation_20260814.md)與對應簡介頁（狀態應視為截至08/14，之後未再更新）。若streak管線恢復產出新資料，下期將重新納入評估。本期評估對象因此**僅限candidates的2檔**，未違反「不能靜默跳過」的原則——streak的失敗與處理決策已在此完整說明,而非略而不提。

框架回顧：找「市場半信半疑的高成長」——分析師估計持續上修、但估值倍數仍打折（PEG<0.7或forward P/E明顯落後於成長率）、財報能兌現、敘事可命名且有主題群聚。發酵分數 = S1估計上修(0-3) + S2半信半疑落差(0-3) + S3財報兌現(0-2) + S4敘事可命名/群聚(0-2) + S5已全信扣分(0~-2)，滿分10。

## 1. 總覽表

| Ticker | 來源 | Sector | 發酵分數 | 一句話主題 | 審查結論 |
|---|---|---|---|---|---|
| [TTAN](profiles/TTAN.md) | candidates | Technology（垂直SaaS，現場服務業管理軟體，CSV原始sector欄位誤植為Financial/Exchange Traded Fund，詳見第4節） | **8** | AI賦能水電空調等現場服務業SaaS，估值倍數不便宜但空頭部位同樣不小 | Partial |
| [SSD](profiles/SSD.md) | candidates | Basic Materials（建材結構連接件，CSV原始sector欄位誤植為Energy/Oil & Gas E&P，詳見第4節） | 4 | 建材連接件龍頭靠漲價撐營收，估值已超前個位數成長率 | 未達門檻 |

## 2. 高分標的（≥7）

### TTAN — ServiceTitan, Inc.（發酵分數 8）

> 📄 [公司簡介：TTAN 在做什麼、TAM、競爭者、營收結構](profiles/TTAN.md)

**六訊號逐項證據**
- **S1 估計上修軌跡（3/3）**：stockanalysis.com/stocks/ttan/forecast/顯示FY2026 EPS共識由$1.02上修至$1.31、FY2027由$1.31上修至$1.64，方向一致向上（頁面未標明確切90天區間，以查得原始描述呈現，未過度解讀為精確90天窗口）。同期至少三家大行於過去約2個月內上調目標價：TD Cowen上調至$125、Morgan Stanley上調至$124、Piper Sandler上調至$115（來源：stockanalysis.com整理之最新分析師動作）。
- **S2 半信半疑落差（2/3）**：finviz.com顯示Forward P/E 57.80、PEG 2.15；stockanalysis.com顯示FY2027 non-GAAP Forward P/E約72.35（兩來源對Forward P/E定義/基期不同，數字有落差，兩者並列）。以絕對倍數而言PEG遠高於<0.7門檻，並非典型「估值打折」。但股價目前距52週高點-20.7%、過去一年報酬-8.67%（finviz），與同期EPS估計大幅上修（$1.02→$1.31、$1.31→$1.64）方向相反，代表**forward倍數正隨獲利上修而收斂**（NVDA型態的方向性特徵），因此打折給2/3，而非依絕對PEG給0分。
- **S3 財報兌現節奏（2/2）**：近5季4次擊敗共識——Q1FY27(6/4)實際$0.37對共識$0.28（+32.1%）、Q4FY26(3/12)實際$0.27對$0.18（+50.0%）、Q3FY26(12/4/2025)實際$0.24對$0.15（+60.0%）、Q1FY26(6/5/2025)實際$0.18對$0.12（+50.0%）；唯一一次未達標為Q2FY26(9/4/2025)實際-$0.22對共識$0.18（-222.2%，未查證到具體一次性項目說明，列為缺口而非編造原因）。來源：marketbeat.com/stocks/NASDAQ/TTAN/earnings/。
- **S4 敘事可命名+群聚（1/2）**：敘事可一句話說出——「AI賦能水電空調等現場服務業的雲端SaaS作業系統」，公司2026年Pantheon大會發表Atlas AI Sidekick（Titan Intelligence引擎）與Maximize Pro產品綑綁包，分析師稱2026年為「多年期Pro/AI採用順風」起點（Yahoo Finance報導）。惟本期candidates僅2檔且無同題材第2檔，streak群聚資料因42天陳舊未採用，本期無法確認同主題群聚，故不給滿分。
- **S5 已全信扣分（0）**：股價仍在52週高點下方20.7%、過去一年報酬為負，且做空比例達16.67%（finviz），另一來源顯示2026年初短部位曾隨內部人出售大增（ticker.report，1月數據，較舊）。多項訊號顯示市場遠未「全信」，不扣分。
- **S6 分析師動作（參考）**：17位分析師、共識評等Strong Buy（finviz Recom 1.29）；共識目標價$110.40（+16.37%），最高$125、最低$83，區間仍寬。

**引爆條件**：Pro/AI加購產品（Maximize Program、Atlas AI Sidekick）實際滲透率與ARPU數據在下季財報揭露；EPS估計上修軌跡能否延續且伴隨forward P/E持續收斂；內部人出售(CEO、董事、CAO均於近月出售)是否降溫。

**主要風險（對抗性審查後）**：
1. 持續且多層級的內部人出售：CEO Ara Mahdessian近90天內出售約88,525股（約$952萬，ticker.report，1月數據）；董事William Griffith出售94,615股（約$600萬）；董事Byron Deeter出售17,690股（約$113.8萬）；財務長辦公室層級的Chief Accounting Officer Michele O'Connor於6/9出售10,000股，同日股價下跌近4%（blockonomi.com）。IPO後（2024/12上市）常見的lockup後供給壓力仍是實質賣壓來源，並非純粹市場非理性。
2. 做空比例16.67%屬偏高水位，且被歸因於「高成長SaaS類股在利率疑慮下遭資金撤出」的總經敏感度（tipranks/相關報導），代表市場的保留態度部分建立在合理的總經與流動性風險上，而非單純資訊落差。
3. 中低階競爭者（Housecall Pro、Jobber）持續向上市場移動，長期可能壓縮TTAN在中型承包商區隔的滲透空間；FieldEdge、Salesforce Field Service亦為既有對手。
4. 絕對估值不便宜：Forward P/E 57.8-72倍區間本身仍為典型高成長股溢價，並非「打骨折價」，S2的收斂邏輯建立在方向而非絕對水準。

**結論**：Partial——EPS估計上修方向明確、財報兌現節奏扎實（4/5季擊敗）、且forward倍數隨獲利上修同步收斂，符合框架核心「半信半疑」的方向性特徵；但對抗性審查顯示市場的保留有相當理性基礎（IPO後內部人結構性賣壓、做空比例偏高反映真實總經/流動性顧慮、絕對估值仍不便宜），故判定Partial而非Fits。

**來源 URL**：
https://stockanalysis.com/stocks/ttan/forecast/ ・ https://stockanalysis.com/stocks/ttan/ ・ https://finviz.com/quote.ashx?t=TTAN ・ https://www.marketbeat.com/stocks/NASDAQ/TTAN/earnings/ ・ https://finance.yahoo.com/news/servicetitan-ttan-stock-reaffirmed-overweight-223011642.html ・ https://www.servicetitan.com/press/servicetitan-introducing-the-next-evolution-of-ai-at-pantheon-2025-keynote ・ https://ticker.report/news/ttan-servicetitan-short-interest-jumps-amid-substantial-insider-selling-2026-01-19 ・ https://blockonomi.com/servicetitan-ttan-drops-nearly-4-following-insider-share-sale-by-chief-accounting-officer/

---

## 3. 其餘標的（一行帶過）

- **SSD（4）**：Simpson Manufacturing（建材結構連接件龍頭，北美市佔逾75%），財報連續6季擊敗共識（+3.3%~+15.8%），但PEG達2.22、Forward P/E約19.4-20.8倍遠高於次年EPS成長率6.17%（finviz），屬「估值已超前成長」而非「半信半疑」；公司自身指引更明言下半年成長與毛利率將轉弱（漲價貢獻多於銷量），本期成長驅動力主要來自提價而非需求擴張，不符合框架鎖定的「未被定價的高成長」剖面，S2/S4皆低分，未達門檻。

## 4. 附註

- **本期CSV日期**：`candidates_20260821.csv`（報告當日產出，距今0天，新鮮）；`streak_20260710.csv`（現存最新streak檔案，距今42天，已逾8天新鮮度門檻，判定streak管線本期仍失敗，詳見下段）。
- **評估檔數**：candidates全數2檔（SSD、TTAN）皆納入評估，0檔跳過。streak因42天陳舊，本期起不再沿用（理由詳見報告開頭），故本期無streak來源標的；上期(08/14)沿用之12檔streak標的狀態請參閱[08/14報告](fermentation_20260814.md)，本期不重複評估。
- **管線健康度**：candidates本期恢復產出2檔非零結果，優於過去4次執行中3次繳出0-1檔的紀錄，值得留意但樣本仍小（僅2檔），暫不足以判定篩選邏輯已系統性改善。streak自2026-07-10最後一次成功後至今42天未見新檔案，與08/14報告記錄之Yahoo Finance/yfinance速率限制中止問題（`RuntimeError`，覆蓋率<50%即fail loud）性質一致，建議持有人參考08/14報告第4節之根因與修復建議（縮減股票池、分散排程、或改用付費資料源）。
- **資料品質重大發現（本期新增）**：`candidates_20260821.csv`的sector/industry欄位本期查證**兩檔全數誤植**——SSD在CSV中標示為「Energy / Oil & Gas E&P」，但Finviz官方頁面(finviz.com/quote.ashx?t=SSD)查得SSD實際為「Basic Materials / Lumber & Wood Production」（Simpson Manufacturing，建材結構連接件）；TTAN在CSV中標示為「Financial / Exchange Traded Fund」，但TTAN實際為ServiceTitan（現場服務業SaaS，非ETF），Finviz/stockanalysis.com/Yahoo Finance三方一致確認為科技股。經追查`universe.py`程式碼（`_parse_metadata`函式，`git log`顯示由commit 81603aa於2026-07-11引入），該函式直接複用Finviz screener單次批次查詢回傳的`Sector`/`Industry`欄位、邏輯本身無明顯錯誤，故懷疑問題出在Finviz screener批次查詢當下回傳的原始資料本身有誤（例如快取延遲、或該批次查詢回傳列與ticker對應有誤），而非下游程式邏輯錯誤；本報告的六訊號評估已改用直接查證所得之正確sector/industry，但建議持有人檢查`universe.py`/`screener.py`日後是否有辦法對Finviz回傳的sector/industry做基本合理性校驗（例如與ticker既有分類資料庫比對），避免未來的主題群聚判斷（S4訊號）因錯誤sector標籤而失真。
- 所有財務數字均要求至少2個獨立來源交叉確認；查無或僅單一來源支持者已於SSD、TTAN段落內以「查無」或標明單一來源方式註明,未憑記憶或訓練資料杜撰數字。
- **簡介頁計畫**：本期2檔評估對象（SSD、TTAN）皆無既存簡介頁，將於週報commit+push後新建兩份完整簡介頁，完成後一次commit送出。

---
本報告為研究彙整，非投資建議，不構成買賣任何證券之要約或建議。所有數字如有時效性差異，請以來源網站當下顯示為準。
