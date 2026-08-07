# BLZE — Backblaze, Inc.

## 這家公司在做什麼

Backblaze 是一家美國雲端儲存公司,最早以「幫個人電腦和中小企業備份資料」起家,月費幾美元就能把整台電腦的檔案自動備份到雲端。但公司真正的成長引擎,是後來推出的 B2 Cloud Storage——一種和 Amazon S3 相容的「雲端硬碟」服務,讓開發者、媒體公司、以及現在的 AI 公司可以用比 AWS 便宜很多的價格,把大量資料(影片、圖片、AI 訓練資料、模型檔案)存放在雲端並隨時取用。簡單說:Backblaze 現在是一家想從「幫你備份電腦」轉型成「AI 時代資料倉庫供應商」的公司。

## 解決什麼問題、為誰解決

**傳統客戶**:一般消費者與中小企業主,買的是「電腦壞掉/中毒/被偷,資料還能救回來」的保險,對應產品是 Computer Backup。

**現在的成長客戶**:開發者、媒體/影音公司、以及大量湧入的 AI 基礎設施業者(尤其是「neocloud」——專門出租 GPU 運算力給 AI 公司的新創雲端業者,例如 CoreWeave)。這些客戶買的其實是「儲存空間」本身,但更關鍵的是買「不被兩大痛點卡住」:一是 AWS S3 等大廠的高額「資料取出費」(egress fee),二是超大規模資料(EB 等級)在單一供應商滿足不了頻寬與速率需求時的替代方案。B2 Cloud Storage 打的就是「S3 相容(轉換容易)+ 免費/低價取出資料 + 價格更低」這幾個訴求。

## 商業模式與營收結構

以 2026 年第一季(截至 2026/3/31,10-Q)為準,Backblaze 總營收 3,870 萬美元,兩大產品線占比為:

- **B2 Cloud Storage**:2,240 萬美元,年增 24%,約占總營收 **58%**(一年前同季僅占 52%)
- **Computer Backup**:1,620 萬美元,年增幾乎持平,約占總營收 **42%**

換算成完整 2025 財年(全年):B2 Cloud Storage 營收 7,990 萬美元(年增 26%),Computer Backup 營收 6,590 萬美元(年增 3%),兩者占比約 55% / 45%。兩個時間點對照可以看出,B2 雲端儲存正快速取代傳統備份業務,成為公司的主要營收來源與成長引擎(來源:Backblaze 2026 Q1 10-Q、2025 Q4/全年財報新聞稿、Blocks & Files 產業媒體報導)。

**2026 Q2 更新(2026/8/3 公布)**:總營收 4,271 萬美元,年增 18%(為 6 季來最快);B2 Cloud Storage 營收 2,660 萬美元,年增 34%(7 季來最強)。公司同步將 2026 全年營收指引由 1.615–1.635 億美元大幅上修至 **1.72–1.74 億美元**,調整後 EBITDA 利益率指引由 23–25% 上修至 27–29%,並預告 2027 年 B2 成長率將超過 40%。當季新增 RPO(未履行合約)約 3.2 億美元,其中 3.13 億美元來自 CoreWeave 單一合約,顯示成長引擎高度集中的情況在 Q2 進一步加深而非分散。

地區分布(2026 Q1,10-Q):美國本土 2,800 萬美元(約 72%),國際市場合計約 1,070 萬美元(約 28%,其中英國約 5%、加拿大約 4%、其他地區約 18%)。與一年前同期(國際占比約 27%)相比變化不大,顯示公司目前仍高度集中在美國市場,國際化程度有限。

## 產業與 TAM

**公司自己講的故事(投資人簡報/公司公告,需注意這是 Backblaze 自估,非獨立第三方研究)**:Backblaze 管理層在 2026 年多次公開簡報中提出,「neocloud」(專門出租 GPU 運算力的新興雲端業者,目前全球約 200 家)市場整體規模預計以每年 46% 的速度成長,5 年內達到 2,300 億美元;其中「資料儲存」部分約占這些業者整體經濟模型的 6%,換算下來到 2030 年儲存這塊的市場機會約 **140 億美元**,這是 Backblaze 目前主打的成長故事(來源:Blocks & Files、Investing.com 對 Backblaze 投資人簡報的報導)。這個數字目前沒有找到獨立第三方研究機構(如 IDC、Gartner)公開驗證,屬於公司單方面框定的細分市場估計,規模也遠小於整體雲端儲存市場。

