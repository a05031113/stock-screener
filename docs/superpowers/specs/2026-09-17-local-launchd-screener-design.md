# 將 screener 資料抓取搬回本機（launchd）設計

日期：2026-09-17

## 背景

`Weekly Early Momentum Screener` GitHub Actions 自 2026-07-25 起連續 14 次失敗。
根因是 Yahoo Finance 對 GitHub Actions 出口 IP 限流：`_download_daily_closes`
在 1344～3640 檔中只拿到 20～25 檔，四輪重試後以
`RuntimeError: Batch download coverage ... below 50%` 中止。candidates 這段雖跑完，
但 8 月起幾乎都是 0 檔，很可能是同一個限流在前段被靜默吞掉。

雲端流程有兩段：

1. GitHub Actions `screener.yml`：週五收盤後跑 `main.py`，把 `output/*.csv` commit 回 main
2. Claude 雲端 routine（敘事發酵週報）：週六讀 `output/`，產出
   `reports/fermentation_*.md` push 到 `fermentation-reports` 分支，
   `report-notify.yml` 再發 Telegram

只有第 1 段壞掉，且只有它需要家用 IP 才能解。第 2 段維持不動。

## 目標

- `main.py` 在使用者的 Mac 上由 launchd 每週執行，結果 push 回 GitHub `main`
- 雲端 routine 與 Telegram 通知零改動
- GitHub Actions 的排程觸發停用，只留手動備援

## 時間窗

雲端 routine 於 UTC 22:37～22:54（台北週日約 06:40）push 報告。
本機只要在 **週日 06:00 前** 完成即可。排程定在台北時間 **週六 06:00** 主跑、
**週六 18:00** 補跑；補跑靠 freshness check 在主跑成功時自動跳過。

## 本機目錄

```
~/stock-screener/
├── .venv/                                   uv venv（Python 3.13，對齊 CI）
├── run_screener.sh                          launchd 呼叫的包裝腳本（進 repo）
├── launchd/com.yanghaoyu.stock-screener.plist   原檔進 repo，安裝時複製到 ~/Library/LaunchAgents/
├── logs/                                    launchd stdout/stderr（.gitignore）
├── main.py / screener.py / universe.py      不動
└── output/                                  照舊 commit 回 GitHub
```

`.venv/`、`logs/` 加入 `.gitignore`。

## `run_screener.sh`

把 `screener.yml` 的步驟一對一搬過來，換成 macOS 語法：

1. `cd ~/stock-screener`；所有 log 行前綴時間戳
2. 同步遠端：`git pull --ff-only origin main`。若 `output/` 以外有未提交變更
   → 中止並以非零 exit 結束，不硬跑
3. Freshness check：最新 `output/candidates_*.csv` 的日期距今 ≤ 3 天，
   且同日 `output/streak_<date>.csv` 存在 → log「本週已完成」→ exit 0。
   日期解析用 `date -j -f '%Y%m%d'`（macOS 無 `date -d`）
4. 執行 `.venv/bin/python main.py`，記錄 exit code，不立刻結束
5. 不論步驟 4 成敗：`git add output/`；有 staged 變更才
   `git commit -m "screener: YYYY-MM-DD results"`；然後 `git push origin main`。
   對應原 workflow 的 `if: always()`——streak 段失敗時前段的 candidates 仍保留
6. 以步驟 4 的 exit code 結束

不需要 Telegram 環境變數：`main.py` 不做通知。

## launchd plist

比照現有 `~/Library/LaunchAgents/com.qsearch.patrol.plist` 的寫法：

- `Label`: `com.yanghaoyu.stock-screener`
- `ProgramArguments`: `/bin/bash /Users/yanghaoyu/stock-screener/run_screener.sh`
- `WorkingDirectory`: `/Users/yanghaoyu/stock-screener`
- `StartCalendarInterval`: Weekday 6 / Hour 6 / Minute 0，Weekday 6 / Hour 18 / Minute 0
- `EnvironmentVariables`: `PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin`、
  `HOME=/Users/yanghaoyu`
- `StandardOutPath` / `StandardErrorPath` → `logs/launchd_stdout.log`、`logs/launchd_stderr.log`
- 不設 `KeepAlive`、不設 `RunAtLoad`

睡眠中錯過的時段 launchd 會在喚醒後補跑；關機錯過的靠 18:00 那次或下週。

## GitHub 端修改（直接 push 到 main）

- `.github/workflows/screener.yml`：移除 `schedule:` 下兩條 cron，只留
  `workflow_dispatch`。其餘步驟不動
- `README.md`「執行時間」與「本地執行」段、`CLAUDE.md` 的排程敘述：
  改為「本機 launchd 週六執行，GitHub Actions 僅手動觸發」
- `.github/workflows/report-notify.yml` 不動

## 錯誤處理

- `main.py` 失敗：部分結果仍 commit；launchd stderr 有 traceback；
  雲端 routine 會在週報中標註 CSV 過期。不另做通知（YAGNI）
- push 失敗：非零 exit，log 可查；下次跑會先 `git pull --ff-only`，
  若本機已有未 push 的 commit 而遠端也前進，ff-only 會失敗並中止，需人工處理
- 若 launchd 環境下 SSH push 不通（無 ssh-agent），備案：`gh auth setup-git`
  並把 remote 改成 https

## 驗證

1. `uv venv --python 3.13 .venv && uv pip install -r requirements.txt`
2. 終端直接 `bash run_screener.sh`：確認家用 IP 不被限流
   （log 中 `daily closes downloaded` 覆蓋率應接近 100%）並成功 push
3. `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.yanghaoyu.stock-screener.plist`
   後 `launchctl kickstart -k gui/$(id -u)/com.yanghaoyu.stock-screener`：
   在 launchd 環境下 freshness check 應跳過（因步驟 2 已產出當日檔）
4. 隔週日確認 `fermentation_*.md` 有標的

## 補記（2026-09-17 實跑後）

原設計假設「程式碼不用改，家用 IP 就不會被限流」。第一次本機實跑推翻了這點：

- candidates 段（逐檔 `Ticker.history`）199 檔全部正常
- streak 段 `yf.download` 批次 38/2180 後連續空 chunk，**且隨後整個 IP 被封**
  （單檔 `AAPL.history()` 也回 `YFRateLimitError`），約 30 分鐘後解封

結論與 `fix/batch-retry-fail-loud` 分支 7/19 的診斷一致：Yahoo 懲罰的是批次 burst
模式本身，與 IP 類型無關。因此追加變更：

- `_download_daily_closes` 改為**純序列、永不批次**：每檔一次 `history(period="8mo")`、
  檔間 0.5s；連續 30 次失敗（含靜默回空）→ 冷卻 120s，最多 6 次；第一輪失敗的 ticker
  做一輪補抓；覆蓋率 < 50% 仍 raise
- 移除 `import yfinance.shared`（只有批次路徑用到）
- 新增 `tests/test_download_daily_closes.py`（stdlib unittest，mock 掉 yfinance）
  釘住上述契約
- 預估 streak 段 2180 檔約 60～70 分鐘；本機 launchd 無 timeout，週六 06:00 起跑
  綽綽有餘
