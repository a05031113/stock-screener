# SNOW — Snowflake Inc

**1. 這家公司在做什麼**
Snowflake 是一個雲端資料平台,企業把所有資料集中存放在這裡,並在上面執行分析、AI模型與應用程式,不需要自行管理伺服器。它本身架構在 AWS、Azure 與 Google Cloud 之上,而非擁有自己的資料中心。

**2. 解決什麼問題、為誰解決**
大型與中型企業的資料往往分散在許多系統與雲端之間,Snowflake 把它們整合進一個統一且具治理機制的平台,讓資料團隊、分析師,現在也包括AI代理人(agent),都能在不必各自搭建基礎設施的情況下查詢並運用這些資料。

**3. 商業模式與營收結構**
以用量計費的「產品營收」(消費多少運算/儲存資源就付多少錢,而非傳統訂閱席位制)是絕對主力:Q2 FY2027 總營收15.5億美元中,產品營收14.9億美元(約96%);淨收入留存率(NRR)126%,顯示既有客戶用量正在快速擴張。本次查證未能取得可靠的美國/國際地區營收拆分,需查10-K分部附註補強。

Q2 FY2027(2026/9/2發布)營收15.5億美元(+35% YoY),產品營收+37%,non-GAAP EPS $0.62遠優於共識$0.45;公司上修FY27產品營收財測由58.4億美元上修至60.7億美元(年增36%)、non-GAAP營業利益率財測由13.5%上修至14.5%;RPO(剩餘履約義務)+30%至90億美元。財報後股價單日跳漲約22-24%。(來源:[pulse2.com](https://pulse2.com/snowflake-q2-fiscal-2027-revenue-rises-35-to-1-55-billion-as-product-revenue-guidance-is-raised/)、[itiger.com](https://www.itiger.com/news/2664872360))

**4. 產業與 TAM**
公司自稱 TAM(2024年投資人日簡報,透過二手來源引用,未直接核對原始簡報,應謹慎看待):由2023年約1,520億美元成長至2028年達3,420億美元,涵蓋資料倉儲/湖倉/Unistore + 協作/資料工程 + 資安 + 資料科學/機器學習,AI(Cortex AI、Document AI、Copilot)被定位為主要驅動力。第三方(較窄口徑、非直接可比):資料庫管理系統(DBMS)整體市場2024年約1,197億美元,2026年約達1,610億美元(Gartner數字,經部落格二手引用)——與公司自稱的3,420億美元口徑差異極大,兩者定義範圍不同,不應直接比較。

**5. 主要競爭者與定位**
**Databricks**(成長最快,在機器學習/非結構化資料工作負載上最強,一份過時比較資料顯示私募估值約1,000億美元)、**Google BigQuery**、**AWS Redshift**、**Microsoft Azure Synapse/Fabric**,以及(在AI基礎設施面向日益相關的)**Oracle**(曾因SNOW可轉債消息連動下跌)。

**6. 敘事發酵為什麼可能成立**
企業資料與AI工作負載需求持續成長 → 反映在Cortex AI/Snowflake Intelligence這類「代理式AI」產品定位 → Q2 FY2027營收加速至+35%、EPS大幅超預期並帶動財測上修 → 4家大型投行(大摩、美銀、高盛、Monness Crespi)於財報後30-45天內大幅上修目標價,屬跨來源一致的正面訊號 → 這本該是「估值隨財測上修持續變便宜」的理想型態。但查證發現PEG已達2.43、forward P/E逾120倍,顯示市場已經給予這個故事相當豐厚的信心溢價,並非「便宜被忽視」;且9/28發行37.5億美元零息可轉債造成股價單日下跌4%(稀釋隱憂),10月初更出現ASOS資料外洩的駭客威脅事件(公司聲明自身平台未遭入侵,但這類標題雜訊屬2024年類似客戶端外洩事件的重複模式)。整體讀法是:基本面動能(S1/S3/S4)確實紮實,但估值已經「發酵完畢」而非「早期半信半疑」。發酵評分 5/10,未達門檻。

**7. 反方觀點**
1. **估值已反映近乎完美預期**:PEG 2.43、forward P/E逾120倍,任何成長放緩都可能對股價造成不成比例的衝擊。
2. **Databricks成長更快且在AI/ML訓練工作負載上更受青睞**:Databricks營收成長率約50%+,高於Snowflake的約35%;一份大摩CIO調查顯示68%大型企業同時使用兩個平台(非取代關係),但這也限制了Snowflake在成長最快AI工作負載市占的空間。
3. **可轉債與持續的股權薪酬壓力**:新發行37.5億美元可轉債增加稀釋與利率敏感度,即便公司宣稱該季「獲利」,GAAP營業虧損仍達2.63億美元,主因股權薪酬費用龐大。
4. **重複出現的資安聲譽風險**:Snowflake客戶環境(非必然是Snowflake自身平台)多次成為攻擊目標(2024年大規模客戶端外洩事件,如今2026年10月的ASOS聲稱事件),即便每次都被證實非平台本身遭入侵,這類標題雜訊具結構性重複性,可能持續影響市場情緒。

更新日期:2026-10-10
來源:
https://pulse2.com/snowflake-q2-fiscal-2027-revenue-rises-35-to-1-55-billion-as-product-revenue-guidance-is-raised/ ・ https://www.itiger.com/news/2664872360 ・ https://www.sec.gov/Archives/edgar/data/0001640147/000164014726000043/snow-20260928.htm ・ https://247wallst.com/investing/2026/09/28/snowflake-slides-4-on-proposed-3-5b-convertible-offering-oracle-falls-3-datadog-drops-4/ ・ https://www.salesforceben.com/hackers-threaten-to-leak-asos-snowflake-instance/ ・ https://finviz.com/quote.ashx?t=SNOW ・ https://stockanalysis.com/stocks/SNOW/forecast/ ・ https://www.doit.com/blog/snowflake-competitors-compared ・ https://www.firebolt.io/blog/cloud-data-warehouse-market-share-breakdown

本文為研究彙整,非投資建議。