**第三方研究機構估計(獨立市場調查,非公司自估)**:多家市場研究機構對「整體雲端儲存市場」(不限於 AI/neocloud)給出的 2026 年市場規模估計互有出入但量級相近:
- Fortune Business Insights:2026 年約 1,978 億美元,預估 2026–2034 年複合成長率(CAGR)19.3%
- MarketsandMarkets:2026 年約 1,730 億美元,預估 2026–2031 年 CAGR 17.1%;其中「物件儲存」(Backblaze 所在的細分市場)這個子類別預估成長最快,CAGR 達 19.1%
- Mordor Intelligence:2026 年約 1,793 億美元,預估 2026–2031 年 CAGR 23.4%

換句話說,第三方機構認為整個雲端儲存產業本身就是千億美元級、且以近 20% 年複合成長率擴張的大市場;Backblaze 自己鎖定的「AI/neocloud 儲存」140 億美元,只是這個大餅裡一個成長特別快、但目前公司實際市占仍非常小的利基區塊。

## 主要競爭者與定位

- **Amazon S3(AWS)**:市場龍頭、產業標準制定者(B2 之所以做「S3 相容」API 就是為了方便客戶從 AWS 轉移過來)。定價較高、資料取出費約每 GB 0.09 美元,是 Backblaze 主打「省錢替代方案」時最常拿來比較的對象。
- **Google Cloud Storage / Microsoft Azure Blob Storage**:另外兩大公有雲巨頭,取出費用更高(Google 約每 GB 0.12 美元),企業客戶多因既有雲端合約綁定而使用,是 B2 爭取「多雲備援/降低成本」需求時的競爭對手。
- **Cloudflare R2**:近年崛起的強力對手,主打「零資料取出費」,儲存單價略高於 Backblaze(約每 GB 0.015 美元,換算每 TB 約 15 美元 vs. Backblaze 約 6.95 美元),特別適合網站/CDN 這類需要頻繁對外傳輸資料的場景,與 B2 在「開發者/中小型雲端原生客戶」這個族群上直接競爭。
- **Wasabi Technologies(未上市)**:Backblaze 自己網站上最常直接拿來做價格比較的對手,定位幾乎相同——「純儲存、不玩複雜分層定價的 S3 相容雲端儲存」。Wasabi 是私人公司,近年完成多輪募資,估值約 18 億美元,累計募資超過 6 億美元,並在 2026 年再取得 2.5 億美元信用額度擴充基礎設施,顯示這個利基市場資金也在快速湧入、競爭正在加劇。
- **MinIO、Cloudian 等自架式/混合雲儲存軟體商**:鎖定企業自建資料中心或混合雲場景,與 Backblaze「公有雲代管」的模式不同,主要在企業內部 IT 客戶群上分食市場,但因為都遵循 S3 相容標準,客戶轉換門檻普遍偏低。

整體來看,B2 Cloud Storage 所在的物件儲存市場「轉換成本低、標準化程度高(S3 相容)」,這既是 Backblaze 能快速搶客戶的原因,反過來也是它自己隨時可能被更便宜/更大牌對手搶走客戶的風險來源。

## 敘事發酵為什麼可能成立

把目前手上的證據串成一條因果鏈:AI 模型訓練與推論會產生海量非結構化資料(影片、圖片、模型權重、向量資料庫等),這些資料需要「S3 相容、大量、可負擔」的儲存底層——而專門出租 GPU 算力給 AI 公司的「neocloud」業者(如 CoreWeave)自己並不想、也不擅長從零打造這層儲存基礎設施,尤其在 AWS 動輒收取高額資料取出費的情況下,更有動機找像 Backblaze 這種專注做儲存、價格更低的夥伴。

