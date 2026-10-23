# 敘事發酵週報 — 2026-10-24

**本期無可評估標的(0 檔)。** 本週(對應 `screener: 2026-10-24 results` 這次排程)上游 screener 兩條管線(candidates、streak)雙雙未產出任何標的——而且 candidates 側這次不是「跑完但 0 檔命中門檻」的正常空結果,而是**連 `output/candidates_20261024.csv` 這個檔案本身都沒有被寫出來**,這點與過去幾次「0 檔」週報(09/04、09/11)不同,值得特別記錄。本報告已追到程式碼層級的可能根因(見第 4.2 節),這份報告本身就是本期的成功心跳:即使沒有標的可評,仍照常產出、commit、push。

框架回顧:找「市場半信半疑的高成長」——分析師估計持續上修、但估值倍數仍打折(PEG<0.7 或 forward P/E 明顯落後於成長率)、財報能兌現、敘事可命名且有主題群聚。發酵分數 = S1 估計上修(0-3) + S2 半信半疑落差(0-3) + S3 財報兌現(0-2) + S4 敘事可命名/群聚(0-2) + S5 已全信扣分(0~-2),滿分 10(S6 分析師動向僅供參考,不計分)。

## 1. 總覽表

無。本期沒有任何新 candidates 或 streak 標的可放進總覽表——詳見第 4.1 節的檔案狀態說明。上期(2026-10-17)已評估的 12 檔(BLK、NDSN、PRSU、FIGS、EOG、RPRX、TALO、MDT、IMO、CRGY、TRV)仍可在 [fermentation_20261017](fermentation_20261017.md) 查閱,本期未重新查證、分數不變。

## 2. 高分標的(≥7)

無標的可評估,本節從缺。

## 3. 其餘標的(一行帶過)

無。

## 4. 附註

### 4.1 本期 CSV 狀態

| 檔案 | 日期 | 距今 | 狀態 |
|---|---|---|---|
| `candidates_20261024.csv` | — | — | **不存在**。最新的 candidates 檔仍是 `candidates_20261017.csv`(7 天前,已於上期報告完整評估,未逾 8 天新鮮度門檻,但對本期而言是「舊」資料,不重複計入) |
| `streak_20261024.csv` | 2026-10-24 | 0 天 | 存在,但**僅表頭、0 檔**——streak 管線本身有跑,只是 Finviz 本期上游回傳空清單 |

candidates 與 streak 這次是同一個時間點(本次排程執行)的兩個不同結果:streak 寫出了「0 檔但有檔案」,candidates 則完全沒有新檔案產生。兩者的差異本身就是本期最重要的診斷線索,見下節。

### 4.2 根因追蹤:candidates 本期為何連檔案都沒寫出來

這次沒有 GitHub Actions job log 可查(`screener.yml` 現在只是手動 workflow_dispatch 備援,本週正式執行是在持有人 Mac 上透過 launchd 跑的 `run_screener.sh`,本 session 沒有該機器的終端機/launchd log 存取權限,因此以下是直接讀程式碼比對兩個實際觀察到的檔案狀態、回溯出的最可能路徑,**不是**從實際執行 log 確認的根因,請持有人自行核對 launchd log 以確認):

1. `main.py` 執行順序是先呼叫 `screener.main()`(candidates),再呼叫 `universe.get_weekly_up_universe()` + `screener.run_weekly_streak_screener()`(streak)。streak 這次確實寫出了(即使是空的)`streak_20261024.csv`,代表 `main.py` **完整跑到底、沒有在中途丟未捕捉的例外中止**——也就是說 candidates 那段的例外(如果有)已經被內部處理掉,不是整支腳本崩潰。
2. 翻 `screener.py` 的 `main()`(`screener.py:782`)可以看到兩條「0 標的」的路徑,處理方式並不一致:
   - 技術面+基本面都跑完、但沒有任何標的通過門檻 → `df.empty` → 會呼叫 `save_results(pd.DataFrame(columns=CANDIDATE_COLUMNS))`,寫出一份**有表頭、0 列**的 CSV(這是 09/04、09/11 當時觀察到的型態)。
   - **Finviz 預篩(`get_prefiltered_universe()`)本身回傳空的 ticker 清單** → `if not tickers:` 這個分支只 `logger.error(...)` 後直接 `return pd.DataFrame()`,**沒有呼叫 `save_results()`**——也就是完全不會產生任何 `candidates_YYYYMMDD.csv`,無論是有資料還是空檔。
   
   本週觀察到的現象(candidates 檔案不存在,而不是「有表頭 0 列」)與第二條路徑完全吻合。
