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

- 自動：每週五美東收盤後（台灣時間週六凌晨 5:00）
- 手動：GitHub Actions 頁面 → Run workflow

## 本地執行

```bash
pip install -r requirements.txt

# 設定環境變數
export TELEGRAM_BOT_TOKEN=xxx
export TELEGRAM_CHAT_ID=xxx

python main.py
```

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
