# FSLY — Fastly, Inc.

**1. 這家公司在做什麼**
Fastly 經營一個全球「邊緣伺服器」網路,把伺服器節點盡量放在靠近網路使用者的地方,讓網站、App 與 API 的回應速度變快,同時防護惡意流量攻擊;開發者也能把程式碼直接部署在這些邊緣節點上執行,而不需等待遠端資料中心處理。

**2. 解決什麼問題、為誰解決**
媒體、電商、SaaS 與遊戲公司是主要客戶,付費項目包括:傳輸的資料流量(頻寬)、在邊緣執行的運算請求,以及資安訂閱服務(WAF網頁應用防火牆、機器人流量管理、DDoS防護),目的是讓自家網站/App 保持快速且不被流量尖峰或攻擊打垮。

**3. 商業模式與營收結構**
FY2025(10-K)總營收 6.240 億美元(FY2024 為 5.437 億美元)。地區分布:美國 4.6545 億美元、國際 1.5857 億美元(約 75% / 25%);產品線方面,安全性產品營收 1.251 億美元(約佔 20%),其餘為網路服務(Network Services)及其他,本次查證未能取得網路服務單獨拆分的精確數字,需直接查 10-K 完整營收附註。(來源:[SEC 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1517413/000151741326000053/fsly-20251231.htm))

Q2 2026(2026/8/8 發布)營收創紀錄 1.833 億美元(+23% YoY,優於 1.70–1.76 億美元財測上緣),營業利益 2,700 萬美元遠優於 1,200–1,600 萬美元財測,安全性產品營收 +43% 至 4,170 萬美元,毛利率創紀錄 65.8%。公司同時將 FY2026 non-GAAP EPS 財測大幅上修至 $0.50–$0.54(原 $0.27–$0.33),營收財測上修至 7.32–7.46 億美元(原 7.10–7.25 億美元)。(來源:[marketbeat.com](https://www.marketbeat.com/instant-alerts/fastly-q2-earnings-call-highlights-2026-08-08/))

**4. 產業與 TAM**
公司自稱 TAM(2026年投資人日,透過二手來源引用,未直接核對原始投資人簡報,應謹慎看待):220 億美元,目標 2029 年營收達 11–13 億美元。第三方估計:整體 CDN 市場 2025 年約 272.5 億美元,2030 年將達 428.9 億美元(CAGR 9.5%,MarketsandMarkets);更窄的「CDN 上的邊緣函式」細分市場 2025 年約 59 億美元,2030 年達 135 億美元(CAGR 17.8%,TBRC)。(來源:[itbrief.com.au](https://itbrief.com.au/story/cdn-market-to-hit-usd-42-89bn-as-edge-demand-surges)、[giikorea.co.kr](https://www.giikorea.co.kr/report/tbrc1987708-edge-functions-on-content-delivery-network-cdn.html))

**5. 主要競爭者與定位**
**Cloudflare**(平台更廣、規模遠大於 Fastly)、**Akamai**(CDN 市場老牌龍頭,2019年IDC 數據顯示市佔約42%)、超大規模雲端業者捆綁服務(AWS CloudFront、Google Cloud CDN、Azure CDN),以及規模較小/私人業者(BunnyCDN、StackPath、CDN77,此處未逐一獨立查證)。

**6. 敘事發酵為什麼可能成立**
AI 推論流量快速成長 + 企業安全性產品交叉銷售 → 反映在 Q2 2026 安全性產品營收 +43%、整體營收創紀錄 +23% YoY → 公司大幅上修全年 EPS 與營收財測 → 管理層明確將本季優於預期歸功於「AI 相關流量與平台交叉銷售」→ 這本應是一個「估值隨財測上修持續變便宜」的理想型態,但查證時發現估值落差僅存在於多年期視角(5年成長率隱含 PEG 0.55),若以next-12個月基準計算(forward P/E 45.6–55.8倍 vs 次年成長率20–22%),PEG 已回升至 2.0–2.5,顯示近期的樂觀情境已被相當程度定價。更關鍵的是,查證**當天**(10/9)Oppenheimer一則升評報告便讓股價單日暴漲 15.9%,顯示重新評價正在實時發生而非尚未發生。發酵評分 8/10,觸發對抗性審查,結論為 Partial(詳見本期週報第2節完整六訊號分析)。

**7. 反方觀點**
1. **商品化風險**:超大規模雲端業者可將 CDN 幾近免費地捆綁進更廣泛雲端合約,長期侵蝕 Fastly 的訂價能力,公司自身在 10-Q 中亦承認此競爭壓力。
2. **客戶集中度**:公司 10-Q 風險因子揭露,銷售額有相當集中度,失去一個或多個主要客戶可能造成重大財務衝擊。(來源:[SEC 10-Q](https://www.sec.gov/Archives/edgar/data/0001517413/000151741326000213/fsly-20260630.htm))
3. **重新評價已經在發生**:股價已從52週低點約 $6.71 上漲近4倍至 $29.30,且在本次研究期間因單一分析師報告單日再漲 15.9%,「仍便宜被忽視」的論點正在被市場自己推翻。
4. **潛在股權稀釋**:公司已於 2026 年 8 月申報一般性股權增資架(S-3ASR),存在未來發行新股稀釋現有股東的可能性。(來源:[SEC S-3ASR](https://www.sec.gov/Archives/edgar/data/0001517413/000151741326000222/fastly-universalsx3asraugu.htm))

更新日期:2026-10-10
來源:
https://www.marketbeat.com/instant-alerts/fastly-q2-earnings-call-highlights-2026-08-08/ ・ https://stockanalysis.com/stocks/fsly/forecast/ ・ https://finviz.com/quote.ashx?t=FSLY ・ https://www.webull.com/news/15422154456974336 ・ https://www.sec.gov/Archives/edgar/data/0001517413/000151741326000213/fsly-20260630.htm ・ https://www.sec.gov/Archives/edgar/data/0001517413/000151741326000222/fastly-universalsx3asraugu.htm ・ https://upstox.com/us-stocks/fsly-share-price/ ・ https://www.sec.gov/Archives/edgar/data/1517413/000151741326000053/fsly-20251231.htm ・ https://itbrief.com.au/story/cdn-market-to-hit-usd-42-89bn-as-edge-demand-surges ・ https://site.financialmodelingprep.com/market-news/fastly-fsly-sector-perform-rating-growth-ai-expansion

本文為研究彙整,非投資建議。
