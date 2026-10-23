# 敘事發酵週報索引

每週六由雲端 routine 自動產出。點日期看當週完整報告;ticker 連結在各報告內。
簡介頁(profiles/)會就地更新,想看「當週狀態」用對應的 git tag(`report-YYYYMMDD`)。

| 日期 | 週報 | 評估檔數 | 高分標的(≥7) |
|---|---|---|---|
| 2026-10-24 | [fermentation_20261024](fermentation_20261024.md) | 0(candidates本期連檔案都未產出——追到screener.py的`main()`在Finviz預篩回傳空清單時直接return、未呼叫save_results的程式碼落差；streak本期也是空清單；三組Finviz篩選同時回傳空清單，詳見報告4.2節） | 無 |
| 2026-10-17 | [fermentation_20261017](fermentation_20261017.md) | 12(candidates本週暴增至48檔，依total_score/tech_score/rel_vol排序取前12；streak本期0檔未貢獻標的；本期連續三期以來首次無標的達≥7分，候選結構偏向大型成熟公司〔資產管理/產險/整合型石油/工業設備龍頭〕；CRGY查證發現10/8公告收購Devon Energy的Eagle Ford資產，次年EPS下修幅度收斂） | 無 |
| 2026-10-10 | [fermentation_20261010](fermentation_20261010.md) | 12(candidates本週26檔，依total_score/tech_score/rel_vol排序取前12；streak本期0檔未貢獻標的；其中PCRX經查證為10/8公告、即將完成交割的併購套利標的〔Viatris以$36.50現金收購〕，非敘事發酵；HPK的M&A狀態自上期「探索出售」演變為引入印尼主權資本的可轉換優先股再融資） | OPRT(9)、FSLY(8) |
| 2026-10-03 | [fermentation_20261003](fermentation_20261003.md) | 12(candidates本週29檔，依total_score/tech_score/rel_vol排序取前12；streak本期0檔未貢獻標的；其中WBD、ATKR、QRVO三檔經查證為即將完成交割的併購套利標的，非敘事發酵） | WK(9) |
| 2026-09-25 | [fermentation_20260925](fermentation_20260925.md) | 12(candidates本週異常暴增至232檔，依total_score/return_3m排序取前12；streak群聚訊號佐證能源/航運題材為本期最強跨清單群聚，但未貢獻額外候選標的） | NVGS(8)、CVX(7) |
| 2026-09-18 | [fermentation_20260918](fermentation_20260918.md) | 12(candidates與streak管線同步恢復正常產出；本期12檔中3檔為併購/私有化套利中的標的〔BWMN、BWIN、MG〕，框架前提已被固定收購價封頂） | GFR(8)、SMCI(9)、PUBM(7) |
| 2026-09-11 | [fermentation_20260911](fermentation_20260911.md) | 0(candidates本週仍0檔;streak已連續6週以上故障,本期調閱最新09/05 run #45 log確認根因不變,並發現repo內有未合併的修復分支fix/batch-retry-fail-loud,詳見報告4.2節) | 無 |
| 2026-09-04 | [fermentation_20260904](fermentation_20260904.md) | 0(candidates本週0檔；streak已連續8週故障，本期查到精確根因：Yahoo批次下載被限流，40/3354觸發50%覆蓋率保護閾值中止，詳見報告4.2節) | 無 |
| 2026-08-28 | [fermentation_20260828](fermentation_20260828.md) | 2(與08/21同一份08-21收盤快照,沿用分數+增量查證;streak陳舊49天未採用) | TTAN(8) |
| 2026-08-21 | [fermentation_20260821](fermentation_20260821.md) | 2(candidates恢復產出2檔；streak陳舊42天，本期起不再沿用舊快照) | TTAN(8) |
| 2026-08-14 | [fermentation_20260814](fermentation_20260814.md) | 12(candidates本期0檔,沿用streak 20260710舊快照【第三週】,與過去兩期相同12檔) | IMMX(9)、DAVE(8)、KYMR(8)、ACRS(8)、CTNM(8)、KURA(8)、BLLN(8)、DYN(7) |
| 2026-08-07 | [fermentation_20260807](fermentation_20260807.md) | 12(candidates本期0檔,沿用streak 20260710舊快照,與上週相同12檔) | IMMX(9)、ACRS(8)、CTNM(8)、KYMR(8)、DAVE(7)、DYN(7)、HNGE(7)、BLLN(7) |
| 2026-07-31 | [fermentation_20260731](fermentation_20260731.md) | 12(有效樣本10,candidates僅1檔為資料異常) | BLZE(8)、ACRS(8)、AVAH(8)、DAVE(7)、KYMR(7)、DYN(7)、IMMX(7) |
| 2026-07-24 | [fermentation_20260724](fermentation_20260724.md) | 0（screener 批次下載失敗未產出資料） | 無 |
| 2026-07-17 | [fermentation_20260717](fermentation_20260717.md) | 0（screener 逾時未產出資料） | 無 |
| 2026-07-11 | [fermentation_20260711](fermentation_20260711.md) | 12 | BNED(8)、MRVI(7)、OPRT(7) |