這股需求目前具體反映在財報最快成長的那條線——B2 Cloud Storage,而不是原本的 Computer Backup:2026 Q1 B2 營收年增 24%,AI 相關客戶數年增高達 76%,同期 Computer Backup 幾乎零成長,兩條產品線走勢明顯分岔。2026/6/23 與 CoreWeave 簽下 5 年 3.35 億美元的多 EB 級合約,是這條故事線目前最重的一筆驗證——把一家原本被市場視為「小型消費級備份公司」,一舉推上「被大型 AI 基礎設施業者選中的儲存供應商」位置,當天股價應聲大漲 30%。

獲利端也出現放大訊號:因為 B2 毛利率結構優於傳統備份業務,加上儲存基礎設施本身有規模經濟(固定的資料中心成本攤在愈來愈大的用量上),公司整體毛利率從 56% 提升到 61%,調整後 EBITDA 利益率幾乎翻倍(18% → 26%),全年營收指引也因此上修。

市場目前還沒完全買單,主要是因為兩件事沒解決:第一,帳面上公司 GAAP 淨利率仍是負值(約 -18%),表面數字看起來仍是虧損中的小型股;第二,CoreWeave 這筆大單占比極高,讓人擔心這是「一次性運氣」而非「趨勢常態」。要讓市場真正相信這個故事,需要看到:B2 客戶名單持續多元化(不只靠 CoreWeave)、B2 營收成長率能維持在 20% 以上數季、以及 GAAP 財報轉虧為盈——只要這幾點陸續兌現,目前偏保守的市場定價就有重新評估的壓力。

**2026/8 更新**:上述「市場尚未買單」的窗口已明顯收窄。8/3 公布的 Q2 財報與大幅上修指引,加上財報後 5 家以上券商密集調高目標價,推動股價單日暴漲逾 60%、年初至今累計漲幅超過 300%;Forward P/E 已飆升至 76–107 倍(不同來源估算不一),PEG 高達 60 倍以上,估值已明顯超前於成長率本身。換言之,原本「市場半信半疑」的估值缺口已在財報後迅速收斂甚至反轉——CoreWeave 客戶集中度風險並未消失(見反方觀點),但股價已提前為「完美劇本」定價,後續能否繼續發酵取決於能否證明 B2 有機成長(排除 CoreWeave 貢獻後)同樣強勁。

## 反方觀點

1. **客戶集中度與信用傳導風險被低估**:CoreWeave 合約可能貢獻 BLZE 營收四成以上,但 CoreWeave 自身財務結構高度槓桿(負債約 210 億美元、約 7 倍槓桿),而且 CoreWeave 本身高度依賴單一客戶 Microsoft(占其營收約 67%)。這代表 Backblaze 的成長故事,某種程度上是把風險「借道」CoreWeave 再借道 Microsoft——只要這條鏈任何一環出狀況(例如 Microsoft 減少採購、CoreWeave 再融資出問題),BLZE 最亮眼的成長引擎可能瞬間熄火。

2. **產業商品化與價格戰壓力**:物件儲存市場因為 S3 相容標準普及,客戶轉換供應商的技術門檻很低,而競爭對手一個比一個財力雄厚或打法更狠——AWS/Google/Azure 是現金牛巨頭,Cloudflare R2 直接打「零取出費」,私人對手 Wasabi 剛拿到數億美元新資金加碼擴張。Backblaze 目前的賣點很大一部分就是「比較便宜」,這種定位長期容易被拖入價格戰,壓縮本來就不算厚的毛利空間。

3. **帳面獲利能力仍脆弱、且股權持續稀釋**:儘管調整後 EBITDA 利益率明顯改善,但公司 GAAP 淨利率仍為負(約 -18%),「獲利轉機」故事目前主要靠非 GAAP 指標撐著;同時過去一年流通在外股數增加約 17%,代表既有股東的每股權益持續被稀釋,實際到手的每股獲利改善幅度會比營收/EBITDA 數字看起來的更保守。

4. **公司自稱的 TAM 需要打折扣看待**:Backblaze 主打的「2030 年 140 億美元 neocloud 儲存 TAM」是公司自己框定的細分市場估計,目前沒有找到 Gartner、IDC 等獨立研究機構的公開數字直接佐證;相較之下,第三方機構估計的整體雲端儲存市場已達 1,700~2,000 億美元量級,Backblaze 目前實際市占仍極小,能否把「市場很大」轉換成「自己吃得到的份額」,仍是未知數。