3. 若 candidates 側確實走了第二條路徑,代表 `universe.py` 的 `get_prefiltered_universe()`(呼叫 Finviz 的 Stage 2 + Base Breakout 兩組篩選)兩組都回傳了空清單。而 `get_weekly_up_universe()`(streak 用的 Weekly Up 篩選)同樣也回傳空清單,才會觸發 `run_weekly_streak_screener` 裡「empty ticker universe from Finviz」那條警告路徑,寫出空的 `streak_20261024.csv`。三組獨立的 Finviz 篩選**同時**回傳空清單,比較像是 Finviz 本身這次請求失敗(例如暫時性網路問題、Finviz 網站結構變動讓 `finvizfinance` 套件解析失敗、或請求被 Finviz 端擋掉),而不是「市場本週剛好沒有標的」這種正常情況——`_run_finviz_screen()` 和 `get_weekly_up_universe()` 內部把所有例外都吞掉只留一行 log,沒有留下更細的錯誤訊息供事後比對,這點本身也是個觀測死角。
4. **程式碼層的具體落差(建議修復)**:`screener.py` 的 `main()` 在「Finviz 預篩空清單」這個分支應該跟「掃完 0 檔」分支一樣呼叫 `save_results(pd.DataFrame(columns=CANDIDATE_COLUMNS))`,而不是直接 `return` 不留痕跡。目前的行為會讓 `run_screener.sh` 的 freshness check(找今天日期的 `candidates_*.csv`)永遠找不到檔案,週六 18:00 的補跑會用同樣的輸入再跑一次、很可能再次落入同一個空清單分支,陷入「每次補跑都靜默失敗、沒有任何錄」的循環,且下週報告也沒辦法從檔案本身分辨「本週真的 0 候選」跟「Finviz 這次根本沒回應」。

**建議持有人**:(1) 檢查這次排程執行當天 Mac 上 `run_screener.sh` 的終端輸出或系統 log,確認 Finviz 當時的實際回應(逾時?HTTP 錯誤?回傳格式變了?);(2) 考慮把 `main()` 裡「Finviz 預篩空清單」分支也補上 `save_results()`,並把 `_run_finviz_screen()` / `get_weekly_up_universe()` 的例外訊息記錄得更細(至少記下例外型別與前 200 字),避免下次又只能靠猜。這不屬於本 session 權限範圍(本 session 只在 `fermentation-reports` 分支產出報告,不碰 `main` 分支程式碼),僅記錄於此供持有人後續處理。

### 4.3 本期評估與跳過

- 評估檔數:**0**。
- 跳過檔數:0(沒有任何標的輸入,無從跳過個別標的)。
- 未對任何標的做六訊號評分或對抗性審查,因為沒有輸入資料,強行評分等同杜撰。

### 4.4 簡介頁計畫

本期沒有新評估標的,**不會有新的或更新的簡介頁**,也不會有 `profiles:` commit。上期(2026-10-17)新建的 9 份簡介頁(BLK、FIGS、PRSU、EOG、NDSN、RPRX、TRV、IMO、TALO)與更新的 CRGY、沿用的 MDT、TTE 均在 90 天效期內,留待下次真正評估到這些標的時再視需要更新。

---
本報告為研究彙整,非投資建議,不構成買賣任何證券之要約或建議。所有數字如有時效性差異,請以來源網站當下顯示為準。
