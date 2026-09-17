# Stock Momentum Screener

每週自動掃描 S&P500 + Nasdaq100 + Russell 2000，找出符合動能條件的候選股，透過 Telegram 通知。

## 策略邏輯

技術面初篩 → Telegram 通知 → **手動確認基本面**

### Breakout 型（突破型）
- 股價距 52 週高點 12% 以內
- 月漲幅 7~50%（漲了但沒瘋）
- 相對成交量 > 1.5x
- MA5 > MA20（均線開始多頭）

### Coiling 型（蓄力型）
- 底部橫盤，布林帶寬度收縮（< 0.15）
- 3 個月漲幅平坦（-10% ~ 30%）
- 近期突然放量（相對量 > 2x）
- MA5 剛穿越 MA20

## 設定方式

### 1. Telegram Bot

1. 找 [@BotFather](https://t.me/BotFather) 建立 bot，取得 `BOT_TOKEN`
2. 傳一則訊息給你的 bot，然後打開：
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```
   找到 `chat.id`（就是你的 `CHAT_ID`）

### 2. GitHub Secrets

在 repo Settings → Secrets → Actions 新增：

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | 你的 bot token |
| `TELEGRAM_CHAT_ID` | 你的 chat id |

### 3. 啟用 Actions 寫入權限

Settings → Actions → General → Workflow permissions → 選 **Read and write permissions**

（讓 bot 可以 commit output CSV）

## 執行時間

- 自動：本機 macOS launchd，台北時間**週六 06:00** 主跑、**18:00** 補跑
  （主跑成功時補跑由 freshness check 自動跳過）。結果 push 回 GitHub `main`，
  週日早上的雲端敘事發酵 routine 再讀取 `output/` 產出週報。
- 手動備援：GitHub Actions 頁面 → Run workflow（排程已停用；Yahoo 對 CI IP 限流，
  批次下載在 Actions 上長期失敗，見 `docs/superpowers/specs/2026-09-17-local-launchd-screener-design.md`）

## 本地執行

```bash
# 一次性安裝
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r requirements.txt

# 手動跑一次（含 pull / freshness check / commit / push）
bash run_screener.sh

# 只跑 screener、不碰 git
.venv/bin/python main.py
```

### 安裝 launchd 排程

```bash
cp launchd/com.yanghaoyu.stock-screener.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.yanghaoyu.stock-screener.plist

# 立刻觸發一次 / 查看狀態 / 卸載
launchctl kickstart -k gui/$(id -u)/com.yanghaoyu.stock-screener
launchctl print gui/$(id -u)/com.yanghaoyu.stock-screener | head -20
launchctl bootout gui/$(id -u)/com.yanghaoyu.stock-screener
```

Log 在 `logs/launchd_stdout.log`、`logs/launchd_stderr.log`。
`main.py` 本身不需要 Telegram 環境變數；通知由 `report-notify.yml` 承接。

## 輸出格式

`output/candidates_YYYYMMDD.csv`

| 欄位 | 說明 |
|------|------|
| ticker | 股票代號 |
| price | 當前股價 |
| rel_vol | 相對成交量 |
| return_1w/1m/3m | 漲跌幅 |
| pct_from_high | 距 52 週高點距離 |
| pattern | Breakout / Coiling / 兩者皆是 |
| score | 通過條件數（越高越強） |
| signals | 觸發的具體條件 |

## 手動確認 Checklist

收到通知後，針對每檔候選股確認：

- [ ] Seeking Alpha 最新文章：narrative 是否合理？
- [ ] 最近一次 Earnings transcript：管理層語氣是否轉正？
- [ ] Revenue/EPS 趨勢：由負轉正或加速成長？
- [ ] 機構持股：Whale Wisdom 看是否有大基金開始建倉？

四項至少過三項才考慮進場。