5. **股價已大幅超前基本面,估值風險上升**:8/3 財報後股價單日暴漲逾 60%,Forward P/E 飆升至 70–100 倍以上區間,PEG 高達 60 倍以上(遠高於一般「合理」門檻 1-2 倍),顯示市場已為 CoreWeave 大單與指引上修的樂觀情境完全定價,一旦後續季度成長不如預期或 CoreWeave 相關風險兌現,股價回檔空間可能相當可觀。

6. **新增股份稀釋**:公司於 8/3 財報同時登記約 419.5 萬股(約占已發行股數 6.8%)供轉售,主要與 CoreWeave 認股權證(履約價 $7.60)相關,雖非全新募資,仍構成潛在稀釋來源。

---
更新日期:2026-08-07

來源:
- Backblaze 2026 年第一季 10-Q(SEC EDGAR):https://www.sec.gov/Archives/edgar/data/0001462056/000162828026029797/blze-20260331.htm
- Backblaze 2026 年第一季財報新聞稿(SEC 8-K 附件):https://www.sec.gov/Archives/edgar/data/1462056/000162828026029795/ex991blze20260331earningsp.htm
- Backblaze 官方投資人關係頁—2026 Q1 財報:https://ir.backblaze.com/news/news-details/2026/Backblaze-Announces-First-Quarter-2026-Financial-Results/default.aspx
- Backblaze 官方投資人關係頁—2025 Q4/全年財報:https://ir.backblaze.com/news/news-details/2026/Backblaze-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx
- Blocks & Files:「Backblaze cloud storage revenues fire up nicely while backup is flat」(2025/11/7):https://www.blocksandfiles.com/public-cloud/2025/11/07/backblaze-cloud-storage-revenues-fire-up-nicely-while-backup-is-flat/1718738
- Blocks & Files:「Backblaze lands first eight-figure neocloud deal as revenue climbs 12%」(2026/2/25):https://www.blocksandfiles.com/public-cloud/2026/02/25/backblaze-secures-major-neocloud-deal-as-revenue-climbs-12/4091815
- Investing.com:「Backblaze Q1 2026 slides: AI storage drives 24% B2 growth」:https://www.investing.com/news/company-news/backblaze-q1-2026-slides-ai-storage-drives-24-b2-growth-93CH-4674827
- Fortune Business Insights,雲端儲存市場報告:https://www.fortunebusinessinsights.com/cloud-storage-market-102773
- MarketsandMarkets,雲端儲存市場報告:https://www.marketsandmarkets.com/Market-Reports/cloud-storage-market-902.html
- Mordor Intelligence,雲端儲存市場報告:https://www.mordorintelligence.com/industry-reports/cloud-storage-market
- Backblaze B2 vs Wasabi 官方比較頁:https://www.backblaze.com/cloud-storage/comparison/backblaze-vs-wasabi
- Wasabi Technologies 募資新聞稿:https://wasabi.com/company/newsroom/press-releases/wasabi-raises-70m-in-new-equity-to-power-the-next-era-of-data-infrastructure
- Gartner Peer Insights,Backblaze 競爭對手列表:https://www.gartner.com/reviews/market/file-and-object-storage-platforms/vendor/backblaze/alternatives
- LeanOps,雲端儲存定價比較(2026):https://leanopstech.com/blog/cloud-storage-pricing-comparison-2026/
- Backblaze 2026 年第二季財報新聞稿(IR):https://ir.backblaze.com/news/news-details/2026/Backblaze-Announces-Second-Quarter-2026-Financial-Results/default.aspx
- Yahoo Finance:「Backblaze (BLZE) 64.0% narrower...」(Q2 財報後股價反應):https://finance.yahoo.com/markets/stocks/articles/backblaze-blze-64-0-narrower-031801602.html
- Futurum Group:「Backblaze Q2 FY 2026: CoreWeave Deal Strengthens AI Storage Position」:https://futurumgroup.com/insights/backblaze-q2-fy-2026-coreweave-deal-strengthens-ai-storage-position/

本文為研究彙整,非投資建議。
